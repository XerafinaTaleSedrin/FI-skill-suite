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
last-reviewed: 2026-07-14
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

The skill is **idempotent**: re-running with new data refreshes the chart in place. The sentinel file at `<finances_root>/wallchart.md` is always the latest snapshot; previous renders are not preserved (the trend itself is the history).

---

## What the skill does at runtime

### Step 1 — Source data check

Resolve `<finances_root>` per the four-step convention in AGENTS.md (FI_ROOT env var → `.fi-root` walk-up → `~/.fi/config.toml` → `~/finances/` default). Then check for required inputs:

- `<finances_root>/monthly-tabs/_trend-totals.csv` (from `/fi:track-flow`) — required
- `<finances_root>/holdings.md` (from `/fi:holdings-scaffold`) — required for the FI threshold reference line
- `<finances_root>/hourly-wage/*.md` (from `/fi:hourly-wage`) — optional, for life-energy-hour annotation on Y-axis labels

If `<finances_root>` itself can't be resolved, fail loudly per the AGENTS.md path-resolution spec. If a required input is missing inside a resolved finances root, instruct the user to run the prerequisite skill first and stop. Be specific:

> *"Need `<finances_root>/monthly-tabs/_trend-totals.csv` from `/fi:track-flow`. Run that first (drops a fresh aggregator export, takes ~5 minutes), then come back."*

### Step 2 — Aggregate the data series

Read `_trend-totals.csv`. **Include ALL months by default** (both `complete: true` and `complete: false`). Render solid line for complete months, dashed line for partial months (`complete: false`). **Never silently filter to complete-only** — the current month is the one the user most wants to see, and it will always be partial.

Extract per-month, per stream:

**Income streams** (all of these, each as its own line, summed into a combined total):
- `personal_active_income` — current-labor income only (wage + family-support + side-hustle + investment-cash + income-other, per track-flow Step 7). **Not pensions or UI** — track-flow classifies those `government-benefit` and excludes them from this column; they appear in the monthly tab only, so a user living mainly on benefit income will chart near-zero here. Say so rather than letting the low line read as an error.
- `business_net` — net consulting / LLC / side-hustle revenue. Read the CSV's `business_net` column directly (it equals `business_income + business_expense` by track-flow's own invariant — don't recompute from the gross columns and risk disagreeing with it)
- `personal_gross_yield` — actual investment yield (cash dividends/interest that hit the account this month). This goes IN income, not as a separate "method" — see Step 3.
- Any additional income column the user has declared in `<finances_root>/profile/wallchart-config.md` (rental, royalties, etc.)

**Default rule**: include ALL income streams. User opts OUT of streams they don't want on the chart via wallchart-config.md, not in. Silent exclusion produces a chart that lies about life-energy-in.

**Spending** = `-1 × personal_expense` (the refund-netted expense, sign-flipped to positive for plotting).

**Outlier detection** (mandatory): scan the income data for monthly values > 5× the trailing-12-month median (when fewer than 12 months exist — most first-year users — use the median of all available months), OR > 3 standard deviations from the trailing mean. Compute the median / mean / SD **excluding the candidate month itself**: a large outlier left in its own baseline inflates the SD enough to mask itself from the 3-SD test (the 5× median test is the robust one; the SD test only works on outlier-excluded stats). When detected, surface to the user:

> *"I detected an outlier: [month] income of [$X] is [N]× the trailing median ([$Y]). This looks like a windfall (severance, sale, inheritance, etc.) miscategorized as recurring income. How should I handle it?*
>
> *1. Render raw — chart auto-scale will be dominated by the outlier, but the truth is preserved*
> *2. Annotate + use trailing-median for the trend line — outlier shown as a labeled callout, trend line not yanked upward*
> *3. Move to a separate "windfall" marker — render as a single point above the chart, distinct from the recurring income trend*
> *4. Push back to source — this should be re-categorized in /fi:track-flow as `personal_windfall` not `personal_active_income`. I'll emit a hint for that fix."*

Persist the user's decision per-outlier-month to `<finances_root>/profile/wallchart-config.md` so re-runs don't re-prompt.

### Step 3 — Compute the FI threshold reference line

**Conceptual clarification** (load-bearing — read this before you write the prompt):

The wall chart plots two conceptually different kinds of lines simultaneously:
- **Flow lines** — income streams (incl. actual investment yield) and spending. These are monthly cash events.
- **Reference line** — projected investment-income CAPACITY (portfolio × SWR / 12). This is NOT a monthly cash event; it's a portfolio-derived "what could this portfolio support sustainably?" question.

