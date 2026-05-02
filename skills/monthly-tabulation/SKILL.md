---
name: monthly-tabulation
description: Aggregates a month of transactions into category totals + life-energy-cost per category. YMOYL Step 3.
layer: concept+pattern
ymoyl_step: 3
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 3 — monthly tabulation by category, with life-energy cost"
last-reviewed: 2026-05-01
---

# /fi:monthly-tabulation

Reads a month's transactions (from `/fi:track-spending`) and produces a category-aggregated monthly tab — total dollars per category PLUS life-energy cost per category (using the user's real hourly wage from `/fi:hourly-wage`).

---

## The concept (decades-stable)

A category total in dollars is information. A category total in *hours of life energy* is consciousness. YMOYL's load-bearing move at Step 3 is multiplying every category by the inverse of the real hourly wage — so "$300 on streaming subscriptions" becomes "12 hours of your life this month."

---

## The pattern (~5-year stable)

Read transactions, aggregate by category, multiply by inverse of real hourly wage, output the dual-currency view.

---

## What the skill does at runtime

1. Reads `~/finances/transactions/YYYY-MM.csv` (latest by default; user can specify a month).
2. Reads the latest `hourly-wage-YYYY-MM-DD.md` from `/fi:hourly-wage`.
3. Computes per-category totals + life-energy cost (hours = dollars / real-hourly-wage).
4. Reports the tabulation as a markdown table.
5. Writes to `~/finances/monthly-tabs/YYYY-MM.md` for `/fi:three-questions`, `/fi:wallchart`, and `/fi:crossover` to read.

---

## Headless behavior

Fully supported. Cron can run this on the 1st of the month to produce the prior-month tab.

---

## TODO

- [ ] Schema for the monthly tab output file.
- [ ] Handling for un-categorized transactions (block? warn? let them flow as "uncategorized"?).
- [ ] Trend-line view across multiple months.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 3.
