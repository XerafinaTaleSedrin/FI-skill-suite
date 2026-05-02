---
name: fi-track-spending
description: Captures every penny of spending — YMOYL Step 2b. Aggregator-import OR manual capture, with category schema that downstream skills read.
layer: concept+pattern
ymoyl_step: 2
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 2b — track every dollar (no rounding)"
last-reviewed: 2026-05-01
---

# fi-track-spending

Captures the user's every-penny spending into a per-month transaction log. Two modes: (1) import from an aggregator export (Monarch, Copilot, plain CSV), or (2) manual capture. Output is a per-month transaction file other skills (`fi-monthly-tabulation`, `fi-three-questions`, `fi-wallchart`) read from.

---

## The concept (decades-stable)

Every dollar in and out, no rounding, no "estimating." YMOYL is firm on this — partial tracking produces partial consciousness. The discomfort of capturing everything (including the embarrassing or inconsistent purchases) is the point; rounding lets the data lie back to you.

---

## The pattern (~5-year stable)

A category-tagged transaction log per month, stored in `~/finances/transactions/YYYY-MM.csv` (or `.md` for manual capture). Categories are user-defined but follow a stable taxonomy so cross-month comparison works. Aggregator imports get re-tagged manually (aggregators are notoriously bad at categorizing).

---

## What the skill does at runtime

1. Asks: aggregator import or manual capture?
2. **Aggregator import**: walks the user through exporting from their aggregator (Monarch, Copilot, etc.); imports the CSV; re-tags categories per the user's taxonomy.
3. **Manual capture**: walks the user through entering each transaction since the last capture session.
4. Validates that no duplicates exist, no obvious gaps in dates.
5. Writes to `~/finances/transactions/YYYY-MM.csv`.
6. Reports completeness (any gaps, any uncategorized, any unusual totals).

---

## Headless behavior

Aggregator-import mode supports headless invocation when the export file is at a known path. Manual capture mode is interactive only.

---

## TODO

- [ ] Define the canonical category taxonomy (with country-agnostic core and locale-extensible).
- [ ] Aggregator-specific import flows for Monarch, Copilot, Lunch Money, plain CSV.
- [ ] Output schema for the transactions CSV so downstream skills can read.
- [ ] De-duplication logic for re-imports.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2b.
