# Hardening pass readout — 2026-07-14

Steward pass over the live suite (Jack role): tighten what exists, add nothing, publish nothing. Every change is on branch `claude/fi-skill-suite-hardening-0d8k47`, one concern per commit, each edited file snapshotted as `<file>.bak` in the first commit so `.bak` + diff tells the whole story. **Nothing pushed to main; no manifest bump; no release.** All of it awaits Marika's review.

---

## Ranked summary — strongest tightenings first

1. **Deterministic invariants folded into every computing skill** (commit `e30d2ed`). New AGENTS.md §Deterministic invariants (recompute by a second route; stop on failure; never write output that fails its own math) plus a compact checks section in all nine skills: track-flow's ledger identities (net = income + expense, category sums = gross expenses, row conservation), holdings-scaffold's net-worth-two-ways + roll-ups-sum-to-100, crossover's bridge-row identity + sensitivity monotonicity + headline-position consistency, hourly-wage's blended-is-a-ratio-of-sums, etc. This is the guard against confidently-wrong finance output. Backwards compatible by construction — checks change no computation, they only gate wrong output.
2. **Frontmatter of four skills failed strict YAML parsing** (`f786b58`). holdings-scaffold, hourly-wage, track-flow, crossover had unquoted scalars containing `: ` (e.g. `/fi: skill`, `baseline-source: manual` inside status-history). A strict-YAML consumer of the plugin chokes on these. Quoted; content unchanged. money-date's `layer: pattern` (out of enum) → `concept+pattern`; `ymoyl_step: cadence-companion` → `n/a`.
3. **Income-streams contract drift healed** (`80639bf`). The 2026-05-23 decision made holdings.md the single source of truth for income streams, but fu-money-readout still read (and fully documented) the superseded `profile/future-income-streams.md`, and crossover kept two leftover references. All three sides now agree; a legacy file is still read as fallback with a one-time migration offer, so nobody's existing setup breaks.
4. **Privacy strip** (`8b18309`). Real UI-benefit figures (weekly amount / funds remaining / end date), a six-figure buyout amount + "USAID" as deposit source, a named-platform rebalance trace, a refund composite, two dated private-validation references, `life/finances/`, WA-specific "B&O tax" — all in track-flow; a Komorebi private-memory cross-ref in wallchart; the author-tracing "age 57" in fu-money-readout. Stripped, not paraphrased.
5. **Path resolution unified on `<finances_root>`** (`c704499`). Only wallchart complied with AGENTS.md's resolution order; six skills hard-coded `~/finances/`, hourly-wage had invented a competing env var (still honored as a legacy alias), and holdings-scaffold never mentioned the `.fi-root` sentinel AGENTS.md says it owns — it now writes/verifies it in Step 6.
6. **AGENTS.md contract table rebuilt against reality** (`35091e2`). Three dead `SCHEMA.md` pointers, two wrong reader claims (wallchart doesn't read `_trend-categories.csv`; crossover doesn't read `wallchart.md`), missing readers, ~14 missing sentinel rows, a stale `/fi:audit` row, a deprecated-sentinel note, and a latest-by-filename-date rule.
7. **`_trend-totals.csv` schema accuracy** (`8f43750`). The `complete` flag was documented `true|false` but exampled and grepped as `partial` — three consumers filter on the literal value. Canonicalized to `true|false`. Also "Eleven-column" → twelve.
8. **Runtime-freshness rewording** (`1943a21`). redirect's "runtime freshness check" step baked a specific year's contribution limits into its own prompt copy ("The 2026 limit is $7,000..."); now it names what to fetch and the authoritative source, values-free. crossover's SSA 2034/−19% mentions are now explicitly labeled tool-layer shape-examples to re-verify at runtime.
9. **Stale-audit purge + doc accuracy** (`3193b69`, `422755c`). CLAUDE.md claimed 12 skills (9 exist), still advertised `/fi:audit` + `book-audits/`, omitted money-date; README's structure diagram listed two directories that don't exist; CONTRIBUTING still *invited* book-audit submissions — contradicting CLAUDE.md's "audits are CLOSED" and pointing contributors at an unmergeable PR. All reconciled. Conduct-section typos fixed.
10. **Smaller drift fixes**: vendor map unified on `profile/vendor-defaults.md` (`0f8e666`); wallchart's retired "investment-income-method" purged from frontmatter/headless + the headless new-outlier gap closed (`63a0a32`); money-date's gitignore posture raised from warn-and-write to add-before-write per AGENTS rule 2 (`84f4ff3`).

