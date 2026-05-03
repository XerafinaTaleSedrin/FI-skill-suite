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
3. **Asks the user for third-leg income inputs** — these used to live in `/fi:lifetime-earnings` (deleted 2026-05-02; reasoning in `book-audits/2026-05-01-ymoyl.md` §4 and the holdings-scaffold SKILL.md design notes); now folded in here as direct prompts:
   - Projected SSA / Social Security benefit at 62, full retirement age, and 70 (30 seconds on user's SSA statement at ssa.gov).
   - Pension benefit if applicable, with eligibility year and any uncertainty (e.g., pending litigation, vesting schedule).
   - Annuity income if applicable.
   These are the income streams that bridge or supplement portfolio withdrawals — load-bearing for the crossover math, especially in mode-aware variants.
4. Asks the user (or reads from profile) the retirement frame.
5. **Runtime freshness check**: pulls current 10-year Treasury yield, current S&P historical real return, current inflation rate. Does NOT hard-code these.
6. Computes:
   - Crossover age (using assumed real return + third-leg income from step 3).
   - Crossover sensitivity table (real return ±1%, spending ±10%, contribution rate ±2%, SSA-benefit timing 62/FRA/70).
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
- [ ] Cross-reference with `/fi:redirect` for portfolio-mix assumptions.
- [ ] **SSA-benefit-projection prompt UX** — when the user doesn't have their SSA statement on hand, offer the choice between (a) pause the skill and come back, (b) skip third-leg input and run portfolio-only crossover (note that the result will be conservative — likely understates true crossover age by 5-15 years for users with substantial SS earnings history). Document the conservative-skip outcome clearly.
- [ ] **SSA-earnings-record audit reminder** — when the user pulls their SSA statement for the first time, surface a one-liner: *"While you have this open: scan year-by-year for missing earnings. If any look wrong, file SSA Form 7008 to correct. One-time task, but missed earnings cost real benefit dollars later."* Don't make this a sub-skill; just a side note.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 8.
- **Mr. Money Mustache** (online, 2012). The 4% rule popularized for FI; folded in as one of several real-return assumptions.
