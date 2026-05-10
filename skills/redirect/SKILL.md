---
name: redirect
description: Question-asking skill for surplus-cashflow deployment — walks the user through what to do with the dollars freed up by spending audits. Handles both debt paydown and investment management as forms of redirecting surplus. Vehicle-agnostic; runtime-fresh on rates and limits.
layer: concept+pattern+tool
ymoyl_step: 9
mode_aware: true
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 9 — managing your finances (foundation; their specific advice is dated). 1992 original prescribed Treasuries-only; 2018 revision added the case for low-cost index funds (VTSAX-class) and SRI-screened options. The 'redirect' verb itself recurs throughout YMOYL (especially around Steps 4-6 and 9) — the freed-up dollars from the values-fit audit get redirected to debt or investments. Treat both editions as concept-layer; runtime freshness pulls current rates and platforms."
  - book: Just Keep Buying
    contribution: "Front-loading vs. dollar-cost averaging; tail-event handling"
  - book: Psychology of Money
    contribution: "Tail-event awareness; behavioral discipline over forecasting"
  - book: The Four Pillars of Investing (Bernstein)
    contribution: "IPS (Investment Policy Statement) framing; diversification depth"
  - author: Marika Olson
    contribution: "2026 design refinements: behavioral-fit framing for debt-paydown approach (avalanche vs snowball vs equal vs hybrid), country-aware tax-advantaged placement audit, runtime freshness for contribution limits / yields / market rates, integration with /fi:fu-money-readout for surplus identification, integration with /fi:three-questions minus-rated categories as upstream inputs."
last-reviewed: 2026-05-09
---

# /fi:redirect

