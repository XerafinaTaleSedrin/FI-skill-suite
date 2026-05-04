---
name: crossover
description: Computes the financial-independence threshold — when investment income covers expenses (or when bridge income covers cost-of-living through retirement). YMOYL Step 8, mode-aware for the user's chosen retirement frame, sensitivity-aware for the load-bearing assumptions. Writes the load-bearing answer to crossover-headline.md for /fi:fu-money-readout to echo.
layer: concept+pattern
ymoyl_step: 8
mode_aware: true
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 8 — capital and the crossover point"
  - author: Marika Olson
    contribution: "2026 design refinements — bridge math vs perpetual-portfolio math; load-bearing headline written here, echoed in fu-money-readout; shared profile files with fu-money-readout; two-scenario sensitivity for streams with early-reduced and waited-full options; trust-fund-haircut sensitivity for government retirement; same future-expense-reductions and active-income-forward-projection rules as fu-money-readout"
last-reviewed: 2026-05-03
---

# /fi:crossover

Reads holdings + monthly spending baseline + future-income-streams + future-expense-reductions + the user's chosen retirement frame, computes when (or whether) the user crosses the FI threshold, surfaces sensitivity to the load-bearing assumptions, and writes the load-bearing headline that `/fi:fu-money-readout` echoes at user-chosen cadence.

---

## The concept (decades-stable)

The crossover point is when monthly investment income exceeds monthly expenses. After that point, work for money becomes optional. YMOYL framed this as a single threshold; in 2026 reality, **the crossover is often a bridge problem, not a perpetual-portfolio problem.**

For users with future income streams that activate at known ages (employer pension, deferred annuity, Social Security / state pension equivalent), the FI math has two phases:

1. **Bridge years**: from FI target year to the activation age of the largest fixed-income stream. Portfolio funds the gap between active income (if any) and cost-of-living.
2. **Stacked-income years**: when fixed income streams (pension + government retirement income + any other annuities) exceed cost-of-living. Portfolio stops draining, may even grow.

The bridge math is often easier than the perpetual-portfolio math because the bridge is finite. A user whose projected fixed income (pension + government retirement) at full retirement age covers their cost-of-living doesn't need their portfolio to support spending forever — only to bridge from FI target year to full retirement age.

YMOYL hard-coded a 1992-era 15% bond yield. In 2026 (and forever after), the skill must pull current rates dynamically rather than trust any number embedded in the source.

---

## The pattern (~5-year stable)

Sensitivity-aware projection. NOT a single "you're FI at age X" output — instead, a sensitivity table showing how the answer changes if real return drops by 1%, if spending grows by 10%, if the user retires earlier, etc. The user's job is to see the *shape* of FI, not chase a specific number.

Output is two-tier:
- **Headline answer** (one line): the load-bearing crossover statement. Written to `crossover-headline.md` for `/fi:fu-money-readout` to echo at user-chosen cadence.
- **Full report** (markdown file): sensitivity table, scenario breakdowns, assumption log.

---

## What the skill does at runtime

1. **Reads `holdings.md`** for current invested assets, real estate, vehicles, mortgage balance, mortgage rate. Validates schema. Reports if missing — points at `/fi:holdings-scaffold`.

2. **Reads `~/finances/monthly-tabs/_trend-totals.csv`** (output from `/fi:track-flow`). Computes:
   - Median monthly active income (recent 3-month rolling, complete months only, anomalies excluded)
   - Median monthly gross expenses
   - Median monthly gross investment yield (capacity)
   - **Active-income forward-projection prompt**: *"Are there any income sources in this median that will end soon? UI benefits, severance, a contract ending, a side gig you're winding down?"* If yes, recompute post-cliff baseline.

3. **Reads `~/finances/profile/future-income-streams.md`** (shared with `/fi:fu-money-readout`). For each stream:
   - Pension / deferred annuity (employer-specific)
   - Government retirement income (locale-aware: US SSA / UK State Pension / CA CPP+OAS / etc.)
   - Other (rental net, royalties, annuities purchased)
   - **Future expense reductions** (mortgage payoff, auto loan payoff, student loan payoff) — symmetric to income streams; compute payoff date from current payment + balance + rate via amortization formula. **Trust the math, not lender-stated maturity** (lenders often display original 30-yr maturity even when user is paying above minimum scheduled P&I).

4. **Reads `~/finances/profile/retirement-frame.md`** for the user's chosen frame:
   - **Full stop**: traditional retirement; crossover target = 100% of expenses covered by passive + fixed income
   - **Location-time flexibility**: working partially; target = 60-80%
   - **Income downshift**: working in lower-income role aligned with values; target = 40-60%
   - **Coast FI**: invested enough that compounding alone reaches FI by traditional retirement age; target = 0% (test: existing invested × expected real return → target by year N?)

5. **Runtime freshness check**: pulls current 10-year Treasury yield (for safe-withdrawal-rate sensitivity), current S&P historical real return (for portfolio growth assumption), current inflation rate. **Does NOT hard-code these.** When WebFetch is unavailable, prompts user for current values.

