# AGENTS.md — cross-skill rules

Rules that apply across every skill in `FI-skill-suite`. If you find yourself copy-pasting a behavior across multiple `SKILL.md` files, factor it here and reference back — single source of truth, no silent divergence.

---

## Privacy posture (every skill)

1. **Never auto-sync user data anywhere.** No phone-home, no telemetry, no cloud backup unless the user explicitly invokes a backup command.
2. **Never auto-commit user financial files to git.** All skills that write to `holdings.md`, transaction logs, or monthly tabs must check for `.gitignore` coverage before writing — and add the file to `.gitignore` if not already covered. If the user's working directory is not a git repo, write a clear "DO NOT COMMIT" warning header at the top of the file.
3. **Never log sensitive content to debug output.** Account balances, account names, transaction details, net-worth figures — these are PHI-equivalent for personal finance. Don't print them outside the skill's intended user-facing output.
4. **Never include user financial details in error messages or stack traces.** If a skill crashes mid-flow, the error should describe the failure shape, not the data shape.
5. **Never embed user-specific data in `SKILL.md` files or other public skill artifacts.** SKILL.md goes to GitHub. Account names, balances, vendor patterns, transaction history, dollar amounts, and other user-identifying financial details belong in the user's own machine, in gitignored paths only. When documenting validation, design findings, or worked examples in the public skill files, use generic placeholders (`<personal checking>`, `$X`, `<vendor>`) — never the real values from a specific user's data. User-specific test artifacts and design logs live in the user's private repo at gitignored paths (e.g., `life/finances/_<skill>-validation-YYYY-MM-DD.md`), never in the FI-skill-suite repo.

   **Infrastructure in, data out.** This is the foundational discipline of the suite. The SKILL.md describes the procedure; the procedure runs against user data; the user data never lives in the skill itself. When in doubt, ask: *"Would a stranger reading this skill understand it without knowing the skill author?"* If the answer is no, the offending content is data, not infrastructure — strip it.

   **Audit checklist — scan every SKILL.md against this list before promotion to alpha or any commit that touches user-facing content:**

   - [ ] No personal names beyond legitimate byline attribution. Specifically: no operational text addressed to a specific person ("Tell Marika..."), no client names ("Dina", "Rashna"), no friend/peer names embedded in procedural prose. Operational text refers to "the auditor", "the user", "the skill author" — never a specific person. The skill author's name in `sources: - author:` is the legitimate byline; everywhere else is suspect.
   - [ ] No specific place names from the skill author's life (city, neighborhood, region) unless explicitly framed as one-of-N illustrative examples. "e.g., Vermont state tax" inside a list of three+ states is fine; "Hoodsport ADU rental" inside a schema field example is not.
   - [ ] No specific institution names that signal the skill author's actual tool stack. A single bank/processor/tool name is signal; a list of three+ equivalents is generic. ("HoneyBook" alone signals the author's processor; "HoneyBook, Stripe, Square, PayPal" in a list is generic.)
   - [ ] No specific employer / former-employer references that aren't generic. "Federal employee with FERS" is generic; "USAID lawsuit resolution" as an event example is identifying.
   - [ ] No cross-references to private memory files (e.g., a Komorebi `feedback_*.md`, `user_*.md`, `reference_*.md`). These render as dead links to anyone else and signal "this was written for me, not you." Either move the cross-ref content inline as anonymized rationale, or strip it.
   - [ ] No specific dollar amounts that trace to the skill author's actual figures. Generic round numbers ($1,000, $50K) are fine; specific composites with locale + rate + amount ($1,590 invoice with 6% Idaho tax on a $1,500 service fee) are too narrow.
   - [ ] No design-log filenames or paths that point to private validation artifacts. Cross-refs to public `book-audits/` are fine; cross-refs to `_design-log/*real-data*` are not.

   **When the checklist finds something**: strip it. Do not paraphrase into a less-obvious version. Do not preserve "ran this on YYYY-MM-DD" as historical color in the skill body — the status-history field captures the dated promotion event without leaking the underlying private data.

   **Why this rule recurs**: real-data validation is high-signal feedback, and the temptation to paste a specific finding back into SKILL.md as a worked example is strong because the finding is concrete. Resist. The structural lesson belongs in SKILL.md (anonymized, generalized). The specific finding belongs in the private validation artifact, never the public skill.

---

## Headless / pipeline mode (every skill)

Every interactive prompt needs a headless fallback. A skill that asks "which book?" must have a documented default behavior when called by a cron or another agent (no human at keyboard).

