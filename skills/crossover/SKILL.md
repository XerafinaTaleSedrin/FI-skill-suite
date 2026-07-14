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
  - book: Just Keep Buying (Maggiulli, 2022)
    contribution: "The 'transfer the load' framing of the crossover point — keep buying income-producing assets until they out-earn your labor and carry you by the time you can no longer work. Conceptual reinforcement of YMOYL Step 8 rather than a new mechanic."
  - author: Marika Olson
    contribution: "2026 design refinements — bridge math vs perpetual-portfolio math; load-bearing headline written here, echoed in fu-money-readout; income streams read from holdings.md (single source of truth) rather than a separate profile file; future expense reductions derived from holdings.md liabilities via amortization (not a separate input); two-scenario sensitivity for streams with early-reduced and waited-full options; trust-fund-haircut sensitivity for government retirement; active-income-forward-projection rule"
last-reviewed: 2026-05-23
status-history:
  - "2026-05-03: draft (initial design — compute crossover as output, bridge-math framing, two-tier output, sensitivity-aware)"
  - "2026-05-23: draft + data-flow correction. Income streams now read from `holdings.md` `## Income streams (non-labor)` section (added by holdings-scaffold Step 4d earlier same session) rather than a separate `~/finances/profile/future-income-streams.md` file. Future expense reductions clarified as derived from holdings.md liabilities via amortization, not a separate input file. Single source of truth, no contract drift. Caught when the crossover walkthrough hit a fork — tonight's holdings-scaffold edit had created two homes for the same data without resolving which is canonical."
  - "2026-05-23: draft + retirement-frame.md stays as a separate profile file (decision recorded). Different kind of data from holdings.md (stated intention, not a measurement) and different cadence (rarely changes; tied to life events). Headless behavior updated to write a setup template when the file is missing so the user has a clear next step rather than a hard fail."
  - "2026-05-23: draft + manual-baseline override for spending when `_trend-totals.csv` is missing. A first-time crossover analysis should not require having already run `/fi:track-flow` — the skill now prompts for rough monthly numbers and tags the run as `baseline-source: manual` (with inline caveat in the headline). Preferred behavior: prefer track-flow data automatically once it becomes available on a later run. Headless mode still hard-fails on missing track-flow (no human present to provide the override)."
  - "2026-05-23: draft + 7 load-bearing-and-medium gaps closed from real-data walkthrough: (C) `birth_year` field added to `retirement-frame.md` — was the missing anchor for all age-relative math; (F) `desired_action_age` field added to same file — distinct from FI crossover age, used for behavior planning and bridge-start anchoring; (G) bridge-capital accessibility tiers defined (Tier 1 fully accessible, Tier 2 rule-gated like Roth contributions / Rule of 55 / 72(t), Tier 3 penalty-unless-age-gated, Tier 4 fully restricted) with per-locale rules referenced via `references/tax/<COUNTRY>.md`; (J) tax-on-bridge-withdrawal subsection added — without it, bridge capital was overstated 20–30%; covers LTCG / ordinary / Roth-qualified / HSA-medical-vs-non / cash with US baseline; (D) real-return methodology defined — default 5% real for 70/30, portfolio-mix-aware scale, live-rate sanity check, user override, sensitivity ±1pp; (E) mode-aware crossover math per frame defined — full-stop ≥100%, location-time-flex 60–80% (reports both ends + implied hours-per-week), income-downshift 40–60% (reports both ends or explicit downshift target), coast-FI binary with margin shown; (K) inflation handling — projects in nominal by default with both nominal+real rendered, expense baseline grows at expected inflation, income streams grow per `cola_adjusted` flag (from holdings.md), portfolio returns already real (don't double-count). TODOs #1 and #2 marked done; new TODOs added for per-country tax references and sequence-of-returns risk modeling."
---

# /fi:crossover

Reads holdings + monthly spending baseline + future-income-streams + future-expense-reductions + the user's chosen retirement frame, computes when (or whether) the user crosses the FI threshold, surfaces sensitivity to the load-bearing assumptions, and writes the load-bearing headline that `/fi:fu-money-readout` echoes at user-chosen cadence.

---

## The concept (decades-stable)

The crossover point is when monthly fixed retirement income (pension + government retirement + any other annuity income) exceeds monthly expenses. After that point, work for money becomes optional and the portfolio's job is bridge-only, not perpetual.