The FI crossover moment is when the **reference line crosses the spending line**. That's a portfolio-size milestone made visible, not a flow event.

Earlier versions of this skill framed Step 3 as a "pick a method" choice between actual yield, balance-change, and forward-projected. That framing was wrong — they're not alternatives, they answer different questions:
- Actual yield is **part of income** (folds into the income total — handled in Step 2 above).
- Forward-projected capacity is **the FI threshold reference** (handled here in Step 3).
- Balance-change is a net-worth-delta line that doesn't belong on the default wall chart (offer as a separate panel toggle for users who want it).

**What this step actually does**: ask the user to confirm the safe-withdrawal rate, compute the reference line, and persist the preference.

**Prompt copy**:

> *"To draw the FI threshold reference line, I need a safe-withdrawal rate. The historical SWR convention used by the FI community is 4% (Bengen 1994 / Trinity Study 1998). YMMV — please pick a rate you feel is suitable based on your level of risk acceptance. Modern conservative readers go 3.3-3.5% for long horizons; aggressive 4.5-5% for shorter horizons.*
>
> *At your current portfolio of [$P] from holdings.md, here's what each rate would draw:*
> *- 3.5% → [$P × 0.035 / 12]/mo*
> *- 4.0% → [$P × 0.04 / 12]/mo*
> *- 4.5% → [$P × 0.045 / 12]/mo*
>
> *Want me to explain any of these in more depth, or compare them side-by-side, before you pick? Otherwise — what rate do you want me to use?"*

The skill MUST explicitly invite Q&A before accepting an answer. Do not just collect a number and proceed. Users who are new to FI need conversational space to understand what they're choosing.

Apply the chosen rate to today's portfolio value — the **investment-accounts total** from `holdings.md` (the same total the asset-class roll-up sums to), NOT net worth. Cash accounts, home equity, and other non-investment assets aren't perpetually SWR-drawable; using net worth silently inflates the reference line. (In the prompt above, `[$P]` is this same investment-accounts total.)

```
projected_monthly_investment_income_capacity = (portfolio_value × annual_swr) / 12
```

