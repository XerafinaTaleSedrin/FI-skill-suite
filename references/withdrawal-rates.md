---
name: withdrawal-rates
last-reviewed: 2026-07-20
contributors:
  - XerafinaTaleSedrin
---

# Withdrawal rates — the evidence base

> Shared reference. Concept+pattern layer: the *derivation* of the safe-withdrawal literature (what the numbers mean, what they assume) is decades-stable; the *specific rates and figures* quoted below are tool-layer snapshots, correct as of `last-reviewed`, and go stale. Skills read this file for framing, not for baked constants.

**Runtime-fresh rule (read first).** Per AGENTS.md §Runtime freshness: any skill quoting a specific safe-withdrawal rate, a SAFEMAX figure, or a success-rate percentage must treat the figures below as illustrations of the structure, verify anything load-bearing at runtime (WebFetch against the cited source, or ask the user), and always render rates as sensitivity ranges rather than a single point.

---

## Where 4% comes from — and what kind of number it is

- **Bengen (1994), "Determining Withdrawal Rates Using Historical Data," *Journal of Financial Planning*.** Tested inflation-adjusted withdrawals against every rolling historical retirement cohort (US data, 50–75% stocks, 30-year horizons). The ~4% answer (his worst-case rate, later named "SAFEMAX," was ~4.15%) is the rate that survived the **single worst historical start date** — a late-1968 retiree who hit sequential bear markets plus high inflation. Full paper: <https://www.financialplanningassociation.org/sites/default/files/2021-04/MAR04%20Determining%20Withdrawal%20Rates%20Using%20Historical%20Data.pdf>
- **Trinity study — Cooley, Hubbard & Walz (1998), "Retirement Savings: Choosing a Withdrawal Rate That Is Sustainable," *AAII Journal*.** Tested 3–12% withdrawal rates across five stock/bond mixes, 1926–1995. A 4% inflation-adjusted withdrawal from a 50/50–75/25 portfolio succeeded in ~95–100% of historical 30-year periods; the authors' 2011 update through 2009 held up similarly. Overview: <https://en.wikipedia.org/wiki/Trinity_study>
- **The structural point: 4% is a floor-shaped number.** It was derived from the worst cohort in the historical record. Every other cohort in the same data could have withdrawn more — most of them substantially more. Bengen himself has said as much publicly, and with broader asset diversification has since revised his worst-case SAFEMAX upward (~4.7% in his later work — a tool-layer figure; verify against his current published position before quoting). See <https://www.aaii.com/journal/article/insights-on-using-the-withdrawal-rule-from-its-creator> and <https://www.bengenfs.com/the-4-percent-rule/>
- **Corollary for FI math**: `expenses × 25` (the inverse of 4%) is therefore a *conservative* FI threshold, not a knife-edge. Treating it as the minimum admission price to FI overstates the requirement for most historical outcomes. The honest rendering is a range, which is why `/fi:crossover` runs a sensitivity band instead of a point estimate.

## The static rule's hidden assumption: zero adaptation

- The historical "failure" cases behind the 4% derivation assume a retiree who mechanically increases spending with inflation every year while their portfolio collapses, and never adjusts anything. That is a stress-test assumption, not a description of human behavior.
- **Kitces, "The Ratcheting Safe Withdrawal Rate"** (kitces.com): following the 4% rule historically, the retiree finishes the 30-year horizon with **more than double the starting principal over two-thirds of the time**, and median terminal wealth is roughly **2.8× starting principal** — on top of a lifetime of inflation-adjusted spending. The typical outcome of the static rule is a large surplus, not depletion. <https://www.kitces.com/blog/the-ratcheting-safe-withdrawal-rate-a-more-dominant-version-of-the-4-rule/>
- Read together: the static 4% rule is calibrated to the worst case *and* assumes no adaptation. Both conservatisms stack. The cost of that stacked conservatism is real — extra working years bought against a scenario that rarely materializes, paid for with time that does not come back.

## Dynamic / flexible spending rules

- **Pfau (2015), "Making Sense Out of Variable Spending Strategies for Retirees," *Journal of Financial Planning*.** Surveys the family of variable-spending rules — decision-rule methods (floor-and-ceiling, guardrail-style adjustments) and actuarial methods — and finds that variable strategies reduce sequence-of-returns risk and **allow greater initial spending rates** and a more efficient drawdown than constant inflation-adjusted spending. <https://www.financialplanningassociation.org/article/journal/OCT15-making-sense-out-variable-spending-strategies-retirees>
- **Kitces' ratchet** (same article as above) is the one-sided version: start at 4%, raise spending 10% whenever the portfolio rises 50%+ above its starting value — never requires a cut, and historically dominates the static rule.
- **The conditionality, stated plainly**: a withdrawal rate above the static-safe floor is defensible **only with a pre-committed adjustment rule** — named triggers, named cut sizes — and a spending baseline that can actually absorb the cuts. Flexibility that hasn't been quantified is not flexibility; it's optimism. This is the same discipline as the suite's compute-position-not-target rule: adaptations are position inputs, not vibes.

