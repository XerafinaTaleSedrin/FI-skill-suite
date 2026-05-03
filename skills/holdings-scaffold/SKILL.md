---
name: holdings-scaffold
description: Build the user's local holdings.md file from scratch — every account, every holding, asset-class roll-up, current net worth, with strict gitignore enforcement before any data is written. Use when the user wants to track their net worth, set up a financial inventory, scaffold their finances, build a security-blanket file of what they own, organize scattered accounts, or asks where to keep their financial data. The output file is the gateway artifact every other /fi: skill reads from.
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 1 framing — current net worth as 'making peace with the past'. (YMOYL prescribes a second half — lifetime earnings reconstruction — which this suite deliberately does not implement; see book-audits/2026-05-01-ymoyl.md for reasoning.)"
  - author: Marika Olson
    contribution: "2026 generalization of the holdings-file structure she built for personal use; the FX-at-read-time rule from the Monarch failure case"
last-reviewed: 2026-05-02
---

# /fi:holdings-scaffold

The flagship onboarding skill. Walks the user through populating a `holdings.md` file from scratch, account by account, with privacy enforcement built in. Every other skill in the suite reads from this file; without it, nothing else has data.

---

## When to invoke this skill

**Invoke when** the user says or implies any of:

- *"I want to track my net worth."*
- *"Set up my finances / set up my holdings."*
- *"I have accounts scattered everywhere and I want to consolidate."*
- *"Where should I keep my financial data?"*
- *"How do I figure out what I'm worth?"*
- *"I want a single view of all my accounts."*
- Any request that maps to "build me a security-blanket inventory of what I own."

**This skill handles BOTH fresh builds AND updates.** If the user already has a `holdings.md` file, the skill switches into update mode in Step 1 — same flow, different starting state. There is no separate update skill.

**Do NOT invoke when:**
- The user asks about a specific calculation (real hourly wage, crossover point, monthly tabulation) — those are downstream skills that read from holdings.md after this one has run.
- The user wants stock tips, market timing, or product recommendations (out of scope for the entire FI suite).
- The user wants fund-level placement / diversification analysis — that's `/fi:redirect`. This skill captures account-level data; fund-level detail is layered in later.

---

## The concept (decades-stable)

Knowing what you own is the prerequisite for any conscious financial decision. Most adults don't know — their assets are scattered across employer-managed retirement accounts they barely look at, brokerages with auto-deposits they forgot about, foreign currency holdings, retirement contributions from old jobs, real estate equity they don't track, and debts whose balances are stale. The catch-up framing of YMOYL Step 1 names this honestly: most adults are running their financial lives on partial information.

A consolidated holdings file resolves this — not as a planning tool, but as a security-blanket artifact you can read like a weather report.

---

## The pattern (~5-year stable)

A single, hand-curated, locally-owned markdown file with structured sections per account. **NOT** an auto-aggregated dashboard pulled from a third-party service (those go stale, lose accounts, mis-categorize, and lock you to a vendor). The hand-curated approach means:

- Updates happen on a deliberate cadence (monthly typically), not in real time.
- The file exists offline. No service can take it away.
- Schema is portable — if Claude Code goes away, the markdown still reads.
- Asset-class tagging is user-controlled, not vendor-imposed.

---

## Procedure

When this skill is invoked, execute the following procedure in order. Each step has explicit decision points; don't skip ahead.

### Step 1 — Detect existing file; choose fresh-build vs update mode

Ask the user:

> "Do you already have a holdings file you're trying to update, or are we building one from scratch? If you have one already, share the path."

**Branch on the answer:**

#### 1a. Update mode (existing file)

If an existing `holdings.md` is provided:

