# Last reviewed

This file tracks the last full review of the repo's contents. The intent: at any time, a reader can see how stale the *aggregate* repo is, separate from any individual file's freshness.

---

## Most recent review

- **2026-07-14** — Full hardening pass (every SKILL.md read end-to-end; branch `claude/fi-skill-suite-hardening-0d8k47`, readout in `_design-log/2026-07-14-hardening-pass-readout.md`): YAML frontmatter parse fixes, privacy strip per the AGENTS.md checklist, income-streams contract drift healed, `<finances_root>` resolution unified, contract table rebuilt, deterministic invariants folded into all nine skills. Status sync: holdings-scaffold / fu-money-readout / track-flow / crossover frontmatter promoted draft → alpha, matching the 2026-05-22 index promotions. **beta** rung added to the status legend (non-author run + no contract drift + checks exercised live); nothing qualifies yet.

---

## Review history

(Reverse chronological; append at top.)

- **2026-07-14**: Hardening pass + status sync (see above). Four skills' frontmatter draft → alpha on already-recorded real-run evidence; beta gate defined.
- **2026-05-12** PM: `audit` draft → alpha. Profit First audit complete. All 9 skills with at least one real-world run now reach alpha: holdings-scaffold, fu-money-readout, track-flow, crossover, audit.
- **2026-05-12** AM: `audit` scaffold → draft.
- **2026-05-09**: `hourly-wage` + `three-questions` + `wallchart` + `redirect` scaffold → draft.
- **2026-05-01**: Initial scaffold. All skills at `status: scaffold`. Inaugural Rogue Reads audit shipped same day: YMOYL, Hearth verdict `nap-worthy` (book) / `windowsill-approved` (tools).

---

## Next review due

- **2026-10-14** target — quarterly review per "What review means" below; includes the first `last-reviewed > 6 months` staleness sweep of any `tools/` entries authored by then.
- Standing gates (event-driven, not dated): wallchart's clean second walkthrough → alpha; first non-author run through holdings-scaffold + track-flow → first beta candidates.

(Earlier targets — 2026-06-01 iteration pass, 2026-07-01 first audit, 2026-Q3 first runnable skill — all met; see history.)

---

## What "review" means

- Read every `SKILL.md` end-to-end. Confirm frontmatter is current. Confirm sources cited still resolve.
- Check `tools/` register for stale entries (anything `last-reviewed > 6 months` gets re-verified or moved to "no longer recommended").
- Check `references/tax/` files for anything `last-reviewed > 12 months` and ping the original contributor or author an update PR.
- Confirm the README's getting-started section still works.
- Confirm the architecture rule (concept / pattern / tool) hasn't been violated by drift.
