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

Critical for honest cashflow rollups. Tag every positive-amount row (positive amounts only — negatives are expenses or internal) with one of these source-types (orthogonal to category):

| Source-type | Definition | Active cashflow? | Notes |
|---|---|---|---|
| **wage** | Paycheck-shaped income — UI, severance, W-2 payroll, employer bonuses | ✓ yes | apply phantom-paycheck filter first (Step 6 — savings-institution P2P transfers tagged Paychecks reclassify to internal) |
| **family-support** | Recurring transfers from family members (mom, dad, partner, parents-in-law) | ✓ yes | declared markers per user |
| **side-hustle** | Informal / platform / sporadic income — Poshmark, Etsy, Substack tips, gig work | ✓ yes | platform list user-extensible |
| **investment-cash** | Investment income paid as cash to a non-investment account — HYSA interest, money-market interest, dividends paid to checking | ✓ yes | counted in BOTH active cashflow AND gross-yield |
| **refund** | Reversal of a prior expense — flight refund, return credit, insurance reimbursement, vendor adjustment | ❌ no — see cross-period attribution below | reduces in-window expense magnitude only when matched original is in-window |
| **windfall** | Cross-period refund (original expense out-of-window OR unmatched) AND unmatched positive-shape events that don't fit other types — settlements, lump-sum gifts, inheritance, sale of major asset, severance lump sum, etc. | ✓ yes (but flagged as one-time, separate line) | NEVER folded into recurring-baseline; surface as discrete event |
| **business-income** | Income to business buckets (handled separately in business breakdown) | n/a | shown in business section, not personal |

**Investment-account internal flows (default behavior)**

All transactions in investment-bucket accounts (Brokerage, IRA, Roth IRA, Traditional IRA, TSP, 401k, Fundrise, Robinhood, etc.) are **excluded from cashflow income/expense by default**. The auto-reinvest assumption: dividends and yield events round-trip inside the account, principal sales pair with reinvestment buys, no money exits to checking unless explicitly withdrawn. This applies to:

- Interest, Dividends & Capital Gains, Investment Income categories
- Sell rows (whether yield distributions or principal redemptions)
- Buy rows
- Transfer rows
- Retirement Account contributions/sweeps

These rows still contribute to **gross investment yield** (extracted separately, see below) but never to active cashflow.

**User confirmation in Step 2 — account-purpose interrogation:** the skill confirms with the user *"this account auto-reinvests dividends, yes? Or do dividends flow to checking?"* for each investment-bucket account. Default = auto-reinvest. If a user has an account that DOES cash out yield to checking, flip the default; those yield events then count as `investment-cash` for that account.

**Why this matters:** without this rule, every quarterly dividend distribution and every fund rebalance (e.g., consolidating multiple eREIT positions into a single fund) inflates "income" — sometimes by thousands of dollars in a single month. The validation case: a 7-sells-to-1-buy same-day rebalance event totaling ~5K of principal moving sideways inside a Fundrise account looked like ~5K of income until the rule was added.

**Gross investment yield (capacity number, separate from cashflow):**

Compute by scanning all rows (including internal-account ones) for yield-event shape:

- Direct yield categories: Interest, Dividends & Capital Gains, Investment Income (sum |amount| — Monarch sometimes shows in-account yield as negative; absolute value gives the right magnitude)
- Sell rows that are NOT principal redemptions (no "Redemption" or "SOLD" keyword in merchant/statement) — these are realized capital gains
- Vanguard-pattern dividend rows: Transfer category with merchant "Dividend" (positive leg only, to avoid double-counting the reinvest leg)

**Sells that ARE redemptions (merchant/statement contains "Redemption" or "SOLD")**: principal moving between funds within the same account → not yield, not cashflow. If unpaired (no same-day buy in same account), surface as anomaly: *"this looks like a principal withdrawal — did $X exit to checking?"*

**Two views, both honest:**