**Critical framing — compute the crossover, don't ask the user to set it.** YMOYL and most FI guides ask the user to pick a target year ("when do you want to retire?") and then evaluate whether they'll get there. This skill inverts that: **based on current numbers, here is your crossover age. The bridge years are then defined backwards from that computed answer.**

The user does not pick "FI target year." The skill computes "FI crossover age" as an output and then names the bridge years that fall between today (or the user's optional desired-action age) and that crossover.

For some users, the answer is: *"You are already past the FI threshold. You're FI now."* The skill should state this clearly when it's true, rather than burying the finding in sensitivity tables. Many users with employer pensions + government retirement income + a paid-down mortgage + reasonable savings cross the threshold earlier than they realize.

For users with future income streams that activate at known ages (employer pension, deferred annuity, Social Security / state pension equivalent), the FI math has two phases:

1. **Bridge years**: from today (or desired-action age) to the FI crossover age. Portfolio funds any gap between active income and cost-of-living. May be zero years if the user is already past crossover.
2. **Post-crossover years**: when fixed income streams alone cover cost-of-living. Portfolio stops draining, may even grow. Active work becomes optional.

The bridge math is often easier than the perpetual-portfolio math because the bridge is finite. A user whose projected fixed income at full retirement age covers their cost-of-living doesn't need their portfolio to support spending forever — only to bridge from today to that activation age.

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

2. **Reads `~/finances/monthly-tabs/_trend-totals.csv`** (output from `/fi:track-flow`) when available. Computes:
   - Median monthly active income (recent 3-month rolling, complete months only, anomalies excluded)
   - Median monthly gross expenses
   - Median monthly gross investment yield (capacity)
   - **Active-income forward-projection prompt**: *"Are there any income sources in this median that will end soon? UI benefits, severance, a contract ending, a side gig you're winding down?"* If yes, recompute post-cliff baseline.

   **Manual-override fallback (when `_trend-totals.csv` is missing or stale):** Don't hard-fail — a first-time crossover analysis should not require having run `/fi:track-flow` first. Prompt instead:

   > *"No track-flow data found (or it's older than 90 days). Give me rough monthly numbers so we can still run a provisional analysis: monthly gross expenses, monthly active income, monthly investment yield if you know it. We'll tag this run as `baseline-source: manual` so you know to refresh once track-flow is set up."*

   Capture the manually-stated baseline, mark the run as provisional in both the headline file (`baseline-source: manual` in frontmatter, plus inline caveat in the headline) and the full report (banner: *"Baseline manually estimated; sensitivity-table widths should be read with extra caution"*). When `/fi:track-flow` data becomes available on a later run, prefer it automatically.

3. **Reads income streams from `holdings.md` `## Income streams (non-labor)` section** (the cross-skill source of truth; populated by `/fi:holdings-scaffold` Step 4d). For each stream:
   - Pension / deferred annuity (employer-specific)
   - Government retirement income (locale-aware: US SSA / UK State Pension / CA CPP+OAS / etc.)
   - Other (rental net, royalties, annuities purchased)

   Reads per-stream fields: `name`, `kind`, `monthly_amount`, `currency`, `status` (active / future-activates-at-date / future-activates-at-event / expires-at-date / expires-at-event), `activation`, `expiration`, `cola_adjusted`, `taxable_treatment`, `source`. Multi-scenario streams (e.g., an employer pension claimable at an earlier age with a per-year reduction vs full at full eligibility age; a government retirement benefit claimable across a range of ages with different per-age multipliers) are captured as separate stream entries in holdings.md — crossover models scenarios against the options, doesn't ask the user to pick one upfront.

   **Future expense reductions** are NOT a separate input file — they're *derived from `holdings.md` `## Liabilities`* via amortization. For each liability with `rate`, `balance`, and current monthly payment, compute the payoff date from current payment + balance + rate. **Trust the math, not lender-stated maturity** (lenders often display original 30-yr maturity even when the user is paying above minimum scheduled P&I). Mortgage payoff, auto loan payoff, student loan payoff all fold in this way — symmetric to income stream activations, opposite sign on the burn line.

4. **Reads `~/finances/profile/retirement-frame.md`** for the user's personal-intention data — three fields, separate from holdings.md (different cadence: holdings is monthly, frame is rare/life-event-driven):
   - **`birth_year`** (YYYY) — required. Anchors all age-relative math: years until crossover, years on the bridge, age at each future stream activation. The skill computes current age as `(today - birth_year)` for the projection year, not asking interactively each run.
   - **`frame`** (required) — one of:
     - **Full stop**: traditional retirement; crossover target = passive + fixed income ≥ 100% of expenses
     - **Location-time flexibility**: working partially by choice; target = passive + fixed ≥ 60–80% of expenses (remaining 20–40% from optional reduced-hours work that the user finds meaningful or location-bound)
     - **Income downshift**: working in a lower-income values-aligned role; target = passive + fixed ≥ 40–60% of expenses (remaining 40–60% from the downshift role)
     - **Coast FI**: invested enough that compounding alone reaches FI by traditional retirement age; target = `existing_invested × (1 + expected_real_return)^(years_to_target_age) ≥ FI_threshold` with zero further contributions
   - **`desired_action_age`** (optional integer) — the age at which the user wants to stop being *required* to earn. Distinct from the computed FI crossover age. Used for behavior planning (bridge-capital projections start from this age, not from today) and for the optional "you have N years of optional work between desired-action-age and FI-crossover-age" framing.

   **If the file is missing**, write a setup template to `~/finances/profile/retirement-frame.md.template` and exit with a clear "edit the template and re-run" message — don't silently default.

5. **Runtime freshness check**: pulls current 10-year Treasury yield (for safe-withdrawal-rate sensitivity), current S&P historical real return (for portfolio growth assumption), current inflation rate. **Does NOT hard-code these.** When WebFetch is unavailable, prompts user for current values.

6. **Computes the crossover analysis** (computed outputs, not user inputs):
   - **FI crossover age**: the age at which fixed retirement income alone (pension + government retirement + any annuities) covers cost-of-living. May be in the past — meaning the user is already FI.
   - **Already-FI check**: is the user currently past the FI crossover threshold? If yes, the headline answer is *"You are already FI."* Don't bury this in sensitivity tables.
   - **Year-of-stop**: when does monthly portfolio drainage stop? (active income + first activated future income ≥ expenses)
   - **Year-of-break-even**: when does monthly net hit zero or positive on cashflow basis?
   - **Bridge years (computed, not user-set)**: from `desired_action_age` (or today, if not specified) to the FI crossover age. May be zero years if already FI.
   - **Bridge gap**: cumulative drawdown across the bridge years, in nominal and real dollars. May be negative (surplus) if already FI.
   - **Available bridge capital** (net of accessibility + tax — see subsections below): the realistic dollars the bridge can spend per year of bridge.
   - **Bridge ratio**: available bridge capital / required bridge gap. >1.0 = bridge math works. <1.0 = short by some amount. N/A if already FI.

   #### Bridge-capital accessibility (locale-aware)

   "Available bridge capital" is NOT just `sum(account balances)`. Each account has different access rules during the bridge years, and the rules depend on the user's age at each year of the bridge and on locale (country-specific retirement-account regulations).

   Per-account access tiers — the skill assigns each holdings.md account a tier based on `type` and the user's age at the bridge year being projected:

   - **Tier 1 — fully accessible**: taxable brokerage, savings, CDs (at maturity), checking, money markets. No age gate, no penalty. Counts at face value (minus tax — see below).
   - **Tier 2 — accessible with rule**: Roth IRA contributions (US — 5-year rule on conversions; contributions themselves always accessible); Rule of 55 for 401(k) distributions from the employer the user separated from at age 55+ (US); 72(t) substantially-equal-periodic-payments from any IRA (US). UK / CA / other locales: per locale's rules referenced in `references/tax/<COUNTRY>.md`.
   - **Tier 3 — penalty unless age-gated**: Trad IRA, 401(k), TSP, 403(b) before age 59½ (US — 10% penalty + ordinary income tax). UK: pensions before age 55 (rising to 57 in 2028). CA: RRSP at any age but full taxation. Per-locale specifics in country tax reference.
   - **Tier 4 — fully restricted**: HSA non-medical before 65 (US — 20% penalty + tax). LISA non-house non-60 (UK — 25% penalty). Annuities pre-activation. Tier 4 contributes ZERO to bridge capital regardless of balance.

   The skill computes bridge capital per year of the bridge — accounts can shift tiers as the user ages (Tier 3 Trad IRA becomes Tier 1 at 59½). For each year, sum the tier-1 + tier-2 balances available that year (with tier-2 rules applied), then apply tax-on-withdrawal (next subsection).

   #### Tax on bridge withdrawal (locale-aware)

   Each account type withdraws differently for tax purposes — without this, bridge capital is overstated by 20–30%. Per-account tax treatment (US baseline; per-locale in `references/tax/<COUNTRY>.md`):

   - **Taxable brokerage**: LTCG rates (0% / 15% / 20% per income bracket — most bridge years land in the 15% bracket; first-year-of-bridge users with low ordinary income may land in 0%). Cost basis matters — only the gain is taxed. If holdings.md captures `cost_basis` per holding (via the optional `holdings:` list populated by `/fi:redirect`), the skill computes gain-to-basis ratio and applies rate to the gain portion. If no cost basis available, default to taxing the full withdrawal at LTCG (conservative).
   - **Trad IRA / 401(k) / TSP / 403(b)**: ordinary marginal income tax (US — bracket per year's projected income). State tax if applicable.
   - **Roth IRA contributions**: zero tax.
   - **Roth IRA earnings**: zero tax if qualified (5-year rule + age 59½); otherwise ordinary income + 10% penalty.
   - **HSA**: zero tax if medical; ordinary income + 20% penalty if non-medical and under 65; ordinary income only if non-medical and 65+.
   - **Cash / checking / savings / CDs**: zero withdrawal tax (interest already taxed annually).
   - **Foreign accounts**: per locale's tax treaty rules — note if the user has any flagged.

   Compute `net_available = gross_balance × (1 - effective_tax_rate)` per account per year. Sum across accessible accounts for each bridge year. The bridge-ratio math then uses NET capital, not gross.

   **Caveat to surface in the report**: tax rates change. The skill uses current-year rates and notes them in the assumption log. Long bridges (10+ years) should sensitivity-test against ±5pp tax-rate shifts.

7. **Sensitivity table** — vary the load-bearing assumptions, show how the answer shifts:
   - Real return on portfolio: ±1% from baseline (typically 5% real)
   - Spending baseline: ±10%
   - High-3 / pension multiplier: per the confidence noted on the stream's `source` field in `holdings.md`'s income-streams section
   - Government retirement timing: early / full / late (locale-aware — US SSA at 62/67/70, UK State Pension at State Pension Age with 1% deferral bonus per 9 weeks, Canada CPP at 60-70 with adjustments per month, etc.)
   - Trust-fund haircut: locale-aware; for US, model SSA 2034 -19% scenario per current law; for UK, model State Pension means-testing scenarios; etc.
   - Mortgage payoff timing: as-amortized vs accelerated curtailments
   - Active income through bridge: zero / current-rate / declining 5%/yr / etc.

8. **Computes mode-aware crossover %** based on retirement frame:
   - Full stop: passive + fixed income ≥ 100% of expenses?
   - Location-time flex: 60-80%?
   - Income downshift: 40-60%?
   - Coast FI: existing invested × expected real return → reach target by year N?

9. **Writes the load-bearing headline** to `~/finances/profile/crossover-headline.md`. One line plus optional caveat acknowledgment, computed from the crossover analysis. The headline should be honest and direct about which case applies — AND must acknowledge material caveats inline (see "State the already-FI case clearly with caveats" below). Format examples (placeholders, not user data):

   **Already-FI case with caveats acknowledged:**
   - *"You are already FI under your chosen frame, assuming current conditions hold. Known caveats: <government-retirement trust fund risk, e.g., US SSA -19% from 2034>, <pension high-3 pending verification>, <other material risks>."*
   - *"FI threshold already passed at scheduled-law assumptions. Under combined haircut scenarios, margin reduced but still positive."*

   **Already-FI case with no material caveats:**
   - *"You are already FI under your chosen frame. All caveats immaterial (none shift the answer by >5%). Maintain trajectory."*

   **Future-crossover case (state the age + range + caveats):**
   - *"FI crossover at age <est> under baseline assumptions; sensitivity shows <range> across the assumption space. Bridge from today to crossover: <N> years. Caveats: <list>."*

   **Trajectory-deficit case (state what's needed):**
   - *"Current trajectory does not cross FI threshold within sensitivity range. Gap: <specifics>. Closing the gap requires <active income / spending reduction / additional savings>."*

   **Coast FI case:**
   - *"Coast FI test passes: existing $<X> invested compounds to FI threshold by <target-year> with no further contributions, assuming <real-return assumption>."*

   The skill should NEVER write a stale or demoralizing version when the already-FI case applies. State the win directly. AND never write an unqualified already-FI headline when material caveats exist — surface them in the same line.

10. **Writes the full report** to `~/finances/crossover-YYYY-MM-DD.md`. Sensitivity table, scenario breakdowns, assumption log, year-by-year bridge cashflow projection.

---

## Output formats

### `~/finances/profile/crossover-headline.md`

```
---
last-computed: YYYY-MM-DD
computed-against: holdings.md (YYYY-MM-DD) [accounts + income-streams + liabilities-for-expense-reductions], _trend-totals.csv (YYYY-MM), retirement-frame.md (YYYY-MM-DD)
frame: <retirement-frame>
position: already-fi | future-crossover | trajectory-deficit | coast-fi-passing | coast-fi-failing
material-caveats-count: <integer>
---

# Headline
<one-line load-bearing answer with material caveats acknowledged inline>

# Material caveats (full detail)
- **<caveat-name>**: <description and how it shifts the answer; magnitude in % or $ terms>
- **<caveat-name>**: ...

# Immaterial caveats (logged but not in headline)
- ...
```

Read by `/fi:fu-money-readout` for the headline echo. Readout echoes the headline line; full-caveat detail available via `/fi:crossover` re-run or by reading the file directly.

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

## Bridge analysis (rows depend on user's declared streams + reductions)

| Phase | Age range | Active income | Fixed income | Burn | Net |
|---|---|---|---|---|---|
| Today through first event | age <today> to age <X> | $<active> | $0 | $<expense> | <net> |
| <Each future-expense-reduction event, e.g. mortgage payoff> | age <X> | $<active> | $0 | $<expense> minus reduction | <net> |
| <Each future-income activation, e.g. pension reduced> | age <Y> | $<active> | $<stream-amt> | $<adjusted-expense> | <net> |
| <Subsequent stream activations> | age <Z> | $<active> | $<combined-streams> | ... | ... |
| Post-crossover (fixed income covers expenses) | age <FI-crossover>+ | $0 (assumed) | $<combined-streams> | $<expense> | breakeven or surplus |

The actual rows render dynamically per the user's profile — users without a mortgage, or without an employer pension, or without government retirement, will see different phases. The skill names whatever events apply.

## Sensitivity table

| Variable | Baseline | -1σ | +1σ | Effect on FI crossover age |
|---|---|---|---|---|
| Real portfolio return | <baseline %> | <-1%> | <+1%> | <crossover age shifts: ±N years> |
| Spending baseline | $<baseline>/mo | -10% | +10% | <crossover age shifts: ±N years> |
| Pension/annuity multiplier | <baseline> | low estimate | high estimate | <effect> |
| Government retirement timing | full age | early-reduced | delayed | <effect> |
| Trust-fund-haircut scenario (locale-aware) | scheduled benefits | per current law (e.g., US SSA -19% from 2034; UK State Pension means-testing; etc.) | scheduled | <effect> |

## Assumption log
- ...

## Year-by-year bridge cashflow projection
(table)
```

---

## Real-return assumption methodology

The skill's projections require a real-return assumption (nominal portfolio
return minus inflation). Standard practice picks a single number; this skill
treats it as a sensitivity input.

**Default baseline**: **5.0% real annualized** for a 70/30 stock/bond
portfolio. Source: long-run historical US data (Shiller, Bogleheads
real-return tables) for a diversified portfolio over rolling 30-year windows
post-WWII. This is the conservative end of the common 5–7% range — the skill
defaults toward conservative because a too-rosy assumption produces
"you're FI" false positives.

**Adjusted for portfolio mix**: if `/fi:redirect` has populated the
asset-class roll-up in holdings.md, scale the default toward portfolio
composition:

| Portfolio mix | Default real-return assumption |
|---|---|
| 100% equity | 6.0% |
| 80/20 stock/bond | 5.5% |
| 70/30 stock/bond | 5.0% |
| 60/40 stock/bond | 4.5% |
| 50/50 stock/bond | 4.0% |
| 40/60 stock/bond | 3.5% |
| Conservative (heavy bond + cash) | 2.5–3.0% |

**Live-rate refinement**: when WebFetch is available, the skill pulls the
current 10-year Treasury yield as a sanity check. If the 10-yr is unusually
low (<2%) or unusually high (>6%), surface a one-line note in the report
suggesting the user manually consider whether the historical real-return
default still applies — don't auto-adjust, just flag.

**User override**: the user can set `real_return_override` in
`retirement-frame.md` if they prefer their own assumption. The override is
honored but the baseline + sensitivity-range is still shown for comparison.

**Sensitivity range**: the sensitivity table always shows baseline ±1pp
(typically 4% / 5% / 6%). This isn't precision — it's acknowledging that any
single point estimate is wrong. The shape of FI matters more than the point.

## Mode-aware crossover math (per frame)

Each retirement frame has different success criteria. The headline
calls the position relative to the frame's threshold, not a universal 100%.

**Full stop:**
- Crossover when `passive_income + fixed_income ≥ 100% × expenses`
- "Passive income" = sustainable portfolio withdrawal at the chosen real-return
  assumption (defaults to 4% safe-withdrawal rate per Trinity/Bengen unless
  the user overrides — but show the underlying real-return math, not a magic
  number).
- Bridge math applies until fixed income alone hits the threshold; after that,
  portfolio is restorative (may grow during retirement).

**Location-time flexibility:**
- Crossover when `passive_income + fixed_income ≥ 60–80% × expenses`
- The skill reports against **both ends** of the 60–80% band:
  - "70% threshold passed at age X" — the comfortable median
  - "80% threshold passed at age Y" — the conservative upper end
- The 20–40% gap is explicitly tagged as "this frame expects reduced-hours
  work to fund this portion" — surface the implied hours-per-week at the
  user's hourly wage (read from `/fi:hourly-wage` output if available).

**Income downshift:**
- Crossover when `passive_income + fixed_income ≥ 40–60% × expenses`
- Reports against both 50% (median) and 60% (conservative).
- 40–60% gap tagged as "downshift role expected to fund this portion."
- If a downshift income target is declared in `retirement-frame.md`
  (`downshift_income_target: <amount>/mo`), use that explicit figure instead
  of the implied gap.

**Coast FI:**
- Test: `existing_invested × (1 + real_return)^(target_age - current_age) ≥ FI_threshold`
- Where `FI_threshold` = `expenses × 25` (the inverse-4%-rule shorthand) OR
  the user's explicit override.
- Coast FI is binary at the moment of test (passing or failing) — but the
  sensitivity table shows the margin: how much slower can real return be
  while coast still passes? At what real-return assumption does coast fail?
- For coast-FI passing users, the headline names the year coast achieves
  threshold and notes "zero further contributions required for FI; any
  earnings now are optional."

## Inflation handling

The skill projects in **nominal dollars by default** but renders both nominal
and real numbers in the report so the user can see purchasing-power impact.

- **Expense baseline**: grows at expected inflation per year of projection
  (default 2.5%/yr; user override in `retirement-frame.md`). Without this,
  long bridges (10–20 years) understate the gap by 25–50%.
- **Income streams**: grow per stream's `cola_adjusted` flag (from
  holdings.md `## Income streams` section). COLA-adjusted streams (most
  US/UK government retirement income, most defined-benefit pensions) grow with
  CPI. Non-COLA streams (most private annuities, US FERS supplement, fixed
  payouts) stay nominal — meaning their real value erodes.
- **Portfolio returns**: stated as real (already net of inflation by
  definition of the real-return assumption above). Don't double-count
  inflation on the return side.
- **Caveat to surface**: inflation assumption is itself a sensitivity. The
  table shows ±1pp on the inflation assumption — a 2.5% baseline vs 3.5% can
  shift a 15-year bridge gap by 15–20%.

## Architectural features

- **Compute the crossover, don't ask the user to set it.** The skill INVERTS the standard FI question. Standard FI guides ask: *"When do you want to retire? Will you make it?"* — this skill asks no such thing. Instead it computes: *"Based on your current numbers, here is your FI crossover age."* The user does not pick a target year; the skill names their position. This produces honest answers, especially the *"you are already FI"* case which standard target-driven framings tend to bury.

- **Bridge years are derived, not specified.** "Bridge years" = the period between today (or the user's optional desired-action age) and the computed FI crossover age. Bridge years may be zero (already FI), positive (years of active income still needed), or negative-relevance (the user already crossed and may not have realized).

- **State the already-FI case clearly when it's true — with material caveats acknowledged inline.** Many users with employer pension + government retirement + paid-down mortgage + reasonable savings cross the FI threshold earlier than they think. The skill must surface this directly. BUT the headline must also acknowledge known caveats that could materially shift the answer:
  - Government retirement trust-fund solvency (e.g., US SSA -19% from 2034 per current law if Congress doesn't act)
  - Pension-fund solvency for any user-declared employer pension
  - Inflation creep on expense baseline outpacing COLA on income streams
  - Sequence-of-returns risk during bridge years
  - High-3 / pension multiplier still pending verification (e.g., user hasn't confirmed actual benefit estimate yet)

  **Format**: state the position, then the qualifier. Examples:
  - *"You are already FI under your chosen frame, **assuming current conditions hold**. Known caveats: SSA trust fund 2034 (-19% haircut still leaves you FI but with reduced margin); pension high-3 still pending verification."*
  - *"You are already FI under your chosen frame **at scheduled-law assumptions**. Under SSA-2034-haircut scenario: still FI, margin tighter. Under combined haircut + spending +10%: borderline."*

  When all caveats are immaterial (each shifts the answer by less than ~5%), the headline can be unqualified. When any caveat shifts the position-status (already-FI → not-FI, or not-FI → already-FI), it MUST be in the headline. When caveats reduce margin without shifting status, acknowledge in the headline ("with reduced margin under <scenario>") rather than burying.

  The principle: the user should not be surprised by a caveat later that they could have known about now. The headline carries the load.

- **Bridge math, not perpetual-portfolio math.** When future fixed-income streams exceed cost-of-living at activation, the portfolio's job is to bridge — not support spending forever. This is often the more honest frame than the textbook "4% rule" perpetual-portfolio model. The skill defaults to bridge-math framing if `holdings.md`'s income-streams section declares any stream ≥ 50% of expense baseline.

- **Headline written here, echoed in fu-money-readout.** Decouples slow sensitivity math (run periodically) from fast daily orientation (echoed every readout). The headline file is the contract between skills.

- **Two-scenario for streams with reduced/full eligibility ages.** Same pattern as fu-money-readout — for any stream that offers both an early-reduced option (e.g., taking benefits at reduced amount before full eligibility age) and a waited-full option (e.g., waiting for unreduced amount), run the analysis under both. Surface the time-arbitrage decision honestly. Common in employer pensions (US FERS, UK final-salary schemes, etc.), government retirement income (US SSA early at 62 / FRA at 67 / max at 70), and some annuities. Counterintuitively, early-reduced often produces better bridge math in nuclear scenarios.

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
- If `holdings.md` is missing or stale (or its `## Income streams (non-labor)` section is missing for users with non-account income): writes an error note to the report file with a clear next step (pointer to `/fi:holdings-scaffold`), exits cleanly without overwriting the previous headline (don't write a stale headline).
- If `retirement-frame.md` is missing: writes a one-time setup template to `~/finances/profile/retirement-frame.md.template` showing the four frame options (full-stop / location-time-flex / income-downshift / coast-fi) and notes in the error message that the user can copy and edit to enable the run. Don't hard-fail forever — make the setup step obvious.
- If `_trend-totals.csv` is missing: cannot run in headless mode (no human present to provide the manual fallback). Exits with a clear error pointing at `/fi:track-flow` and noting that interactive runs support a manual-baseline override.

---

## Privacy posture

This SKILL.md describes the procedure in general terms. User-specific data (account names, dollar amounts, pension figures, vendor patterns) is never embedded in the public skill files. All user data writes go to gitignored paths on the user's machine — `~/finances/profile/`, `~/finances/crossover-*.md`.

User-specific test artifacts and design logs live on the user's machine in their gitignored finance directory. They do not get published.

---

## Validation

Bridge-math framing emerged paired with `/fi:fu-money-readout` validation 2026-05-03. Findings encoded back into both SKILL.mds as design rules. The validation case: a user with both an employer-deferred pension and government retirement income where the perpetual-portfolio frame produced a misleading future-target FI age when the bridge frame more honestly captured that fixed income at retirement age exceeds cost-of-living, making the portfolio's job temporally bounded rather than perpetual. The validation also surfaced the deeper insight: target-driven framings ("when do you want to retire?") buried the fact that the user was already past the FI crossover threshold; computing the crossover as an output and naming the bridge backwards from it reveals "already-FI" cases that target-driven framings miss.

---

## TODO

- [x] Real-return assumption methodology — defined in "Real-return assumption methodology" section above (default 5% real for 70/30, portfolio-mix-aware scale, live-rate sanity check, user override).
- [x] Mode-aware variants of the crossover math (4 frames) — defined in "Mode-aware crossover math (per frame)" section above.
- [ ] Sensitivity-table format that's actually useful, not overwhelming
- [ ] Cross-reference with `/fi:redirect` for portfolio-mix assumptions (partial — real-return scale uses redirect's asset-class roll-up when available)
- [x] **Government-retirement-projection prompt UX** — pulled from official statement (US: ssa.gov; UK: gov.uk State Pension forecast; CA: My Service Canada Account; etc.). Locale-aware prompt copy.
- [ ] **Government earnings-record audit reminder** — when the user pulls their statement for the first time, surface a one-liner: *"While you have this open: scan year-by-year for missing or wrong earnings. If any look off, file the locale-appropriate correction form. One-time task, but missed earnings cost real benefit dollars later."* Don't make this a sub-skill; just a side note.
- [ ] Trust-fund-haircut scenario library by country (US 2034 SSA; UK State Pension means-testing; etc.) — keep updated as legislation changes.
- [ ] Year-by-year bridge cashflow projection format — visualization vs table.
- [ ] Worked examples in `examples/` for each retirement frame.
- [ ] Headline-file schema versioning — if format changes, fu-money-readout needs to handle gracefully.
- [ ] Per-country tax/accessibility references (`references/tax/<COUNTRY>.md`) for the bridge-capital accessibility tiers and tax-on-withdrawal logic. US baseline written inline; UK / CA / EU / AU still need authoring.
- [ ] Sequence-of-returns risk modeling — mean-return sensitivity is shown but order-of-returns variation (which can be 2–3× more impactful for portfolios in drawdown) is not. Future addition.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 8 (capital and the crossover point). The 1992 framing assumed a single perpetual-portfolio threshold; the 2026 reframing as bridge-math acknowledges that most users have non-portfolio future income streams that change the shape of the answer.
- **Mr. Money Mustache** (online, 2012). The 4% rule popularized for FI; folded in as one of several real-return assumptions for sensitivity testing, not as the load-bearing answer.
- **Marika Olson** (2026). Design refinements: **compute-the-crossover-don't-ask-the-user-to-set-it** (invert the standard "when do you want to retire?" target-driven framing — the skill computes the user's FI crossover age as an OUTPUT and names the bridge years backwards from that; many users find they are already FI and standard framings bury this); **state-the-already-FI-case-clearly-with-caveats-acknowledged** (first-class output, not special case; never an unqualified already-FI headline when material caveats exist — surface them inline so the user is not surprised by a foreseeable risk later); **bridge-years-derived-not-specified** (period between today/desired-action-age and computed FI crossover age); **desired-action age vs FI crossover age** (separate concepts — FI crossover is the math, desired-action age is the behavior plan); bridge math vs perpetual-portfolio math (acknowledges that FERS/SSA-equivalent streams change the shape of FI from "support spending forever" to "bridge to retirement age"); load-bearing headline written here and echoed in fu-money-readout (decouples slow sensitivity math from fast daily orientation); **holdings.md as single source of truth for income streams + liabilities** (income streams live in holdings.md's `## Income streams (non-labor)` section per holdings-scaffold Step 4d; future expense reductions are derived from holdings.md liabilities via amortization — neither lives in a separate profile file, avoiding contract drift); two-scenario sensitivity for streams with early-reduced and waited-full options; trust-fund-haircut sensitivity for government retirement; active-income forward-projection (don't trust UI-inflated medians for bridge math); compute-payoff-from-current-payment rule (lender-stated maturity unreliable when user paid above minimum scheduled P&I); mode-aware target thresholds (frame-specific success criteria, not universal 100%).
