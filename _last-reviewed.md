# Last reviewed

This file tracks the last full review of the repo's contents. The intent: at any time, a reader can see how stale the *aggregate* repo is, separate from any individual file's freshness.

---

## Most recent review

- **2026-05-14** — `hourly-wage` tightening pass (no new features). Added gitignore enforcement to Step 8 (parity with track-flow Step 10 and holdings-scaffold Step 3 — was a real privacy gap), deduped PTO valuation between Steps 3 and 3.5, removed speculative `/fi:track-flow` canonical-category names from Step 4 that didn't match the actual contract in AGENTS.md, added `Validation status` section + privacy footer (parity with track-flow). Skill remains at `draft` pending a real-data walkthrough on at least one work mode — that walkthrough is the next promotion gate.

---

## Review history

(Reverse chronological; append at top.)

- **2026-05-14**: `hourly-wage` tightening pass — gitignore enforcement, dedup, contract honesty, validation-status section. No new features. Still draft.
- **2026-05-12** PM: `audit` draft → alpha. Profit First audit complete. All 9 skills with at least one real-world run now reach alpha: holdings-scaffold, fu-money-readout, track-flow, crossover, audit.
- **2026-05-12** AM: `audit` scaffold → draft.
- **2026-05-09**: `hourly-wage` + `three-questions` + `wallchart` + `redirect` scaffold → draft.
- **2026-05-01**: Initial scaffold. All skills at `status: scaffold`. Inaugural Rogue Reads audit shipped same day: YMOYL, Hearth verdict `nap-worthy` (book) / `windowsill-approved` (tools).

---

## Next review due

- **2026-06-01** target — first iteration pass with Marika to flesh out the YMOYL-specific skills based on her active reading.
- **2026-07-01** target — book audit pipeline runnable; first audit published (likely YMOYL or Profit First).
- **2026-Q3** target — first runnable skill (likely `/fi:holdings-scaffold` since it's the gateway).

---

## What "review" means

- Read every `SKILL.md` end-to-end. Confirm frontmatter is current. Confirm sources cited still resolve.
- Check `tools/` register for stale entries (anything `last-reviewed > 6 months` gets re-verified or moved to "no longer recommended").
- Check `references/tax/` files for anything `last-reviewed > 12 months` and ping the original contributor or author an update PR.
- Confirm the README's getting-started section still works.
- Confirm the architecture rule (concept / pattern / tool) hasn't been violated by drift.