- **Active cashflow income** = wage + family-support + side-hustle + investment-cash + income-other. Excludes refund (nets to expense), excludes windfall (separate one-time line), excludes investment-account internal flows. Useful for "can I cover this month with recurring income?"
- **Gross investment yield** = sum of yield-event amounts across all accounts. Useful for "what's my portfolio's retirement-income capacity?" — relevant for `/fi:fu-money-readout`, `/fi:crossover`.

**Cross-period refund attribution (rule + user confirmation)**

When a refund-shaped row is detected (positive amount in expense-shaped category), attempt to match against same-merchant negative rows in the prior 12 months across the FULL transaction history (not just the in-window slice). Three outcomes:

| Match outcome | Treatment |
|---|---|
| In-window match (original expense in same tracking window) | Tag as `refund`. Reduces current-month expense magnitude (current behavior). |
| Out-of-window match (original expense pre-tracking) | Reclassify as `windfall`. Does NOT reduce current expense magnitude — surfaces as separate windfall line. |
| No match (no prior same-merchant negative found) | Reclassify as `windfall`, flag for user: *"This positive-amount row from [vendor] looks refund-shaped but I can't find a matching original expense. Refund of an out-of-window purchase, or income event?"* |

**Why this matters:** refunds for purchases made before the tracking window started would otherwise net against unrelated current-month expenses, making the period look artificially cheap. The validation case: a flight cancelation refund of ~2K in April for tickets purchased the previous September would have understated April's actual spending by 40%.

### Step 8 — Tabulate

Compute per-month rollups. Show **gross**, **netting adjustments**, and **windfalls separately** — never collapse into a single hidden number.

- **Active cashflow income** (per Step 7): wage + family-support + side-hustle + investment-cash + income-other
- **Gross expenses**: sum of negative-amount rows in personal bucket (excluding internal-flow rows)
- **In-window refunds**: sum of `refund`-tagged rows (positive, original expense in tracking window) — netted against gross expenses
- **Net expenses (refund-netted)**: gross expenses + in-window refunds
- **Personal net cashflow**: active cashflow income + net expenses
- **Windfall income** (separate line, not folded into recurring baseline): cross-period refunds + unmatched windfall events
- **Gross investment yield (capacity)**: extracted from yield-shape rows in investment accounts (per Step 7)
- **Business cashflow**: business income - business expenses (per bucket)
- **Combined month-closed-at**: personal net + business net + windfalls
- Per-category total (in base currency)
- Per-category transaction count, expense count, top expense vendor (NOT top vendor weighted by absolute amount — that biases toward income rows)
- **Mixed-sign categories**: when a category has both expense rows AND income/refund rows (e.g., Shopping with a 1K family transfer mis-tagged), report expenses separately from income/refund and flag in a Note column
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
- **Refund pairing (cross-period attribution)**: positive-amount rows in expense-shaped categories trigger a full-history scan for same-merchant negatives in the prior 12 months. In-window match → tag as `refund` (nets against current expenses). Out-of-window match OR no match → reclassify as `windfall` AND prompt the user: *"This refund-shaped row from [vendor] for $X: matched original expense from [date], which is outside the tracking window. Treat as windfall (one-time, not recurring), or did I miss something?"*
- **Investment-account anomaly**: investment-bucket accounts default to fully-internal (auto-reinvest assumption). If a Sell row (with "Redemption" or "SOLD" keyword) does NOT pair with a same-day or next-day buy in the same account, flag: *"This redemption of $X from [account] doesn't have a matching reinvestment leg. Did $X exit to checking, or is the buy leg appearing in a different aggregator window?"*
- **Phantom-paycheck candidate**: aggregator-tagged Paychecks rows from savings-institution merchants — confirm with user before excluding from income
- **Transfer disambiguation**: aggregator-tagged Transfer rows where merchant suggests an outbound payment (IRS, state Dept of Revenue, etc.) — these may be real expenses, not internal moves
- **Account-purpose ambiguity**: a positive Interest/Dividend row in a non-investment account (regular checking) — confirm with user: *"Interest paid into your checking account from [source] — yield event, or something else?"*

