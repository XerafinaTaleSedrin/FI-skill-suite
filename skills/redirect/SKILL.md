---
name: redirect
description: Question-asking skill for surplus-cashflow deployment — walks the user through what to do with the dollars freed up by spending audits. Handles both debt paydown and investment management as forms of redirecting surplus. Vehicle-agnostic; runtime-fresh on rates and limits.
layer: concept+pattern+tool
ymoyl_step: 9
mode_aware: true
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 9 — managing your finances (foundation; their specific advice is dated). 1992 original prescribed Treasuries-only; 2018 revision added the case for low-cost index funds (VTSAX-class) and SRI-screened options. The 'redirect' verb itself recurs throughout YMOYL (especially around Steps 4-6 and 9) — the freed-up dollars from the values-fit audit get redirected to debt or investments. Treat both editions as concept-layer; runtime freshness pulls current rates and platforms."
  - book: Just Keep Buying
    contribution: "Front-loading vs. dollar-cost averaging; tail-event handling"
  - book: Psychology of Money
    contribution: "Tail-event awareness; behavioral discipline over forecasting"
last-reviewed: 2026-05-03
---

# /fi:redirect

The deployment skill. Once the upstream skills have surfaced your surplus cashflow (`/fi:track-flow` shows what's coming in and going out, `/fi:fu-money-readout` shows your gap, `/fi:hourly-wage` shows what your work clears), this is where you decide where each surplus dollar goes.

The verb is YMOYL's own — Step 5 calls for *redirecting the funds the audit freed up*. We take that verb literally and make it cover the full menu of destinations: debt paydown AND investment, weighed against each other, with the user's actual situation as the input.

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

The skill surfaces these questions at the user's actual setup. It does NOT prescribe specific allocations, specific funds, specific platforms, or a single "correct" debt-paydown approach.

---

## The pattern (~5-year stable)

Walk the user through their real setup (which debts, which broker, which accounts, which holdings) → ask the question set → identify gaps → suggest *shapes* of corrective action (not specific tools). Tool-layer guidance lives in `tools/` with explicit `last-reviewed` dates.

The unified yield-comparison frame: when a user has surplus capital and competing destinations, the skill helps them compare the guaranteed rate of debt avoidance against the expected rate of investment return — and weigh the behavioral fit of each approach.

---

## What the skill does at runtime

1. **Reads `holdings.md`.** Validates schema. Pulls debts (with `rate` + `rate_type`), investment accounts, cash positions.
2. **Reads the user's country tax file** (`references/tax/<COUNTRY>.md`) for tax-advantaged-account hierarchy and any deductibility rules (e.g., US mortgage interest, retirement-account contribution limits).
3. **Runtime freshness check**: pulls current contribution limits (US: 401k, IRA, HSA, FSA; UK: ISA, SIPP, LISA; etc.), current Treasury yields, current HYSA market rates from authoritative sources.
4. **Walks the user through:**
   - **Surplus identification** — what are we actually deploying? Reads from `/fi:fu-money-readout` if available, otherwise asks.
   - **Debt-side review** — every debt with its rate; flag high-rate debt (typically credit cards >18%) for first-priority paydown regardless of approach.
   - **Debt-paydown approach selection** — avalanche / snowball / equal / hybrid. Skill asks behavioral-fit questions, not "which is mathematically optimal."
   - **Investment-side review** — IPS check, diversification reality check, tax-advantaged placement audit, behavioral-history check, contribution-rate audit, continuity plan.
   - **Order-of-operations heuristic** — high-rate debt → emergency fund → tax-advantaged accounts → taxable. Walks through where the user actually is in that ladder.
5. **Writes findings to** `~/finances/redirect-review-YYYY-MM-DD.md`.
6. **References tool-register entries by category** (e.g., "current low-cost index funds at category X — see tools/index-funds.md") rather than naming specific tickers.

---

## Debt-paydown approaches (the user picks based on behavioral fit)

| Approach | How it works | Best for |
|---|---|---|
| **Avalanche** | Pay minimums on all debts; throw extra at highest-rate first | Users who are math-motivated and won't lose engagement waiting for the first balance to clear |
| **Snowball** | Pay minimums on all debts; throw extra at smallest-balance first | Users who need early wins to maintain engagement; psychological momentum is real and load-bearing |
| **Equal-pay** | Pay extra equally across all debts | Users who feel paralyzed by the "pick one" framing; mechanically simple |
| **Hybrid** | Avalanche on high-rate debt, snowball on lower-rate | Users who want the math advantage on the worst debt and the psychological wins on the rest |

The skill does NOT default to avalanche just because it's mathematically optimal. Snowball wins for many users because they actually finish; avalanche loses for many users because they quit. Behavioral fit is the load-bearing question.

---

## Order-of-operations heuristic (US-default; country-aware)

Most personal-finance literature converges on a rough priority order. The skill walks through where the user is in this ladder:

1. **Minimum payments on all debts** (avoid late fees / credit damage)
2. **High-rate debt** (credit cards, payday loans, anything >~10% after-tax)
3. **Employer match on retirement accounts** (free money; capture before anything else)
4. **Emergency fund** (3-6 months expenses; HYSA or money market)
5. **Tax-advantaged accounts** (HSA → IRA → 401k beyond match → backdoor Roth where applicable)
6. **Moderate-rate debt** (student loans, mortgage above current market; trade off vs. expected investment return)
7. **Taxable brokerage** (after tax-advantaged is maxed)
8. **Low-rate debt** (mortgage at sub-market rates — often *not* a paydown priority because the spread between mortgage rate and HYSA/investment yield favors holding cash)

Country variants live in `references/tax/<COUNTRY>.md`.

---

## Headless behavior

Not generally headless — interactive walkthrough. The runtime freshness checks could run headlessly (pull current limits, write a snapshot) but the question-asking flow needs a human.

---

## TODO

- [ ] IPS template (in `references/`).
- [ ] Diversification overlap analysis — methodology + tooling.
- [ ] Tax-advantaged placement audit — country-aware.
- [ ] Continuity-plan template.
- [ ] Tool-register entries: index-funds.md, brokerages.md, robo-advisors.md, debt-payoff-calculators.md.
- [ ] Decision tree for "this dollar to debt or to investment" given user's specific debt-rate landscape and investment expected-return assumption.
- [ ] Worked examples for each debt-paydown approach.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 9 (managing your finances) — foundational concept; specifics dated. The 'redirect' verb recurs throughout — the freed-up dollars from the values-fit audit (Steps 4-6) get redirected to debt or investments (Step 9).
- **Nick Maggiulli**, *Just Keep Buying* (2022). Front-loading; tail-event responses.
- **Morgan Housel**, *Psychology of Money* (2020). Behavioral discipline.
- **William Bernstein**, *The Four Pillars of Investing* (2002, rev. 2024). Concept depth on diversification and IPS.
- **Dave Ramsey** / popular-finance debt literature — snowball method origin and behavioral case for it.