## Per-skill: which of the 7 QA checks flagged

| Skill | 1 frontmatter | 2 layer | 3 contracts | 4 privacy | 5 freshness | 6 invariants | 7 clarity |
|---|---|---|---|---|---|---|---|
| holdings-scaffold | **fixed** (YAML) | flagged (aggregator tables → tools/) | **fixed** (.fi-root duty) | ok | ok | **added** | ok |
| fu-money-readout | ok | ok | **fixed** (income streams, paths) | **fixed** (age 57) | ok | **added** | ok |
| track-flow | **fixed** (YAML) | flagged (aggregator table) | **fixed** (complete flag, vendor map, paths) | **fixed** (5 items) | ok | **added** | ok |
| crossover | **fixed** (YAML) | flagged (US tax rules inline → references/tax/US.md) | **fixed** (2 leftovers, paths) | ok | **fixed** (SSA note) | **added** | ok |
| hourly-wage | **fixed** (YAML) | flagged (SS wage base etc., hedged inline) | **fixed** (vendor map name, env var) | ok | ok (hedges present) | **added** | ok |
| wallchart | ok | ok | **fixed** (complete flag, method leftovers) | **fixed** (Komorebi ref) | ok | **added** | **fixed** (headless outlier) |
| three-questions | ok | ok | **fixed** (paths) | ok | ok | **added** | note: "3-letter shorthand" describes 1-char symbols (cosmetic, left) |
| redirect | ok | ok | **fixed** (paths, [latest] rule) | ok | **fixed** (limits) | **added** | ok |
| money-date | **fixed** (layer/step enums) | ok | **fixed** (paths) | ok | ok | **added** | **fixed** (gitignore posture) |

## Left for Marika's call (deliberately NOT changed)

1. **Status sync direction.** 00-overview's table says holdings-scaffold / fu-money-readout / track-flow / crossover are **alpha** (promotions recorded 2026-05-22 on real-run evidence), but each skill's frontmatter still says `status: draft`. Also holdings-scaffold's `## Status` section still reads "Not yet tested in a live invocation" — contradicted by its own status-history. Syncing frontmatter to the recorded promotions looks right, but status promotion is yours.
2. **Layer re-homes (proposed, not moved).** Tool-layer content living inline that belongs in `tools/` with `last-reviewed` + replacement-shape: (a) the aggregator export-shape tables in holdings-scaffold Step 4a and track-flow Step 1 → `tools/transaction-aggregators.md`; (b) `api.frankfurter.dev` (holdings-scaffold, track-flow) → `tools/fx-sources.md`; (c) the ticker→asset-class map (holdings-scaffold Step 4b) → a dated tools/reference entry. `tools/` currently holds only the template — these would be its first real entries, and granularity is your call.
3. **`references/tax/US.md` doesn't exist** though crossover's bridge-capital tiers and redirect's placement audit lean on it; the US baseline currently lives inline in crossover (works, but it's the natural first country file and your stated expertise).
4. **redirect references `references/ips-template.md` and `references/funds/<TICKER>.md`** — neither exists (its TODOs acknowledge). Dead references until authored.
5. **`_trend-categories.csv` has no consumer.** track-flow writes it "for /fi:wallchart" but wallchart never reads it. Keep writing it (cheap, future per-category panels) or drop the claim?
6. **External-attribution question.** README acknowledges Kate Chapman's "per-skill SKILL.md + SCHEMA.md discipline" — this suite never adopted standalone SCHEMA.md files (the contract table now points at SKILL.md sections). Wording is yours to adjust or leave.
7. **exit-skill-suite (`/xp:`) pass — flags only, no edits.** All 7 stubs parse clean, all honestly `status: scaffold`, layers valid — stub-vs-finished labeling is accurate throughout (readiness-score is the most developed leg). Before that repo ever publishes: README carries private Komorebi cross-refs (`.claude/agents/jack.md`, `work/moc/research/20260624_...`, the "Rosalind-vet" note) that are dead links to strangers — same strip rule the FI suite's checklist mandates. Left untouched because the repo is explicitly pre-publication working state.

## Verification run

- YAML: all 9 frontmatters parse under strict `yaml.safe_load`; `layer` ∈ enum; required fields present.
- Greps: no operational references remain to `future-income-streams.md` (outside legacy-fallback/deprecation notes and historical status-history), `mixed-purpose-vendors.md`, `SCHEMA.md`, `/fi:audit`-as-live, or hard-coded `~/finances/` data paths (the survivors are the resolution-order text itself, one historical status-history entry, and holdings-scaffold's concrete default *offer*).