**The user-confirmation principle:** any anomaly the skill detects but can't resolve confidently — large windfall, unmatched refund, principal sale that may have exited an investment account, account-purpose ambiguity — surface to the user for disambiguation. The skill does not silently assume; it asks.

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
date,amount_native,currency,amount_base,description,category_imported,category_canonical,account,vendor,bucket,is_internal,is_yield,source_type,recurring_flag
2026-04-12,-87.34,USD,-87.34,<grocery store>,Groceries,food,<personal checking>,<grocery vendor>,personal,false,false,,recurring
2026-04-15,-29.99,USD,-29.99,<streaming service>,Entertainment,subscription-streaming,<personal credit card>,<streaming vendor>,personal,false,false,,recurring
2026-04-01,250.00,USD,250.00,Zelle from family,Other Income,income-other,<personal checking>,<family member>,personal,false,false,family-support,recurring
2026-04-30,500.00,USD,500.00,Dividend distribution,Dividends & Capital Gains,income-passive,<brokerage>,<fund vendor>,personal,true,true,,
2026-04-15,1500.00,USD,1500.00,Refund from prior-year purchase,Travel & Vacation,travel-and-vacation,<personal checking>,<travel vendor>,personal,false,false,windfall,
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
| Personal active cashflow income | $X |
| Personal expenses (gross) | -$Y |
| Refunds (in-window, net against expenses) | +$R |
| Personal expenses (net of in-window refunds) | -$Yn |
| **Personal net (cashflow)** | **$Z** |
| Windfall income (cross-period refunds, settlements, etc.) | +$W |
| Business net | $A (accumulating in business account) |
| **Month closed at** | **$B combined (incl. windfalls)** |
| Gross investment yield (capacity) | $G (auto-reinvested in investment accounts) |

*Cashflow only. Net worth (with market moves on holdings) lives in `holdings.md`. Investment-account internal flows (Brokerage/IRA/Roth/TSP/etc. dividends + reinvestments + redemption rebalances) are excluded from cashflow but counted toward gross-yield capacity. Cross-period refunds (original expense outside the tracking window) treated as windfall, not expense reduction.*

## Personal income by source-type

