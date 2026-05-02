---
name: fi-wallchart
description: Plots monthly income vs. spending vs. investment income across all logged months. YMOYL Step 5 long-arc visual.
layer: concept+pattern
ymoyl_step: 5
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 5 — make life energy visible via long-arc chart"
last-reviewed: 2026-05-01
---

# fi-wallchart

Reads all available monthly tabs + holdings.md (for investment income trend) and produces YMOYL's wall chart: three lines plotted over time (monthly income, monthly spending, monthly investment income). The crossover where investment income meets spending is the FI threshold.

---

## The concept (decades-stable)

Three numbers, plotted side by side over time, are an emotional anchor that no spreadsheet replicates. Watching the curves bend over months and years makes financial behavior real in a way the underlying numbers don't.

The wallchart is meant to be visible — printed, taped to a wall, looked at every day. The skill produces both the data and a renderable chart format (initially: ASCII art for terminals; later: SVG / PNG for printing).

---

## The pattern (~5-year stable)

Aggregate monthly data → render a chart with three series (income, spending, investment income) → write to a sentinel file the user can re-render or update over time.

---

## What the skill does at runtime

1. Reads all `~/finances/monthly-tabs/YYYY-MM.md` files (sorted by date).
2. Reads `holdings.md` to compute monthly investment income (dividends + interest + rental net + other passive).
3. Aggregates into a data table.
4. Renders an ASCII chart (initial implementation); optional SVG output for printing.
5. Writes to `~/finances/wallchart.md` (data) + `~/finances/wallchart.svg` (image, when implemented).
6. Highlights the crossover point if visible (where investment income meets spending).

---

## Headless behavior

Fully supported. Cron-friendly; produces an updated chart on a monthly cadence.

---

## TODO

- [ ] Investment-income computation methodology (snapshots vs. trailing-12-month vs. forward-projection).
- [ ] Chart rendering — start with ASCII; later add SVG/PNG via matplotlib or similar.
- [ ] Crossover detection logic and visual call-out.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 5.
