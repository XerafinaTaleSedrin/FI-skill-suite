# AGENTS.md — cross-skill rules

Rules that apply across every skill in `FI-skill-suite`. If you find yourself copy-pasting a behavior across multiple `SKILL.md` files, factor it here and reference back — single source of truth, no silent divergence.

---

## Privacy posture (every skill)

1. **Never auto-sync user data anywhere.** No phone-home, no telemetry, no cloud backup unless the user explicitly invokes a backup command.
2. **Never auto-commit user financial files to git.** All skills that write to `holdings.md`, transaction logs, or monthly tabs must check for `.gitignore` coverage before writing — and add the file to `.gitignore` if not already covered. If the user's working directory is not a git repo, write a clear "DO NOT COMMIT" warning header at the top of the file.
3. **Never log sensitive content to debug output.** Account balances, account names, transaction details, net-worth figures — these are PHI-equivalent for personal finance. Don't print them outside the skill's intended user-facing output.
4. **Never include user financial details in error messages or stack traces.** If a skill crashes mid-flow, the error should describe the failure shape, not the data shape.

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

## Cross-skill data contracts

Skills that read from / write to shared sentinel files must respect the schema:

| Sentinel file | Owner skill | Reader skills | Schema source |
|---|---|---|---|
| `holdings.md` (user repo) | `/fi:holdings-scaffold` | `/fi:fu-money-readout`, `/fi:crossover`, `/fi:investing`, `/fi:monthly-tabulation` | See `skills/holdings-scaffold/SCHEMA.md` |
| `transactions/<YYYY-MM>.csv` (user repo) | `/fi:track-spending` | `/fi:monthly-tabulation`, `/fi:three-questions`, `/fi:wallchart` | See `skills/track-spending/SCHEMA.md` |
| `wallchart.md` (user repo) | `/fi:wallchart` | `/fi:crossover` | See `skills/wallchart/SCHEMA.md` |
| `book-audits/<DATE>-<book>.md` (this repo) | `/fi:audit` | (read by humans, surfaced in cross-references) | See `book-audits/_audit-template.md` |

**Rule:** if a skill reads from a sentinel file, it MUST validate the schema and fail loudly if the file is malformed. Don't silently ignore unexpected fields.

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
