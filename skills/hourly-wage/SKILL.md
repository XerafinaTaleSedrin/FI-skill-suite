---
name: hourly-wage
description: Computes real hourly wage — the YMOYL life-energy math, modernized for 2026 work modes (remote, hybrid, on-site, gig). Subtracts every cost incurred because of the job; adds every hour spent because of the job. Mode-aware so it doesn't flatter remote workers or overstate on-site costs.
layer: concept+pattern
ymoyl_step: 2
mode_aware: true
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 2 — real hourly wage formula (life-energy math). 1992 original assumed an office commuter; the formula structure (subtract work-related costs, add work-related hours, divide) carries forward."
  - book: Profit First (Michalowicz, 2017)
    contribution: "Owner-as-key-employee principle: the small-business owner deserves a real wage for their labor, separate from any profit return on bearing risk. Naturalizes the real-hourly-wage calculation for the business-owner case where 'wage' might otherwise be conflated with owner draw or treated as a residual. Adds a 'owner as employee' branch to the skill so the math works for business owners, not only W-2 / 1099 workers."
  - author: Marika Olson
    contribution: "2026 design refinements: work-mode branching (remote / hybrid / on-site / gig), AI-tooling OpEx as a load-bearing line item, blurred-boundary hours for remote workers, multi-stream income handling (W-2 + 1099 + side hustle + UI / severance simultaneously), user-extensible category capture, dated output for trend-over-time analysis."
last-reviewed: 2026-05-12
---

# /fi:hourly-wage

Walks the user through computing their *real* hourly wage — gross pay minus every cost incurred *because* you have this job, divided by every hour spent *because* you have this job. The 2026 update makes it work-mode-aware so it doesn't apply 1992 office-commuter assumptions to remote workers, and so it doesn't miss the modern line items (AI/SaaS OpEx, blurred-boundary hours, home-office utility allocation) that 1992 didn't have to consider.

Output: a dated wage file the user can re-run quarterly or after major work-mode changes, with trend-over-time analysis as multiple runs accrete.

---

## The concept (decades-stable)

What you actually earn per hour of life energy spent on work is almost never what your paycheck says. The YMOYL formula:

- **Subtract** from gross pay: every cost incurred *because* you have this job.
- **Add** to total hours: every hour spent *because* you have this job.
- Divide.

The result is your real hourly wage — and it's almost always shocking.

The 1992 version assumed an office commuter. The 2026 version has to handle remote, hybrid, on-site, and gig workers, each with completely different line items. The skill is **mode-aware** so it doesn't apply the wrong subset.

The point is not to discourage work. The point is to *see* what each hour is worth, so the next time someone asks you to "just take this on" or "stay another two hours" you have a number you can think with.

---

## The pattern (~5-year stable)

Branching walk-through based on work mode. For each mode, surface the relevant subset of subtractions and additions. Capture user-specific custom categories at runtime. Compute and report. Write to a dated file so subsequent runs show trend.

For users with multiple income streams (a W-2 + a 1099 side hustle + UI + severance), the skill optionally splits — computes a real hourly wage *per stream* — because the line items often differ dramatically between streams (the side hustle has zero commute but full AI/SaaS overhead; the W-2 has a commute but employer-provided tooling).

---

## What the skill does at runtime

### Step 1 — Establish work mode

Ask:

> *"What's your current work mode? Pick the one closest:*
> - *Fully remote (work from home or chosen location, no regular office days)*
> - *Hybrid (X days/week in office, the rest remote)*
> - *Fully on-site (every workday at an employer location)*
> - *Gig / freelance / consulting (multi-client, often remote, sometimes site visits)*
> - *Other / mixed — tell me about it"*

Mode determines which line-item subset gets surfaced in Step 4. For hybrid, also ask:

> *"How many days per week in office?"*

Used to weight commute-side line items proportionally.

For "Other / mixed," capture the description and apply judgment about which subset(s) to show. Common: a fully-remote primary job + on-site side gig (e.g., farmers market sales) — run the computation per stream.