6. **Computes the bridge analysis**:
   - **Year-of-stop**: when does monthly drainage stop? (active income + first activated future income ≥ expenses)
   - **Year-of-break-even**: when does monthly net hit zero or positive on cashflow basis?
   - **Year-of-stacked-income**: when does fixed income alone (no active income, no portfolio drawdown) cover cost-of-living?
   - **Bridge gap**: cumulative drawdown from FI target year to year-of-stacked-income, in nominal and real dollars.
   - **Available bridge capital**: accessible accounts (cash + brokerage taxable + Roth contributions if declared) at FI target year, after compounding.
   - **Bridge ratio**: available bridge capital / required bridge gap. >1.0 = bridge math works. <1.0 = bridge math is short by some amount.

7. **Sensitivity table** — vary the load-bearing assumptions, show how the answer shifts:
   - Real return on portfolio: ±1% from baseline (typically 5% real)
   - Spending baseline: ±10%
   - High-3 / pension multiplier: per the confidence interval declared in `future-income-streams.md`
   - Government retirement timing: early / full / late (e.g., SSA at 62 / 67 / 70)
   - Trust-fund haircut: locale-aware; for US, model SSA 2034 -19% scenario per current law; for UK, model State Pension means-testing scenarios; etc.
   - Mortgage payoff timing: as-amortized vs accelerated curtailments
   - Active income through bridge: zero / current-rate / declining 5%/yr / etc.

8. **Computes mode-aware crossover %** based on retirement frame:
   - Full stop: passive + fixed income ≥ 100% of expenses?
   - Location-time flex: 60-80%?
   - Income downshift: 40-60%?
   - Coast FI: existing invested × expected real return → reach target by year N?

9. **Writes the load-bearing headline** to `~/finances/profile/crossover-headline.md`. One line, plain text, computed from the bridge analysis. Format examples (placeholders, not user data):
   - *"Bridge math is solved. Portfolio holds indefinitely under both early and late activation scenarios."*
   - *"Bridge math is short by $X. Need active income of $Y/mo through age <pension-age> to close the gap."*
   - *"You hit FI threshold at age <est> under baseline assumptions; sensitivity shows <range> across the assumption space."*
   - *"Coast FI test passes: existing $X invested compounds to FI threshold by <target-year> with no further contributions."*

10. **Writes the full report** to `~/finances/crossover-YYYY-MM-DD.md`. Sensitivity table, scenario breakdowns, assumption log, year-by-year bridge cashflow projection.

---

## Output formats

### `~/finances/profile/crossover-headline.md`

```
---
last-computed: YYYY-MM-DD
computed-against: holdings.md (YYYY-MM-DD), _trend-totals.csv (YYYY-MM), future-income-streams.md (YYYY-MM-DD)
frame: <retirement-frame>
---
<one-line load-bearing answer>
```

Read by `/fi:fu-money-readout` for the headline echo.

### `~/finances/crossover-YYYY-MM-DD.md`

```markdown
---
date: YYYY-MM-DD
frame: <retirement-frame>
high-confidence: true|false
---

# Crossover analysis — YYYY-MM-DD

## Headline
<one-line answer>

## Bridge analysis
| Phase | Age range | Active income | Fixed income | Burn | Net |
|---|---|---|---|---|---|
| Pre-bridge | <FI-target> to <pre-payoff> | $A | $0 | $E | -$gap |
| Mortgage payoff | <payoff age> | $A | $0 | $E - $P&I | ... |
| Early pension activation | <pension age> | $A | $pension | ... | ... |
| Stacked income | <full-age>+ | $0 (assumed) | $pension + $govt-retirement | $E | +$surplus or breakeven |

## Sensitivity table
| Variable | Baseline | -1σ | +1σ | Effect on FI year |
|---|---|---|---|---|
| Real portfolio return | 5% | 4% | 6% | 50 → 53, 50 → 47 |
| Spending baseline | $X/mo | -10% | +10% | ... |
| Pension high-3 | $X | low estimate | high estimate | ... |
| Government retirement timing | full age | early | late | ... |
| Trust-fund-haircut scenario | scheduled | -19% | scheduled | ... |

## Assumption log
- ...

## Year-by-year bridge cashflow projection
(table)
```

---

## Architectural features

- **Bridge math, not perpetual-portfolio math.** When future fixed-income streams exceed cost-of-living at activation, the portfolio's job is to bridge — not support spending forever. This is often the more honest frame than the textbook "4% rule" perpetual-portfolio model. The skill defaults to bridge-math framing if `future-income-streams.md` declares any stream ≥ 50% of expense baseline.

- **Headline written here, echoed in fu-money-readout.** Decouples slow sensitivity math (run periodically) from fast daily orientation (echoed every readout). The headline file is the contract between skills.

- **Two-scenario for streams with reduced/full eligibility ages.** Same pattern as fu-money-readout — for FERS-deferred-annuity-style streams with both an early-reduced and waited-full option, run the analysis under both. Surface the time-arbitrage decision honestly. Counterintuitively, early-reduced often produces better bridge math in nuclear scenarios.