| Source-type | Amount | # txns | Treatment |
|---|---|---|---|
| wage | $X | N | ✓ active cashflow |
| family-support | $X | N | ✓ active cashflow |
| side-hustle | $X | N | ✓ active cashflow |
| investment-cash | $X | N | ✓ active cashflow |
| refund | $X | N | ✗ reverses in-window expense |
| windfall | $X | N | ✗ one-time, separate line |
| **Active cashflow income** | **$Y** | | |
| **Gross investment yield** | **$Z** | | capacity (incl. auto-reinvested) |

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
month,personal_active_income,personal_gross_yield,personal_windfall,personal_expense_gross,personal_refund_in_window,personal_expense,personal_net,business_income,business_expense,business_net,complete
2026-04,X.XX,X.XX,X.XX,-X.XX,X.XX,-X.XX,X.XX,X.XX,-X.XX,X.XX,true
2026-05,...,...,...,...,...,...,...,...,...,...,partial
```

Eleven-column schema gives downstream skills (`/fi:crossover`, `/fi:redirect`, `/fi:fu-money-readout`) access to:
- `personal_active_income` — recurring cashflow baseline (use as crossover-target denominator)
- `personal_gross_yield` — retirement-income capacity (use for "what could the portfolio support?")
- `personal_windfall` — one-time events (exclude from rolling-baseline averages)
- `personal_expense_gross` vs `personal_expense` — see how much is real vs refund-netted
- `personal_refund_in_window` — magnitude of in-period reversals
- `complete: true|false` — partial months flagged so consumers can filter

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

The skill has been end-to-end-validated against real aggregator data on a multi-stream multi-currency user with a Profit-First-architected business. Each design point in this SKILL.md was surfaced by friction in the actual run. Validation pass updates incorporated:

1. **Phantom-paycheck filtering** — savings-institution P2P transfers tagged Paychecks reclassify to internal-flow before source-type classification
2. **Mixed-purpose vendor handling** — vendors used for multiple categories (e.g., big-box stores) default to user-declared dominant category
3. **User-intentional override preservation** — user-tagged categories preserved; canonical category exposed alongside for reporting
4. **Mixed-sign category fix** — categories with both expense and income/refund rows split for honest top-vendor display
5. **Two-view investment yield treatment** — gross yield (capacity) vs active cashflow (recurring) shown separately
6. **Investment-account internal flows** — all transactions in investment-bucket accounts (Brokerage/IRA/Roth/TSP/Fundrise/etc.) excluded from cashflow by default per auto-reinvest assumption; yield events extracted separately for gross-yield capacity
7. **Cross-period refund attribution** — refunds matched against full transaction history (not just in-window). In-window match → expense reversal. Out-of-window or unmatched → reclassified as windfall (separate line, not folded into baseline)
8. **Many-to-one principal-sale rebalance pattern** — fund consolidations (sells of multiple specific positions paired with a single buy of a target position, sum-matched) correctly classified as internal rebalance, not yield
9. **Negative-amount in-account dividend convention** — some aggregators show in-account auto-reinvest dividends as negative-amount Interest rows; absolute-value-based gross-yield extraction handles this
10. **Same-account ±2-day reinvest pair window** — dividend-paid-and-reinvested patterns can span date boundaries (e.g., dividend paid D, reinvested D+1); pair-detection window broadened accordingly
11. **Source-type schema** — wage / family-support / side-hustle / investment-cash / refund / windfall / business-income — orthogonal to category
12. **Sub-account architecture recognition** — Profit First and similar pass-through-bucket architectures recognized; per-sub-account purpose preserved
13. **One-time-large income flagging** — positive-amount months >3× median active income flagged for user confirmation (severance, settlement, down-payment, etc.) so they don't pollute the recurring baseline
14. **User-confirmation principle** — anomalies surface for user disambiguation rather than silent assumption

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
- [x] Auto-reinvest pair detection — replaced by simpler "investment-account = internal by default" rule, validated against real data. Per-account override available via account-purpose interrogation.
- [x] Refund-pair matching — full-history same-merchant scan in prior 12 months; in-window match → refund, else → windfall.
- [ ] Account-pair routing rules (e.g., "<savings account> → <checking account> = always internal flow") — declared once, applied forever.
- [ ] Worked example files — write the test artifacts as a permanent reference example in `examples/`.
- [ ] Export-back capability — re-emit user's data in a different format if they want to switch aggregators.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2b (track every dollar) and Step 3 (monthly tabulation by category). Combined here because the 1992 split assumed paper-ledger reality where tracking and tabulating were sequential weekly tasks; in 2026 aggregator-CSV reality they're one invocation.
- **Mike Michalowicz**, *Profit First* (2014). The sub-account allocation pattern (operational / tax reserves / profit pool) is YMOYL-adjacent infrastructure — running the skill on a Profit-First-architected user surfaces that the buckets need to be respected, not collapsed.
- **Marika Olson** (2026). Design refinements surfaced by end-to-end validation on real aggregator data: phantom-paycheck filter, account-purpose interrogation, mixed-purpose vendor reclassification, income source-type split (active cashflow vs gross investment yield capacity vs refund reversals vs cross-period windfalls), investment-account internal-flow exclusion (auto-reinvest assumption), cross-period refund attribution rule, principal-sale rebalance detection, user-confirmation principle for anomalies, Profit First sub-account architecture recognition.
