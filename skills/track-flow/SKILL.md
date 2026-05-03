---
name: track-flow
description: The unified flow skill — captures money in + money out from aggregator data or manual walkthrough, classifies by source-type and bucket (personal vs business), categorizes against canonical names + preserves user-specific discretionary categories, handles multi-currency, tabulates per-month rollups, surfaces patterns neutrally (no values judgment — that's /fi:three-questions). Idempotent re-runs support weekly+ cadence.
layer: concept+pattern
ymoyl_step: 2+3
mode_aware: false
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 2b — track every dollar (no rounding); Step 3 — monthly tabulation by category. Combined here because in 2026 multi-currency multi-stream reality, capture and tabulation share the same user invocation (drop CSV, get tab) — splitting them was overengineering."
  - book: Profit First (Mike Michalowicz)
    contribution: "Sub-account allocation pattern — operational checking, tax reserves, profit pool. Categorization rules respect the sub-account purposes (pass-through vs reserve vs profit) when a user is running this architecture."
  - author: Marika Olson
    contribution: "2026 design refinements surfaced by running the skill end-to-end on real aggregator data: phantom-paycheck filter, account-purpose interrogation, mixed-purpose vendor reclassification, income source-type split, Profit First sub-account architecture recognition."
last-reviewed: 2026-05-03
---

# /fi:track-flow

The unified data layer. Captures money flow (in + out), classifies it by source-type and bucket, categorizes it, tabulates it monthly, surfaces patterns. Output feeds `/fi:fu-money-readout`, `/fi:hourly-wage`, `/fi:three-questions`, `/fi:wallchart`, `/fi:crossover`, `/fi:redirect`. Without this skill running, most of the suite has no current data.

---

## The concept (decades-stable)

Every dollar in and out, no rounding, no estimating. YMOYL Step 2b is firm: partial tracking produces partial consciousness. The discomfort of capturing everything (including embarrassing or inconsistent purchases) is the point. Step 3 then aggregates the captured data into category rollups so patterns become visible.

In 2026 reality, capture and aggregation happen in one user action — user exports CSV from aggregator once a week or once a month, drops it in, gets the tabulated output. Splitting those into two skills is friction for no reason.

**The hard problem isn't the math; it's the classification.** Aggregators systematically mis-categorize: family transfers tagged as Shopping; savings-account drawdowns tagged as Paychecks; business OpEx mixed with personal; investment redemptions and refunds counted as income. The skill's load-bearing work is *getting the classifications honest enough that the rollups tell the truth.*

---

## The pattern (~5-year stable)

Single skill, monthly-or-weekly cadence, idempotent re-runs. User invokes; skill ingests latest data, refreshes the current month's output, updates the rolling trend file. Re-running mid-month overwrites/refreshes the current month's row (with `complete: false` flag). Re-running after month-end produces the final stable row.

Three layers of classification, applied in order:
1. **Bucket** (personal / business-moc / business-sy / business-rb / internal-flow) — answers "whose money is this?"
2. **Source-type** (wage / family-support / side-hustle / investment-cash / investment-reinvest / refund / one-time / NOT-cashflow) — answers "what kind of cashflow event is this?"
3. **Canonical category** (housing / transportation / food / etc., or user-discretionary verbatim) — answers "what was it for?"

---

## What the skill does at runtime

### Step 1 — Ingest

Ask the user:

> *"Got data? Three paths:*
> - *Aggregator export — Monarch, Copilot, Tiller, Empower, plain bank CSV. Drop the file path or paste contents.*
> - *Interactive walkthrough — for capturing transactions you can recall from memory or receipts.*
> - *Both — start with what you have, walk through the rest interactively."*

For aggregator CSVs, auto-detect format by header row. Common shapes:

| Aggregator | Key columns |
|---|---|
| Monarch | Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner |
| Copilot | Date, Description, Category, Amount, Account, Currency |
| Tiller | Date, Description, Category, Amount, Account, Tags |
| Empower / Personal Capital | Date, Description, Category, Account, Amount |
| Plain bank CSV | Map heuristically by header |

If ambiguous, ask which aggregator the export came from.

#### Regime-change cutoff (optional)

> *"Is there a regime-change boundary in your data — moved cities, changed jobs, divorce, kids, retirement, RIF, recovery start — that means older data shouldn't be aggregated with newer? If yes, what's the cutoff date?"*

Mixing regimes pollutes the trend analysis. Pre-RIF DC-area expenses don't belong in the same average as post-RIF cabin life. Default behavior: process all data; user can name a cutoff to filter.

### Step 2 — Account-purpose interrogation

After ingest, before classification, ask the user about each account in the data. Common specialist account types:

> *"Looking at the accounts in your data, are any of them specialist accounts I should know about?"*
>
> - *Business operational (main checking for the business)*
> - *Tax pass-through (sales tax collected on behalf of states, employer payroll-tax reserves) — principal isn't yours, interest may be*
> - *Tax reserve set-asides (federal estimated, state quarterly) — your money but earmarked for an obligation*
> - *Profit pool (e.g., Profit First allocations) — your money, set-aside for owner draw*
> - *Trust / custodial / fiduciary — managing for someone else*
> - *Joint / shared — co-owned with partner / family*
> - *Foreign — different tax treatment*
> - *HSA / FSA — tax-advantaged but restricted-use*
> - *Reserve / sinking fund — emergency, CD ladder, specific savings goal*

User declares per-account roles. Skill applies bucket and treatment rules accordingly. The Profit First architecture (one main + multiple sub-accounts: federal taxes / B&O tax / sales tax / profit pool) is a common pattern; handle each sub-account per its declared purpose.

Also ask:

> *"Are there any accounts that AREN'T in this data that we should add or know about?"*
> - *Accounts whose aggregator connection is broken (TSP, foreign, niche fintech)*
> - *Old / forgotten accounts (savings bonds, custodial, ESOPs, prior-employer 401k, that Robinhood you haven't logged into in years)*
> - *Accounts intentionally not connected (paper-only, cash boxes)*
> - *Brand new accounts opened recently*
> - *Accounts your aggregator can't reach (small credit unions, fintech that doesn't expose data)*

### Step 3 — "Everything flowing" interrogation

After CSV import (or before walkthrough), surface what aggregators systematically miss:

- **Cash flow**: cash income (tips, side gigs, farmer's market sales, cash gifts), cash expenses (in-person spending not on a card)
- **Recurring family / partner support**: monthly transfers from parents, parental subsidies, partner contributions, ongoing financial support framed as "loans"
- **Platform-held balances and informal income**: Poshmark / eBay / Mercari / Etsy / Substack tips / Patreon balances; informal off-platform side hustles
- **Non-cash value flow**: bartering / in-kind exchange (capture even without dollar valuation — *spiritual-vibe-only* exchanges are real life-energy)
- **Missed accounts/channels**: Venmo / Cash App / Zelle / PayPal flows; reimbursements; loans in/out
- **Forgotten/dormant accounts**: surfaced in Step 2 above
- **One-time / annual flows**: tax refunds, bonuses, RSU vesting, insurance reimbursements, settlements, lump-sum gifts received
- **Time-bound government benefits**: UI, severance, disability, COBRA subsidies — capture amount + end date

Capture as monthly-equivalent. Documenting "considered and zero" is honest data.

### Step 4 — Currency handling

Ask: *"What's your base currency? Are all transactions in this currency, or do you have transactions in multiple currencies?"*

For multi-currency users:
- Tag every transaction with its native currency
- FX-at-read-time: convert non-base currencies to base using current ECB rate (`api.frankfurter.dev`); never trust frozen aggregator conversions
- Frontmatter declares `base-currency` and `currencies-present`
- Summary lines report in base-currency with footnote noting FX conversion

### Step 5 — Bucket assignment

Apply in this order. **Category overrides account.** User declarations override defaults.

1. **Internal-flow detection** — tag as `__internal_flow__` and exclude from cashflow math:
   - Aggregator's "Transfer" category
   - Aggregator's "Credit Card Payment" category
   - **Phantom-paycheck filter**: aggregator-tagged "Paychecks" rows where merchant is a known savings institution (Ally, Marcus, Capital One 360, etc.) OR statement contains "P2P" / "$TRANSFER" / "TRANSFER" markers. These are savings-account drawdowns the user set up as recurring auto-transfers; aggregators frequently mis-tag them as paychecks. Without the filter, savings drawdowns inflate "personal income" by their full annual amount, producing wrong cashflow numbers downstream.

2. **Business-category override** — if category is a known business category (Tech Stack, Business Expenses, SaaS subscriptions, etc.), bucket = business regardless of which card paid for it. A business-software subscription on a personal credit card still tags as business.

3. **Account-routing rules** (user-declared) — fall through to account-based bucket:
   - Business operational accounts → business
   - STR / rental property accounts → business-rental
   - Personal cards / personal checking / personal savings → personal
   - Investment accounts (brokerage / IRA / HSA / 529) → personal-investment

4. **User-intentional override preservation** — when a user manually re-tags a row in their aggregator (e.g., putting a family transfer into Shopping for their own balance-the-category reason), honor the override in the source data view. The skill produces TWO views of mixed-categorization rows:
   - **User-tagged view** — what the user literally has. Used by `/fi:three-questions` because values-fit work runs against the user's actual mental categorization.
   - **Canonical view** — auto-mapped to honest source-type. Used by `/fi:fu-money-readout` and `/fi:crossover` because their math needs structurally-honest cashflow numbers.

### Step 6 — Categorize

**Auto-map aggregator categories to canonical core**:

| Canonical | Maps from (examples) |
|---|---|
| housing | Mortgage, Rent, Rent & Utilities, HOA |
| transportation | Auto & Transport, Gas, Parking & Tolls, Auto Maintenance |
| food | Groceries, Restaurants & Bars, Coffee Shops, Food & Dining |
| healthcare | Health & Fitness, Medical, Pharmacy, Dentist, Health Insurance |
| utilities | Bills & Utilities, Internet, Phone, Electric, Water, Garbage, US Phone |
| insurance | Insurance, Auto Insurance, Renters Insurance |
| taxes | Taxes, Tax Payments, Federal Estimated, State Quarterly |

**Preserve discretionary categories verbatim**: aggregator's "Hobbies" stays "Hobbies"; "Movies" stays "Movies"; "Horses" stays "Horses"; user's project-specific tags stay. No forced normalization on discretionary — different users have different texture in their lives, and the texture matters for `/fi:three-questions` later.

**Mixed-purpose vendor reclassification**: vendors that sell across categories (Walmart, Amazon, Costco, Target) are tagged inconsistently by aggregators. Ask the user upfront:

> *"Walmart / Amazon / Costco / Target sell across multiple categories. Aggregators tag them inconsistently. Tell me your default for each:*
> - *Walmart → mostly Groceries? mostly Shopping? other?*
> - *Amazon → mostly Shopping? mostly Electronics? mixed?*
> - *etc."*

User declares one default per mixed-purpose vendor. Skill auto-reclassifies on import. Most users have a 70-80% / 20-30% split for these vendors; the dominant-category default catches the bulk pattern, and the drift averages into noise.

**User verification step**: render the proposed mapping, ask *"these look right?"* Wave-through if yes; point-corrections if no.

### Step 7 — Income source-type classification

Critical for honest cashflow rollups. Tag every positive-amount row with one of these source-types (NOT mutually exclusive with category — orthogonal axis):

| Source-type | Definition | Active cashflow? | Yield event? |
|---|---|---|---|
| **wage** | Paycheck-shaped income — UI, severance, W-2 payroll, employer bonuses | ✓ yes | n/a |
| **family-support** | Recurring transfers from family members (mom, dad, partner, parents-in-law) | ✓ yes | n/a |
| **side-hustle** | Informal / platform / sporadic income — Poshmark, Etsy, Substack tips, gig work | ✓ yes | n/a |
| **investment-cash** | Investment income paid as cash — HYSA interest, money-market interest, dividends paid to checking, REIT distributions to cash | ✓ yes | ✓ yes |
| **investment-yield-realized** | Investment income or principal redemption realized as a transaction — index-fund dividends, REIT distributions, eREIT redemptions, stock dividend events. **Counts as yield income** even when auto-redeployed; the redemption represents potential cashflow the user could redirect to checking by toggling reinvest off. | ⚠️ depends on redeployment (paired event below) | ✓ yes — meaningful for retirement-income modeling |
| **investment-redeployment** | The reinvest leg of a yield event — same-day same-amount share-purchase or eREIT-buy following a yield-realized row. Marker, not income; pairs with `investment-yield-realized` to compute *net cashflow from investments.* | ❌ no — redirects yield away from cash | n/a |
| **refund** | Reversal of a prior expense — flight refund, return credit, insurance reimbursement, vendor adjustment. Should reduce the original expense, NOT count as income. | ❌ no | n/a |
| **one-time-large** | Single large events not part of recurring pattern — severance lump sum, inheritance, settlement, RSU vesting, sale of major asset. Flag explicitly so they don't distort monthly averages. | ✓ yes (but flag as one-time) | n/a |

**Two views of investment income, both honest:**

- **Gross investment yield** = sum of (`investment-cash` + `investment-yield-realized`) — what your portfolio generated this month. This is the *retirement-income capacity* number — what could flow to cash if the user toggled auto-reinvest off. Useful for `/fi:fu-money-readout` runway / passive-income / "you could live off this" framing.
- **Net investment cashflow** = `investment-cash` + (`investment-yield-realized` − `investment-redeployment`) — what actually hit available cash. Useful for current-month spending coverage math.

**Auto-reinvest / redeployment pair detection**: for each investment-bucket account, scan for same-day same-amount yield-event/buy-event pairs. The yield row stays as `investment-yield-realized` (counts as gross yield); the buy row gets tagged `investment-redeployment`. Both are visible in the data; they net to zero in the *net cashflow* view but stay separate in the *gross yield* view. Most modern brokerages auto-reinvest by default; this is the common case.

**Active cashflow income** = sum of (wage + family-support + side-hustle + investment-cash + investment-yield-realized − investment-redeployment + one-time-large), NOT including refund (those reverse the original expense).

**The retirement-income lens** = sum of (investment-cash + investment-yield-realized) — *"what your portfolio is generating per month, regardless of whether you're currently living off it."*

**Why both views matter**: a user with substantial investment yield that's auto-redeploying might look "low income" on the active-cashflow view but be sitting on meaningful retirement capacity. The gross-yield view answers *"what could the portfolio support if I needed it to?"* — relevant for `/fi:fu-money-readout`'s passive-income / runway / Coast-FI framing. The active-cashflow view answers *"can I cover this month's expenses with cash?"* — relevant for current-month spending coverage.

### Step 8 — Tabulate

Compute per-month rollups:

- **Personal cashflow**: real income (per Step 7 source-type) - real expenses (excluding refunds since they reduce the original expense)
- **Business cashflow**: business income - business expenses (per bucket)
- **Combined month-closed-at**: personal net + business net
- Per-category total (in base currency)
- Per-category transaction count, expense count, top expense vendor (NOT top vendor weighted by absolute amount — that biases toward income rows)
- **Mixed-sign categories**: when a category has both expense rows AND income/refund rows (e.g., Shopping with a $1K family transfer mis-tagged), report expenses separately from income/refund and flag in a Note column
- Recurring vs one-time split (recurring = same vendor + similar amount in 3+ months)
- Currency mix (% of category that was non-base-currency, if any)

### Step 9 — Pattern detection (neutral; no judgment)

Surface patterns descriptively. The skill **describes**; it does not **judge**. Judgment lives in `/fi:three-questions`.

Patterns worth flagging:

- **Top-vendor concentration**: "95% of food category went to vendor X" — surfaces when one vendor dominates a category. Computed against expense-side rows only.
- **Subscription stack**: "7 active streaming subscriptions totaling $112/mo" — counts recurring services in any one functional class (streaming, software, news, fitness, etc.)
- **Trend anomaly**: "Healthcare spending up 40% vs 6-month avg" — flags categories that drift significantly from baseline median
- **Recurring discovery**: "First time seeing $X to vendor Y this month — recurring or one-off?" — surfaces new patterns for user awareness
- **One-time income anomaly**: positive-amount rows >3x median monthly income — flag for user confirmation that they're one-time (severance, inheritance, etc.) and shouldn't pollute monthly averages
- **Refund pairing**: refund-shaped rows that may correspond to a prior expense — skill prompts *"This refund from [vendor]: which prior expense does it reverse?"* and the user pairs them.
- **Investment redemption**: `[Sell]` category rows in investment accounts — flag as `investment-yield-realized` (counts as yield), then check for same-day buy events that pair as `investment-redeployment`. Surface BOTH views in the readout: gross yield (retirement-income capacity) + net cashflow (what's actually hitting available cash)
- **Phantom-paycheck candidate**: aggregator-tagged Paychecks rows from savings-institution merchants — confirm with user before excluding from income
- **Transfer disambiguation**: aggregator-tagged Transfer rows where merchant suggests an outbound payment (IRS, state Dept of Revenue, etc.) — these may be real expenses, not internal moves

After computing patterns, ask:

> *"Patterns detected: [N]. Surface them now or save for /fi:three-questions?"*

User picks:
- **Show now** — patterns rendered in chat at end of skill run
- **Save** — patterns written to monthly MD output but not rendered; `/fi:three-questions` reads them later
- **Skip** — patterns computed but not surfaced anywhere

Default: save (respects energy; patterns are still in the output file when wanted).

### Step 10 — Write outputs

Five artifacts. **Idempotent**: re-running mid-month overwrites/refreshes the current month's row.

```
~/finances/transactions/YYYY-MM.csv             # Clean per-row transactions
~/finances/monthly-tabs/YYYY-MM.md              # Human readout per month
~/finances/monthly-tabs/_trend-categories.csv   # Month × category × stats (for /fi:wallchart)
~/finances/monthly-tabs/_trend-totals.csv       # Month × {personal/business income+expense+net} (for /fi:crossover)
~/finances/monthly-tabs/_patterns-detected.md   # Cumulative pattern log (for /fi:three-questions)
```

Trend files use `complete: true|false` column so consumers can filter on stable months only if they want.

### Step 11 — Closing

Show:
- Where the files are
- This month's headlines: real cashflow income / expenses / net (from Step 7's honest definition)
- Month-closed-at combined net (personal + business)
- Currency mix (if multi-currency)
- "Patterns are saved in [path] — run `/fi:three-questions` when ready to walk through values-fit"
- "Net worth (with market moves on holdings) lives in `holdings.md` — this skill is cashflow-only"
- "Run me again next week / month with the new data; I'll refresh in place"

---

## Output schemas

### `transactions/YYYY-MM.csv`

```
date,amount_native,currency,amount_base,description,category_imported,category_canonical,account,vendor,bucket,source_type,recurring_flag
2026-04-12,-87.34,USD,-87.34,<grocery store>,Groceries,food,<personal checking>,<grocery vendor>,personal,,recurring
2026-04-15,-29.99,USD,-29.99,<streaming service>,Entertainment,subscription-streaming,<personal credit card>,<streaming vendor>,personal,,recurring
2026-04-01,250.00,USD,250.00,Zelle from family,Other Income,income-other,<personal checking>,<family member>,personal,family-support,recurring
2026-04-30,500.00,USD,500.00,Investment redemption,Sell,sell,<brokerage>,<investment vendor>,personal-investment,investment-yield-realized,
```

### `monthly-tabs/YYYY-MM.md`

```markdown
---
month: 2026-04
base-currency: USD
currencies-present: [USD]
generated-by: /fi:track-flow
complete: true
patterns-detected: 4
---

# Monthly tab — YYYY-MM

## This month

| | |
|---|---|
| Personal active cashflow income   | $X |
| Personal expenses                 | -$Y |
| **Personal net (cashflow)**       | **$Z** |
| Business net                      | $A (accumulating in business account) |
| **Month closed at**               | **$B combined cashflow net** |

*Cashflow only. Net worth (with market moves on holdings) lives in `holdings.md`. Refunds reverse original expenses, not counted as income — see source-type breakdown below.*

## Personal income by source-type

| Source-type | Amount | Active cashflow? | Yield event? |
|---|---|---|---|
| wage | $X | ✓ | n/a |
| family-support | $X | ✓ | n/a |
| side-hustle | $X | ✓ | n/a |
| investment-cash | $X | ✓ | ✓ |
| investment-yield-realized | $X | (paired with redeployment below) | ✓ |
| investment-redeployment | -$X | (offsets above) | n/a |
| refund | $X | ❌ reverses prior expense | n/a |
| **Active cashflow income** | **$Y** | | |
| **Gross investment yield (capacity)** | **$Z** | | |

## Personal expenses by category (descending)

| Category | Expenses | Txns | Top vendor | Note |
|---|---|---|---|---|
| housing | $-X | N | <vendor> | |
| ... | | | | |

## Business breakdown

| | |
|---|---|
| Business income   | $X |
| Business expenses | -$Y |
| **Business net**  | **$Z** |

## Patterns (saved for /fi:three-questions)
- ...
```

### `monthly-tabs/_trend-categories.csv`

```
month,category,bucket,total,transaction_count,top_vendor,top_vendor_share,recurring_count,one_time_count,complete
2026-04,housing,personal,-1500.00,1,<vendor>,1.00,1,0,true
2026-04,food,personal,-450.00,8,<vendor>,0.62,3,5,true
...
```

### `monthly-tabs/_trend-totals.csv`

```
month,personal_real_income,personal_expense,personal_net,business_income,business_expense,business_net,complete
2026-04,X.XX,-X.XX,X.XX,X.XX,-X.XX,X.XX,true
2026-05,...,...,...,...,...,...,partial
```

---

## Idempotent re-runs

The skill is designed to be re-run as often as the user wants. Common patterns:

- **Weekly users**: drop a fresh week's worth of transactions, skill refreshes current month's row with `complete: false`
- **Monthly users**: run on the 1st, finalize prior month with `complete: true`
- **Mid-cycle review**: run any time mid-month for a current snapshot; row gets `complete: false`

When re-running, the skill:
1. Detects the months covered by the input data
2. For each affected month, REPLACES the row in trend files (no duplicates, no append-only)
3. Rewrites the monthly MD for any affected month
4. Updates the transactions CSV for any affected month

User never has to think about "did I already run this?" — the skill handles it.

---

## Headless behavior

Supports headless invocation when:
- Aggregator export file path is provided via env var or flag
- Currency assumptions are pre-set in user profile
- Account-purpose declarations and mixed-purpose-vendor defaults are in user profile (no interactive prompts)
- Pattern detection defaults to "save" (no interactive prompt)

For interactive walkthrough mode (manual capture, account interrogation, vendor-default setup), headless is not supported — fail loudly with a clear error.

---

## Validation

The skill has been end-to-end-validated against real aggregator data on a multi-stream multi-currency user with a Profit-First-architected business. Each design point in this SKILL.md was surfaced by friction in the actual run — phantom-paycheck filtering, mixed-purpose vendor handling, user-intentional override preservation, mixed-sign category fix, two-view investment yield treatment, refund detection, sub-account architecture recognition.

User-specific test artifacts live on the user's machine in their gitignored finance directory. They do not get published.

**Privacy posture**: this SKILL.md describes the procedure in general terms. User-specific data (account names, dollar amounts, vendor patterns, transaction counts) is never embedded in the public skill files. All user data writes go to gitignored paths on the user's machine.

---

## TODO

- [ ] Aggregator-specific import flows: Monarch / Copilot / Tiller / Empower / plain bank CSV — header detection + column mapping per format.
- [ ] Canonical category taxonomy: country-agnostic core + locale extensions in `references/categories/<COUNTRY>.md`.
- [ ] De-duplication logic for re-imports (transaction IDs from aggregators when available; date+amount+description hash otherwise).
- [ ] Pattern detection thresholds — what counts as "anomaly"? What counts as "recurring"?
- [ ] Currency-conversion audit log per month (which transactions were converted, at what rate, when).
- [ ] Recurring-detection across months — first-month-seen flag, last-month-seen flag for subscriptions ending or starting.
- [ ] Mixed-purpose vendor profile — user-declared defaults stored in `references/user-profile.md` so the skill remembers Walmart=Groceries across runs.
- [ ] Auto-reinvest pair detection — pair-matching algorithm for dividend+buy on same day same account.
- [ ] Refund-pair matching — match inbound refund to specific prior outbound expense by amount + vendor.
- [ ] Account-pair routing rules (e.g., "<savings account> → <checking account> = always internal flow") — declared once, applied forever.
- [ ] Worked example files — write the test artifacts as a permanent reference example in `examples/`.
- [ ] Export-back capability — re-emit user's data in a different format if they want to switch aggregators.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2b (track every dollar) and Step 3 (monthly tabulation by category). Combined here because the 1992 split assumed paper-ledger reality where tracking and tabulating were sequential weekly tasks; in 2026 aggregator-CSV reality they're one invocation.
- **Mike Michalowicz**, *Profit First* (2014). The sub-account allocation pattern (operational / tax reserves / profit pool) is YMOYL-adjacent infrastructure — running the skill on a Profit-First-architected user surfaces that the buckets need to be respected, not collapsed.
- **Marika Olson** (2026). Design refinements surfaced by end-to-end validation on real aggregator data: phantom-paycheck filter, account-purpose interrogation, mixed-purpose vendor reclassification, income source-type split (active cashflow vs investment yield capacity vs refund reversals), Profit First sub-account architecture recognition.
