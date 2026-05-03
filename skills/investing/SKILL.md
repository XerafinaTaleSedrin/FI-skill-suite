---
name: investing
description: Question-asking skill for investment management — walks the user through their actual setup, asks load-bearing questions, runs runtime freshness on rates/limits/platforms.
layer: concept+pattern+tool
ymoyl_step: 9
mode_aware: true
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 9 — managing your finances (foundation; their specific advice is dated). 1992 original prescribed Treasuries-only; 2018 revision added the case for low-cost index funds (VTSAX-class) and SRI-screened options. Treat both editions as concept-layer; runtime freshness pulls current rates and platforms."
  - book: Just Keep Buying
    contribution: "Front-loading vs. dollar-cost averaging; tail-event handling"
  - book: Psychology of Money
    contribution: "Tail-event awareness; behavioral discipline over forecasting"
last-reviewed: 2026-05-01
---

# /fi:investing

The investment-management skill. Deliberately a **question-asking** skill, not an instruction skill. It walks the user through their actual setup, asks the load-bearing questions, runs runtime freshness checks for current rate environment, contribution limits, and platform availability — and helps the user reach their own decisions.

---

## The concept (decades-stable)

Investment management is a behavioral problem, not a stock-picking problem. The load-bearing questions are durable:

- **Do you have an IPS (Investment Policy Statement)?** What does it say about rebalancing triggers?
- **Is your "diversification" real, or are you holding three funds that all hold the same top-30 US large-caps?**
- **Are your tax-advantaged accounts placed correctly relative to your taxable accounts?**
- **What's your behavior under loss?** Have you sold during a drawdown? At what threshold?
- **What's your contribution rate, and is it on autopilot?**
- **What happens to this portfolio if you become unable to manage it?**

The skill surfaces these questions at the user's current setup — it does NOT prescribe specific allocations, specific funds, or specific platforms.

---

## The pattern (~5-year stable)

Walk the user through their real setup (which broker, which accounts, which holdings) → ask the question set → identify gaps → suggest *shapes* of corrective action (not specific tools). Tool-layer guidance lives in `tools/` with explicit `last-reviewed` dates.

---

## What the skill does at runtime

1. Reads `holdings.md`. Validates schema.
2. Reads the user's country tax file (`references/tax/<COUNTRY>.md`) for tax-advantaged-account hierarchy.
3. **Runtime freshness check**: pulls current contribution limits (US: 401k, IRA, HSA, FSA; UK: ISA, SIPP, LISA; etc.) from the relevant authoritative source.
4. Walks the user through:
   - IPS check (do you have one? does it cover triggers?)
   - Diversification reality check (overlap analysis across funds)
   - Tax-advantaged placement audit
   - Behavioral history (any panic-sells? any panic-buys?)
   - Contribution-rate audit (auto vs manual; current vs. limit)
   - Continuity plan (if you're hit by a bus, who manages this?)
5. Writes findings to `~/finances/investing-review-YYYY-MM-DD.md`.
6. References tool-register entries by category (e.g., "current low-cost index funds at category X — see tools/index-funds.md") rather than naming specific tickers.

---

## Headless behavior

Not generally headless — interactive walkthrough. The runtime freshness checks could run headlessly (pull current limits, write a snapshot) but the question-asking flow needs a human.

---

## TODO

- [ ] IPS template (in `references/`).
- [ ] Diversification overlap analysis — methodology + tooling.
- [ ] Tax-advantaged placement audit — country-aware.
- [ ] Continuity-plan template.
- [ ] Tool-register entries: index-funds.md, brokerages.md, robo-advisors.md.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 9 — foundational concept; specifics dated.
- **Nick Maggiulli**, *Just Keep Buying* (2022). Front-loading; tail-event responses.
- **Morgan Housel**, *Psychology of Money* (2020). Behavioral discipline.
- **William Bernstein**, *The Four Pillars of Investing* (2002, rev. 2024). Concept depth on diversification and IPS.