For historical months, default to current value (smooth horizontal reference — that's the wall-chart point). If `holdings.md` has historical balance entries, optionally back-cast per-month for a sloped reference line (offer as a toggle, not the default).

Persist the user's SWR choice to `<finances_root>/profile/wallchart-config.md`. Subsequent runs use stored preference unless user passes `--re-prompt` or similar.

### Step 4 — Compute crossover

Identify the point where `projected_monthly_investment_income_capacity >= monthly_spending`.

(Note: the comparator is the **capacity reference line** vs. the **spending flow line** — NOT the income-total flow line vs. spending. The wall chart's FI moment is when the portfolio could sustainably cover spending, not when this month's income happened to.)

- **Already-crossed**: the projected investment income line is already above the spending line at the most recent month. Surface as a headline:
  > *"Investment-income capacity ($X/mo) is already covering spending ($Y/mo). At a [4]% withdrawal rate, the portfolio supports the current spending baseline indefinitely."*

  Caveat-aware: include the same caveats `/fi:crossover` echoes (pension assumptions, sequence-of-returns risk, healthcare cost trajectory, Social Security or equivalent timing, etc.).

- **Not-yet-crossed**: forward-extrapolate the spending line (as a flat baseline, default) and the investment-income line (growing at the user's recent contribution rate). Ask:
  > *"What's your monthly contribution to investments — recurring 401k / IRA / brokerage adds? I can project when the lines cross at that contribution rate."*

  Show the projected crossover year + the assumptions.

- **Crossing visible in the historical data**: the lines crossed somewhere in the chart's time range. Mark the crossover month with a vertical annotation.

### Step 4b — Deterministic checks (run before rendering; a chart that fails its own math never ships)

Per AGENTS.md §Deterministic invariants:

- **Total is a sum**: per month, Income TOTAL = Σ(stream columns) exactly — in the per-month data table AND in the chart's plotted series (same numbers, two renderings).
- **Spending traceability**: per month, plotted spending = −1 × `personal_expense` from the source CSV row.
- **Reference-line recompute**: FI threshold = portfolio value (holdings.md) × chosen SWR ÷ 12; the at-a-glance line, the chart annotation, and the frontmatter `swr-assumption` all agree.
- **Axis discipline**: months strictly increasing, no month duplicated or skipped silently (a gap in the data renders as a labeled gap, not a compressed axis).
- **Crossover-status consistency**: the frontmatter `crossover-status` value matches the computed comparison of reference line vs. spending at the latest month.

### Step 5 — Render

Two formats. Default: ASCII (universal). Optional: SVG/PNG (matplotlib, planned).

#### ASCII chart

X-axis: months (oldest left, newest right). Y-axis: dollars (auto-scale to fit max value × 1.1, EXCLUDING outliers flagged in Step 2 — outlier handling determines its own axis treatment).

**Series convention** (visual distinction between flow and reference):
- **Income TOTAL** (bold, load-bearing comparator): `█` solid block, FULL height
- **Income per-stream** (lighter, sub-lines): `·` or `┄` or per-stream marker, half-height — see legend
- **Spending** (bold flow line): `▒` medium shade
- **FI threshold reference** (capacity, dashed reference line): `╌╌╌` dashed horizontal
- **Partial months** (any series): dashed variant of the series's marker, NOT solid

Multi-line bold-total over stacked-area: the total is what crosses spending, so the total has to be visually dominant. Stacks bury individual streams.

Example layout (5 months, two income streams + total):

```
 $8000┤
      │             ████████████  ← income TOTAL (bold)
 $6000┤████████████              ┄┄┄┄  ← partial month dashed
      │··················· ·············  ← personal_active stream (light)
 $4000┤▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ← spending
      │╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌  ← FI threshold (4% SWR capacity, dashed reference)
 $2000┤   ········  ·······  ······  ← business_income stream (light)
      │
    $0└────┬────┬────┬────┬────┬
         Jan  Feb  Mar  Apr  May
                                 2026

  Income TOTAL  █   Personal-active  ··  Business  ··  Spending  ▒  FI threshold (4% SWR)  ╌
  Partial month variant: same marker, dashed
```

For longer time ranges (12+ months), narrow the columns. For very long ranges (24+), use compressed-month markers (every 3rd month labeled).

Crossover annotation: when the FI threshold reference line is above the spending line, annotate at the crossing point: `★ FI threshold — capacity ≥ spending starting [month]`.

**Color / typography polish**: the ASCII baseline above is the headless-friendly contract. For print-ready / wall-ready output, downstream upgrade via the `design:` skill (or matplotlib SVG/PNG path below) can add color, hierarchy, and typography. Don't gold-plate the ASCII; keep it readable in a terminal.

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
plt.savefig("<finances_root>/wallchart.png", dpi=300)
```

PNG output is dpi=300 so it prints cleanly at 8×11 or larger. Color choices favor printability (no near-white on white).

### Step 6 — Write outputs

Two artifacts:

```
<finances_root>/wallchart.md       # Data + ASCII chart + caveats
<finances_root>/wallchart.png      # Renderable image (when matplotlib path is implemented)
```

#### `wallchart.md` schema:

```markdown
---
generated: YYYY-MM-DD
data-source: monthly-tabs/_trend-totals.csv
months-included: YYYY-MM to YYYY-MM
swr-assumption: 4%
fi-threshold-method: capacity-projection   # always portfolio × SWR / 12; actual yield folds into income (Step 2), balance-change is an optional separate panel — see Step 3
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

| Month | Active income | Business (net) | Investment yield | Income TOTAL | Spending | FI threshold (capacity) | Complete? | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-01 | $X | $X | $X | $X | $Y | $Z | ✓ / partial | |
| 2026-02 | ... | ... | ... | ... | ... | ... | ... | |
| ... | | | | | | | | |

(Per-stream columns expand or contract based on which income streams the user has declared in `wallchart-config.md`. The TOTAL column is always present.)

## Caveats

- **The FI threshold reference line is capacity, not cash.** At a [4]% SWR, today's portfolio of $P could sustainably support $Z/mo. Actual cash-yield is lower (auto-reinvested) and is plotted separately as an income stream — see Step 2.
- **No sequence-of-returns adjustment.** A 4% SWR assumes a "normal" market trajectory; early-retirement years that hit a bear market reduce the safe rate. For finer-grained scenario work, see `/fi:crossover`.
- **No pension or Social Security overlay.** If you have future income streams (FERS, SSA, etc.), they reduce the spending you need the portfolio to cover. `/fi:crossover` does the bridge math.
- **Spending line is current state.** Lifestyle inflation, healthcare cost trajectory, and time-bucketed spending (Bill Perkins) are not modeled — the chart treats current spending as flat-forward.
- **No tax adjustment.** SWR of 4% is gross; real spendable income depends on the tax mix of your accounts.
- **Outliers are surfaced, not silently filtered.** If your data has a windfall (severance, sale, inheritance) miscategorized as recurring income, the skill flags it and asks how to handle. See Step 2.

## Re-rendering

Re-run `/fi:wallchart` after `/fi:track-flow` adds new monthly data. Chart updates in place; history is the trend itself, not preserved renders.
```

### Step 7 — Closing

Show:

> *"Wall chart at <finances_root>/wallchart.md. Print it, tape it to a wall.*
>
> *Status: [already-crossed | crossing-visible-at-YYYY-MM | not-yet-crossed-projected-YYYY]. [One-line headline.]*
>
> *Refresh me whenever `/fi:track-flow` finishes a fresh month. The trend is the chart's whole point — let the curves bend.*
>
> *For the bridge-math underneath the projection (when does FERS / SSA kick in, what's the depletion timeline if you stop working today), see `/fi:crossover`."*

---

## Output schema

### `<finances_root>/wallchart.md`

(Per Step 6. Frontmatter declares generation date, data source, SWR assumption, crossover status. Body has the at-a-glance summary, ASCII chart, per-month data table, and caveats.)

### `<finances_root>/wallchart.png` (planned)

Generated via matplotlib when the Python optimization is built. Until then, ASCII-only.

---

## Headless behavior

Fully supported. Cron-friendly:

- Pulls from already-existing CSV + holdings.md (no interactive prompts needed if the user has previously declared an SWR and resolved any outlier prompts)
- SWR choice + per-outlier handling decisions persist in `<finances_root>/profile/wallchart-config.md` after first run
- If a NEW outlier appears in a headless run (no human to answer the Step 2 prompt), render it raw with an inline annotation flagging it for the next interactive run — never silently filter it
- Re-renders the wallchart at whatever cadence the cron fires (typically end-of-month after `/fi:track-flow` finalizes)

For first runs, interactive setup is required to capture the SWR preference.

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
- [ ] `design:` skill integration for color/typography polish — the ASCII baseline is the headless contract; print-ready output is a downstream polish pass
- [ ] Historical-portfolio back-cast for the FI threshold reference — if `holdings.md` has historical balance entries, draw a sloped reference line per-month rather than the flat current-value line (toggle, not default)
- [ ] Optional balance-change net-worth-delta panel — separate from the main chart, for users who want it
- [ ] Per-category spending panels reading `monthly-tabs/_trend-categories.csv` — the reserved consumer named in AGENTS.md's contract table; `/fi:track-flow` already writes the file every run, so the data will be waiting
- [ ] Annotation layer: mark major life events (RIF, severance start/end, side-hustle launch, etc.) on the chart so the bends have context
- [ ] Multi-currency rendering — if user is multi-currency, decide whether to plot base-currency only or include side panels per currency
- [ ] Mobile/phone-friendly rendering — ASCII looks bad on narrow terminals; responsive sizing
- [ ] Print-optimized layout: title block + chart + key + per-month data table on one printable page
- [ ] Side-by-side comparison: this year's chart vs prior year's chart, scaled equivalently
- [ ] Optional fifth series: net worth (from `holdings.md` historical snapshots) — useful but can clutter; toggle-on
- [ ] Caveat refresher: when caveats apply specifically (e.g., user has FERS — surface FERS-specific caveats in the file)

## Status history

- **2026-05-28** — Fresh-user QA walkthrough revealed 5 wallchart-specific structural issues (W-1 through W-5), 3 suite-level findings (S-1 path resolution; S-2 + S-3 in `/fi:track-flow`), and 2 cross-cutting meta-patterns (M-1 skills-as-advisors; M-2 default-to-inclusion). SKILL.md updated to reflect: include-all-months default, multi-stream income with bold combined-total comparator, reframed Step 3 as concept-not-method (capacity reference line vs. flow lines), mandatory outlier detection with user-decided handling, conversational prompts with explicit Q&A invitations, persistence to `wallchart-config.md`. Status remains `draft` pending the suite-level path resolution work (S-1) and a clean second walkthrough.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 5 — make life energy visible via long-arc wall chart. The three-line composition (income / spending / investment income) is the original prescription. The "tape it to a wall" framing is theirs and load-bearing.
- **Bill Bengen** (1994) and the **Trinity Study** (Cooley, Hubbard & Walz, 1998). The 4% safe withdrawal rate baseline used as default for projected-investment-income method. Modern conservative readers (e.g., ERN's Big ERN) argue for 3.3-3.5% on long horizons; aggressive readers argue 4.5-5% for shorter horizons. Skill makes the rate configurable.
- **Marika Olson** (2026). Three-method investment-income computation (actual / balance-change-derived / forward-projected), ASCII-first rendering, default to forward-projection because that's the line that conceptually crosses spending in the YMOYL framing, integration with `/fi:track-flow`'s `_trend-totals.csv` rather than re-aggregating from monthly tabs.
