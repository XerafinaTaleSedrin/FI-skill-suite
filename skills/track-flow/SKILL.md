---
name: track-flow
description: The unified flow skill — captures money in + money out from aggregator data or manual walkthrough, categorizes against canonical names + preserves user-specific discretionary categories, handles multi-currency, tabulates per-month rollups, surfaces patterns neutrally (no values judgment — that's /fi:three-questions). Idempotent re-runs support weekly+ cadence.
layer: concept+pattern
ymoyl_step: 2+3
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 2b — track every dollar (no rounding); Step 3 — monthly tabulation by category. Combined here because in 2026 multi-currency multi-stream reality, capture and tabulation share the same user invocation (drop CSV, get tab) — splitting them was overengineering."
last-reviewed: 2026-05-03
---

# /fi:track-flow

The unified data layer. Captures money flow (in + out), categorizes it, tabulates it monthly, surfaces patterns. Output feeds `/fi:fu-money-readout`, `/fi:hourly-wage`, `/fi:three-questions`, `/fi:wallchart`, `/fi:crossover`, `/fi:redirect`. Without this skill running, most of the suite has no current data.

---

## The concept (decades-stable)

Every dollar in and out, no rounding, no estimating. YMOYL Step 2b is firm: partial tracking produces partial consciousness. The discomfort of capturing everything (including embarrassing or inconsistent purchases) is the point. Step 3 then aggregates the captured data into category rollups so patterns become visible.

In 2026 reality, capture and aggregation happen in one user action — user exports CSV from aggregator once a week or once a month, drops it in, gets the tabulated output. Splitting those into two skills is friction for no reason.

---

## The pattern (~5-year stable)

Single skill, monthly-or-weekly cadence, idempotent re-runs. User invokes; skill ingests latest data, refreshes the current month's output, updates the rolling trend file. Re-running mid-month overwrites/refreshes the current month's row (with `complete: false` flag). Re-running after month-end produces the final stable row.

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
| Monarch | Date, Merchant, Category, Account, Amount, Notes |
| Copilot | Date, Description, Category, Amount, Account, Currency |
| Tiller | Date, Description, Category, Amount, Account, Tags |
| Empower / Personal Capital | Date, Description, Category, Account, Amount |
| Plain bank CSV | Map heuristically by header |

If ambiguous, ask which aggregator the export came from.

### Step 2 — "Everything flowing" interrogation

After CSV import (or before walkthrough), surface what aggregators systematically miss:

- **Cash flow**: cash income (tips, side gigs, farmer's market sales, cash gifts), cash expenses (in-person spending not on a card)
- **Recurring family / partner support**: monthly transfers from parents, parental subsidies, partner contributions, ongoing financial support framed as "loans"
- **Platform-held balances and informal income**: Poshmark / eBay / Mercari / Etsy / Substack tips / Patreon balances; informal off-platform side hustles
- **Non-cash value flow**: bartering / in-kind exchange (capture even without dollar valuation — *spiritual-vibe-only* exchanges are real life-energy)
- **Missed accounts/channels**: Venmo / Cash App / Zelle / PayPal flows; old or foreign accounts; reimbursements; loans in/out
- **Forgotten/dormant accounts**: old TSP/401k from previous job, ESOPs, foreign accounts, custodial accounts
- **One-time / annual flows**: tax refunds, bonuses, RSU vesting, insurance reimbursements, settlements, lump-sum gifts received
- **Time-bound government benefits**: UI, severance, disability, COBRA subsidies — capture amount + end date

Capture as monthly-equivalent. Documenting "considered and zero" is honest data.

### Step 3 — Currency handling

Ask: *"What's your base currency? Are all transactions in this currency, or do you have transactions in multiple currencies?"*

For multi-currency users:
- Tag every transaction with its native currency
- FX-at-read-time: convert non-base currencies to base using current ECB rate (`api.frankfurter.dev`); never trust frozen aggregator conversions
- Frontmatter declares `base-currency` and `currencies-present`
- Summary lines report in base-currency with footnote noting FX conversion

### Step 4 — Categorize

**Auto-map aggregator categories to canonical core**:

| Canonical | Maps from (examples) |
|---|---|
| housing | Auto/Transport > Rent, Housing, Mortgage, Rent & Utilities |
| transportation | Auto & Transport, Transportation, Auto, Gas |
| food | Food & Dining, Groceries, Restaurants, Coffee Shops |
| healthcare | Health & Fitness, Medical, Pharmacy, Doctor |
| utilities | Bills & Utilities, Internet, Phone, Electric |
| debt-service | Loan Payment, Credit Card Payment, Student Loans |
| insurance | Insurance, Health Insurance, Auto Insurance |
| taxes | Taxes, Tax Payments |

**Preserve discretionary categories verbatim**: aggregator's "Hobbies" stays "Hobbies"; "Movies" stays "Movies"; "Horses" stays "Horses." No forced normalization on discretionary — different users have different texture in their lives, and the texture matters for `/fi:three-questions` later.

**User verification step**: render the proposed mapping, ask *"these look right?"* Wave-through if yes; point-corrections if no.

### Step 5 — Tabulate

Compute per-month rollups:

- Total income (sum of inflow rows)
- Total expenses (sum of outflow rows, including housing-and-utilities-and-debt as well as discretionary)
- Net (income - expenses)
- Per-category total (in base currency)
- Per-category transaction count
- Top vendor per category (by spend)
- Recurring vs one-time split (recurring = same vendor + similar amount in 3+ consecutive months)
- Currency mix (% of category that was non-base-currency, if any)

### Step 6 — Pattern detection (neutral; no judgment)

Surface patterns descriptively. The skill **describes**; it does not **judge**. Judgment lives in `/fi:three-questions`.

Patterns worth flagging:

- **Top-vendor concentration**: "95% of food category went to vendor X" — surfaces when one vendor dominates a category
- **Subscription stack**: "7 active streaming subscriptions totaling $112/mo" — counts recurring services in any one functional class (streaming, software, news, fitness, etc.)
- **Trend anomaly**: "Healthcare spending up 40% vs 6-month avg" — flags categories that drift significantly from baseline
- **Recurring discovery**: "First time seeing $X to vendor Y this month — recurring or one-off?" — surfaces new patterns for user awareness

After computing patterns, ask:

> *"Patterns detected: [N]. Surface them now or save for /fi:three-questions?"*

User picks:
- **Show now** — patterns rendered in chat at end of skill run
- **Save** — patterns written to monthly MD output but not rendered; `/fi:three-questions` reads them later
- **Skip** — patterns computed but not surfaced anywhere

Default: save (respects energy; patterns are still in the output file when wanted).

### Step 7 — Write outputs

Three artifacts. **Idempotent**: re-running mid-month overwrites/refreshes the current month's row.

```
~/finances/transactions/YYYY-MM.csv     # Clean per-row transactions
~/finances/monthly-tabs/YYYY-MM.md      # Human readout per month
~/finances/monthly-tabs/_trend-categories.csv  # Month × category × stats (for /fi:wallchart)
~/finances/monthly-tabs/_trend-totals.csv      # Month × {income, expenses, net} (for /fi:crossover)
```

Trend files use `complete: true|false` column so consumers can filter on stable months only if they want.

### Step 8 — Closing

Show:
- Where the files are
- Total income, total expenses, net direction for the month
- Currency mix (if multi-currency)
- "Patterns are saved in [path] — run `/fi:three-questions` when ready to walk through values-fit"
- "Run me again next week / month with the new data; I'll refresh in place"

---

## Output schemas

### `transactions/YYYY-MM.csv`

```
date,amount_native,currency,amount_base,description,category_imported,category_canonical,account,vendor,recurring_flag
2026-04-12,-87.34,USD,-87.34,Trader Joe's,Groceries,food,USAA Checking,Trader Joe's,recurring
2026-04-15,-29.99,USD,-29.99,Netflix,Entertainment,subscription-streaming,Sapphire Reserve,Netflix,recurring
2026-04-20,-200.00,EUR,-234.04,Apartment rent,Housing,housing,Banque Populaire,Landlord,recurring
```

### `monthly-tabs/YYYY-MM.md`

```markdown
---
month: 2026-04
base-currency: USD
currencies-present: [USD, EUR]
fx-rates-as-of: 2026-04-30
complete: true
patterns-detected: 4
---

# Monthly tab — April 2026

## Totals
- Income: $X
- Expenses: $Y
- Net: $Z

## By category (descending)
| Category | Total | Transactions | Top vendor | Recurring | Currency mix |
| ... | | | | | |

## Patterns (saved for /fi:three-questions)
- ...
```

### `monthly-tabs/_trend-categories.csv`

```
month,category,total_base,transaction_count,top_vendor,top_vendor_share,recurring_count,one_time_count,complete
2026-04,housing,1500.00,1,Landlord,1.00,1,0,true
2026-04,food,487.34,12,Trader Joe's,0.62,3,9,true
...
```

### `monthly-tabs/_trend-totals.csv`

```
month,income_base,expenses_base,net_base,complete
2026-04,8500.00,4912.34,3587.66,true
2026-05,8500.00,2156.78,6343.22,false
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
- Pattern detection defaults to "save" (no interactive prompt)

For interactive walkthrough mode (manual capture), headless is not supported — fail loudly with a clear error.

---

## TODO

- [ ] Aggregator-specific import flows: Monarch / Copilot / Tiller / Empower / plain bank CSV — header detection + column mapping per format.
- [ ] Canonical category taxonomy: country-agnostic core + locale extensions in `references/categories/<COUNTRY>.md`.
- [ ] De-duplication logic for re-imports (transaction IDs from aggregators when available; date+amount+description hash otherwise).
- [ ] Pattern detection thresholds — what counts as "anomaly"? What counts as "recurring"?
- [ ] Currency-conversion audit log per month (which transactions were converted, at what rate, when).
- [ ] Recurring-detection across months — first-month-seen flag, last-month-seen flag for subscriptions ending or starting.
- [ ] Worked example: full session run for a multi-currency user with mixed aggregator + manual data.
- [ ] Export-back capability — re-emit user's data in a different format if they want to switch aggregators.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2b (track every dollar) and Step 3 (monthly tabulation by category). Combined here because the 1992 split assumed paper-ledger reality where tracking and tabulating were sequential weekly tasks; in 2026 aggregator-CSV reality they're one invocation.
- **Marika Olson** (2026). The "everything flowing" interrogation pass; multi-currency-aware design; idempotent re-run pattern; pattern-detection neutrality (judgment delayed to `/fi:three-questions`).