The deployment skill. Once the upstream skills have surfaced your surplus cashflow (`/fi:track-flow` shows what's coming in and going out, `/fi:fu-money-readout` shows your gap, `/fi:hourly-wage` shows what your work clears, `/fi:three-questions` flags out-of-alignment categories whose freed-up dollars need a destination), this is where you decide where each surplus dollar goes.

The verb is YMOYL's own — Step 5 calls for *redirecting the funds the audit freed up*. The skill covers the full menu of destinations: debt paydown AND investment, weighed against each other, with the user's actual situation as the input. It does NOT prescribe specific allocations, specific funds, specific platforms, or a single "correct" debt-paydown approach. Behavioral fit beats mathematical optimum every time.

---

## The concept (decades-stable)

Surplus capital deployment is a behavioral problem with a math overlay. The math: every dollar of surplus has competing destinations, each with a yield (debt's interest rate is a guaranteed negative return; investment expected return is uncertain positive). Compare the yields, pick the destination. The behavioral problem: which yield-comparison rule the user can actually stick to.

Six durable questions on the investment side, three on the debt side:

**Investment side:**
- Do you have an IPS (Investment Policy Statement)? What does it say about rebalancing triggers?
- Is your "diversification" real, or are you holding three funds that all hold the same top-30 US large-caps?
- Are your tax-advantaged accounts placed correctly relative to your taxable accounts?
- What's your behavior under loss? Have you sold during a drawdown? At what threshold?
- What's your contribution rate, and is it on autopilot?
- What happens to this portfolio if you become unable to manage it?

**Debt side:**
- What rate are you paying on each debt, and what's the after-tax cost? (Mortgage interest deductibility may shift the comparison.)
- Which paydown approach matches your behavior pattern: avalanche, snowball, equal-pay, or hybrid?
- Are there refinance or consolidation opportunities you haven't pursued?

The skill surfaces these questions at the user's actual setup. It does NOT prescribe.

---

## The pattern (~5-year stable)

Walk the user through their real setup (which debts, which broker, which accounts, which holdings) → ask the question set → identify gaps → suggest *shapes* of corrective action (not specific tools). Tool-layer guidance lives in `tools/` with explicit `last-reviewed` dates so it can be refreshed without rewriting the skill.

The unified yield-comparison frame: when a user has surplus capital and competing destinations, the skill helps them compare the guaranteed rate of debt avoidance against the expected rate of investment return — and weigh the behavioral fit of each approach.

---

## What the skill does at runtime

### Step 1 — Read upstream

Required:
- `~/finances/holdings.md` (from `/fi:holdings-scaffold`) — pulls debts (with `rate` + `rate_type`), investment accounts, cash positions, asset-class roll-ups
- `references/tax/<COUNTRY>.md` — for tax-advantaged-account hierarchy, deductibility rules, contribution limits

Optional:
- `~/finances/monthly-tabs/_trend-totals.csv` (from `/fi:track-flow`) — for surplus identification
- `~/finances/fu-money-log/[latest].md` (from `/fi:fu-money-readout`) — for the gap number
- `~/finances/monthly-tabs/YYYY-MM-with-values.md` (from `/fi:three-questions`) — for minus-rated categories whose freed-up dollars are the surplus we're deploying

If `holdings.md` is missing, instruct the user to run `/fi:holdings-scaffold` first and stop.

### Step 2 — Runtime freshness check

Pull current rates from authoritative sources (cache results for 24h to avoid hammering APIs):

- **Treasury yields** (1mo, 3mo, 6mo, 1yr, 2yr, 5yr, 10yr, 30yr) — from US Treasury or equivalent national source
- **HYSA market rates** — top 5 by APY, sourced from a trusted aggregator (Bankrate, NerdWallet, DepositAccounts)
- **Mortgage rates** — current 30-year, 15-year, 5/1 ARM
- **Country-specific contribution limits** (current year):
  - US: 401k ($23K + $7.5K catch-up), IRA ($7K + $1K catch-up), HSA ($4,300 self-only / $8,550 family + $1K catch-up), FSA ($3,300), backdoor Roth process
  - UK: ISA (£20K), SIPP, LISA, pension annual allowance
  - Canada: RRSP, TFSA
  - Other countries: stub for user-declared

Surface stale-data flags if any source can't be fetched: *"Couldn't fetch current Treasury yields; last cached value from [date]. Skill continues with the cached number, flagging for user awareness."*

### Step 3 — Surplus identification

Ask:

> *"How much surplus are we deploying? Three ways to set this number:*
>
> *1. **From `/fi:fu-money-readout`** — your active income minus expenses, monthly. If you ran the readout recently, I have it: [$X/mo].*
>
> *2. **From `/fi:three-questions` minus-rated categories** — the dollars you flagged as out-of-alignment in your last values walk: [$Y/mo] across [N] categories. Read as 'these are dollars I'd cut if I could; they're now surplus.'*
>
> *3. **Manual** — give me a number. Some users prefer to set a deployment target without tying it to a specific source (e.g., 'I want to deploy $1,500/mo regardless of where I pulled it from')."*

Capture the chosen surplus amount and source. Persist in the deployment record.

### Step 4 — Debt-side review

For each debt in `holdings.md`, present:

```
[Debt name]: $[balance] @ [rate]% [rate_type]  →  monthly minimum: $[min]
  After-tax cost: [rate × (1 - marginal_tax_rate)]% if interest is deductible (US mortgage), else same as rate
  Months to payoff at minimum: N
  Months to payoff at minimum + $[surplus]: M
```

Then ask the diagnostic questions:

#### Q1: Refinance / consolidation opportunities

> *"Looking at this debt landscape, are there refinance or consolidation opportunities you haven't pursued?*
> - *Mortgage rate above current market by >0.5pp — refi worth running the math on*
> - *Multiple high-rate credit cards — balance transfer to a 0% intro period could save real money*
> - *Federal student loans — check IDR / PSLF eligibility if you haven't*
> - *Auto loan above current market rate — refi may help"*

For mortgage specifically, surface:

> *"Current 30-year market rate: [X]%. Your mortgage rate: [Y]%. Spread: [Z]pp. Refi-worthwhile threshold is generally 0.5-0.75pp; one-year breakeven on closing costs is typical."*

#### Q2: Paydown approach selection

> *"For the debt you'll prepay (anything beyond minimums), which approach fits your behavior?*
>
> - ***Avalanche** — Pay minimums on all debts; throw extra at highest-rate first. Mathematically optimal. Best for users who are math-motivated and won't lose engagement waiting for the first balance to clear.*
> - ***Snowball** — Pay minimums on all debts; throw extra at smallest-balance first. Emotionally optimal. Best for users who need early wins to maintain engagement; psychological momentum is real and load-bearing.*
> - ***Equal-pay** — Pay extra equally across all debts. Mechanically simple. Best for users who feel paralyzed by 'pick one.'*
> - ***Hybrid** — Avalanche on high-rate (>~10%) debt, snowball on lower-rate. Best for users who want math advantage on the worst debt and psychological wins on the rest.*
>
> *Pick based on behavioral fit, not what's mathematically optimal. Snowball wins for many users because they actually finish; avalanche loses for many users because they quit."*

#### Q3: High-rate debt cap

If any debt is rate >= 10% after-tax, flag explicitly:

> *"You have $[X] in debt at >10% after-tax rates. This is the one debt category where math AND behavior agree: pay it down before everything else (including 401k beyond match, IRA, taxable). The expected return on equity is ~7% real long-term; paying down 18% credit card debt is a guaranteed 18% return. There's no honest investment thesis that beats it."*

This is the only place the skill is directive. High-rate debt is the universal exception.

### Step 5 — Investment-side review

#### Q1: IPS (Investment Policy Statement)

> *"Do you have a written IPS — a one-page document describing your asset allocation, rebalancing rules, and behavior thresholds? It's the single highest-leverage thing on the investment side. If you don't have one, we can scaffold a draft as part of this skill (see `references/ips-template.md`)."*

If user has one, ask: *"What does it say about rebalancing triggers? When did you last review it?"*

If user doesn't, offer to scaffold:

```
Draft IPS — [User Name] — [Date]

Goal: [e.g., Fund retirement starting age 65; portfolio should support $X/mo at 4% SWR]
Time horizon: [e.g., 25 years to retirement, then 35-year drawdown horizon]
Risk tolerance: [Low / Moderate / High — describe what you've actually done in past drawdowns, not aspirational]

Asset allocation target:
  - Stocks: X% (US: A%, International: B%)
  - Bonds: Y%
  - Cash / equivalents: Z%
  - Real estate / REIT: W%
  - Alternative / specialty: V%

Rebalancing triggers:
  - Calendar-based: rebalance every [Q quarters / annually]
  - Threshold-based: rebalance any asset class >5pp away from target

Behavior thresholds:
  - I will not sell during a drawdown of less than [X]% peak-to-trough (commitment to ride out normal volatility)
  - I will reassess (NOT necessarily sell) if drawdown exceeds [Y]% — consult IPS, run /fi:redirect again

Continuity:
  - Primary point of contact for portfolio: [self / financial advisor]
  - Backup point of contact if I'm incapacitated: [name + relationship]
  - Beneficiaries on file at: [list institutions]
```

Walk the user through filling this. Persist to `~/finances/profile/ips.md` (gitignored).

#### Q2: Diversification reality check

Many users hold 3-5 "different" funds that all track the same underlying index. Methodology:

For each equity holding, identify the underlying benchmark (S&P 500, Total US Stock Market, MSCI EAFE, etc.). Look up the top-10 holdings via:
- ETF database (etf.com / portfolio visualizer / fund prospectus)
- Cached data in `references/funds/<TICKER>.md` (last-reviewed dated)

Compute weighted overlap:

```
For each pair of held funds (A, B):
  shared_weight = sum over top-N holdings: min(weight_in_A, weight_in_B)
```

Flag pairs with >70% overlap as redundant. Examples:
- VTI + VTSAX: 99% overlap (same index, different wrappers — fine to consolidate)
- VOO + SPY + IVV: 99% overlap with each other (S&P 500 across providers — pick one)
- VTSAX + FZROX: ~95% overlap (Total US Stock Market — Vanguard vs Fidelity)
- VTSAX + VFIAX: ~80% overlap (Total Market vs S&P 500 — adds 20% small/mid cap exposure)
- VTSAX + VFTAX: ~85% overlap (FTSE Social Index is screened-out version of Total Market)

Surface findings:

> *"Diversification check: of your [N] equity holdings totaling [$X], overlap analysis suggests [you have meaningful diversification / you're effectively holding [Y]% in essentially the same fund]. Specifically: [pair-by-pair findings]."*

The skill does NOT prescribe consolidation. It surfaces the picture. Some users intentionally hold multiple wrappers for tax reasons (avoiding wash-sale rules during tax-loss harvesting).

#### Q3: Tax-advantaged placement audit

Apply asset-location best practices for the user's country (US default; other countries via `references/tax/<COUNTRY>.md`):

US default rules:
- **Tax-inefficient assets** (high turnover, ordinary income generating) → tax-advantaged accounts:
  - Bond funds
  - REITs (high yield, ordinary income)
  - Active equity funds with high turnover
- **Tax-efficient assets** → taxable accounts:
  - Total-market index funds (low turnover, qualified dividends)
  - International equity (foreign tax credit captured in taxable)
  - Municipal bonds (already tax-free)
- **Roth** preferentially for highest-expected-return assets (small-cap, emerging markets, growth tilt) because Roth growth is tax-free

Walk the user's holdings:

```
[Account]                | [Holding]      | Asset class       | Placement assessment
Roth IRA                 | VTSAX          | Total US equity   | OK (could prefer small-cap here)
Traditional IRA          | VBTLX          | US bonds          | OK (bonds in tax-deferred = correct)
Taxable brokerage        | VBTLX          | US bonds          | ⚠ misplaced — bonds in taxable = ordinary-income tax drag
HSA                      | VFIAX          | US large equity   | OK (HSA = triple-tax-advantaged, equities for long horizon)
```

Flag misplacements with specific suggestions (e.g., "consider swapping VBTLX in taxable for a tax-efficient equivalent or relocating to Traditional IRA"). The skill names asset classes and tax-treatment rules; it does NOT prescribe specific ticker swaps.

#### Q4: Behavior-under-loss check

> *"What's your behavior under loss? Have you sold during a drawdown? At what threshold did the urge start?*
>
> - *Never sold during a drawdown — 'just kept buying.' (Strong signal — your IPS can carry higher equity allocation.)*
> - *Sold something during 2022 drawdown / 2020 COVID drop — what fraction of the portfolio?*
> - *Have not been through a real drawdown yet ('I started investing in 2023 / 2024'). Honest answer: 'I don't know.' (Means current allocation is untested — don't take it as confirmed risk tolerance.)*"*

Capture honestly. The user's claimed risk tolerance is less informative than their behavior in past drawdowns.

#### Q5: Contribution rate audit

> *"What's your current contribution rate per account, and is it on autopilot?*
> - *401(k): $X/mo, automatic via payroll*
> - *IRA: $X/mo, automatic transfer / annual lump / sporadic*
> - *Taxable: $X/mo, automatic transfer / sporadic*
>
> *Goal: as much as possible on autopilot. Sporadic contributions tend to under-fund vs intent."*

Compare to current-year contribution limits (from Step 2 freshness check). Surface gaps:

> *"You're contributing $X/yr to your IRA. The 2026 limit is $7,000 ($8,000 if 50+). Gap: $Y. Worth automating the rest? At 8% expected return, that gap costs you ~$Z over the next 10 years compounded."*

The "cost of the gap" framing is grounding. Most users underestimate how much the marginal contribution matters over a decade.

#### Q6: Continuity plan

> *"What happens to this portfolio if you become unable to manage it?*
> - *Primary contact / spouse who knows where everything is*
> - *Beneficiaries on file at every institution (these override your will — make sure they're current)*
> - *Estate plan / trust / will status*
> - *Document for the surviving partner / executor: where everything lives, login info (in a password manager they can access), contacts at each institution"*

This is the question most users skip. The skill surfaces it because it's load-bearing infrastructure.

### Step 6 — Order-of-operations heuristic

For users who want a default deployment ordering, walk through the standard ladder. Most personal-finance literature converges on:

1. **Minimum payments on all debts** (avoid late fees / credit damage)
2. **High-rate debt** (>10% after-tax — credit cards, payday loans)
3. **Employer match on retirement accounts** (free money; capture before anything else)
4. **Emergency fund** (3-6 months expenses; HYSA or money market)
5. **Tax-advantaged accounts** (HSA → IRA → 401k beyond match → backdoor Roth where applicable)
6. **Moderate-rate debt** (student loans, mortgage above current market; trade off vs. expected investment return)
7. **Taxable brokerage** (after tax-advantaged is maxed)
8. **Low-rate debt** (mortgage at sub-market rates — often *not* a paydown priority because the spread between mortgage rate and HYSA/investment yield favors holding cash)

Walk through where the user currently is in the ladder:

> *"At step [N] of the ladder. The next dollar you deploy belongs to [step N+1]. Surplus available: $X/mo. At that rate, you finish step [N+1] in approximately [M] months."*

Country variants live in `references/tax/<COUNTRY>.md`. Ask the user's country in Step 1; load relevant rules.

### Step 7 — Yield comparison summary

Show the unified yield-comparison view:

```
=== Yield comparison — [Date] ===

Guaranteed (debt avoidance):
  Credit card $X       @ 22.0% after-tax    [PAY THIS FIRST — universal]
  Auto loan    $Y      @  6.5% after-tax
  Student loan $Z      @  4.5% after-tax
  Mortgage     $W      @  3.0% after-tax    [keep — sub-market]

Available cash yields:
  HYSA market rate: 4.4% APY (top 5 sources: ...)
  6-month T-Bill:   4.5% APY
  12-month CD:      4.6% APY

Expected investment return (long-term, gross):
  Equity (US total market): ~7% real / 9-10% nominal (historical 1928-2024 avg, sequence-of-returns risk applies)
  Bonds (intermediate Treasury): ~2% real / 4-5% nominal (current yield-to-maturity)
  60/40 blend: ~5% real / 7-8% nominal

Tax-advantaged headroom:
  401k: $X remaining vs limit
  IRA: $Y remaining vs limit
  HSA: $Z remaining vs limit
```

Rates updated [today] from [sources].

### Step 8 — Write the deployment plan

Combine everything into `~/finances/redirect-review-YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
generated-by: /fi:redirect
country: US
surplus-monthly: $X
surplus-source: fu-money-readout | three-questions | manual
ips-status: present | drafted-this-session | absent
---

# Redirect review — YYYY-MM-DD

## Surplus
$X/mo deploying. Source: [readout / values check / manual].

## Debt landscape
[per-debt table with rates, after-tax costs, paydown approach]

## Investment landscape
- Total taxable: $X
- Total tax-advantaged: $Y (Roth $A, Traditional $B, HSA $C)
- Cash position: $Z
- Asset allocation: [actual %s vs IPS target]

## Diagnostics
- IPS status: [present / drafted this session / absent — recommend drafting]
- Diversification overlap: [findings]
- Tax-advantaged placement: [misplacements found]
- Behavior under loss: [user-stated]
- Contribution autopilot: [gaps]
- Continuity plan: [gaps]

## Yield comparison snapshot
[per Step 7 table]

## Recommended deployment for next $X/mo

Based on the ladder + your specific debt rates + tax-advantaged headroom:

1. [Specific shape — e.g., "$200/mo to credit card minimum + $300/mo extra at avalanche-highest"]
2. [Next priority — e.g., "$500/mo to backdoor Roth contribution"]
3. [Next priority]
...

## Open questions for the user
- ...

## Refresh cadence
Re-run after major changes (new debt, new income, sold investments, RIF, raise, life event). Default cadence quarterly.
```

### Step 9 — Closing

Show:

> *"Saved to ~/finances/redirect-review-[date].md.*
>
> *The yield-comparison snapshot is a moment-in-time read; rates move. Re-run me if any of these shift materially:*
> - *Mortgage rate environment moves >0.5pp from your rate*
> - *Tax-advantaged limits update (annually, January)*
> - *You take on new debt or pay one off*
> - *You change jobs / lose a stream / start a new stream*
> - *You go through a life event that changes risk tolerance (kid, illness, inheritance, divorce)*
>
> *Cross-skill: if /fi:three-questions surfaced new minus-rated categories, the freed-up dollars from those need a destination — re-run me with the new surplus number."*

---

## Output schema

### `~/finances/redirect-review-YYYY-MM-DD.md`

(Per Step 8. Frontmatter declares date, source country, surplus number + source, IPS status. Body has debt landscape, investment landscape, diagnostics, yield comparison, recommended deployment shape, open questions.)

### `~/finances/profile/ips.md` (persistent)

User's Investment Policy Statement, scaffolded by the skill if absent. Read by future runs.

### `references/funds/<TICKER>.md` (persistent, repo-shipped)

Per-fund reference data: top holdings, expense ratio, asset class, last-reviewed date. Used for diversification overlap analysis.

### `references/tax/<COUNTRY>.md` (persistent, repo-shipped)

Country-specific contribution limits, deductibility rules, tax-advantaged hierarchy, ladder variant.

---

## Tone and posture

The skill is question-asking, not directive. The only universal directive is "pay down >10% after-tax debt before anything else" (universal because the math AND behavior agree there's no investment thesis that beats it).

Otherwise, the skill surfaces shapes of action and asks the user to choose:

- "You have $X surplus and Y options" — not "you should do Z."
- "Here are the four debt-paydown approaches and what fits which behavior pattern" — not "use avalanche."
- "Your tax-advantaged placement looks suboptimal in these specific ways" — not "swap these tickers."

The reason: the user's behavioral fit is the load-bearing variable. A mathematically-optimal deployment plan that the user can't stick to is worse than a slightly-suboptimal plan that they actually execute. Snowball wins for many users; the skill respects that.

Common reactions:

- *"Just tell me what to do."* — Acknowledge the request, restate why the skill doesn't: behavioral fit varies; the user is the only one who knows what they'll actually do. Offer to walk through the comparison more slowly if helpful.
- *"My financial advisor handles all this."* — Great. The skill is a check on the advisor: are they walking these same questions with you? Is the IPS written? When was the last placement audit? Use the skill to evaluate the advisor's work.
- *"I have no idea what any of this means."* — Slow down. Most users don't have an IPS. Most users don't know their asset allocation. Most users have never run a placement audit. Start with one question (highest-rate debt or IPS draft), come back later for the rest.

---

## Headless behavior

Not generally headless — interactive walkthrough. Two partial-headless modes:

1. **Refresh-rates-only** — pulls current Treasury yields, HYSA rates, mortgage rates, contribution limits, writes a snapshot to `~/finances/redirect-rates-[date].md`. Useful as a cron-fired weekly refresh that the next interactive run reads from.
2. **Manifest-driven deployment** — for users with stable IPS + stable debt landscape, accept a YAML manifest declaring surplus + deployment-plan shape, write the deployment record without prompts. Planned but not built.

Full interactive walkthrough remains the recommended path for first runs and after major life events.

---

## Why this matters

Most personal-finance content treats deployment as a math problem. It's a behavioral problem with a math overlay. The math gives you a deployment shape; the behavior tells you whether you'll execute it.

The skill is structured to surface both layers: the yield-comparison math (Step 7) is the math layer; the IPS / diversification / placement / behavior / autopilot / continuity questions (Step 5) are the behavioral layer. A deployment plan that scores well on math but the user can't stick to is a worse deployment plan than one that scores slightly worse on math but the user actually executes.

The high-rate-debt exception (>10% after-tax) is the only universal directive because that's the only place the math is unambiguously dominant: 18% guaranteed return on debt avoidance > any honest expected return on equity.

For users with multiple income streams + multiple accounts + multiple debts, the unified yield-comparison frame is also the unifying simplification: every dollar of surplus has competing destinations; the skill helps you see them all on the same comparison axis.

---

## TODO

- [ ] IPS template (in `references/`) — refine based on user testing
- [ ] Per-fund reference data files — automate updates from prospectuses or fund pages
- [ ] Diversification overlap calculation — implement weighted-overlap methodology cleanly; accept user-supplied top-10 holdings if reference file missing
- [ ] Country-aware tax rules — US is default; UK / Canada / Australia / EU as next priorities
- [ ] Continuity-plan template (in `references/`)
- [ ] Tool-register entries: index-funds.md, brokerages.md, robo-advisors.md, debt-payoff-calculators.md
- [ ] Decision tree for "this dollar to debt or to investment" given user's specific debt-rate landscape and investment expected-return assumption
- [ ] Worked examples for each debt-paydown approach
- [ ] Integration with `/fi:three-questions` — auto-pull minus-rated categories as surplus source
- [ ] Cross-skill: surplus changes across runs (track-flow shows new pattern, three-questions flags new minus-rated category) should trigger a redirect refresh prompt
- [ ] Behavioral-fit assessment refinement — the four debt-paydown approaches map to behavioral patterns; document which questions reliably distinguish them
- [ ] Tax-loss harvesting walkthrough — separate sub-skill or section here?

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 9 (managing your finances) — foundational concept; specifics dated. The 'redirect' verb recurs throughout — the freed-up dollars from the values-fit audit (Steps 4-6) get redirected to debt or investments (Step 9).
- **Nick Maggiulli**, *Just Keep Buying* (2022). Front-loading; tail-event responses; the case for automated contributions over market timing.
- **Morgan Housel**, *The Psychology of Money* (2020). Behavioral discipline over forecasting. The argument that being "reasonable" is more useful than being "rational" — load-bearing for the behavioral-fit framing.
- **William Bernstein**, *The Four Pillars of Investing* (2002, rev. 2024). Concept depth on diversification and IPS; the original case for asset allocation as the dominant determinant of returns.
- **Burton Malkiel**, *A Random Walk Down Wall Street* (1973, multiple editions). Index-fund case; market-efficiency framing.
- **Dave Ramsey** / popular-finance debt literature — snowball method origin and behavioral case for it.
- **Bill Bengen** (1994) and the **Trinity Study** (Cooley, Hubbard & Walz, 1998). Safe withdrawal rate baseline (4%, configurable).
- **Marika Olson** (2026). Behavioral-fit framing for debt-paydown approach (avalanche vs snowball vs equal vs hybrid), country-aware tax-advantaged placement audit, runtime freshness for contribution limits / yields / market rates, integration with `/fi:fu-money-readout` for surplus identification, integration with `/fi:three-questions` minus-rated categories as upstream inputs, the universal high-rate-debt exception (>10% after-tax) as the only directive in an otherwise question-asking skill.