## The two-number framing: comfortable vs. floor

A position report that carries a single FI number hides decision-relevant information. The evidence above supports carrying two:

- **Comfortable FI number** = `full expense baseline × 25`. Static-rule-safe: survives the worst historical cohort with zero adaptation required. Crossing it means work is optional even if the user never adjusts anything.
- **Floor FI number** = `survival expense baseline × 25`, where the survival baseline is the trimmed budget the user could genuinely sustain (housing, food, health coverage, insurance — the lines that stay when the discretionary lines go). Because a survival baseline typically runs well below the full baseline, the floor number lands materially below the comfortable number — e.g., a survival baseline at 80% of full expenses puts the floor at 20× full expenses. **The floor number is defensible only WITH a dynamic-spending rule and a quantified adaptability inventory** (below). It is a floor with conditions, not a smaller target.
- **The gap between the two numbers is the finding**, not either number alone. The gap prices the user's real options: how much earlier "enough, with flexibility" arrives than "enough, unconditionally" — which is exactly the information needed for a sabbatical decision, a downshift decision, or walking away from a bad situation. Render both; label the conditions on the floor.
- Provenance note: the two-number framing is a suite design synthesis of the verified evidence above (worst-case derivation + terminal-wealth outcomes + variable-spending results). The "20×" figure is illustrative arithmetic from the 80% example, not a research finding — the user's actual floor multiple falls out of their actual survival baseline.

## Adaptability inventory — levers as position inputs

The floor number is only as real as the levers behind it. Each lever counts only when quantified (magnitude + trigger) and only if the user would actually pull it:

- **Spending cut to survival baseline** — which budget lines go, how many dollars/month that releases, and at what portfolio-drawdown trigger the cut fires.
- **Part-time / consulting income** — realistic dollars/month at the user's actual market rate, discounted for how rusty the network gets over time (a lever that decays; note the decay).
- **Relocation / geographic arbitrage** — the honest monthly delta of the cheaper place, and the honest answer to "would you actually move."
- **Purchase deferral** — large lumpy spends in the next five years (vehicle, roof, major travel) that could slide a year or three without harm.
- **Stream-timing levers** — early-reduced vs. waited-full claiming options on pensions and government retirement income. Already modeled structurally by `/fi:crossover`'s two-scenario sensitivity; listed here for completeness of the inventory.

An inventory with two quantified levers supports a floor number; an inventory of "I'd figure something out" supports nothing. Skills reading this file should prompt for magnitude and trigger, and drop unquantified levers from the math.

## Which skills read this

- **`/fi:crossover`** — sensitivity framing (4%-as-floor), the optional comfortable-vs-floor two-number output, and the adaptability-inventory prompt.
- **`/fi:fu-money-readout`** — unchanged; it echoes whatever headline crossover writes.

## Sources

- Bengen, W. (1994). *Determining Withdrawal Rates Using Historical Data.* Journal of Financial Planning. <https://www.financialplanningassociation.org/sites/default/files/2021-04/MAR04%20Determining%20Withdrawal%20Rates%20Using%20Historical%20Data.pdf>
- Cooley, P., Hubbard, C. & Walz, D. (1998). *Retirement Savings: Choosing a Withdrawal Rate That Is Sustainable.* AAII Journal. Overview: <https://en.wikipedia.org/wiki/Trinity_study>
- Pfau, W. (2015). *Making Sense Out of Variable Spending Strategies for Retirees.* Journal of Financial Planning. <https://www.financialplanningassociation.org/article/journal/OCT15-making-sense-out-variable-spending-strategies-retirees>
- Kitces, M. (2015). *The Ratcheting Safe Withdrawal Rate: A More Dominant Version of the 4% Rule.* <https://www.kitces.com/blog/the-ratcheting-safe-withdrawal-rate-a-more-dominant-version-of-the-4-rule/>
- Bengen, W. — current published position on SAFEMAX with broader diversification. <https://www.bengenfs.com/the-4-percent-rule/> and <https://www.aaii.com/journal/article/insights-on-using-the-withdrawal-rule-from-its-creator>