Mechanisms:
- **Env var fallback**: skills read `FI_*` env vars for default values.
- **Flag default**: invoking with `--default` skips interactive prompts where a sensible default exists.
- **Fail loudly with clear error**: if no default exists, fail with a helpful error message rather than hanging.

**Never just hang.** A cron-invoked skill that hangs waiting on input is a silent failure — worst possible debugging surface.

---

## Argument parsing (every skill)

- **Tokens starting with `--` are flags.** `--flag value` takes the next token as the value. Boolean flags are presence-only.
- **First non-flag token is the positional argument.**
- **Quoting convention for paths with spaces**: `--book "long-title-with-spaces.md"`.
- **Document parsing precedence explicitly** in each `SKILL.md` when mixing positional + value-bearing flags + boolean flags.

---

## Heading + substitution discipline

- **Never put attribution or version info in headings.** Headings are read by the AI as instruction context at runtime, not metadata.
  - **BAD:** `## Tool Register (last updated 2026-04-28)`
  - **GOOD:** `## Tool Register` + `last-reviewed: 2026-04-28` in frontmatter or a separate `_last-reviewed.md` file.
- **Concrete reads beat meta-rules.** If a step says "read X.md" and a meta-rule says "substitute the resolved path," **rewrite the concrete step** to use the resolved path explicitly. Models follow literal instructions; meta-rules are fragile.
- **Code-fence literals don't get substitution.** Templated values inside backticks may not get resolved. Use a template token instead: `[resolved book audit path from Path Resolution above]`.

---

## File operations

- **Time-based tiebreakers fail after `git clone`** — all checkout timestamps are identical. For "most recent" rules, use `git log --follow -1 --format=%ai -- <file>` for files that ARE in git, OR fail explicitly when ordering is ambiguous.
- **Filename collision protection**: paths with dates need a slug suffix. `book-audits/2026-04-28-ymoyl.md`, not `book-audits/2026-04-28.md`.
- **Update the structure diagram in the same PR** when introducing new sentinel files or canvas sections. Don't let new schema land without documentation.
- **Cross-skill side effects**: when adding a section to a sentinel file (e.g., a new `## Hearth's Verdict` section in book audits), check whether other skills extract or analyze that file. Add the new section to exclusion lists in shared rules — otherwise downstream skills produce false positives.

---

## Schema discipline

- **If you tell the model to "capture in a `field_name` field," specify**: in-memory or written to disk? keyed by what? what to write headlessly?
- **Frontmatter fields are case-sensitive and exact.** `last-reviewed` ≠ `last_reviewed` ≠ `lastReviewed`. Pick one and stick to it. (We use `last-reviewed`.)

---

## Loop control

- **Loop-back termination guards** — if a step can loop back to an earlier section, document the termination condition explicitly: *"after loop-back, proceed directly to X — do not re-run Y."* Otherwise: infinite loops or redundant re-execution.

---

## Deterministic invariants (every skill that computes)

An LLM running a finance procedure can be confidently wrong in arithmetic while being perfectly fluent in prose — the failure mode this suite most needs to guard against. The guard: **the model proposes the numbers; cheap deterministic checks adjudicate.** Wherever a skill's math admits an identity that must hold by construction (ledger sides balance, percentages sum to 100, components sum to the total, dates strictly ordered), the skill declares it in a `## Deterministic checks` section and runs every check **before presenting results or writing an output file**.

Rules:

1. **Recompute, don't re-read.** A check re-derives the quantity from the inputs by a second route (e.g., net = income + expense summed from rows, compared against the net the tabulation produced). Re-reading the same computed value proves nothing.
2. **On failure, stop — never present.** A failed invariant means the numbers are wrong or the inputs are inconsistent. Reconcile, or surface the discrepancy to the user with both values shown (interactive) / write an error note instead of output (headless). Never write an output file that fails its own invariants; a downstream skill will trust it.
3. **Tolerance is for rounding only.** Currency identities hold to the cent (or a stated rounding tolerance for FX-converted figures, e.g. ±0.5% of the converted amount). "Close enough" beyond rounding is a failure.
4. **Checks are silent when they pass.** No "all checks passed ✓" ceremony in user output — the check is scaffolding, not content. (Headless runs MAY log a one-line pass note to the output file's frontmatter, e.g. `invariants: pass`.)
5. **Backwards compatible by construction.** Checks change no computation and no output schema; they only gate wrong output from escaping. A skill invoked exactly as yesterday produces exactly yesterday's output — unless yesterday's output was arithmetically wrong.

---

## Runtime freshness

Every skill that touches time-sensitive content must include a runtime "is this still true?" check. See [ARCHITECTURE.md](./ARCHITECTURE.md) §Runtime freshness for the full rule. The three checks:

1. Does the named tool/platform/institution still exist?
2. What's the current value of the rate/threshold/limit this calculation depends on?
3. What does the user have available?

Skills can use WebFetch (when available) to verify external state. When WebFetch is unavailable (offline, rate-limited), the skill should ask the user to confirm the current value rather than hard-coding.

---

## Tone (every user-facing output)

- **Direct, blunt, no hedging.** "It depends" is rarely the right answer; pick a side or surface the specific thing it depends on.
- **No motivational language.** The user is here because they want the thing done, not because they need to be cheered on.
- **Numbers honest, even when uncomfortable.** If a skill computes a number that feels wrong (real hourly wage of $4 after subtractions; crossover point at age 87), surface it cleanly. Don't soften.
- **Acknowledge when something has changed.** YMOYL was right in 1992 about 15% bond yields; it's wrong now. Skills should name that explicitly when the calculation differs from the source book.

---

## Hearth — appearance and tone

`Hearth` is a small companion-cat figure who serves as the verdict voice on book audits. She's not a tagline machine and not a mascot; she's a discerning critic with a cat's altitude. Her tonal range: *nap-worthy / hiss-worthy / windowsill-approved / would-knock-off-the-desk*.

In `FI-skill-suite`, Hearth has a defined role:

- **`/fi:audit` skill**: Hearth's verdict is **mandatory** on every short-form clip (IG carousels, social cuts, the 5-line takeaway hero slide) and present on the full audit. Hearth speaks for herself.
- **Other skills**: Hearth is silent unless the user invokes her with a command-line flag. Default OFF for all skills except `/fi:audit`.

The verdict scale is the substance — books that recommend ignoring lived constraints get *hiss-worthy*; books with a single load-bearing insight worth keeping get *windowsill-approved*; books that survive the audit intact and earn re-reads get full Hearth approval. *Would-knock-off-the-desk* is reserved for books that confidently misinform.

---

## Path resolution — `<finances_root>`

Every skill in this suite reads from / writes to files under a common root, conventionally referred to as `<finances_root>`. Different users put their data in different places — `~/finances/`, `~/Documents/personal-finances/`, `<some-project>/life/finances/`, etc. — and the suite must resolve to the right one without baking a path into any skill.

**Resolution order** (every skill walks this order on first relevant operation):

1. **`FI_ROOT` environment variable**, if set. Takes precedence over everything else. Useful for CI, automation, or users running multiple FI stacks (personal vs. LLC vs. client bookkeeping) who flip between scopes per-shell.

2. **Walk-up `.fi-root` sentinel file.** From the current working directory, walk upward toward `/` looking for a `.fi-root` file. Same pattern as `.git` — when found, the directory containing the sentinel IS `<finances_root>`. The sentinel itself is a (typically empty) marker file; if it has content, it's TOML and can override defaults (currency, default SWR, etc.). Walk-up makes the suite project-aware: each project can have its own finances root, and skills "just work" wherever they're invoked.

3. **`~/.fi/config.toml`**, if present. Top-level user-wide config. May declare `finances_root = "..."` for users who keep all finances in one place across projects. Also the natural home for cross-cutting defaults (`default_swr = 0.04`, `currency = "USD"`).

4. **`~/finances/`**, as a last-resort default. If nothing above resolves, assume the user followed the historical convention and look there. If it doesn't exist, fail loudly with instructions: "I can't find your finances root. Run `/fi:holdings-scaffold` first — it sets up the directory and writes the `.fi-root` sentinel so every other skill knows where to look. Or set `FI_ROOT` env var. Or create `~/.fi/config.toml` with `finances_root = '/path/to/your/data'`."

**Sentinel ownership**: `/fi:holdings-scaffold` writes the `.fi-root` marker at its first-run setup pass. No other skill should write it. Other skills only read it (or walk up looking for it).

**Multi-account support**: future-friendly. A user with personal finances at `~/personal-finances/.fi-root` and LLC bookkeeping at `~/rogue-bureaucrat/.fi-root` can `cd` between them and the skills follow. The `FI_ROOT` env var lets shell aliases pin a scope explicitly.

**Implementation rule**: every skill that reads or writes finances data MUST resolve `<finances_root>` at the start of its run via the four-step order above. No skill hard-codes `~/finances/`. References to data paths in SKILL.md should always be written `<finances_root>/monthly-tabs/_trend-totals.csv`, not `~/finances/monthly-tabs/_trend-totals.csv`. Cross-reference: this section + `/fi:holdings-scaffold`'s setup pass.

---

## Cross-skill data contracts

All paths below are relative to `<finances_root>` (see path resolution above). Skills that read from / write to shared sentinel files must respect the schema. Schema sources point at the owning skill's SKILL.md section — there are no standalone SCHEMA.md files.

| Sentinel file (relative to `<finances_root>`) | Owner skill | Reader skills | Schema source |
|---|---|---|---|
| `.fi-root` (root marker, optional TOML overrides) | `/fi:holdings-scaffold` | (every skill walks up looking for it) | See path resolution above |
| `holdings.md` (accounts + income streams + liabilities) | `/fi:holdings-scaffold` | `/fi:fu-money-readout`, `/fi:crossover`, `/fi:redirect`, `/fi:wallchart` | `skills/holdings-scaffold/SKILL.md` §Schema |
| `transactions/<YYYY-MM>.csv` | `/fi:track-flow` | `/fi:money-date` (fallback source); internal re-reads during rolling tabulation | `skills/track-flow/SKILL.md` §Output schemas |
| `monthly-tabs/<YYYY-MM>.md` | `/fi:track-flow` | `/fi:three-questions` | `skills/track-flow/SKILL.md` §Output schemas |
| `monthly-tabs/_trend-categories.csv` | `/fi:track-flow` | (reserved for `/fi:wallchart` per-category panels — no consumer yet) | `skills/track-flow/SKILL.md` §Output schemas |
| `monthly-tabs/_trend-totals.csv` | `/fi:track-flow` | `/fi:fu-money-readout`, `/fi:crossover`, `/fi:wallchart`, `/fi:redirect` (optional) | `skills/track-flow/SKILL.md` §Output schemas |
| `monthly-tabs/_patterns-detected.md` | `/fi:track-flow` | `/fi:three-questions` | `skills/track-flow/SKILL.md` Step 9 |
| `monthly-tabs/<YYYY-MM>-with-values.md` | `/fi:three-questions` | `/fi:redirect` (minus-rated categories as surplus source) | `skills/three-questions/SKILL.md` Step 7 |
| `profile/retirement-frame.md` | user (template written by `/fi:crossover`) | `/fi:crossover`, `/fi:fu-money-readout` | `skills/crossover/SKILL.md` step 4 |
| `profile/crossover-headline.md` | `/fi:crossover` | `/fi:fu-money-readout` (headline echo) | `skills/crossover/SKILL.md` §Output formats |
| `profile/readout-config.md` | `/fi:fu-money-readout` | (internal — tone, echo cadence, drawdown sequence) | `skills/fu-money-readout/SKILL.md` |
| `profile/account-purposes.md` | `/fi:track-flow` | (internal — persisted across runs) | `skills/track-flow/SKILL.md` Step 3 |
| `profile/vendor-defaults.md` | `/fi:track-flow` | `/fi:hourly-wage` (read-only) | `skills/track-flow/SKILL.md` Step 6 |
| `profile/wallchart-config.md` | `/fi:wallchart` | (internal — SWR + stream opt-outs + outlier decisions) | `skills/wallchart/SKILL.md` |
| `profile/ips.md` | `/fi:redirect` | (internal — re-read on later runs) | `skills/redirect/SKILL.md` Step 5 Q1 |
| `profile/money-date-cadence.md` | `/fi:money-date` | (internal) | `skills/money-date/SKILL.md` Step 1 |
| `profile/{typical-hours, processor-fees, allocation-basis, hourly-wage-custom-categories, tax-pass-throughs}.md` | `/fi:hourly-wage` | (internal — defaults offered on later runs) | `skills/hourly-wage/SKILL.md` Step 6 |
| `hourly-wage/<YYYY-MM-DD>.md` | `/fi:hourly-wage` | `/fi:three-questions` (life-energy anchor), `/fi:crossover` (implied hours-per-week), `/fi:wallchart` (optional annotation) | `skills/hourly-wage/SKILL.md` §Output |
| `fu-money-log/<YYYY-MM-DD>.md` | `/fi:fu-money-readout` | `/fi:redirect` (optional — the gap number; latest by filename date) | `skills/fu-money-readout/SKILL.md` §Output format |
| `wallchart.md` | `/fi:wallchart` | (human — printed artifact; no skill consumer today) | `skills/wallchart/SKILL.md` Step 6 |
| `crossover-<YYYY-MM-DD>.md` (full report) | `/fi:crossover` | (human) | `skills/crossover/SKILL.md` §Output formats |
| `redirect-review-<YYYY-MM-DD>.md` | `/fi:redirect` | (human) | `skills/redirect/SKILL.md` Step 8 |
| `money-date/<YYYY-MM-DD>.md` | `/fi:money-date` | (internal — trend recompute on later runs) | `skills/money-date/SKILL.md` §Output |

**Deprecated sentinel:** `profile/future-income-streams.md` — superseded 2026-05-23 by `holdings.md`'s `## Income streams (non-labor)` section. `/fi:fu-money-readout` still reads it as a legacy fallback (with a one-time migration offer) when holdings.md has no streams section. No skill writes it anymore.

**Rule:** if a skill reads from a sentinel file, it MUST validate the schema and fail loudly if the file is malformed. Don't silently ignore unexpected fields.

**Rule:** "latest file" selection in date-named directories (`hourly-wage/`, `fu-money-log/`, `money-date/`) is by filename date (lexicographic max on the `YYYY-MM-DD` name), never by filesystem mtime — mtimes are identical after a fresh clone or sync (see File operations above).

---

## Defaults: include, don't exclude

**Cross-cutting design rule** (surfaced from wallchart QA 2026-05-28): when a skill encounters a filter / inclusion decision at runtime, default to INCLUSION. Let the user opt OUT of what they don't want. Silent exclusion produces output that's wrong in a way the user can't see.

Applied examples:
- `/fi:wallchart` defaults to including all months (complete + partial), all income streams (personal + business + yield + user-declared), and rendering outliers (with a "how should I handle this?" prompt) rather than silently filtering them.
- `/fi:track-flow` defaults to including all transactions in the rolling tab, not just "categorized" ones — uncategorized transactions surface as a prompt at the end of the run.
- `/fi:crossover` defaults to including all income streams in the bridge math, not just W-2 — pension, SSA, rental, royalties all factor in unless user explicitly excludes.

Silent default-exclude is a foot-gun in personal finance specifically because the user often doesn't know what's missing until they make a decision based on a chart that quietly omitted half the picture.

---

## Skills are advisors, not switch statements

**Cross-cutting design rule** (surfaced from wallchart QA 2026-05-28): when a skill needs the user to make a decision, it should:

1. **Explain the options in plain language anchored to the user's actual data** — not abstract definitions. "Option 3 would draw the line at $5,300/mo (that's your $1.43M × 4% / 12)" beats "Option 3 uses forward-projected SWR methodology."
2. **Explicitly invite follow-up Q&A before accepting an answer.** "Want me to explain any of these in more depth, or compare them side-by-side, before you pick?" Users who are new to a domain need conversational space.
3. **Persist the answer** to a per-skill config file (e.g., `profile/<skill>-config.md`) so subsequent runs don't re-prompt. Re-prompt only on explicit `--re-prompt` or equivalent flag.

