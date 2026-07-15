---
country: United States
country_code: US
last-reviewed: 2026-07-15
contributors:
  - XerafinaTaleSedrin
---

# Tax — United States

> Per-country tax reference. Tool-layer (1-3 year half-life). Update annually OR whenever rates / limits change. The skills in `FI-skill-suite/skills/` read this file structurally — keep the schema intact.

**Runtime-fresh rule (read first).** Every dollar figure below is a dated snapshot, correct as of `last-reviewed` in the frontmatter — and by design it goes stale. Per AGENTS.md §Runtime freshness, a skill reading this file MUST verify the current tax year's values at runtime (WebFetch against the named authoritative source, or ask the user) rather than trusting the baked numbers. The structure (account types, access rules, placement hierarchy) is the durable content; the numbers are illustrations of that structure. Annual limits are announced by the IRS each fall (typically October–November) for the following tax year — a figure read in January may already be one announcement behind this file.

---

## Account types

Tax-advantaged account types available in the US, with the current-year snapshot. Verify limits against the IRS's annual cost-of-living-adjustment announcement (irs.gov, "retirement topics — contribution limits") before using in a calculation.

- **401(k) / 403(b) — tax-deferred (Roth variants: tax-free)** — employee deferral $24,500 (2026); catch-up $8,000 at age 50+; enhanced catch-up $11,250 at ages 60–63 (SECURE 2.0). High earners (prior-year wages above an indexed threshold, ~$150K) must make catch-up contributions as Roth. Penalty-free withdrawal at 59½ (see Early-access rules for exceptions); RMDs at 73 (rising to 75 in 2033) — Roth 401(k) balances no longer have RMDs.
- **457(b), governmental — tax-deferred** — same deferral limit as 401(k), tracked separately (a user with both can defer to both). Distinctive: **no 10% early-withdrawal penalty after separation from the employer, at any age** — disproportionately useful for early retirees bridging to 59½.
- **TSP (federal employees / uniformed services)** — the federal 401(k) equivalent; same limits and catch-up rules.
- **Traditional IRA — tax-deferred** — $7,500 (2026); catch-up $1,100 at age 50+. Deduction phases out when the contributor (or spouse) is covered by a workplace plan — fetch the current-year phase-out thresholds at runtime; do not bake them.
- **Roth IRA — tax-free** — shares the IRA limit with Traditional. Direct contributions phase out above an income threshold (fetch current-year MAGI thresholds at runtime). Contributions (not earnings) withdrawable anytime, tax- and penalty-free. Conversions carry a 5-year seasoning rule per conversion. The "backdoor Roth" (non-deductible Trad contribution → conversion) remains viable under current law; the pro-rata rule applies if the user holds pre-tax IRA balances.
- **HSA — triple-tax-advantaged** (deductible in, tax-free growth, tax-free out for medical) — $4,400 self-only / $8,750 family (2026); catch-up $1,000 at age 55. Requires an HSA-qualified high-deductible health plan. Non-medical withdrawals before 65: ordinary income + 20% penalty; at 65+: ordinary income only (works like a Trad IRA). Verify: IRS revenue procedure announced each May for the following year.
- **FSA (health) — pre-tax, use-it-or-lose-it** — $3,400 (2026); small carryover permitted. Not an investment account; relevant only to the expense side.
- **529 — education, tax-free for qualified use** — state-sponsored; contribution limits set per state (high); many states offer a state-tax deduction. Limited lifetime rollover path to the beneficiary's Roth IRA (SECURE 2.0; $35K lifetime cap, account-age and other conditions apply).
- **Taxable brokerage — taxable** — no contribution limits, no access restrictions. Long-term capital gains treatment on holdings held >1 year. The foundation of bridge capital (Tier 1 below).

---

## Early-access rules (bridge years)

Maps US account types onto the accessibility tiers `/fi:crossover` uses for bridge-capital math (Tier 1 fully accessible → Tier 4 fully restricted). These are structural rules (pattern-adjacent — they change on legislation, not annually), but verify anything load-bearing before a user acts on it.

- **Tier 1 — fully accessible**: taxable brokerage, checking, savings, money market, CDs at maturity.
- **Tier 2 — accessible with a rule**:
  - Roth IRA **contributions** — accessible anytime, any age.
  - Roth **conversions** — accessible 5 tax-years after each conversion (the "Roth conversion ladder" bridge pattern).
  - **Rule of 55** — 401(k)/403(b) distributions penalty-free from the plan of the employer the user separated from in or after the year they turn 55 (50 for certain public-safety employees). Plan must permit partial distributions; does not apply to IRAs.
  - **72(t) SEPP** — substantially-equal periodic payments from any IRA at any age, penalty-free, but locked in for 5 years or until 59½ (whichever is longer); breaking the schedule claws back penalties.
  - **Governmental 457(b)** — penalty-free at any age after separation (see above).