- **Trust-fund-haircut sensitivity (locale-aware).** Government retirement systems have known funding risks documented in their official statements. US SSA Trust Fund per current law: ~81% of scheduled benefits payable from 2034. UK State Pension: means-testing risk under future legislation. The skill surfaces the haircut scenario in the sensitivity table — does the FI math still work if scheduled benefits are reduced? Not a prediction; a sensitivity test.

- **Future expense reductions stack with future income streams.** Mortgage payoff, auto loan payoff, student loan payoff — same math, opposite sign. At a known future date (computed via amortization formula, not lender-stated maturity), monthly burn drops. Stacks with pension/government-retirement activations to close the bridge.

- **Active-income forward-projection.** Historical median from `/fi:track-flow` may include UI benefits, severance, ending contracts. Before bridge math, prompt user for ending sources. Use post-cliff baseline.

- **Mode-aware crossover %.** Different retirement frames have different success criteria. Full-stop = 100% passive + fixed coverage. Location-time-flex = 60-80%. Income-downshift = 40-60%. Coast FI = existing invested compounds to target. The skill reports against the user's chosen frame's target, not a universal 100% threshold.

- **Sensitivity over precision.** Don't report a single point estimate (e.g., "you'll be FI at age N"); report a range across the assumption space (e.g., "you cross the FI threshold somewhere in a window of years depending on which assumptions hold"). The shape of FI matters more than the point estimate.

---

## Headless behavior

Fully supported. Cron-friendly; produces an updated projection monthly. Writes both the headline file (1 line, for fu-money-readout to echo) and the full report (markdown, for human review).

When fired with no human present:
- Reads inputs as normal
- Computes against the current profile
- Writes the headline + full report
- Does NOT print to stdout
- Does NOT prompt interactively
- If `holdings.md` or `future-income-streams.md` is missing or stale: writes an error note to the report file with a clear next step, exits cleanly without overwriting the previous headline (don't write a stale headline).

---

## Privacy posture

This SKILL.md describes the procedure in general terms. User-specific data (account names, dollar amounts, pension figures, vendor patterns) is never embedded in the public skill files. All user data writes go to gitignored paths on the user's machine — `~/finances/profile/`, `~/finances/crossover-*.md`.

User-specific test artifacts and design logs live on the user's machine in their gitignored finance directory. They do not get published.

---

## Validation

Bridge-math framing emerged paired with `/fi:fu-money-readout` validation 2026-05-03. Findings encoded back into both SKILL.mds as design rules. The validation case: a user with both employer pension (US-FERS-style deferred annuity) and government retirement income (US SSA) where the perpetual-portfolio frame produced misleading "FI by mid-50s" answers when the bridge frame more honestly captured that fixed income at retirement age exceeds cost-of-living, making the portfolio's job temporally bounded rather than perpetual.

---

## TODO

- [ ] Real-return assumption methodology — what historical window? what inflation source?
- [ ] Mode-aware variants of the crossover math (4 frames) — implementation details
- [ ] Sensitivity-table format that's actually useful, not overwhelming
- [ ] Cross-reference with `/fi:redirect` for portfolio-mix assumptions
- [x] **Government-retirement-projection prompt UX** — pulled from official statement (US: ssa.gov; UK: gov.uk State Pension forecast; CA: My Service Canada Account; etc.). Locale-aware prompt copy.
- [ ] **Government earnings-record audit reminder** — when the user pulls their statement for the first time, surface a one-liner: *"While you have this open: scan year-by-year for missing or wrong earnings. If any look off, file the locale-appropriate correction form. One-time task, but missed earnings cost real benefit dollars later."* Don't make this a sub-skill; just a side note.
- [ ] Trust-fund-haircut scenario library by country (US 2034 SSA; UK State Pension means-testing; etc.) — keep updated as legislation changes.
- [ ] Year-by-year bridge cashflow projection format — visualization vs table.
- [ ] Worked examples in `examples/` for each retirement frame.
- [ ] Headline-file schema versioning — if format changes, fu-money-readout needs to handle gracefully.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 8 (capital and the crossover point). The 1992 framing assumed a single perpetual-portfolio threshold; the 2026 reframing as bridge-math acknowledges that most users have non-portfolio future income streams that change the shape of the answer.
- **Mr. Money Mustache** (online, 2012). The 4% rule popularized for FI; folded in as one of several real-return assumptions for sensitivity testing, not as the load-bearing answer.
- **Marika Olson** (2026). Design refinements: bridge math vs perpetual-portfolio math (acknowledges that FERS/SSA-equivalent streams change the shape of FI from "support spending forever" to "bridge to retirement age"); load-bearing headline written here and echoed in fu-money-readout (decouples slow sensitivity math from fast daily orientation); shared profile files with fu-money-readout (single source of truth for future-income-streams + future-expense-reductions); two-scenario sensitivity for streams with early-reduced and waited-full options; trust-fund-haircut sensitivity for government retirement; future-expense-reductions (mortgage payoff symmetric to future-income-streams); active-income forward-projection (don't trust UI-inflated medians for bridge math); compute-payoff-from-current-payment rule (lender-stated maturity unreliable when user paid above minimum scheduled P&I); mode-aware target thresholds (frame-specific success criteria, not universal 100%).