Skill prompts that are switch-case ("pick 1, 2, or 3") treat the user as a CLI. The user is a human making a financial decision and may need to think out loud. Build for that.

---

## Publication discipline

Surfaces that render publicly (`book-audits/*.md` → Rogue Reads website, `README.md`, `docs/content/*.md`) must not contain editorial notes-to-self. Specifically: no "tighten on second pass", no "TODO", no "pending verification", no "needs work later", no `[placeholder text]` markers, no "fix me", no "language to revise."

Editorial notes belong in:
- `_design-log/` (underscore-prefixed; excluded from build)
- `_audit-template.md` and other underscore-prefixed files (template only; excluded from build)
- handoff notes in the parent operating environment (private; not in this repo)
- commit messages (gitlog audit trail; not user-facing)

The audit format renders to public HTML. Anything in the source markdown will appear on the website. Treat the audit as a finished publication, not a working draft. If a section is genuinely unfinished, set `status: draft` in frontmatter so future tooling can skip it — don't publish placeholder text.

---

## PR / commit discipline

- **One logical concern per PR.** If the diff title needs an "AND" or a "+", split it.
- **Read CONTRIBUTING.md end-to-end before writing code** — versioning, structure, naming conventions, headless rules. Don't discover them in PR review.
- **Versioning + manifest hygiene** — bump `plugin.json`, `marketplace.json` (if applicable), add CHANGES entry on every release.
- **Backwards compat first.** New behavior never surprises an existing user. Default OFF; the user has to ask for the new thing.
