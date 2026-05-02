---
name: crossover
description: Computes the financial-independence threshold — when investment income covers expenses. YMOYL Step 8, mode-aware for the user's chosen retirement frame.
layer: concept+pattern
ymoyl_step: 8
mode_aware: true
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 8 — capital and the crossover point"
last-reviewed: 2026-05-01
---

# /fi:crossover

Reads holdings + monthly spending baseline + the user's chosen retirement frame, computes when (or whether) the user crosses the FI threshold, and surfaces sensitivity to the load-bearing assumptions.

---

## The concept (decades-stable)

The crossover point is when monthly investment income exceeds monthly expenses. After that point, work for money becomes optional. The math depends on:

- Current invested assets
- Expected real return on those assets
- Monthly spending
- Future contributions
- The user's retirement frame (full stop / location-time flex / income downshift / Coast FI)

YMOYL hard-coded a 1992-era 15% bond yield. In 2026 (and forever after), the skill must pull current rates dynamically rather than trust any number embedded in the source.

---

## The pattern (~5-year stable)

Sensitivity-aware projection. NOT a single "you're FI at age X" output — instead, a sensitivity table showing how the answer changes if real return drops by 1%, if spending grows by 10%, if the user retires earlier, etc. The user's job is to see the *shape* of FI, not chase a specific number.

---

## What the skill does at runtime

1. Reads `holdings.md` for current invested assets.
2. Reads recent monthly tabs for spending baseline.
3. Reads `lifetime-earnings.md` if available (informs realistic-savings-rate sanity check).
4. Asks the user (or reads from profile) the retirement frame.
5. **Runtime freshness check**: pulls current 10-year Treasury yield, current S&P historical real return, current inflation rate. Does NOT hard-code these.
6. Computes:
   - Crossover age (using assumed real return).
   - Crossover sensitivity table (real return ±1%, spending ±10%, contribution rate ±2%).
   - Mode-aware crossover %: full-stop = 100%, location-time = 60-80%, downshift = 40-60%, Coast FI = compounding-to-target check.
7. Writes to `~/finances/crossover-YYYY-MM-DD.md`.

---

## Headless behavior

Fully supported. Cron-friendly; produces an updated projection monthly.

---

## TODO

- [ ] Real-return assumption methodology — what historical window? what inflation source?
- [ ] Mode-aware variants of the crossover math (4 frames).
- [ ] Sensitivity-table format that's actually useful, not overwhelming.
- [ ] Cross-reference with `/fi:investing` for portfolio-mix assumptions.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 8.
- **Mr. Money Mustache** (online, 2012). The 4% rule popularized for FI; folded in as one of several real-return assumptions.