1. Read the file. Verify the `holdings-schema-version` matches the current schema (currently `1`). If the version is older, note the diff and migrate the structure as part of the update.
2. Confirm the existing file is gitignored (Step 3 still runs — re-verify, don't assume the prior author got it right).
3. Walk through the existing file with the user:
   - Which accounts have changed balances? (refresh)
   - Which accounts are now stale (last-verified > 30 days)? (refresh or prune)
   - Are there new accounts to add since the last update? (add)
   - Are there closed/old accounts to remove? (prune; note in a removed-accounts comment)
4. Skip Step 2 (file location is already chosen) and Step 4a/4b's bulk-import-vs-walkthrough question (just iterate over what changed). Step 3 still runs. Step 5 (compute roll-ups) and Step 6 (write file) still run.
5. Preserve the file's prior `last-updated` value as a comment at the top, then overwrite with today's date.

#### 1b. Fresh-build mode (no existing file)

Proceed to Step 2.

**One skill, two starting states.** Don't fork into a separate skill for updates — the procedure is the same shape with a different entry point.

### Step 2 — Pick the file location

Suggest two defaults and let the user pick:

- **`~/finances/holdings.md`** — outside any project repo; lives in the user's home directory; suitable when the user wants their financial data fully separate from work projects.
- **`<current-repo>/finances/holdings.md`** — inside the user's currently-active project; suitable when the user is comfortable with one specific repo holding personal data AND that repo is private OR has aggressive `.gitignore` coverage.

If neither fits, accept a custom path. **Do not write the file yet.** Privacy enforcement runs first.

### Step 3 — Enforce no-commit posture (LOAD-BEARING — never skip this)

This is the highest-stakes step in the entire skill. Holdings data is sensitive. Failure to enforce gitignore can result in the user accidentally committing their entire net worth to a public repository.

**Branch on whether the chosen path is inside a git repo:**

#### 3a. Path IS inside a git repo

1. Check whether the path is already covered by `.gitignore`. Use `git check-ignore <path>` if available, or read `.gitignore` and pattern-match manually. Be conservative — if you're not sure the path is covered, treat it as not covered.

2. If NOT already covered: append the necessary patterns to `.gitignore` BEFORE writing any holdings data. Show the user the exact diff:

   ```
   Adding to .gitignore:
   + finances/
   + !finances/.gitkeep
   ```

   Wait for user confirmation before proceeding. If they decline, abort the skill and recommend a different file location.

3. If the file already exists and was previously committed to the repo's history (run `git log --follow -- <path>` to check): warn loudly. Offer to walk them through `git filter-repo` cleanup as a separate task. **Do not write any new data to the file** until the historical exposure is addressed.

4. After gitignore is verified and clean, proceed to Step 4.

#### 3b. Path is NOT inside a git repo

No gitignore enforcement is possible. Instead:

1. Write a "DO NOT COMMIT" warning header at the top of the file, BEFORE any data:

   ```markdown
   <!-- DO NOT COMMIT this file to a public git repository.
        Contains private financial data: account balances, ticker holdings,
        net worth. -->
   ```

2. Verify with the user that this location won't end up in any git repo or cloud-sync folder accidentally. Common pitfalls to flag:
   - The location is inside `~/Dropbox/`, `~/iCloud Drive/`, `~/OneDrive/` → it WILL sync to the cloud
   - The location is inside `~/Documents/` on a Windows machine with OneDrive backup enabled → same problem
   - The location is inside a directory that the user might later turn into a git repo → that future `git init` would expose the file

3. Accept the user's choice (after warning). Proceed to Step 4.

### Step 4 — Populate accounts

For each account the user owns, capture:

| Field | Type | Required? | Notes |
|---|---|---|---|
| `name` | string | yes | Free-form (e.g., "Schwab Brokerage", "TSP", "Banque Populaire EUR") |
| `type` | string (tag) | yes | Free-form tag — DO NOT enumerate. Common US tags: Taxable, Trad-IRA, Roth-IRA, 401k, TSP, HSA, Brokerage, **CD**, Treasury, I-Bond. Common UK tags: ISA, SIPP, LISA. Common Canadian tags: RRSP, TFSA, FHSA. Plus: Foreign, Crypto, Real-Estate, Debt, Cash, Mobile-Payment-System, Other. |
| `balance_native` | number | yes | Current balance in the account's native currency |
| `currency` | ISO-4217 code | yes | e.g., USD, EUR, GBP, CAD. Defaults to user's `base-currency` if unspecified. |
| `rate` | number (% APY/APR) | optional but recommended for cash + liabilities + time-locked instruments | Yield earned (cash/savings/CD) or interest paid (debt). e.g., HYSA at 4.50% APY, mortgage at 3.65% APR, 12-month CD at 4.75% APY. Skip for investment accounts where return is variable. |
| `rate_type` | string | when rate is set | One of: `APY-fixed`, `APY-variable`, `APR-fixed`, `APR-variable`, `intro-rate`. CDs and Treasuries are typically `APY-fixed` for the term. |
| `maturity_date` | YYYY-MM-DD | required for CDs / Treasuries / I-Bonds | When the time-locked instrument matures and principal becomes accessible. Critical for cash-flow planning and ladder strategies. |
| `term` | string | optional, helpful for CDs / Treasuries | Original term length (e.g., `3-month`, `12-month`, `5-year`). Helps the user reason about ladder structures. |
| `ladder_role` | string | optional | If this account is part of a laddered strategy (CD ladder, Treasury ladder), name the ladder (e.g., `RB-12mo-CD-ladder-month-1`) so the skill can roll up ladder-level positions. |
| `holdings` | list | optional (deferred to `/fi:redirect`) | If the account has discrete holdings (stocks, funds, etc.), capture each: ticker, shares, native price-per-share, asset-class tag. Most users won't have this on first run. |
| `last_updated` | YYYY-MM-DD | yes | When the user last verified this balance |

**Why capture `rate`:** knowing the spread between what cash earns and what debt costs is foundational for downstream skills. A user with $50k in a 0.01% checking account and a 24% credit card balance is leaking money in a way the net-worth number alone doesn't surface. `/fi:fu-money-readout` and `/fi:redirect` both want this signal. Aggregators rarely capture it cleanly, so we prompt for it directly.

**Why capture `maturity_date` and `term` for time-locked instruments:** CDs, Treasuries, I-Bonds, and brokered fixed-income all have terms. If the user is running a **laddered strategy** (rolling CDs, rolling Treasuries), the skill should detect the pattern and prompt:

> *"This looks like a [CD / Treasury] ladder — rolling N-month maturities at $X each. Want me to capture the ladder as a unit and surface the maturity calendar in `/fi:fu-money-readout`?"*

When `ladder_role` is populated, downstream skills (`/fi:fu-money-readout`, `/fi:crossover`) treat the ladder as a single composite position with a maturity-stream income property — useful for runway planning. This is the YMOYL Step 8 capital pattern in current-rate-environment form: laddered fixed-income preserves principal, captures rate-environment shifts within the term, and provides predictable monthly liquidity.

**Branch on input style.** Ask the user upfront:

> *"How do you want to provide your account data? Three paths:*
>
> *(a) **Bulk import** — you have an export from an aggregator (Monarch, Copilot, Personal Capital, etc.) or a spreadsheet of accounts. Drop the file path or paste the content. I'll parse it and surface anything ambiguous for your confirmation.*
>
> *(b) **Interactive walkthrough** — one account at a time, conversationally. Slower but lets you reconstruct from memory if you don't have a clean export.*
>
> *(c) **Hybrid** — bulk-import the investment accounts you have a clean export for, then walk through the rest interactively (real estate, cash, debts, foreign accounts that aren't in your aggregator).*"

For most users with an existing aggregator, **(c) is the realistic path**: import what's in the aggregator, then add what isn't.

#### Step 4a — Bulk import path

When the user picks (a) or (c):

1. **Get the data**. Accept any of:
   - File path (CSV, JSON, XLSX) the user gives you. Read with the appropriate tool.
   - File the user attaches to chat. Read directly.
   - Pasted content (CSV / TSV / markdown table).
   - Pasted screenshot of a dashboard. Use vision to extract — note this is the lossiest path; offer to re-do with a real export.

2. **Detect the source format**. Common aggregator export formats:

   | Aggregator | Export format | Key columns |
   |---|---|---|
   | **Monarch** | CSV | Account, Type, Institution, Balance, Currency, AsOf |
   | **Monarch (holdings detail)** | CSV | Account, Symbol, Quantity, Price, Value, Cost Basis |
   | **Copilot** | CSV / JSON | account, balance, type, institution |
   | **Personal Capital / Empower** | CSV | account_name, institution, balance, type |
   | **Empower (holdings)** | CSV | symbol, description, quantity, price, value |
   | **Plain spreadsheet (no specific source)** | Any | Map heuristically based on column names |

   Detect by header row. If ambiguous, ask the user which aggregator the export came from.

3. **Map source columns → our schema fields**. Build a mapping table once you've identified the format. For each row, extract:
   - Account name
   - Account type (map aggregator's type values to your tag system; e.g., Monarch's "401(k)" → `401k`, "Roth IRA" → `Roth-IRA`)
   - Balance + currency
   - Holdings (if a holdings-detail export is provided)
   - Last-updated date (if present)

4. **Surface anomalies for the user to confirm**:
   - Accounts with unusual types not in your common-tags list (ask: keep as-is or re-tag?)
   - Holdings with tickers you don't recognize (ask: what's this? what asset class?)
   - Currencies other than the user's base currency (confirm; flag for FX handling)
   - Balances that look stale (last-updated > 30 days ago) — ask if the user wants to refresh manually before continuing
   - Duplicate-looking accounts (same institution + same balance — possible sync glitch)
   - **Disconnected accounts** — aggregators routinely lose auth. *Disconnected ≠ closed.* Ask: *"Is this account still active, or did you close it? If active, do you want to reconnect the aggregator now or update the balance manually?"* — never auto-prune on disconnect alone.
   - Accounts that should have a `rate` but don't — aggregators rarely export rates. After bulk-import, prompt for rates separately:
     > *"Aggregators don't usually capture interest rates. For each cash account and liability, what's the rate? I'll skip investment accounts since their return is variable."*
     > Walk through cash accounts (APY they earn) and liabilities (APR they cost) one pass.

5. **Run asset-class tag suggestions on tickers**, same as the interactive path. For tickers from a holdings-detail export, suggest the tag and confirm in batch (e.g., "I'm tagging these 8 tickers as US-equity: VTI, VTSAX, ITOT, ... — confirm?").

6. **Don't auto-include non-investment data from the aggregator**. Aggregators sometimes pull in checking-account balances, vehicle values, real-estate estimates from Zillow API, etc. Treat those as candidates, not facts. Re-confirm with the user in Step 4c (below) before including in the holdings.md.

#### Step 4b — Interactive walkthrough path

When the user picks (b) or doesn't have a clean export:

1. Ask: *"What's your base currency?"* (default USD; this is the currency net-worth roll-ups will be denominated in)
2. Ask: *"How many accounts roughly?"* (sets expectations)
3. For each account: walk through the fields in the table above conversationally. Don't be robotic — let the user tell you what they have, then confirm what you captured.
4. Asset-class tagging suggestion: when the user provides a ticker (e.g., VTI, VXUS, BND), SUGGEST an asset-class tag (US-equity, intl-equity, bonds, REIT, cash, commodity, crypto, other) but let the user confirm or override. Common ticker → tag mappings:
   - VTI, VTSAX, FZROX, SWTSX, SCHB → US-equity
   - VXUS, VTIAX, IXUS, FZILX → intl-equity
   - BND, AGG, FXNAX → bonds
   - VNQ, SCHH → REIT
   - SGOV, VMRXX, BIL → cash-equivalent
   - BTC, ETH → crypto
   - When unsure: ask, don't guess.

#### Step 4c — Capture non-investment assets and liabilities (always interactive)

After 4a or 4b, regardless of path:

Capture **non-investment items separately** — these are usually NOT in aggregator exports cleanly:

- **Real estate** (gross value, with mortgage debt as a separate negative entry). Aggregators often pull a Zillow estimate; treat it as a starting point, not gospel.
- **Vehicles** — current market value. Prompt the user to verify via [Kelley Blue Book](https://kbb.com) (KBB) using current mileage and condition. Aggregator-stored vehicle values are often years stale and overstated. Ask: *"What's the year/make/model and roughly the mileage? Want to look it up on KBB now, or use a rough estimate and refresh later?"*
- **Cash** (checking accounts, savings — confirm these aren't already double-counted from a bulk import). **Ask the APY** for each — even a 0.01% checking is worth recording, because the spread between checking-yield and HYSA-yield is exactly the kind of leak `/fi:fu-money-readout` will flag.
- **Other debts** (student loans, credit cards, personal loans). **Always ask the rate** for each — mortgage at 3.65% APR-fixed reads very differently from a credit card at 24.99% APR-variable. Capture rate + rate_type per liability.

**Then prompt for non-standard wealth — the "everything saleable" pass.** This is straight from YMOYL Step 1 original framing: most adults are running on partial information because their net-worth picture only includes what fits in an aggregator. Ask:

> *"YMOYL Step 1 asks you to inventory everything saleable, not just bank accounts. Walk through these categories with me — even a rough estimate is fine; we can refine later:*
>
> - *Musical instruments — violins, guitars, cellos, keyboards, brass instruments, vintage gear*
> - *Computers / electronics — laptops, second machines, audio gear, cameras, professional equipment*
> - *Art — original works, limited prints, photographs (resale market exists for known artists)*
> - *Jewelry — gold/silver by weight even if dated, gemstones, watches*
> - *Collectibles — books (signed/first edition), wine, designed objects, hand tools*
> - *Equipment / studio gear — letterpress, kilns, looms, woodworking tools*
> - *Crypto / NFTs held outside aggregators*
> - *Outstanding loans to others — money others owe you*
>
> *Anything in any of these worth more than ~$500 to you?"*

Capture each as a separate non-investment asset entry with: item description, estimated value, basis-of-estimate (KBB / appraisal / online comp / rough guess), as-of date.

Even if the aggregator did pull in checking-account balances or a Zillow estimate, ask the user to confirm before treating them as final.

### Step 5 — Compute roll-ups

After all data is captured:

1. **Asset-class roll-up**: sum value (in base currency) by asset-class tag across all investment accounts.
2. **Account-type roll-up**: sum value by account type (taxable / tax-deferred / tax-free / other) — needed by `/fi:redirect` for placement audit.
3. **Net worth**: sum all assets (investment + non-investment + cash) minus all debts.
4. **Foreign-currency conversion**: for any non-base-currency holdings, query a current FX rate at this moment of the calculation. **Do NOT store the converted figure in the file.** Store native currency only. Note the FX rate used and the timestamp in a comment so re-runs are auditable. Use a reliable source — `https://api.frankfurter.dev/v1/latest?from=<src>&to=<base>` (free, no API key, ECB-sourced).

### Step 6 — Write the file

Write the holdings.md file using the schema in the next section. Follow the structure exactly — other skills will parse this format.

### Step 7 — Closing readout (literal template)

After writing the file, render this closing block to the user. **Use this template literally** — don't paraphrase, don't add motivational language, don't shorten the framing paragraph. Variations between sessions create drift; the canonical template is below.

The Open Items section is conditional — render it only if real items were flagged during the session. Skip the section entirely (no empty heading) when nothing was flagged.

```
✓ File written: <path-to-holdings.md>
  Local-only · gitignored · schema-conforms-to /fi:holdings-scaffold
  Treat as PHI-equivalent.

──────────────────────────────────────────────────

Net worth: $<amount>
  Assets:       $<amount>
  Liabilities:    -$<amount>

──────────────────────────────────────────────────

This file completes Step 1 of Your Money or Your Life —
what Vicki Robin calls "making peace with the past."

Read it like a weather report. Not a verdict on your self-worth.
The past is just data. It does not determine the future.

We build on this.

──────────────────────────────────────────────────

Refresh cadence — different rows, different speeds

  High-churn (daily-banking, bucket transfers) ......... weekly
  Cash + brokerage + IRAs .............................. monthly
  Slow-sync (TSP, 401k, pension) ....................... quarterly
  Real estate, vehicles, saleable inventory ............ annually
  Rate changes (mortgage refi, HYSA repricing) ......... when they happen
  Life events (job change, inheritance, RIF, marriage) . event-triggered

──────────────────────────────────────────────────

Open items captured to your todo

  • <item>
  • <item>

──────────────────────────────────────────────────

What to do with this

  Daily orientation:  /fi:fu-money-readout
                      ~30 sec; reads this file; gives you runway,
                      passive-income, and crossover-percentage at
                      a glance.

  When you're ready
  to look forward:    /fi:hourly-wage
                      Converts your current spending into time —
                      the forward-looking reframe. This is where
                      YMOYL gets actionable.

  Skill done.
```

**Why these specific design choices:**

- **"Step 1 of YMOYL"**: this skill IS YMOYL Step 1 in this suite. The lifetime-earnings half of YMOYL's original Step 1 is deliberately not implemented. It converts dignified non-paycheck years (caregiving, immigration, illness, recovery, RIF, career pivots, federal service capped at the SSA wage base) into a single dollar figure that under-states the actual life. That's a shame mechanic dressed as motivation. (See `book-audits/2026-05-01-ymoyl.md` for fuller reasoning.) Net worth alone completes Step 1 here.
- **"Read it like a weather report. Not a verdict on your self-worth."**: separates data from judgment. The past is information; it's not a referendum on character. Especially important for users whose past includes federal service, caregiving, immigration, illness, recovery, or RIF — anything where the dollar number distorts the dignity of the actual years.
- **"It does not determine the future. We build on this."**: forward orientation, single sentence, no motivational language. Per AGENTS.md tone rules.
- **No magnitude-branching.** The closing reads the same whether net worth is $50K, $1.7M, or negative. Forward energy lives in the next-skill pointer, not in softening the number.
- **`/fi:hourly-wage` as the natural next**: hourly wage converts current spending into time — the forward-looking reframe. This is where YMOYL gets actionable for current decisions.

---

## Schema (the holdings.md output format)

This format is the **cross-skill data contract**. Other skills (`/fi:fu-money-readout`, `/fi:crossover`, `/fi:redirect`, `/fi:monthly-tabulation`) read from holdings.md using this schema. Don't break it without coordinated updates across the suite.

```markdown
---
last-updated: YYYY-MM-DD
base-currency: USD
country: US
holdings-schema-version: 1
---

# Holdings

## Investment accounts

### Account: <name>
- **type**: <tag>
- **balance**: <amount> <ISO-currency>
- **rate**: <X.XX>% <APY-fixed | APY-variable | APR-fixed | APR-variable | intro-rate>  *(omit for investment accounts; required for cash + liabilities + CDs)*
- **maturity-date**: YYYY-MM-DD  *(required for CDs / Treasuries / I-Bonds)*
- **term**: <e.g., 12-month>  *(optional, helpful for CDs)*
- **ladder-role**: <ladder-name>  *(optional, when part of a laddered strategy)*
- **last-verified**: YYYY-MM-DD
- **holdings**:  *(optional — deferred to `/fi:redirect` for most users)*
  - <TICKER>: <shares> shares @ <price> <currency> = <value> <currency> [asset-class: <tag>]
  - <TICKER>: <shares> shares @ <price> <currency> = <value> <currency> [asset-class: <tag>]

### Account: <name>
... (repeat per account)

## Non-investment assets

- **Real estate (primary residence)**: <value> <currency> (gross), as of YYYY-MM-DD, basis: <Zillow / appraisal / county-assessor / comp-sale>
- **Vehicles**: <value> <currency>, as of YYYY-MM-DD, basis: <KBB / NADA / appraisal>
- **Other saleable assets**:
  - <item description>: <estimated value> <currency>, basis: <appraisal / online comp / rough estimate>

## Liabilities

- **Mortgage**: -<amount> <currency>, rate: <X.XX>% APR-fixed, as of YYYY-MM-DD
- **Student loans**: -<amount> <currency>, rate: <X.XX>% APR-<fixed|variable>
- **Credit cards**: -<amount> <currency>, rate: <X.XX>% APR-variable

## Asset-class roll-up (computed; in base currency)

- **US equity**: $X (XX% of investment portfolio)
- **International equity**: $X (XX%)
- **Bonds**: $X (XX%)
- **REIT**: $X (XX%)
- **Cash-equivalent**: $X (XX%)
- **Crypto**: $X (XX%)
- **Other**: $X (XX%)

## Account-type roll-up (computed; in base currency)

- **Tax-deferred** (401k / Trad-IRA / TSP / RRSP): $X (XX%)
- **Tax-free** (Roth / HSA / ISA / TFSA): $X (XX%)
- **Taxable brokerage**: $X (XX%)
- **Cash**: $X (XX%)
- **Other**: $X (XX%)

## Net worth (current; computed)

- **Investment accounts (total)**: $X
- **Non-investment assets**: $X
- **Cash**: $X
- **Liabilities**: -$X
- **Net worth**: $X

## Step 1 — Making peace with the past (YMOYL)

This file completes Step 1: knowing what is true today.

Read it like a weather report. Not a verdict on your self-worth. The past is just data. It does not determine the future. We build on this.

---

## FX rates used (audit log)

(Computed roll-ups above use these conversions. Re-run the skill to refresh.)

- 1 EUR = X.XXXX USD (queried YYYY-MM-DD HH:MM UTC, source: api.frankfurter.dev)
- 1 GBP = X.XXXX USD (queried YYYY-MM-DD HH:MM UTC, source: api.frankfurter.dev)
```

**Schema rules:**

- The frontmatter `holdings-schema-version` field is load-bearing — if we ever break the schema, increment this and downstream skills branch on the version.
- Currency codes are ISO-4217 (3-letter). No symbols (`$`, `£`, `€`) in the structured fields; symbols only in human-readable computed roll-up sections.
- Asset-class tags are free-form but the canonical list (US-equity, intl-equity, bonds, REIT, cash-equivalent, crypto, commodity, other) covers most cases.
- Account-type tags are free-form; the country tax reference file (`references/tax/<COUNTRY>.md`) provides the canonical list per country.

**Progressive-enrichment philosophy.** The schema is layered, not all-at-once:

- This skill captures **account-level** data (account → balance → currency → last-verified). That's enough to compute net worth, account-type roll-up, and serve as input to most downstream skills.
- **Fund-level holdings detail** (per-ticker shares, prices, cost basis) is OUT OF SCOPE here. That layer is added later by `/fi:redirect` when the user runs a placement audit or diversification analysis. The schema's `holdings:` field per investment account is **optional** and may be empty initially — `/fi:redirect` will populate it during its own walkthrough.
- **Asset-class roll-up** sections in the file may be left as `*deferred to /fi:redirect*` placeholders if fund-level detail isn't yet captured. Don't fail or block — leave a clear marker.

This matters because most users start with a generic aggregator drag-and-drop ("By Account" view), not a per-holding export. Forcing them to provide fund-level data upfront blocks the skill on something they don't yet have. Layered enrichment respects that.

---

## Privacy guardrails (every step enforces)

Per [`AGENTS.md`](../../AGENTS.md), and reinforced specifically for this skill:

1. **Never write any data to the holdings file before gitignore is verified-clean (Step 3).** This is the load-bearing rule.
2. **Never auto-commit the file.** If the user runs `git add .` after this skill, gitignore should prevent it. Verify before exit.
3. **Never auto-sync.** Do not connect to cloud services. Do not call any external API except the FX-rate query, and even that returns only currency exchange rates — never holdings data goes outbound.
4. **Echoing readouts to the user is expected and fine.** The user is the user — they want to see their own net worth, account balances, roll-ups. The workflow depends on this. **The privacy concern is log visibility, not chat output.** Remind the user once during the skill: *"Heads up — your chat transcript with me is visible wherever your Claude Code session syncs (this machine, anyone with access to it, any session-log backups you've configured). If your machine is shared, or your session logs sync somewhere you don't fully control, this readout is visible there. Standard hygiene applies — same as with a banking app."*
5. **Don't write balances, holdings, or net worth to OTHER files** (handoff notes, session summaries, memory, todo.md, cross-project context). Treat the holdings file as the only authorized destination for the data. If a downstream skill needs net worth, it reads from the file at runtime — it does not get cached into another file.
6. **Crash output should describe the failure shape, not the data shape.** If FX query fails: *"FX rate query failed for EUR→USD"* — not *"failed to convert €15,432.50"*. Stack traces and error logs have a different visibility surface from chat output.

---

## Multi-currency handling

**Rule: store native, convert at read-time.**

For any holding in a non-base currency:

- Store the value in the **native** currency (e.g., `12,500 EUR`, not `$13,400 USD`).
- At calculation time (Step 5 and any downstream skill), query a fresh FX rate.
- Record the rate used, the source, and the timestamp in the audit log section of the file.
- **Never trust an aggregator's pre-converted figure.** Aggregators (Monarch, Copilot, Personal Capital, Mint-replacements) freeze the conversion at sync time. By the next read it can be stale by hundreds of dollars.

**Recommended FX source**: [`api.frankfurter.dev`](https://api.frankfurter.dev) — free, no API key required, ECB-sourced rates updated daily. Example query: `GET https://api.frankfurter.dev/v1/latest?from=EUR&to=USD`.

If the FX query fails (offline, API down, rate-limited), warn the user and proceed with the most-recently-cached rate from the audit log. Mark the readout as "stale FX" so they know.

---

## Mode-awareness

Currently `mode_aware: false` — this skill operates the same way regardless of the user's retirement frame, work mode, or country.

The country-aware piece happens via `references/tax/<COUNTRY>.md`: when the user states their country in Step 4, the skill can suggest country-appropriate account-type tags from that file. But the skill itself doesn't branch behavior on country.

---

## Headless / batch mode

This skill is **interactive by default**. Running it headlessly (cron / pipeline / no human present) should fail loudly with a clear error: *"This skill requires interactive input. To populate holdings.md headlessly, provide a `holdings-input.yaml` manifest file with the same schema."*

**Manifest mode (planned, not yet implemented)**: a structured input file with all account data pre-filled. Useful for users who already have data in another format and want to bulk-import. The manifest schema will mirror the holdings.md schema. **TODO**: implement and document.

---

## Cross-skill data contracts

| Reader skill | Reads from holdings.md | What it does with the data |
|---|---|---|
| `/fi:fu-money-readout` | All sections | Daily ground-state report; uses net worth, recurring passive (computed from holdings), runway calculation |
| `/fi:crossover` | Investment accounts + asset-class roll-up | Computes FI threshold; needs portfolio composition for expected-return assumptions |
| `/fi:redirect` | Investment accounts + account-type roll-up + holdings list | Tax-advantaged placement audit; diversification overlap analysis |
| `/fi:monthly-tabulation` | Doesn't read holdings.md directly, but reads transactions/ which are gitignored alongside | n/a |

**If you change the schema**: update every reader skill in the same PR. The `holdings-schema-version` frontmatter field exists to make breakage detectable.

---

## Examples

See `examples/` (when populated):

- `examples/holdings-us-5-account.md` — typical US user, single currency, 5 accounts (taxable + Roth + 401k + HSA + cash)
- `examples/holdings-multi-currency-uk-us.md` — multi-currency user (UK ISA + US taxable brokerage + GBP cash + USD cash)

**TODO**: write these examples as part of skill testing.

---

## Status

`draft` — the skill is documented end-to-end with concrete procedures, schema, privacy enforcement, and downstream contracts. Not yet tested in a live invocation. Pre-launch checklist:

- [ ] Run the skill end-to-end on Marika's own holdings (the original source of the pattern).
- [ ] Write the two `examples/` files.
- [ ] Stress-test gitignore enforcement on a fresh repo.
- [ ] Verify FX-rate query against api.frankfurter.dev returns expected format.
- [ ] Test what happens when the user already has a holdings.md (Step 1 branch).

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1 of the 9-step program; the catch-up framing.
- **Marika Olson** (2026). The holdings-file structure was built for personal use first, then generalized into this skill. The FX-at-read-time rule comes from the Monarch failure case (April 2026): aggregator-frozen conversions silently stale, leading to ~$400 misreport on EUR holdings.
