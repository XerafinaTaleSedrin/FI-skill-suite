---
name: wallchart
description: Plots monthly income vs. spending vs. investment income across all logged months. YMOYL Step 5 — make life energy visible. Reads /fi:track-flow trend CSVs and /fi:holdings-scaffold's holdings.md, renders three series (income, spending, projected investment income), highlights the crossover threshold. ASCII output for terminal; SVG/PNG planned for printing.
layer: concept+pattern+tool
ymoyl_step: 5
mode_aware: false
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 5 — make life energy visible via long-arc chart. Three lines (income, spending, investment income) plotted over time; crossover where investment income meets spending = FI threshold."
  - author: Marika Olson
    contribution: "2026 design refinements: three-method investment-income computation (actual yield / balance-change derived / forward-projected), default to forward-projection because it's the line that conceptually crosses spending. ASCII-first rendering for universal terminal compatibility, SVG/PNG via matplotlib as printable wall-chart upgrade. Reads track-flow trend CSVs rather than re-aggregating monthly tabs."
last-reviewed: 2026-05-09
---

# /fi:wallchart

Reads all available trend data from `/fi:track-flow` and the holdings snapshot from `/fi:holdings-scaffold`, produces YMOYL's wall chart: three lines plotted over time (monthly income, monthly spending, projected monthly investment income). The crossover where investment income meets spending is the FI threshold — the point where you don't need a paycheck.

The wallchart is meant to be visible — printed, taped to a wall, looked at every day. The skill produces both the data and a renderable chart format (ASCII for terminals; SVG/PNG via matplotlib for printing, planned).

---

## The concept (decades-stable)

Three numbers, plotted side by side over time, are an emotional anchor that no spreadsheet replicates. Watching the curves bend over months and years makes financial behavior real in a way the underlying numbers don't.

YMOYL's prescription: tape the chart to a wall where you'll see it every day. The repeated visual exposure is the substance. The crossover point — where the investment-income line meets the spending line — is the FI threshold made visible.

In 2026 reality, the chart can be rendered (rather than hand-plotted), and the underlying data updates automatically as `/fi:track-flow` runs each month. But the *function* of the chart is the same: an at-a-glance picture of life energy in vs. life energy out vs. life energy already captured.

---

## The pattern (~5-year stable)

Aggregate trend data from `/fi:track-flow` (monthly income + spending) → derive or project monthly investment income from `/fi:holdings-scaffold` → render a chart with three series → write to a sentinel file the user can re-render or update over time.

The skill is **idempotent**: re-running with new data refreshes the chart in place. The sentinel file at `~/finances/wallchart.md` is always the latest snapshot; previous renders are not preserved (the trend itself is the history).

---

## What the skill does at runtime

### Step 1 — Source data check

Check for required inputs:

- `~/finances/monthly-tabs/_trend-totals.csv` (from `/fi:track-flow`) — required
- `~/finances/holdings.md` (from `/fi:holdings-scaffold`) — required for investment-income line
- `~/finances/hourly-wage/*.md` (from `/fi:hourly-wage`) — optional, for life-energy-hour annotation on Y-axis labels

If any required input is missing, instruct the user to run the prerequisite skill first and stop. Be specific:

> *"Need `~/finances/monthly-tabs/_trend-totals.csv` from `/fi:track-flow`. Run that first (drops a fresh aggregator export, takes ~5 minutes), then come back."*

### Step 2 — Aggregate the data series

Read `_trend-totals.csv`. Extract per-month:

- **Monthly income** = `personal_active_income` (the recurring cashflow baseline, NOT including windfalls; per `/fi:track-flow`'s source-type schema)
- **Monthly spending** = `-1 × personal_expense` (the refund-netted expense, sign-flipped to positive for plotting)

Filter to `complete: true` rows by default. Show partial months with a dashed line if user requests.

### Step 3 — Compute investment-income series

Three computation methods. Ask the user which to use, with a default recommendation:

> *"How should we compute the investment-income line? Three options:*
>
> *1. **Actual yield from track-flow** (`personal_gross_yield`) — what your portfolio actually produced as dividends/interest each month. Real, but lumpy and often lower than capacity (auto-reinvest dilutes the visible cash yield).*
>
> *2. **Balance-change derived** — month-over-month holdings.md balance change, minus net contributions. Captures market-driven gains AND yield, but volatile because of market moves.*
>
> *3. **Forward-projected (recommended for the wall chart)** — today's portfolio × assumed safe-withdrawal rate (default 4%, configurable). Smooth line. This is the line that conceptually crosses spending — the YMOYL chart wants the answer to "what could this portfolio support sustainably?" not "what did it cough up last month."*
>
> *Default: option 3, with options 1 + 2 plottable as side-bands if you want the volatility visible."*

For option 3, ask:

> *"Safe-withdrawal rate? Default 4% (Bengen / Trinity classic). Modern conservative readers use 3.3-3.5%. Aggressive uses 4.5-5%. Enter a percentage."*

Apply the rate to today's portfolio value (from `holdings.md`):

```
projected_monthly_investment_income = (portfolio_value × annual_swr) / 12
```

For historical months, optionally back-cast: use that month's holdings snapshot (if `holdings.md` has historical entries) or the current value (if not). Default to current value (smooth line — that's the wall-chart point).

