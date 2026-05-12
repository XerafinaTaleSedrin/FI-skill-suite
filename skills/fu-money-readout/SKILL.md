---
name: fu-money-readout
description: Optional daily ground-state report — net direction, runway, recurring passive income, crossover %, nuclear runway. Reads from holdings.md + track-flow's _trend-totals.csv + future-income-streams profile. ("FU" in the skill name is intentional FI-community slang for "fuck-you money" — having enough to walk away from any situation. Not a typo of "FI money.")
layer: concept+pattern
ymoyl_step: 8
mode_aware: true
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Crossover-point concept (Step 8) — when investment income covers expenses"
  - book: Profit First (Michalowicz, 2017)
    contribution: "Three-month operating reserve / 'vault' concept (Chapter 9) — the business-level equivalent of the personal runway field in this readout. For users running a business, the runway calc operates on two layers: personal-side liquid savings (existing) and business-side reserve buffer (Profit First's vault). Surfaces both in the readout when the user has a business."
  - author: Marika Olson
    contribution: "2026 design refinements — Nuclear runway mandatory; future-income-streams profile shared with /fi:crossover; context footer for future income streams without folding into present-tense math"
last-reviewed: 2026-05-12
---

# /fi:fu-money-readout

> **About the name** — "FU money" is established FI-community slang for **"fuck-you money"**: the amount of money that gives you the freedom to walk away from any situation you don't want to be in (a bad job, a bad client, a bad relationship structure, a bad city). It's not a typo of "FI money" — it's a specific, deliberate term that captures the *agency* aspect of financial independence rather than the retirement-age aspect. James Altucher, Suze Orman, and the broader FI community have all used the term. This skill is named to keep the ethos visible.

Optional daily check-in skill. Produces a brief ground-state report from `holdings.md` so the user has a regular pulse on their financial position. Inspired by YMOYL's crossover-point model, modernized for a 2026 rate environment and any user-defined "retirement" frame.

---

## The concept (decades-stable)

The financial brain operates on a small number of orientation questions: *Am I gaining ground or losing it? How long can I sustain this? What's the worst case if everything fails?* When those questions are unanswered, anxiety fills the gap. When they're answered honestly and regularly, anxiety has nothing to feed on.

The reading should feel like a weather report — short, factual, no drama. Not "you're ahead by 12%!" Not "you'll never retire." Just the numbers, in a tone the user picked.

---

## The pattern (~5-year stable)

A short daily readout, rendered in the terminal or saved to a log file, produced from the user's local `holdings.md` file. NOT an interactive dashboard; NOT a real-time market ticker. The cadence is daily-or-less; the data updates only as fast as the user updates `holdings.md` (typically monthly). What changes day-to-day is the date, the freshness flag, and any recent events — not the underlying numbers.

---

## What the skill does at runtime

1. **Reads `holdings.md`.** Validates schema. Reports if the file is missing — points at `/fi:holdings-scaffold` to create one.
2. **Reads `~/finances/monthly-tabs/_trend-totals.csv`** (output from `/fi:track-flow`). Pulls recent-3-month median for active cashflow income, gross expenses, net cashflow, gross yield. If file missing, points at `/fi:track-flow`.
3. **Reads `~/finances/profile/future-income-streams.md`** (shared with `/fi:crossover` — see schema below). Captures pension/annuity/SSA estimates with eligibility ages. If file missing on first run, prompts the user to create it.
4. **Checks freshness.** Flags `holdings.md` warm if last-updated >14 days ago; stale if >30 days. Flags `_trend-totals.csv` stale if last month is >2 months old.
5. **Pulls the user's "retirement frame"** from `~/finances/profile/retirement-frame.md`. Frame options:
   - **Full stop**: traditional retirement, all income from passive sources.
   - **Location-time flexibility**: working, but able to choose where and when.
   - **Income downshift**: working, but at lower income because non-money values are weighted higher.
   - **Coast FI**: invested enough that compounding alone gets to FI by traditional retirement age, even with no further contributions.