- **Tier 3 — penalty unless age-gated**: Trad IRA, 401(k), TSP, 403(b) before 59½ — 10% penalty + ordinary income tax (limited hardship/exception carve-outs exist; don't plan a bridge on them).
- **Tier 4 — fully restricted**: HSA non-medical before 65 (20% penalty + tax — contributes zero to bridge capital); annuities pre-activation.

---

## Tax on withdrawal (per account type)

What `/fi:crossover` applies as `effective_tax_rate` per bridge year and what `/fi:redirect`'s placement audit reasons from:

- **Taxable brokerage**: long-term capital gains rates on the *gain portion* only (cost basis returns tax-free). Qualified dividends at LTCG rates; interest and non-qualified dividends at ordinary rates.
- **Trad IRA / 401(k) / TSP / 403(b) / governmental 457(b)**: ordinary income tax on the full withdrawal (plus state income tax where applicable).
- **Roth IRA / Roth 401(k)**: zero on contributions; zero on earnings if qualified (5-year rule + 59½); otherwise earnings at ordinary income + 10% penalty.
- **HSA**: zero if medical (any age); see Tier 4 for non-medical.
- **Cash / savings / CDs**: zero withdrawal tax (interest already taxed annually).

---

## Placement hierarchy

Default tax-efficient placement order (general rule of thumb; user-specific situations may differ):

1. **HSA** — the only triple-advantaged type; long-horizon equities if cash flow allows paying medical costs out of pocket.
2. **Tax-deferred (401(k) / Trad IRA / TSP)** — tax-inefficient assets: bond funds, REITs, high-turnover active funds (their ordinary-income drag is sheltered here).
3. **Tax-free (Roth)** — highest-expected-growth assets (small-cap, emerging markets, growth tilts): growth is never taxed.
4. **Taxable** — tax-efficient assets: broad-market index funds (low turnover, qualified dividends), international equity (the foreign tax credit is only claimable in taxable), municipal bonds (already federal-tax-free).

The contribution *order-of-operations* ladder (match → high-rate debt → emergency fund → HSA/IRA/401(k) → taxable) lives in `/fi:redirect` Step 6; this file supplies the account facts that ladder consumes.

---

## Current rates (snapshot — verify at runtime)

- **LTCG rates**: 0% / 15% / 20% by taxable-income bracket. The 0% bracket covers roughly the first ~$49K (single) / ~$99K (married filing jointly) of taxable income (2026 — fetch the exact current-year thresholds from the IRS's annual inflation-adjustment revenue procedure); 20% applies only at high incomes. Bridge-years users with little ordinary income often land partly in the 0% bracket — material to `/fi:crossover`'s net-available math.
- **NIIT**: +3.8% on net investment income above $200K single / $250K MFJ MAGI. These thresholds are **not inflation-indexed** — they quietly capture more filers each year.
- **Ordinary income brackets**: seven brackets, 10%–37% (fetch current-year boundaries at runtime; they move annually with inflation).
- **Estate/gift exemption**: $15M per person (2026, set by the 2025 tax law; indexed thereafter).
- **Mortgage interest deductibility**: interest on up to $750K of acquisition debt is deductible **only if itemizing**. With the standard deduction as large as it is, most filers do NOT itemize — meaning the effective after-tax cost of their mortgage equals its nominal rate. `/fi:redirect`'s after-tax debt-cost step must check "do you actually itemize?" before applying any deductibility discount.
- **State income tax**: 0% (nine states, e.g. FL, TX, WA) up to ~13% (top CA bracket). State tax applies to tax-deferred withdrawals and (in most states) capital gains — ask the user's state; don't assume.
- **Social Security wage base**: $184,500 (2026) — FICA's 6.2% OASDI applies only up to this; relevant to `/fi:hourly-wage` gross-to-net math.

---

## Standard deductions / exemptions

- **Standard deduction**: $16,100 single / $32,200 married filing jointly (2026 — verify current year); additional amounts for 65+ and blind filers.
- **Personal exemption**: N/A (eliminated).
- **Dependent credits**: child tax credit and other dependent credits exist — fetch current values at runtime if a calculation needs them.
- **SALT deduction cap**: $40K (2026; phases down at high incomes; scheduled to change — verify).

---

## Reporting / filing

- **Tax year**: calendar year.
- **Filing deadline**: April 15 (following year), extensions to October 15.
- **Major forms**: 1040 (individual); Schedule B (interest/dividends), D (capital gains), C (sole-proprietor business); 1099-R (retirement distributions); 5498 (IRA contributions); 8889 (HSA).
- **Estimated taxes**: self-employed / untaxed-income filers pay quarterly (April / June / September / January).

---

## Replacement-shape notes

- *If an annual limit changes* (every year, by design): update the numerical values and `last-reviewed`; structure stays.
- *If retirement legislation restructures an account type* (SECURE-style churn — catch-up rules, RMD ages, and Roth treatment have all moved in the last few years): update the affected account-type entry AND re-check the Early-access tier mapping — `/fi:crossover`'s bridge math reads the tiers, not the account names.
- *If the backdoor Roth or a bridge mechanism (Rule of 55, 72(t)) is legislated away*: strip it here and note the date; skills reference these only through this file.
- *If this file's `last-reviewed` is more than 12 months old*: treat every dollar figure as expired; fetch fresh before any calculation (this is also `_last-reviewed.md`'s standing audit rule).

---

## What's NOT in this file

This is not legal or tax advice. The skill suite reads structural facts (account types, limits, hierarchies, access rules) — not "what should I do?" The user consults their actual tax professional for advice. The file's job is to surface the *menu* of options, not to recommend specific moves.

---

## Sources

- IRS annual cost-of-living-adjustment announcements (irs.gov) — retirement plan limits, announced each fall for the following year.
- IRS annual inflation-adjustment revenue procedure (irs.gov) — brackets, standard deduction, LTCG thresholds.
- IRS revenue procedure on HSA limits (irs.gov) — announced each May for the following year.
- SSA (ssa.gov) — Social Security wage base, announced each October.

---

*Reviewed by XerafinaTaleSedrin on 2026-07-15. Schema version: 1.0.*