### Step 4 — Compute crossover

Identify the point where `projected_monthly_investment_income >= monthly_spending`.

- **Already-crossed**: the projected investment income line is already above the spending line at the most recent month. Surface as a headline:
  > *"Investment-income capacity ($X/mo) is already covering spending ($Y/mo). At a [4]% withdrawal rate, the portfolio supports the current spending baseline indefinitely."*

  Caveat-aware: include the same caveats `/fi:crossover` echoes (pension assumptions, sequence-of-returns risk, healthcare cost trajectory, Social Security or equivalent timing, etc.).

- **Not-yet-crossed**: forward-extrapolate the spending line (as a flat baseline, default) and the investment-income line (growing at the user's recent contribution rate). Ask:
  > *"What's your monthly contribution to investments — recurring 401k / IRA / brokerage adds? I can project when the lines cross at that contribution rate."*

  Show the projected crossover year + the assumptions.

- **Crossing visible in the historical data**: the lines crossed somewhere in the chart's time range. Mark the crossover month with a vertical annotation.

### Step 5 — Render

Two formats. Default: ASCII (universal). Optional: SVG/PNG (matplotlib, planned).

#### ASCII chart

X-axis: months (oldest left, newest right). Y-axis: dollars (auto-scale to fit max value × 1.1).

Three series with distinct markers:
- Income: `█` (solid block)
- Spending: `▒` (medium shade)
- Investment income (projected): `─` (horizontal line — the smooth one)

Example layout (small):

```
 $8000┤
      │   ███████████████
 $6000┤████              ██████
      │
 $4000┤▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
      │───────────────────────── ← projected investment income (4% SWR on current portfolio)
 $2000┤
      │
    $0└────┬────┬────┬────┬────┬
         Jan  Feb  Mar  Apr  May
                                 2026

  Income    █  Spending   ▒  Investment-income capacity   ─
```

For longer time ranges (12+ months), narrow the columns. For very long ranges (24+), use compressed-month markers (every 3rd month labeled).

Crossover annotation: when the projected investment income line is above the spending line, annotate at the crossing point: `★ FI threshold — investment income capacity ≥ spending starting [month]`.

#### SVG / PNG (planned)

Pseudocode using matplotlib:

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(months, income, label="Income", color="#2a9d8f", linewidth=2)
ax.plot(months, spending, label="Spending", color="#e76f51", linewidth=2)
ax.plot(months, investment_income_projected, label="Inv. income capacity (4% SWR)",
        color="#264653", linewidth=2, linestyle="--")
ax.fill_between(months, 0, investment_income_actual, alpha=0.2, color="#264653",
                label="Inv. income actual (yield)")
ax.axhline(y=crossover_value, color="gold", linestyle=":", label="FI threshold")
ax.set_ylabel("Monthly $")
ax.set_xlabel("Month")
ax.legend()
plt.savefig("~/finances/wallchart.png", dpi=300)
```

PNG output is dpi=300 so it prints cleanly at 8×11 or larger. Color choices favor printability (no near-white on white).

### Step 6 — Write outputs

Two artifacts:

```
~/finances/wallchart.md       # Data + ASCII chart + caveats
~/finances/wallchart.png      # Renderable image (when matplotlib path is implemented)
```

#### `wallchart.md` schema:

```markdown
---
generated: YYYY-MM-DD
data-source: monthly-tabs/_trend-totals.csv
months-included: YYYY-MM to YYYY-MM
swr-assumption: 4%
investment-income-method: projected | actual | balance-change-derived
crossover-status: already-crossed | crossing-visible | not-yet-crossed
generated-by: /fi:wallchart
---

# Wall chart — generated YYYY-MM-DD

## At a glance
- Income trailing 6mo: $X/mo (median) / $X/mo (mean)
- Spending trailing 6mo: $Y/mo (median) / $Y/mo (mean)
- Investment-income capacity (4% SWR on current portfolio of $P): $Z/mo
- Crossover status: [already-crossed | not-yet-crossed at projected year YYYY | visible in historical data at YYYY-MM]

## Chart

[ASCII chart per Step 5]

## Per-month data

| Month | Income | Spending | Inv. income (projected) | Notes |
|---|---|---|---|---|
| 2026-01 | $X | $Y | $Z | |
| 2026-02 | ... | ... | ... | |
| ... | | | | |

## Caveats

- **Investment-income line is projected, not actual.** At a [4]% SWR, today's portfolio of $P would support $Z/mo. Actual cash-yield is lower (auto-reinvested); this is capacity, not realized.
- **No sequence-of-returns adjustment.** A 4% SWR assumes a "normal" market trajectory; early-retirement years that hit a bear market reduce the safe rate. For finer-grained scenario work, see `/fi:crossover`.
- **No pension or Social Security overlay.** If you have future income streams (FERS, SSA, etc.), they reduce the spending you need the portfolio to cover. `/fi:crossover` does the bridge math.
- **Spending line is current state.** Lifestyle inflation, healthcare cost trajectory, and time-bucketed spending (Bill Perkins) are not modeled — the chart treats current spending as flat-forward.
- **No tax adjustment.** SWR of 4% is gross; real spendable income depends on the tax mix of your accounts.

## Re-rendering

Re-run `/fi:wallchart` after `/fi:track-flow` adds new monthly data. Chart updates in place; history is the trend itself, not preserved renders.
```

### Step 7 — Closing

Show:

> *"Wall chart at ~/finances/wallchart.md. Print it, tape it to a wall.*
>
> *Status: [already-crossed | crossing-visible-at-YYYY-MM | not-yet-crossed-projected-YYYY]. [One-line headline.]*
>
> *Refresh me whenever `/fi:track-flow` finishes a fresh month. The trend is the chart's whole point — let the curves bend.*
>
> *For the bridge-math underneath the projection (when does FERS / SSA kick in, what's the depletion timeline if you stop working today), see `/fi:crossover`."*

---

## Output schema

### `~/finances/wallchart.md`

(Per Step 6. Frontmatter declares generation date, data source, SWR assumption, crossover status. Body has the at-a-glance summary, ASCII chart, per-month data table, and caveats.)

### `~/finances/wallchart.png` (planned)

Generated via matplotlib when the Python optimization is built. Until then, ASCII-only.

---

## Headless behavior

Fully supported. Cron-friendly:

- Pulls from already-existing CSV + holdings.md (no interactive prompts needed if user has previously declared SWR + investment-income method)
- SWR + method declarations persist in `~/finances/profile/wallchart-config.md` after first run
- Re-renders the wallchart at whatever cadence the cron fires (typically end-of-month after `/fi:track-flow` finalizes)

For first runs, interactive setup is required to capture SWR + method preference.

---

## Why this matters

The wall chart is YMOYL's most physical artifact. Vicki Robin and Joe Dominguez insisted on a printed chart taped to a wall — visible daily, no opening-an-app required. The argument: financial behavior is shaped by what you see, repeatedly, without effort. A chart on a wall does work that a chart in an app cannot.

The skill respects that — the ASCII chart prints cleanly to a small piece of paper, and the planned PNG output is sized for an 8×11 print. The point is that the chart leaves the screen.

The crossover moment — where the investment-income line meets the spending line — is the FI moment made visible. Most people who reach FI describe the moment they noticed the lines crossing as more emotionally significant than the moment they hit a particular dollar amount. The chart is what makes that moment visible.

For users early in the journey (lines far apart, crossing projected years away): the value isn't the crossover, it's watching spending start to bend down or income start to bend up. Trend matters more than absolute level.

For users near or at crossover: the value is the daily exposure to the fact that they don't have to keep working at the same intensity. The chart makes the option visible.

---

## TODO

- [ ] Matplotlib SVG/PNG renderer (the planned upgrade)
- [ ] Historical-portfolio back-cast for option 3 — if `holdings.md` has historical balance entries, use them per-month rather than current value (more accurate but volatile)
- [ ] Annotation layer: mark major life events (RIF, severance start/end, side-hustle launch, etc.) on the chart so the bends have context
- [ ] Multi-currency rendering — if user is multi-currency, decide whether to plot base-currency only or include side panels per currency
- [ ] Mobile/phone-friendly rendering — ASCII looks bad on narrow terminals; responsive sizing
- [ ] Print-optimized layout: title block + chart + key + per-month data table on one printable page
- [ ] Side-by-side comparison: this year's chart vs prior year's chart, scaled equivalently
- [ ] Optional fourth series: net worth (from `holdings.md` historical snapshots) — useful but can clutter; toggle-on
- [ ] Caveat refresher: when caveats apply specifically (e.g., user has FERS — surface FERS-specific caveats in the file)

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 5 — make life energy visible via long-arc wall chart. The three-line composition (income / spending / investment income) is the original prescription. The "tape it to a wall" framing is theirs and load-bearing.
- **Bill Bengen** (1994) and the **Trinity Study** (Cooley, Hubbard & Walz, 1998). The 4% safe withdrawal rate baseline used as default for projected-investment-income method. Modern conservative readers (e.g., ERN's Big ERN) argue for 3.3-3.5% on long horizons; aggressive readers argue 4.5-5% for shorter horizons. Skill makes the rate configurable.
- **Marika Olson** (2026). Three-method investment-income computation (actual / balance-change-derived / forward-projected), ASCII-first rendering, default to forward-projection because that's the line that conceptually crosses spending in the YMOYL framing, integration with `/fi:track-flow`'s `_trend-totals.csv` rather than re-aggregating from monthly tabs.