6. **Computes the readout fields (PRESENT-TENSE only — no future income folded in):**
   - **Net direction**: this month vs. last month (active cashflow income − gross expenses; windfalls noted separately if present).
   - **Runway**: months of expenses covered by liquid savings (cash + CDs + brokerage taxable assets) if all income stopped today.
   - **Recurring passive income**: current-month rate from HYSA interest + non-reinvesting dividends + rental net + cash-yielding investments. NOT future pension/SSA; NOT auto-reinvested portfolio yield (that's capacity, not active cashflow).
   - **Crossover %**: recurring passive income ÷ monthly expense baseline. Present-tense only.
   - **Nuclear runway**: if all active income stopped AND drawdown begins, how many years until portfolio depleted. **This calc DOES incorporate future income offsets** — at age 57 (or wherever pension/annuity activates), monthly burn against the portfolio drops by the annuity amount, extending nuclear runway. Reports the user's age at depletion.
7. **Renders the readout** in the user's chosen tone (matter-of-fact / warm / blunt).
8. **Footer: future income streams context line.** Names the streams (pension at age X, SSA at 62-70, etc.) without folding into present-tense math.
9. **Optional: load-bearing crossover line.** If `/fi:crossover` has run and saved a "load-bearing answer" to `~/finances/profile/crossover-headline.md`, echo it in the readout at user-chosen cadence. The crossover headline states the user's POSITION (computed FI crossover age, or "already FI") rather than a target-vs-progress framing. Examples: *"You are already FI under your chosen frame. Maintain trajectory."* or *"FI crossover at age 52 (range 49-56). Bridge from today: 8 years."* or *"Current trajectory does not cross FI threshold; gap is $X cumulative."* The readout doesn't recompute — `/fi:crossover` writes the line, readout repeats it. Cadence options: every readout / Mondays only / first-of-month / quarterly / on-request only. User picks at setup.
10. **Logs it** to `~/finances/fu-money-log/YYYY-MM-DD.md` so the user has a history.

---

## Output format

```
--- FU Money Readout (YYYY-MM-DD) ---

Right now:    [Net positive/negative direction] ([+/-]$X,XXX/mo)
Runway:       XX months from liquid savings
Recurring:    $X,XXX/mo passive (list sources)
Crossover %:  XX% of monthly expenses covered passively
Nuclear:      XX years at full burn, zero income, before depleted (age you'd be: XX)
              Pension/annuity offsets activated: at age X, burn drops by $Y/mo

Future income streams (context — not in above):
  • [Pension/annuity 1, eligibility year, est. amount]
  • [SSA at 62/FRA/70 estimate]
  • See /fi:crossover for the FI-threshold math

Crossover headline (cadence: [every readout / Mondays / monthly / on-request]):
  → "[Load-bearing answer from last /fi:crossover run]"

[One grounding sentence — chosen from user's tone preference]
---
```

---

## Architectural features

- **Mandatory Nuclear line.** This is the anxiety answer. Even if everything fails, here's how long the user lasts. Not a plan — a grounding number. Calculated from the full draw-down sequence the user defines (savings → cash → brokerage → Roth contributions → Trad IRA penalty-eligible → real estate liquidation → etc.). **Future income offsets are incorporated**: at the eligibility age for any future income stream (pension, deferred annuity, SSA), the monthly burn against the portfolio drops by that stream's amount, extending nuclear runway. Reports the activation year(s) and the offset amount(s) inline.
- **Two-scenario nuclear runway for streams with reduced/full eligibility ages.** When a stream offers an early-reduced option (e.g., FERS deferred annuity at 57 with 25% reduction vs full at 62), run the simulation twice and report both. Often counterintuitive: the early-reduced scenario produces *longer* nuclear runway because more months of income > higher monthly amount over fewer months. The two-scenario frame surfaces the time-arbitrage decision honestly.
- **Crossover % reframe.** The default crossover % uses cash-yielding income only (HYSA interest, dividends paid to checking, rental net). For users whose portfolios auto-reinvest most yield, this number reads brutally low. Surface a parenthetical: *"X% if portfolio reinvest were toggled off"* — honest framing of latent capacity. Frame as optionality, not recommendation (toggling reinvest stops compounding). Computes via `gross_yield - cash_yield_already_counted` from track-flow's per-month yield breakdown.
- **Pending-stream caveat.** If `future-income-streams.md` declares a stream type but the data fields are empty (e.g., government retirement income placeholder with no estimates yet — US SSA, UK State Pension, Canadian CPP/OAS, Australian Age Pension, French régime général, etc.), flag the depletion-age numbers as conservative. They almost certainly extend further once the missing data is filled in. Surface the gap explicitly with a locale-appropriate prompt (e.g., "pull statement at ssa.gov" for US users); don't silently treat empty as zero. Government retirement income is the most common pending-stream case for users who haven't yet pulled their projection statement; the skill should specifically prompt for it on first run when the user's declared country has such a system.

- **Future expense reductions (mortgage, auto loan, student loan payoffs).** Symmetric to future income streams. At a known future date (computed via amortization formula), the monthly burn drops by the P&I portion of the payment. For mortgages with escrow, only P&I drops — taxes and insurance continue as direct payments after payoff. Treat as a "future income stream" mathematically (positive offset to burn at activation date) but tag with `type: future-expense-reduction` for honest framing. The skill should specifically prompt for mortgage on first run for any user with `holdings.md` showing a mortgage liability, since the payoff event often falls in bridge years and meaningfully changes the FI math. Common case: 30-year mortgage taken at age 35 pays off at 65, just as government retirement income stacks with employer pension — the combined effect (mortgage drops + retirement income stacks) often closes any remaining FI gap entirely.

- **Compute payoff from current payment, NOT lender-stated maturity.** Many mortgage servicers display "remaining term" or "maturity date" reflecting the *original loan schedule with minimum scheduled P&I* — not what the user is actually paying. If the user made principal curtailments earlier in the loan or is otherwise paying above the minimum scheduled P&I, the actual payoff date is significantly sooner than the stated maturity. The skill computes payoff via the amortization formula `months = log(P / (P - rL)) / log(1 + r)` where P = current monthly P&I payment, r = monthly rate, L = current balance. Trust the math, not the lender's display. Common case: user is paying ~2x the minimum P&I → loan pays off in roughly half the stated remaining months. The skill should surface the discrepancy explicitly when it exists: *"Your lender shows X months remaining, but at your current P&I payment, actual payoff is Y months. Past curtailments are why."*

- **Active-income baseline forward-projection.** The historical median active income from `/fi:track-flow` may be inflated by finite income sources (UI benefits, severance, a contract job that's ending). Before using the historical median in nuclear-runway or bridge calcs, ask the user: *"Are there any income sources in this median that will end soon? UI benefits, severance, a contract ending, a side gig you're winding down?"* If yes, recompute a "post-cliff" baseline excluding those sources. The bridge math should run against the post-cliff baseline, not the inflated historical median. This is a common case for recently-RIFed federal employees (UI ends 6-12 months after filing), severance recipients (severance covers a defined period), and contract-to-perm transitions.
- **Present-tense vs. future-tense discipline.** The readout's primary numbers (Runway, Recurring, Crossover %) are STRICTLY present-tense — they do NOT include future pension/annuity/SSA streams. The Nuclear line and the Future Income footer are where future streams show up. The crossover skill is where future streams do their FI-threshold math. Mixing tenses in the present-tense numbers makes today's anxiety answer unreliable; keeping them clean keeps the readout honest.
- **Crossover headline echo.** If `/fi:crossover` has run, its load-bearing answer is saved to `~/finances/profile/crossover-headline.md`. The readout echoes that line at user-configured cadence (every readout / Mondays / first-of-month / quarterly / on-request). The readout never recomputes the crossover; it just repeats. Decouples slow sensitivity math from fast daily orientation.
- **Tone selectable**: matter-of-fact / warm / blunt. User picks at setup. The skill offers grounding sentence variants in the chosen tone (kept in `tone-options.md` per the skill folder).
- **Runtime freshness**: pulls `holdings.md`'s `last-updated` date; flags if stale.
- **Pluggable into session start**: optional; default OFF. User opts in. If opted in, the readout fires on first session of the day after any other session-start rituals.
- **Mode-aware**: readout adjusts based on the user's retirement frame. The crossover math is different for each variant.
  - Full stop: crossover% target is 100%.
  - Location-time flexibility: crossover% target is 60-80% (working partially).
  - Income downshift: crossover% target is 40-60% (downshift while working).
  - Coast FI: crossover% target is 0% (just need invested enough to compound).

---

## Profile files (shared with /fi:crossover)

### `~/finances/profile/future-income-streams.md`

User declares each future income stream once; both `/fi:fu-money-readout` and `/fi:crossover` read this file. Schema:

```yaml
---
last-updated: YYYY-MM-DD
schema-version: 1
---

# Future income streams

## Pension / Deferred Annuity 1
type: pension|deferred-annuity|annuity-purchased
source: <employer or institution>
status: vested|partially-vested|projected
eligibility_age_full: <age, e.g. 62>
eligibility_age_reduced: <age, e.g. 57>
estimated_monthly_full: <USD/mo at full eligibility>
estimated_monthly_reduced: <USD/mo at reduced eligibility>
confidence: high|medium|low
notes: |
  <free text — assumptions, pending verifications, etc.>

## Government Retirement Income
# US: Social Security (SSA). UK: State Pension. Canada: CPP/OAS. Australia: Age Pension.
# France: régime général. Etc. Schema is locale-neutral; prompt copy adapts to user's country.
type: government-retirement
country: <ISO 3166-1 alpha-2, e.g. US, GB, CA>
projected_monthly_at_early: <local currency>     # e.g. SSA at 62, UK at 66 (approx)
projected_monthly_at_full: <local currency>      # e.g. SSA at FRA, UK at State Pension Age
projected_monthly_at_late: <local currency>      # e.g. SSA at 70, UK delayed-pension-bonus
early_age: <age>
full_age: <age>
late_age: <age>
last_pulled: YYYY-MM-DD

## Other (rental net, royalties, etc.)
- type: <kind>
  amount_monthly: <USD>
  starts_age: <age>
  ends_age: <age|null>

## Future expense reductions (amortizing debt with payoff date)
- type: mortgage|auto-loan|student-loan|other-amortizing
  balance: <USD as of last_balance_check>
  rate_apr: <%, e.g. 3.65>
  monthly_payment_pi: <USD>             # principal + interest portion
  monthly_payment_total: <USD>          # PITI for mortgages: P&I + tax/insurance escrow
  escrow_continues_after_payoff: true|false  # for mortgages, T&I doesn't disappear when loan ends
  payoff_date_estimated: YYYY-MM         # auto-computed from balance + rate + payment
  last_balance_check: YYYY-MM-DD
```

The skill computes payoff date from amortization formula:
`months = log(P / (P - rL)) / log(1 + r)` where P = monthly P&I payment, r = monthly rate, L = current balance.

At payoff, monthly burn drops by `monthly_payment_pi` (or `monthly_payment_total` if no escrow continues). For mortgages with escrow, drop only the P&I portion — taxes and insurance continue as direct payments.

**Why this matters:** for users with a mortgage payoff in their bridge years, the post-payoff drop in burn (often $1,000-$3,000/mo) is meaningful. A 30-year mortgage taken at age 35 pays off at 65 — right when SSA stacks. The combined effect (mortgage drops + FERS/SSA stacks) often closes any remaining FI gap entirely.

### `~/finances/profile/retirement-frame.md`

```yaml
---
frame: full-stop|location-time-flexibility|income-downshift|coast-fi
target_crossover_pct: <0-100>  # auto-derived from frame; user can override
target_age: <age>
notes: |
  <user's working definition of retirement>
---
```

### `~/finances/profile/crossover-headline.md`

Written by `/fi:crossover`. One line, plain text. Read by `/fi:fu-money-readout` for the headline echo.

```
Until <year> to grow <income stream> to $<amount>/mo for the bridge years.
```

### `~/finances/profile/readout-config.md`

```yaml
---
tone: matter-of-fact|warm|blunt
crossover_echo_cadence: every-readout|mondays|first-of-month|quarterly|on-request
nuclear_drawdown_sequence:
  - cash-and-cd
  - brokerage-taxable
  - roth-contributions
  - trad-ira-after-59-and-half
  - real-estate-equity
  - vehicle
---
```

---

## Headless behavior

This skill is **explicitly designed to run headlessly** as a session-start ritual or a daily cron. When fired with no human present:

- Reads `holdings.md` as normal.
- Computes the readout.
- Writes it to `~/finances/fu-money-log/YYYY-MM-DD.md`.
- Does NOT print to stdout (no human there to read it).
- Does NOT block on any interactive prompt.
- If `holdings.md` is missing or malformed: writes an error note to the log file with a clear next step (run `/fi:holdings-scaffold`), exits cleanly.

---

## Mode-aware retirement frames

The user picks one frame at setup; the skill stores the choice in a profile file. Frame definitions:

### Full stop
Traditional retirement. All income from passive sources. Crossover target = 100% of expenses.

### Location-time flexibility
Working, but with full freedom to choose where and when. Crossover target = 60-80% (partial work fills the gap).

### Income downshift
Working in a deliberately lower-income role aligned with values, not maximization. Crossover target = 40-60% (work fills more than half).

### Coast FI
Invested enough that compounding alone reaches FI by traditional retirement age, even with zero further contributions. Crossover target = 0% (the math is "is the existing invested amount × expected real return enough to compound to target by year N?").

For each frame, the readout uses different language and different math. The output fields stay the same; the targets differ.

---

## Validation

End-to-end-validated against real user data 2026-05-03. Findings encoded back into SKILL.md as design rules:

1. Present-tense vs future-tense discipline (don't fold pension/SSA into present-tense Crossover %)
2. Two-scenario nuclear runway for streams with reduced/full eligibility ages — counterintuitively, early-reduced often outperforms waited-full because of time arbitrage
3. Crossover % reframe with auto-reinvest-toggled-off parenthetical (otherwise crossover reads brutally low for users whose portfolios reinvest)
4. Pending-stream caveat (locale-neutral — US SSA, UK State Pension, CA CPP/OAS, etc.; don't let empty government-retirement-income fields silently understate runway)
5. Crossover headline echo from `/fi:crossover` — readout repeats, doesn't recompute (decouples slow sensitivity math from fast daily orientation)
6. Mortgage payoff event modeled as future-expense-reduction (symmetric to future-income-stream); often falls in bridge years and meaningfully closes the FI gap
7. Active-income baseline forward-projection (don't use UI-inflated or severance-inflated historical median for bridge math; ask user about ending income sources before computing)
8. Compute payoff from current payment, not lender-stated maturity (lenders often display original 30-yr maturity even when user is paying ~2x the minimum P&I; trust the amortization formula, not the lender's display)

User-specific test artifacts live on the user's machine in their gitignored finance directory. They do not get published.

**Privacy posture**: this SKILL.md describes the procedure in general terms. User-specific data (account names, dollar amounts, vendor patterns, transaction counts) is never embedded in the public skill files. All user data writes go to gitignored paths on the user's machine.

---

## TODO

- [x] Define the schema for the user's profile files (retirement frame + tone preference + draw-down sequence + future-income-streams + crossover-headline + readout-config) — done in this draft
- [ ] Build the headless cron-friendly entry point.
- [ ] Implement the four retirement-frame variants of the crossover math.
- [ ] Define the tone-options.md content (grounding-sentence pool per tone).
- [ ] Worked examples in `examples/` for each retirement frame.
- [x] Cross-skill: define how `/fi:track-flow` feeds the monthly-expense baseline — reads `_trend-totals.csv` per the new schema
- [ ] Roth contribution tracking — currently nuclear runway omits the Roth-contributions-only pool because it requires user-declared contribution history. Add a `roth-contributions.md` profile entry with annual contribution log so the penalty-free pre-59.5 pool can be computed.
- [ ] Aggregator-style ingestion of HYSA/CD APYs from holdings.md so recurring-passive-income calc auto-refreshes when rates change.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Crossover point as Step 8.
- **Marika Olson** (2026). Design refinements: the "Nuclear runway" concept (worst-case grounding number addressing anxiety more than crossover% alone); present-tense-vs-future-tense discipline (don't fold pension/government-retirement income into Crossover %); two-scenario nuclear runway for streams with early-reduced and waited-full options (time-arbitrage decision surfaced explicitly); crossover-% reframe with auto-reinvest-toggled-off parenthetical; locale-neutral pending-stream caveat; crossover-headline echo pattern (decouples slow sensitivity math from fast daily orientation); future-income-streams profile shared with `/fi:crossover`; future-expense-reductions (mortgage payoff modeled symmetrically to future-income-streams); active-income forward-projection (don't use UI-inflated historical median for bridge math); compute-payoff-from-current-payment rule (lender-stated maturity is unreliable when user paid above minimum scheduled P&I).
