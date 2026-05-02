---
country: (Full country name)
country_code: (ISO 3166-1 alpha-2, e.g., US, GB, CA, AU)
last-reviewed: YYYY-MM-DD
contributors:
  - (GitHub handle of person who authored / last updated)
---

# Tax — [Country]

> Per-country tax reference. Tool-layer (1-3 year half-life). Update annually OR whenever rates / limits change. The skills in `FI-skill-suite/skills/` read this file structurally — keep the schema below intact.

---

## Account types

List every tax-advantaged account type available in this country. For each:

- **Name**: (e.g., 401(k), IRA, ISA, RRSP)
- **Tax treatment**: tax-deferred / tax-free / taxable / hybrid
- **Annual contribution limit (current year)**: amount + currency
- **Catch-up provision (if any)**: amount and age threshold
- **Withdrawal rules**: penalty-eligible age, RMDs, etc.
- **Common providers**: tool-register reference (e.g., "see tools/brokerages.md")

Example (US, partial):

```
- 401(k) — tax-deferred — $23,500 (2025); $30,500 with catch-up at age 50+; penalty-free withdrawal at 59½; RMDs at 73
- IRA (Trad) — tax-deferred — $7,000 (2025); $8,000 with catch-up at age 50+
- IRA (Roth) — tax-free — same limit as Trad; income phase-out applies
- HSA — triple-tax-advantaged — $4,300 individual / $8,550 family (2025); usable for medical only
- (etc.)
```

---

## Placement hierarchy

Default tax-efficient placement order (general rule of thumb; user-specific situations may differ):

1. **High-priority**: (e.g., HSA — pre-tax + tax-free growth + tax-free medical withdrawals = best account type if available)
2. **Tax-deferred**: (e.g., 401(k), Trad IRA — for assets with regular income / less tax-efficient on their own)
3. **Tax-free**: (e.g., Roth — for highest-growth assets, since growth is never taxed)
4. **Taxable**: (e.g., brokerage — for tax-efficient assets like broad-market index funds with low turnover)

For each, give a one-line "what asset class typically goes here, and why."

---

## Current rates (last-reviewed YYYY-MM-DD)

- **LTCG bracket thresholds**: (e.g., US 2025: 0% up to $48,350 single / $96,700 married)
- **Capital gains tax rates**: short-term, long-term
- **Income tax brackets** (top of, for illustration; full table not needed)
- **Estate tax exemption** (if relevant)
- **Other relevant rates**

---

## Standard deductions / exemptions

- **Standard deduction**: amount
- **Personal exemption**: amount (or N/A if abolished)
- **Dependent allowances**: amount
- **Other major deductions / credits**: brief mention

---

## Reporting / filing

- **Tax year**: (e.g., calendar year, April-March)
- **Filing deadline**: typical date
- **Major forms**: 1040 (US), Self Assessment (UK), T1 (Canada), etc.

---

## Replacement-shape notes

If the structure of a major account type changes (e.g., the UK abolishes ISAs, or the US expands HSA to non-medical), note here what happens to the file:

- *"If [Account Type X] changes structurally: [what to do]."*
- *"If [Limit Y] changes: just update the numerical values; structure stays."*

---

## What's NOT in this file

This is not legal or tax advice. The skill suite reads structural facts (account types, limits, hierarchies) — not "what should I do?" The user consults their actual tax professional for advice. The file's job is to surface the *menu* of options, not to recommend specific moves.

---

## Sources

- (Authoritative source for limits — e.g., IRS.gov, HMRC.gov.uk, CRA.ca)
- (Reference link for any non-obvious claims)

---

*Reviewed by [contributor handle] on YYYY-MM-DD. Schema version: 1.0.*