### Step 2 — Multi-stream check

Ask:

> *"Is this for one income stream, or do you have multiple streams you'd like to compute separately? Examples:*
> - *Single stream — one job, one paycheck shape, all-in.*
> - *Multi-stream split — W-2 + side hustle, two W-2s at different rates, etc. The skill runs once per stream and shows you both real hourly wages plus a blended one."*

If multi-stream, capture stream names + relative time allocation (e.g., "W-2 = 40 hr/week declared, side hustle = 8 hr/week"). The skill loops Steps 3-5 per stream.

For users currently between full-time roles (UI + severance + occasional consulting), this matters: severance has near-zero work-attributable cost; UI has zero cost (it's not work); consulting has full overhead. Bundling them all into one wage number obscures the picture.

### Step 3 — Capture gross income for the stream

Ask:

> *"For this stream, gross pay (annualized or monthly — whichever you have on hand). Pre-tax. If you have variable income (commission, bonus, RSU vest), give me the realistic 12-month rolling number, not the optimistic projection."*

Also ask:

> *"How many declared work hours per week? What the contract / job description says, regardless of what you actually work."*

This is the **denominator anchor** — the official hour count we'll add unpaid work-related hours TO.

**PTO and paid holidays note**: if the user includes PTO/vacation/holiday weeks in their "declared hours" (counting all 52 weeks at full hours), that's the simplest treatment and the skill defaults to it. If the user wants to be more precise — declared hours = working weeks × hours/week (e.g., 48 weeks × 40 = 1920) — capture that separately. Either approach is honest; just don't mix.

### Step 3.5 — Capture employer-sponsored benefits and special compensation

Critical for honest W-2 vs gig comparisons. Gig/freelance workers pay for everything an employer would otherwise provide; ignoring employer-paid benefits artificially inflates gig wages relative to W-2.

For W-2 / employee streams, ask:

> *"Beyond gross pay, what employer-sponsored benefits do you receive? I'll add the employer-paid value to the compensation side. Walk through these — answer with annual dollar value or 'none / N/A':*

**Insurance and healthcare:**
- *Employer-paid health insurance premium (the employer's share, not yours — usually $5,000-$20,000/year for employee-only, more for family). Check your benefits portal or W-2 box 12 code DD.*
- *Dental + vision premiums (employer share)*
- *Life insurance (typically 1-2× salary, employer-paid)*
- *Short-term + long-term disability premiums*
- *Mental health / EAP (Employee Assistance Program) — usually nominal but real*

**Retirement and tax-advantaged:**
- *401(k) / 403(b) employer match — the dollars the employer puts in (NOT your contribution). Up to the match cap.*
- *HSA employer contribution*
- *Pension / cash-balance plan accruals (rare in 2026 private sector; common in government)*

**Family and care:**
- *Childcare subsidy or on-site daycare*
- *Dependent Care FSA admin (the tax savings, if employer-administered)*
- *Parental leave (paid weeks × weekly salary, divided by years between expected uses if you want it amortized — most users count it as zero unless actively planning)*

**Time off (paid):**
- *Paid vacation / PTO days*
- *Paid holidays*
- *Paid sick leave*
- *Sabbatical (some employers; rare)*

**Stipends and reimbursements:**
- *Phone / internet stipend*
- *Work-from-home equipment stipend*
- *Commuter benefits (pre-tax transit / parking — value = tax savings × employer admin value)*
- *Professional development / tuition reimbursement (annual cap × utilization rate)*
- *Wellness stipend, gym subsidy*
- *Free meals (uncommon outside tech; if present, $5-$15/day × workdays)*

**Equity (employee streams only):**
- *RSU vests this year (count at vest-date value — this is W-2 income and should already be in gross pay if reported correctly)*
- *Stock options exercised this year (NQSO bargain element OR ISO if disqualifying disposition — already in gross pay if reported)*
- *ESPP discount (15% discount on shares purchased — counts as compensation)*

If user is unsure about benefits values, point them at:
- W-2 box 12 codes (DD = employer health insurance, D = 401k contribution amount, W = HSA employer contribution)
- The annual benefits statement most employers issue (often called "Total Compensation Statement")
- Benefits portal / HR if neither is handy

**Stock options not yet vested**: handle separately:

> *"Unvested stock options or RSUs — handle three ways:*
> *1. **Don't count** (default, conservative — chickens-not-yet-hatched). Skip these.*
> *2. **Count at grant value × vesting probability** — for stable public-company RSUs with predictable vesting, multiply remaining shares by current price by (probability you'll be there to vest). Skip for private-company / pre-IPO options.*
> *3. **Mark as optionality** — track on a separate line, don't include in real-hourly-wage math, but surface as 'potential additional compensation if X happens.'"*

Default: option 1 (don't count). The real hourly wage is what your time is worth right now in this configuration; future-conditional value belongs in a separate analysis.

For gig / freelance / consulting streams, **most of these are zero (or the gig worker pays for them themselves)**. The contrast is the point — surface it:

> *"As a gig/freelance worker, you pay for what an employer would normally cover. That cost shows up in Step 4 as subtractions (your own health insurance premium, your own SE tax differential, your own equipment, your own PTO when you take it). The benefits side stays mostly empty here, which makes the contrast visible: your gig gross sounds higher than an equivalent W-2 because you're carrying the cost of all this."*

**PTO valuation note (employee streams only):**

PTO is tricky. Two valid framings:

1. **PTO is part of declared hours** — you already counted it when you said 40hr/wk × 52 weeks. No additional value adjustment. Simplest.
2. **PTO is additional compensation** — declared hours = working weeks only (e.g., 48 weeks × 40 = 1920); PTO weeks × weekly pay = additional value to add to compensation. More precise but requires the user to carve up declared hours.

Default to (1) unless the user is comparing across jobs with different PTO levels (e.g., W-2 with 4 weeks vs gig with 0 weeks). In that case, (2) makes the comparison honest.

### Step 3.6 — Compute total compensation (numerator)

```
gross_pay_annual = annual gross from Step 3
employer_benefits_total = sum of all employer-paid benefit values from Step 3.5
total_compensation = gross_pay_annual + employer_benefits_total
```

For the rest of the skill, "real annual pay" comes off `total_compensation`, NOT off `gross_pay_annual`. This is the load-bearing change for honest W-2 vs gig comparisons.

For multi-stream users: capture benefits per stream (W-2 has them; gig usually doesn't).

### Step 4 — Walk the line items (mode-branched)

Apply the relevant subset based on Step 1 mode. Capture per-line-item annual dollar amount or hour count.

Frame each prompt with the same template:

> *"[Line item]: roughly $X/year (or N hours/week) — does that fit, lower, higher, or N/A for you?"*

Use the user's last-12-months actuals where available (from `/fi:track-flow` if present — read the trend CSV for relevant categories like Transportation, Subscription-AI, Restaurants-work-meals). Otherwise, ask.

#### YMOYL-classic adjustments (apply for on-site, hybrid, gig site-visit days)

**Subtract from wages — work-attributable expenses:**

- **Commuting costs**: gas, transit, parking, vehicle wear, maintenance allocation, insurance differential. For hybrid, weight by office-days/total-days.
- **Work clothes**: dry cleaning, shoes wear, the wardrobe you wouldn't own otherwise.
- **Work meals out**: lunches, coffees, after-work-with-coworkers drinks. The "I don't pack lunch because I'm tired" line item.
- **Decompression spending**: the post-work drink, the "I deserve this" Amazon order, the impulse purchase that rides on top of work fatigue.
- **Escape entertainment**: the streaming service that's really an "I'm too tired to do anything else" subscription. The sport you don't actually attend but pay for. The video game you bought to numb out.
- **Job-related healthcare**: stress-related healthcare (therapy attributable to job stress, body work for desk-induced injuries, sleep aids, anti-anxiety medication).
- **Childcare / pet care during work hours**: only the work-attributable portion (not the date-night portion).
- **Convenience taxes**: prepared meals, grocery delivery, housekeeping you wouldn't pay for if you had time, lawn service, etc. — only the "I outsource this because I'm working too many hours" portion.

**Add to denominator — work-attributable hours:**

- **Commute hours**: door-to-desk-to-door. For hybrid, weight by office-days/total-days.
- **Prep hours**: getting ready (shower, dressing, grooming above what you'd do on a non-work day, packing).
- **Decompression hours**: the wind-down after work — the "I can't do anything for an hour after closing the laptop" period.
- **Work-related shopping hours**: errands you only do because of work (work-clothes shopping, prepping the home for work-from-home days, work-event coordination).
- **Work-event hours**: networking events, work parties, weekend retreats, mandatory-fun.
- **Work-related sickness time**: sick days you used because of work-induced burnout (different from sick days for ordinary illness).

#### 2026 remote / hybrid additions (additive — apply to remote and hybrid modes)

**Subtract from wages:**

- **Home internet (work-attributed portion)**: typically 30-70% depending on how much your role hits the network. Ask: *"What % of your home internet usage is work? If you're not sure, 50% is a reasonable default for a knowledge worker."*
- **Home electricity (work-attributed portion)**: desk + monitors + lighting + heating/cooling during work hours. For US, typically $20-60/month in attributed cost depending on home size and HVAC efficiency.
- **Home office space allocation**: the rent or mortgage interest portion attributable to the dedicated work area. Square-footage method: (work-area-sqft / total-home-sqft) × (rent or mortgage interest annual).
- **Ergonomic furniture amortization**: chair, desk, monitor, monitor arm, keyboard, mouse, headset. Sum cost / useful-life (5 years for chair, 7 years for desk, 4 years for monitor).
- **AI / SaaS OpEx — the load-bearing 2026 line item**: Claude / ChatGPT / Notion / Buffer / Canva / Linear / 1Password / etc. Sum annual subscriptions. For a serious knowledge worker, this is often $1,500-$5,000/year and growing. **Ignoring this line item pretends the wage is higher than it is.**
- **Equipment refresh cycle**: laptop, monitor, headset, webcam. (Cost of last refresh) / (years until next refresh). Typical: $3,000 over 4 years = $750/year.
- **Work-from-home isolation costs**: therapy attributable to isolation, body work for sedentary work, social re-entry costs (drinks/dinners just to maintain network), gym membership replacing the incidental walking of office life.
- **Increased home-meal cost**: counterintuitive but real — eating every meal at home raises grocery spend even when you're not eating out. Not always large, but worth flagging.

**Add to denominator:**

- **Blurred-boundary hours**: the "always-on" tax of working from where you live. The Slack-check at 9pm, the email scan over morning coffee, the "quick thing" on the weekend. Ask: *"Honest estimate of hours per week you spend on work outside your declared work hours, including digital-only checks?"* Most remote workers under-report this. Probe gently for accuracy: *"Including the morning Slack scroll? The Sunday-night dread-check?"*
- **Cognitive context-switching cost**: working from home means switching modes 10-20 times a day (work / household / kids / personal admin). Hard to quantify directly, but the user can estimate the daily drag in minutes. Many people land on 30-60 minutes/day of friction loss.
- **Tooling-maintenance hours**: AI prompt engineering, software updates, MCP debugging, integration setup, plugin troubleshooting, model migrations. For someone running an AI-heavy stack, often 2-4 hours/week.

#### Gig / freelance / consulting additions

Apply YMOYL-classic on any in-person engagement days, plus 2026 remote additions for the home/office time, PLUS gig-specific:

**Subtract from wages:**

- **Self-employment tax differential**: gig workers pay both halves of FICA (15.3% vs employee's 7.65%). The differential (~7.65% of self-employment income above the threshold) is a work-attributable cost vs an equivalent W-2 wage.
- **Health insurance you'd otherwise get from an employer**: the difference between your individual market premium and the equivalent employer-subsidized plan. Often $500-$1,500/month differential.
- **Liability insurance** (E&O, BOP, professional liability): annual premium.
- **Business-incidental costs**: domain renewals, legal fees for entity setup, bookkeeping software, tax-prep for the business return.
- **Marketing / business development**: website hosting, conference fees, networking event tickets, paid lead-gen.
- **Equipment + software not covered by clients**: own laptop, own software, own everything.
- **Unpaid time between engagements**: the gap weeks where you're working on the business but not earning.

**Add to denominator:**

- **Sales/business-development hours**: time pitching, writing proposals, doing intake calls, networking. For most gig workers this is 20-40% of total hours.
- **Admin / accounting hours**: invoicing, bookkeeping, tax prep, contract review, follow-up on receivables.
- **Continuing education hours**: required for professional credentials, but also informal "stay current" reading and exploration.

### Step 5 — User-extensible categories

After walking the standard list, ask:

> *"Are there categories specific to your situation we should factor in? Examples:*
> - *A side hustle that demands its own subscription stack*
> - *A specialty insurance or licensing fee for your profession*
> - *A geographic-specific cost (e.g., paying for parking in a high-cost-of-living city)*
> - *A travel-heavy role (lounge memberships, business-class differential, lost-personal-time)*
> - *Caregiving or accommodation costs your employer doesn't cover*
> - *Anything else you think 'I'm only paying for this because I work'"*

Capture each user-named category with annual dollar amount and/or hours/week. Persist to `~/finances/profile/hourly-wage-custom-categories.md` (gitignored) so subsequent runs offer them automatically.

### Step 6 — Compute

For each stream:

```
declared_annual_hours = declared_hours_per_week × 52
work_attributable_hours = sum(all "add to denominator" line items) × 52  (or appropriate annualization)
total_life_energy_hours = declared_annual_hours + work_attributable_hours

total_compensation = gross_pay_annual + employer_benefits_total       # from Step 3.6
work_attributable_costs = sum(all "subtract from wages" line items, annualized)
real_annual_pay = total_compensation - work_attributable_costs

real_hourly_wage = real_annual_pay / total_life_energy_hours
declared_hourly_wage = gross_pay_annual / declared_annual_hours        # uses gross only — what most people think they earn
total_comp_hourly = total_compensation / declared_annual_hours          # uses total comp — honest "what employer pays for you per declared hour"
delta_from_declared = declared_hourly_wage - real_hourly_wage
delta_from_total_comp = total_comp_hourly - real_hourly_wage
delta_pct = delta_from_total_comp / total_comp_hourly
```

The skill reports THREE numbers per stream (not two):
1. **Declared hourly wage** — what the user thinks they earn (gross / declared hours)
2. **Total comp hourly** — what the employer actually pays for them (gross + benefits / declared hours) — usually 15-30% higher than declared
3. **Real hourly wage** — what their life energy is actually worth (total comp - work-attributable costs / total life energy hours including unpaid work hours)

The most useful headline is #1 → #3 (declared vs real) because that's what the user feels day-to-day. Total comp is shown as a "for context" line so the user can see how much their benefits package is worth before subtractions hit it.

For multi-stream: compute per-stream, then a blended:

```
blended_real_hourly = sum(stream_real_pay) / sum(stream_total_hours)
```

### Step 7 — Report

Show:

```
=== Real Hourly Wage Report — [Stream Name] ===

Compensation:
  Gross annual pay:           $G
  Employer-paid benefits:     +$B
  Total compensation:         $T = $G + $B
  Declared hours/year:        N hours

Hourly wages — three views:
  Declared hourly wage:       $D/hr  ($G / N — what most people think they earn)
  Total comp hourly:          $T_h/hr ($T / N — what employer actually pays per declared hour)
  Real hourly wage:           $R/hr  ($T - subtractions / N + additions — life-energy honest)

Benefits side (added to compensation):
  1. [Category]               +$X
  2. ...
  Total benefits:             +$B
  Benefits as % of gross:     P%

Subtractions (top 5 work-attributable costs):
  1. [Category]               -$X
  2. ...
  Total subtractions:         -$S
  Work-attributable cost as % of total comp: Q%

Additions to hours (top 5 work-attributable hours):
  1. [Category]               +N hr/year
  2. ...
  Total additional hours:     +M hr/year
  Total life-energy hours:    K hours

Headline:
  $D/hr declared → $R/hr real    ([X]% reduction)
  $T_h/hr total-comp → $R/hr real    ([Y]% reduction)

For context:
  At $R/hr, the cost of [example purchase: $100 dinner] is W hours of life energy.
  At $R/hr, the cost of [example purchase: $1,000 vacation] is X hours.
  At $R/hr, the cost of [example purchase: $30,000 car] is Y hours.
```

Use the user's actual recent purchases (from `/fi:track-flow` if available) for the "for context" anchor — it's more grounding when the example is something they actually bought.

For multi-stream, also show the comparison:

```
=== Multi-Stream Summary ===
Stream A (W-2):     $D_a declared / $R_a real  (-Q_a%)
Stream B (gig):     $D_b declared / $R_b real  (-Q_b%)
Blended:                              $R_blended

The W-2 pays $R_a real per hour. The gig pays $R_b real per hour.
[Honest descriptive sentence about the gap, no judgment.]
```

### Step 8 — Write output

Write to `~/finances/hourly-wage/YYYY-MM-DD.md` (creating the dir if needed). Schema:

```markdown
---
date: 2026-05-09
mode: remote | hybrid | on-site | gig | mixed
streams: [W-2, side-hustle, ...]
generated-by: /fi:hourly-wage
---

# Real hourly wage — YYYY-MM-DD

## [Stream name]

| | Declared | Total Comp | Real | Delta (decl→real) |
|---|---|---|---|---|
| Hourly wage | $D | $T_h | $R | -$X (-Q%) |
| Annual | $G | $G + $B = $T | $T - $S | -($G - ($T - $S)) |
| Annual hours | N | N | N + M | +M |

### Employer benefits (added to compensation)
| Category | Annual value | % of gross |
|---|---|---|
| Health insurance (employer share) | $X | P% |
| 401(k) match | $X | P% |
| ... | ... | ... |
| **Total benefits** | **$B** | **B/G %** |

### Subtractions (work-attributable costs)
| Category | Amount | % of total comp |
|---|---|---|
| ... | ... | ... |

### Additions (work-attributable hours)
| Category | Hours/year | % of declared |
|---|---|---|
| ... | ... | ... |

### User-declared custom categories
- ...

### Equity / unvested compensation (tracked separately, not in math)
- [List any RSUs/options the user wanted to track as optionality but not include in real-hourly math]

## [Next stream, if multi-stream]

...

## Blended summary
- Real blended wage: $R/hr
- Notes: ...

## Trend (auto-populated on subsequent runs)
| Date | Mode | Real hourly | Delta from prior |
|---|---|---|---|
| YYYY-MM-DD | mode | $R | first run |
```

Subsequent runs:
- Read prior `hourly-wage/*.md` files
- Append a row to the Trend table at the bottom of the latest run
- Don't modify prior files (each run is a snapshot)

### Step 9 — Closing + cross-skill nudge

Show:

> *"Saved to ~/finances/hourly-wage/[date].md. The number is what it is — descriptive, not prescriptive. A few useful next steps if any of this surprised you:*
>
> - *`/fi:three-questions` — walk your spending categories with the real hourly wage as anchor: was that $50 dinner worth W hours of life energy? Does it pass the values check?*
> - *`/fi:redirect` — if the wage is much lower than you thought, the surplus you have to redirect is also smaller than you thought. Re-do the deployment math.*
> - *`/fi:fu-money-readout` — runway shifts when real income shifts. Re-pull.*
>
> *Re-run me quarterly, or after any major work-mode change (new job, RTO mandate, going freelance, etc.) — the math drifts as the line items shift."*

---

## Output schema

### `~/finances/hourly-wage/YYYY-MM-DD.md`

(Per Step 8 above. Front-matter declares mode + streams; tables show subtractions, additions, deltas; Trend section at bottom auto-grows.)

### `~/finances/profile/hourly-wage-custom-categories.md` (persistent)

```markdown
# User-declared custom categories — hourly wage

| Category | Side (subtract / add) | Default amount | Notes |
|---|---|---|---|
| [User category] | subtract | $X/year | [user note about why] |
| [User category] | add | N hr/week | [user note about why] |
```

Read at start of subsequent runs; offer each as a known prompt rather than re-asking from scratch.

---

## Tone and reporting style

The skill is matter-of-fact, not preachy. The number is the number. Don't moralize about whether the wage is too low or too high — that's the user's call. The output gives them a number they can think with; the values check is `/fi:three-questions`'s job.

Common scenarios where the user has a strong reaction to their number:

- *"That's much lower than I thought."* — Acknowledge calmly. The shock is the consciousness-raising. Surface "context anchors" (X hours per dinner, Y hours per car) without prescribing.
- *"This makes my job feel pointless."* — Reframe as data: the number tells them what their time is worth right now in this configuration; it doesn't say anything about whether the work is meaningful. Two different conversations.
- *"This means I should quit."* — Wrong skill for that decision. Point them at `/fi:three-questions` (values check) and `/fi:fu-money-readout` (runway check) before any quit decision.

The skill describes; it does not direct.

---

## Headless behavior

Not generally headless — the line-item walkthrough requires user input. Two partial-headless modes possible:

1. **Refresh-only mode**: re-runs against the user's most recent answers (from prior dated wage file + persisted custom categories), refreshes only AI/SaaS OpEx, equipment refresh, and any line items the user marked "use track-flow data" for. Outputs an updated dated file. Useful for monthly trend without full re-walk.
2. **Manifest mode** (planned): user provides a YAML manifest of all line items; skill computes and writes output without prompts.

Full interactive walkthrough remains the default and the recommended path for first runs and after major work-mode changes.

---

## Why this matters

A 2026 fully-remote consultant who runs YMOYL's classic-only calc gets a flattering number — no commuting subtraction, work clothes near zero, work meals minimal. The number reads high. But the modern line items (AI/SaaS OpEx, home utilities work-portion, blurred-boundary hours) often more than replace what 1992-office-worker line items used to cost. The honest 2026 number is often **lower than the YMOYL-1992-only calc would suggest** for remote workers — and equally honest for hybrid and on-site workers because the classic items still apply.

That honesty across all work modes is the whole point.

The skill also catches a particular failure mode common to gig workers: counting only billable hours and forgetting the unpaid sales / admin / continuing-ed time. A consultant pulling $200/hr who only books 25 billable hours/week but actually puts in 50 hours/week is making $100/hr real, not $200/hr. The blended view per stream makes that visible.

---

## TODO

- [ ] Validate against multiple users in different work modes — refine line-item lists based on what's missed
- [ ] Country-aware tax differential rules (US: SE tax; UK: NI; etc.)
- [ ] Worked examples for each work mode in `examples/`
- [ ] Output format: SVG / PDF version for printing / sharing with a partner
- [ ] Integration with `/fi:track-flow` — auto-pull last-12-months actuals for transportation / restaurants-work-meals / subscription-AI categories rather than asking the user to estimate
- [ ] "Marginal hour" mode — what's the real hourly wage of the *next* hour you work overtime, given fixed costs are already paid?
- [ ] "Quitting math" mode — what real hourly wage would make this stream worth keeping vs not? (Threshold mode for users considering whether to drop a stream.)

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2 — real hourly wage formula. The structural insight (subtract every cost incurred because of the job; add every hour spent because of the job; divide) is durable. The 1992 line-item list assumed an office commuter; the 2018 revision didn't update the line-item list to reflect remote work realities.
- **Marika Olson** (2026). Mode-aware branching, AI/SaaS OpEx as a load-bearing 2026 line item, blurred-boundary hours, multi-stream split, dated-output trend tracking, "for context" anchors using user's actual recent purchases.
