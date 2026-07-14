---
name: holdings-scaffold
description: "Build the user's local holdings.md file from scratch — every account, every holding, asset-class roll-up, current net worth, with strict gitignore enforcement before any data is written. Use when the user wants to track their net worth, set up a financial inventory, scaffold their finances, build a security-blanket file of what they own, organize scattered accounts, or asks where to keep their financial data. The output file is the gateway artifact every other /fi: skill reads from."
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 1 framing — current net worth as 'making peace with the past'. (YMOYL prescribes a second half — lifetime earnings reconstruction — which this suite deliberately does not implement; see book-audits/2026-05-01-ymoyl.md for reasoning.)"
  - author: Marika Olson
    contribution: "2026 generalization of the holdings-file structure she built for personal use; the FX-at-read-time rule from the Monarch failure case"
last-reviewed: 2026-05-23
status-history:
  - "2026-05-02: draft (initial 2026 design — full procedure, schema, privacy enforcement, cross-skill contracts)"
  - "2026-05-23: draft + `purpose` field added (cash/CD/ladder/earmarked accounts — surfaces user-intent so downstream skills don't flatten emergency-fund and growth-cash into one undifferentiated pool; observed during real-data walkthrough when a CD ladder's \"one-year emergency fund + behavioral guardrail\" purpose had no schema home)"
  - "2026-05-23: draft + walkthrough pass (7 gaps from a real-data fresh-build run) — (1) Step 1a update-mode now asks balance-vs-structural-vs-both before walking the file, plus a life-event check; (2) Step 2 file-location gains a third default for dedicated life-ops repos (the work-vs-personal binary missed users with a \"personal OS\" repo); (3) Step 4a source-format table distinguishes Monarch's snapshot / history / holdings / dashboard-paste shapes and prescribes wrong-shape handling; (4) `status` field — active / dormant / closed — with dormant preserving row for traceability while zeroing roll-ups; (5) `sync_status` field — adds the manual-only case for federal accounts and similar chronic-disconnect items, distinct from open/closed; (6) hidden-accounts prompt added to the anomaly-surface list (most aggregators hide accounts users forget about); (7) `ladder_state` + `ladder_target_size` fields — captures in-progress ladders (1-of-12 built) vs steady-state. Output schema template updated to match."
  - "2026-05-23: draft + variable-rate disambiguation. `rate_type: APY-variable` and `APR-variable` previously conflated two different things — bank-discretionary market-rate variability vs. user-conditional qualifier-driven variability (the headline rate is offered only if the user meets a per-month activity threshold). Added a follow-up prompt + `qualifier_description` and `qualifier_met` fields. Downstream skills now compute opportunity-cost off the effective rate (qualifier met or not), not the headline."
  - "2026-05-23: draft + Step 4d (income streams, non-labor) sketched in. New procedure step + schema section captures streams that aren't tied to an account balance — pensions, annuities, supplements, dividends, rental, royalties, future government retirement benefits. Per-stream fields: name, kind, monthly_amount, currency, status (active / future-activates-at-date / future-activates-at-event / expires-at-date / expires-at-event), activation, expiration, cola_adjusted, taxable_treatment, source. Multi-scenario streams (different eligibility ages, different claim timings) captured as separate stream entries — crossover models scenarios against the options. **Sketch-level — schema will refine as `/fi:crossover` and `/fi:fu-money-readout` make real demands.**"
  - "2026-05-23: draft + Step 4d split into two prompts (current vs future-anticipated income streams). Future streams get glossed over when bundled with current ones — many users default to \"my income is my paycheck\" and skip the question. Asking future separately catches deferred pensions, not-yet-claimed government benefits, future-rental cases. Step 7 closing readout gains a conditional income-streams block — rendered only when streams exist, with active-now and future-activated rendered independently; whole block omitted if no streams (matches the open-items-conditional pattern already used)."
  - "2026-05-23: draft + holdings→crossover contract hardening (4 fixes). (1) Liabilities now capture `current_monthly_payment` (P&I only) — was missing; crossover needs it for amortization-based payoff-date computation. (2) Per-holding `cost_basis` added as optional but recommended field — without it crossover defaults to taxing full withdrawal at LTCG (overstates tax by 50%+ on long-held positions). (3) Closing readout gains explicit pointer to `/fi:crossover` as the FI-threshold-math next-step — previously only pointed to fu-money-readout and hourly-wage, missing the most load-bearing skill for retirement-shaped decisions. (4) New \"Downstream-ready check\" section in closing — skill now tells the user which downstream skills can run and what's missing to unlock the rest. Caught during track-flow walkthrough when the meta-question surfaced: \"does holdings-scaffold understand what crossover needs?\""
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
3. **Ask the user what kind of update this is** — don't assume balance-refresh is the goal. Three common shapes:
   - **Balance refresh only** — same accounts, new numbers. The fast monthly cadence.
   - **Structural changes only** — add/remove accounts, change a rate, fix a tag, mark something dormant. No balance re-pull.
   - **Both** — balance refresh AND structural changes (rarer; usually triggered by a life event or a quarterly cleanup).
   Branch the walkthrough on the answer. Don't drag a user who only wants a structural change through a per-account refresh sweep.
4. Walk through the existing file with the user, scoped to what they chose in (3):
   - *(balance-refresh paths)* Which accounts have changed balances? Which are stale (last-verified > 30 days)?
   - *(structural-change paths)* Are there new accounts to add? Are any now dormant (zero out, keep row) or closed (remove)? Any rates, tags, or purposes to update?
5. **Life-event check.** Before completing, ask once: *"Has anything material changed in your life since the last update — job change, RIF, pension status change, marriage, new dependent, inheritance, major health diagnosis, geographic move, significant runway shift?"* If yes, flag that downstream skills (`/fi:crossover`, `/fi:fu-money-readout`) should be re-run end-to-end, not just refreshed — the assumptions they're computing against may have shifted.
6. Skip Step 2 (file location is already chosen) and Step 4a/4b's bulk-import-vs-walkthrough question (just iterate over what changed). Step 3 still runs. Step 5 (compute roll-ups) and Step 6 (write file) still run.
7. Preserve the file's prior `last-updated` value as a comment at the top, then overwrite with today's date.

#### 1b. Fresh-build mode (no existing file)

Proceed to Step 2.

**One skill, two starting states.** Don't fork into a separate skill for updates — the procedure is the same shape with a different entry point.

### Step 2 — Pick the file location

Suggest three defaults and let the user pick:

- **`~/finances/holdings.md`** — outside any project repo; lives in the user's home directory; suitable when the user wants their financial data fully separate from any project.
- **`<current-repo>/finances/holdings.md`** — inside the user's currently-active project; suitable when the user is comfortable with one specific work repo holding personal data AND that repo is private OR has aggressive `.gitignore` coverage.
- **A dedicated personal-ops / life-ops repo** (e.g. `<life-ops-repo>/finances/holdings.md`) — a private repo the user already uses to track personal data (todos, journals, health, relationships, finances) with established gitignore patterns. This pattern is common among technical users who keep a single "operating system for my life" repo and want financial data to live there alongside the rest. Ask the user whether they have such a repo before defaulting to the home-dir option — the framing "work or personal" misses this case.

If none fits, accept a custom path. **Do not write the file yet.** Privacy enforcement runs first.

**Sentinel duty (this skill only).** The directory containing `holdings.md` is the user's `<finances_root>` — the root every other `/fi:` skill resolves via the AGENTS.md §Path resolution order. This skill is the sole writer of the `.fi-root` sentinel file: in Step 6, alongside `holdings.md`, write an empty `.fi-root` marker in the chosen directory if one isn't already there (and in update mode, verify it exists — add it if missing). Without the sentinel, downstream skills fall back to `~/finances/` and silently miss a custom location.

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
| `rate_type` | string | when rate is set | One of: `APY-fixed`, `APY-variable`, `APR-fixed`, `APR-variable`, `intro-rate`. CDs and Treasuries are typically `APY-fixed` for the term. **When the user selects `APY-variable` or `APR-variable`, ask the follow-up:** *"Is this variable because the bank can adjust the market rate at will, or because the rate depends on you meeting a qualifier (minimum deposits, monthly spend threshold, balance tier, account-tier upgrade)?"* If qualifier-driven, populate the `qualifier_description` and `qualifier_met` fields below. |
| `qualifier_description` | string | required when rate_type is variable AND qualifier-driven | Free-form description of the qualifier condition. e.g., "1.30% APY if ≥$2,500/mo deposits OR ≥$487/mo card spend, else 0%"; "5.00% APY on first $10K, 0.50% above that"; "0.75% bonus tier if total balance ≥$50K." Capture the user's actual conditional structure — these vary widely and shouldn't be enumerated. |
| `qualifier_met` | boolean | required when qualifier_description is set | `true` if the qualifier is currently being met (so the headline rate applies), `false` if not (so the realistic effective rate is the fallback — often 0% or the tier-floor). Downstream skills compute opportunity cost off the **effective** rate, not the headline — a 1.30% APY that's currently earning 0% leaks the same as a 0% account, not the same as a true 1.30% account. |
| `maturity_date` | YYYY-MM-DD | required for CDs / Treasuries / I-Bonds | When the time-locked instrument matures and principal becomes accessible. Critical for cash-flow planning and ladder strategies. |
| `term` | string | optional, helpful for CDs / Treasuries | Original term length (e.g., `3-month`, `12-month`, `5-year`). Helps the user reason about ladder structures. |
| `ladder_role` | string | optional | If this account is part of a laddered strategy (CD ladder, Treasury ladder), name the ladder (e.g., `RB-12mo-CD-ladder-month-1`) so the skill can roll up ladder-level positions. |
| `purpose` | string | optional, recommended for cash + CDs + ladders + earmarked accounts | Why the position exists. Common values: `emergency-fund`, `runway`, `sinking-fund-<target>` (e.g., `sinking-fund-house-repair`), `tax-reserve`, `sabbatical-reserve`, `behavioral-guardrail`, `long-term-growth`, `bridge-income`. Capture the user's own phrasing if they have one — the field is descriptive, not enumerated. |
| `status` | string | yes (default `active`) | One of: `active` (counts in roll-ups), `dormant` (keep row for record but treat as $0 in roll-ups — used for old aggregator entries the user wants traceability on without including in net-worth math), `closed` (remove from active holdings; move to a `## Removed accounts` audit section at the bottom of the file with the date removed and the last-known balance). |
| `sync_status` | string | optional | One of: `aggregator-synced` (aggregator currently has live auth), `aggregator-disconnected` (aggregator lost auth — DOES NOT MEAN CLOSED), `manual-only` (account is active but chronically hard to keep in any aggregator — federal accounts like TSP, some pensions, foreign banks; manual refresh is the realistic cadence). Distinct from `status` — a `manual-only sync_status` account is fully active, the sync mechanism is just different. |
| `ladder_state` | string | optional, only when `ladder_role` is set | One of: `building` (the ladder is being constructed — current count < target count) or `steady-state` (target count reached, fully rotating). Pair with `ladder_target_size` (integer, e.g., `12` for a monthly 12-month CD ladder). Lets downstream skills surface "ladder is N/M rungs built, M-N remaining" vs. assuming the ladder is fully populated. |
| `holdings` | list | optional (deferred to `/fi:redirect`) | If the account has discrete holdings (stocks, funds, etc.), capture each: ticker, shares, native price-per-share, asset-class tag, **cost-basis** (per holding, in native currency — needed by `/fi:crossover` to compute LTCG tax on bridge withdrawals; without it crossover defaults to taxing the full withdrawal at LTCG which can overstate tax by 50%+ on long-held positions). Most users won't have this on first run — if the user volunteers they have cost-basis available (Vanguard / Fidelity / Schwab usually show it), capture; otherwise defer to `/fi:redirect`. |
| `last_updated` | YYYY-MM-DD | yes | When the user last verified this balance |

**Why capture `rate`:** knowing the spread between what cash earns and what debt costs is foundational for downstream skills. A user with $50k in a 0.01% checking account and a 24% credit card balance is leaking money in a way the net-worth number alone doesn't surface. `/fi:fu-money-readout` and `/fi:redirect` both want this signal. Aggregators rarely capture it cleanly, so we prompt for it directly.

**Why capture `maturity_date` and `term` for time-locked instruments:** CDs, Treasuries, I-Bonds, and brokered fixed-income all have terms. If the user is running a **laddered strategy** (rolling CDs, rolling Treasuries), the skill should detect the pattern and prompt:

> *"This looks like a [CD / Treasury] ladder — rolling N-month maturities at $X each. Want me to capture the ladder as a unit and surface the maturity calendar in `/fi:fu-money-readout`?"*

When `ladder_role` is populated, downstream skills (`/fi:fu-money-readout`, `/fi:crossover`) treat the ladder as a single composite position with a maturity-stream income property — useful for runway planning. This is the YMOYL Step 8 capital pattern in current-rate-environment form: laddered fixed-income preserves principal, captures rate-environment shifts within the term, and provides predictable monthly liquidity.

**Why capture `purpose`:** an emergency fund and a long-term growth position
might both be $50k in a HYSA, but they're not interchangeable. Purpose tells
downstream skills how the position should be treated — an emergency fund
should not be the first source for opportunistic redeployment; a tax reserve
shouldn't show up as net liquidity in a runway calc; a behavioral guardrail
(money parked in a CD ladder specifically to add friction against impulse
spending) is data for `/fi:fu-money-readout` to surface as such, not noise.
Without this field, every cash position looks the same to downstream skills,
and the user's deliberate structure becomes invisible. Ask for it whenever
the user volunteers a reason ("this is my emergency fund," "this is for
quarterly taxes") and offer it explicitly for CDs, ladders, and any account
the user describes as earmarked. Investment accounts (brokerage, IRAs, 401k)
can default to `long-term-growth` and don't need an explicit prompt.

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

   | Aggregator | Export shape | Key columns |
   |---|---|---|
   | **Monarch (snapshot)** | "By Account" CSV | Account, Type, Institution, Balance, Currency, AsOf |
   | **Monarch (balance history)** | "Balances" CSV | Date, Balance, Account |
   | **Monarch (holdings detail)** | CSV | Account, Symbol, Quantity, Price, Value, Cost Basis |
   | **Monarch (dashboard paste)** | Pasted text | Section headers (Cash/Investments/etc.) + per-account rows with name, type, balance, time-since-update |
   | **Copilot** | CSV / JSON | account, balance, type, institution |
   | **Personal Capital / Empower** | CSV | account_name, institution, balance, type |
   | **Empower (holdings)** | CSV | symbol, description, quantity, price, value |
   | **Plain spreadsheet (no specific source)** | Any | Map heuristically based on column names |

   Detect by header row. If ambiguous, ask the user which aggregator AND which export view the export came from — most aggregators produce multiple export shapes for the same underlying data (snapshot vs. history vs. holdings detail), and only one is right for this skill.

   **Wrong-shape handling.** If the user provides a *history* export (date-indexed time series) when the skill needs a *snapshot*, do not silently coerce — surface it: *"This is a balance-history export (one row per account per day, ~N rows). I need a snapshot (one row per account, latest balance, with type/institution/currency). I can either (a) derive the snapshot by taking the latest row per account from this file — but that loses type, institution, and currency fields — or (b) you grab the snapshot export instead. Which?"* Same pattern applies to any aggregator with multiple export shapes.

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
   - **Disconnected accounts** — aggregators routinely lose auth. *Disconnected ≠ closed.* Ask: *"Is this account still active, did you close it, or is it active-but-chronically-hard-to-sync (federal accounts, foreign banks, some pensions)? If active, do you want to reconnect the aggregator now, update manually, or set `sync_status: manual-only` and refresh on a slower cadence?"* — never auto-prune on disconnect alone, and don't conflate "active but manual" with "disconnected."
   - **Hidden accounts in the aggregator** — most aggregators let users hide accounts to declutter the dashboard, and the user often forgets they exist. After parsing visible accounts, ask: *"Does your aggregator have any hidden accounts? If yes, are any of them non-zero — old IRAs, dormant business checking, foreign accounts you stopped looking at? If yes, surface them; we'll either include them (active), mark dormant, or close-and-record."* Don't assume hidden = zero.
   - Accounts that should have a `rate` but don't — aggregators rarely export rates. After bulk-import, prompt for rates separately:
     > *"Aggregators don't usually capture interest rates. For each cash account and liability, what's the rate? I'll skip investment accounts since their return is variable."*
     > Walk through cash accounts (APY they earn) and liabilities (APR they cost) one pass.
     > **For each variable rate, follow up:** *"Is this variable because the bank can adjust the market rate at will, or because it depends on you meeting a qualifier (deposit minimum, spend threshold, balance tier)?"* If qualifier-driven, capture the qualifier description and whether it's currently being met — see `qualifier_description` and `qualifier_met` in the Step 4 schema table. Conditional rates that aren't being qualified for currently earn the fallback (often 0%), and downstream skills need that distinction.

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

#### Step 4d — Capture income streams (non-labor; always interactive)

Some users have income streams that aren't tied to an account balance —
pensions, annuities, dividends thrown off by investment positions, rental
income, royalties, future Social Security or government-benefit payments,
trust distributions. These are **load-bearing inputs to `/fi:crossover` and
`/fi:fu-money-readout`** (runway math, FI threshold math, retirement-income
picture) but they don't fit anywhere in Steps 4a–4c.

After investment / cash / non-investment assets / liabilities are captured,
ask in **two separate prompts** so future streams don't get glossed over:

**Prompt 1 — current income streams:**

> *"Do you have any current income streams that aren't tied to an account
> balance? Common ones: pensions you're drawing now, annuity payments, rental
> income, royalties, trust distributions, dividends you treat as income
> rather than reinvest."*

**Prompt 2 — future anticipated income streams:**

> *"Do you anticipate any future income streams? Examples: a pension you've
> earned but haven't started drawing, future Social Security benefits, a
> deferred annuity, planned rental income from a property in development, a
> trust distribution scheduled at a future date or age, an annuity supplement
> that activates at retirement."*

Many users have one but not the other — and future streams especially tend
to get skipped when the question is collapsed into "do you have income
streams" (the user thinks "I'm working, my income is my paycheck" and answers
no). Asking the future question separately catches the deferred-pension,
government-retirement-not-yet-claimed, future-rental, and similar cases
that downstream skills genuinely need. If the user has none of either, that's fine — skip Step 4d's data
capture and the closing readout's income-streams block (Step 7) renders
empty / is omitted.

For each stream, capture:

| Field | Notes |
|---|---|
| `name` | Free-form descriptive label (e.g., "employer pension", "pension supplement", "government retirement at FRA", "fund dividends", "rental income") |
| `kind` | One of: `pension`, `annuity`, `supplement`, `dividends`, `royalty`, `rental`, `trust-distribution`, `other-passive`. Free-form if none fit. |
| `monthly_amount` | Current or projected $/month in native currency. Use `0` for future-only streams. |
| `currency` | ISO-4217 (defaults to base) |
| `status` | One of: `active` (paying now), `future-activates-at-date` (e.g., 2043-11-16), `future-activates-at-event` (e.g., "age 62", "litigation settlement"), `expires-at-date`, `expires-at-event` (e.g., a bridge supplement that expires when full eligibility kicks in). Can have both activation and expiration. |
| `activation` | Date or event when the stream starts paying. Omit if `status: active`. |
| `expiration` | Date or event when the stream stops. Omit if no end. |
| `cola_adjusted` | `true` if the stream gets cost-of-living adjustments (most government retirement benefits and many public-sector pensions), `false` if fixed-nominal (most private annuities, some private pensions). |
| `taxable_treatment` | Free-form. e.g., "fully taxable as ordinary income", "partially taxable up to a per-locale threshold", "tax-free (Roth qualified distribution)", "depends on per-locale rules" — capture the specific rule the user understands applies to their stream. |
| `source` | Where the figure comes from — the calculation, statement, or dated projection that produced the monthly_amount. Be specific enough that a year-from-now-you can re-derive the number. |

**This section is sketch-level (2026-05-23).** It captures the right *shape*
but the schema will refine as `/fi:crossover` and `/fi:fu-money-readout` make
real demands on it (e.g., do they need projected COLA growth rates? sequence-
of-activation modeling? trust-fund-haircut scenarios for SSA?). For now: get
the streams in the file with enough detail that downstream skills can ask
for what's missing.

Pensions / annuities / government retirement benefits with **multiple
scenarios** (early-reduced vs full-eligibility, different claim ages,
deferred vs immediate options) — capture each scenario as its own stream
entry with descriptive names ("pension at full eligibility age", "government
retirement at FRA", "government retirement at max-claim age"). Don't try to
collapse into a "pick one" structure here — `/fi:crossover` will model
scenarios against the captured options.

### Step 5 — Compute roll-ups

After all data is captured:

1. **Asset-class roll-up**: sum value (in base currency) by asset-class tag across all investment accounts.
2. **Account-type roll-up**: sum value by account type (taxable / tax-deferred / tax-free / other) — needed by `/fi:redirect` for placement audit.
3. **Net worth**: sum all assets (investment + non-investment + cash) minus all debts.
4. **Foreign-currency conversion**: for any non-base-currency holdings, query a current FX rate at this moment of the calculation. **Do NOT store the converted figure in the file.** Store native currency only. Note the FX rate used and the timestamp in a comment so re-runs are auditable. Use a reliable source — `https://api.frankfurter.dev/v1/latest?from=<src>&to=<base>` (free, no API key, ECB-sourced).

### Step 5b — Deterministic checks (run before Step 6; never write a file that fails)

Per AGENTS.md §Deterministic invariants — recompute each identity from the per-account data and compare against the roll-ups from Step 5. On mismatch: stop and reconcile (usual causes: a double-counted bulk-import row, a dormant account leaking into a sum, a stale FX figure); don't write.

- **Net-worth identity**: net worth = Σ(all asset balances, base currency) − Σ(all liability balances). Recomputed from the account rows, compared against the Step 5 figure to the cent (FX-converted amounts: ±0.5% rounding tolerance).
- **Roll-up conservation**: Σ(asset-class roll-up values) = investment-accounts total; Σ(account-type roll-up values) = same total; each roll-up's percentages sum to 100% ± rounding.
- **Status discipline**: `dormant` accounts contribute exactly $0 to every roll-up (row present, value excluded); `closed` accounts appear only in `## Removed accounts`.
- **Holdings-level sum** (when a `holdings:` list is populated): Σ(shares × price) per account = that account's `balance` within rounding; flag the gap otherwise (usually cash drag or a stale price — name which).
- **Ladder consistency**: rung count ≤ `ladder_target_size`; `ladder_state: steady-state` requires rung count = target.
- **Date sanity**: every `last-verified` ≤ today; `maturity_date` in the future for any active CD/Treasury (a past maturity on an active row means the instrument rolled or the row is stale — ask).
- **FX audit completeness**: every non-base currency appearing in any balance has a rate + timestamp line in the FX audit log.

### Step 6 — Write the file

Write the holdings.md file using the schema in the next section. Follow the structure exactly — other skills will parse this format.

Also write (or verify) the `.fi-root` sentinel in the same directory, per the sentinel-duty note in Step 2 — an empty marker file that lets every other `/fi:` skill resolve `<finances_root>` by walk-up.

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

Income streams (non-labor)            *(omit this block entirely if no streams captured)*

  Active now:        $<amount>/month across <N> stream(s)
  Future-activated:  <N> stream(s) — see file for activation timing and projected amounts

  (Render only the rows that have data. If only "active now" streams exist,
  omit the "future-activated" line. Same in reverse. If neither, omit the
  whole block — don't leave an empty heading. See Step 4d for capture logic.)

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

Downstream-ready check

  (Skill computes which downstream skills can run now vs. what's still
  missing, and renders the result inline. Don't bury — this is the
  user's "what's unlocked" signal.)

  Ready to run now:
    ✓ /fi:fu-money-readout        (always — only needs holdings.md)
    ✓ /fi:hourly-wage              (independent of holdings.md)
    <conditional based on captured data:>
    ✓ /fi:crossover                (income streams + retirement-frame present)
    ⚠ /fi:crossover                (income streams ready; create
                                    <finances_root>/profile/retirement-frame.md first)
    ⚠ /fi:crossover                (no income streams declared via Step 4d —
                                    runs in perpetual-portfolio mode without them)

  Optional refinements (improve downstream accuracy):
    • Add cost-basis to taxable holdings → tightens /fi:crossover tax math
    • Add current-monthly-payment to liabilities → enables
      /fi:crossover payoff projections

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

  When you want the
  FI threshold math:  /fi:crossover
                      Reads what you just captured (holdings, income
                      streams, liabilities for amortization); computes
                      your FI crossover age, bridge years, and the
                      "are you already FI?" check. The most load-
                      bearing skill for retirement-shaped decisions.

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

This format is the **cross-skill data contract**. Other skills (`/fi:fu-money-readout`, `/fi:crossover`, `/fi:redirect`, `/fi:track-flow`) read from holdings.md using this schema. Don't break it without coordinated updates across the suite.

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
- **qualifier-description**: <free-form description of the qualifier condition>  *(required when rate_type is variable AND qualifier-driven — e.g., a high-yield account whose headline APY is only earned when monthly debit-card activity or deposit volume meets a stated threshold)*
- **qualifier-met**: <true | false>  *(required when qualifier-description is set; downstream skills use the effective rate, not the headline)*
- **maturity-date**: YYYY-MM-DD  *(required for CDs / Treasuries / I-Bonds)*
- **term**: <e.g., 12-month>  *(optional, helpful for CDs)*
- **ladder-role**: <ladder-name>  *(optional, when part of a laddered strategy)*
- **ladder-state**: <building | steady-state>  *(optional, paired with ladder-role)*
- **ladder-target-size**: <integer>  *(optional, paired with ladder-role — e.g., 12 for a monthly 12-month CD ladder)*
- **purpose**: <emergency-fund | runway | sinking-fund-<target> | tax-reserve | sabbatical-reserve | behavioral-guardrail | long-term-growth | bridge-income | custom>  *(optional, recommended for cash + CDs + earmarked accounts)*
- **status**: <active | dormant | closed>  *(default active; dormant = keep row, zero out roll-ups; closed = move to ## Removed accounts section)*
- **sync-status**: <aggregator-synced | aggregator-disconnected | manual-only>  *(optional; distinct from status)*
- **last-verified**: YYYY-MM-DD
- **holdings**:  *(optional — deferred to `/fi:redirect` for most users)*
  - <TICKER>: <shares> shares @ <price> <currency> = <value> <currency> [asset-class: <tag>]
  - <TICKER>: <shares> shares @ <price> <currency> = <value> <currency> [asset-class: <tag>]

### Account: <name>
... (repeat per account)

## Income streams (non-labor)

*Streams that aren't tied to an account balance — pensions, annuities, SSA, dividends, rental, royalties. Load-bearing inputs to `/fi:crossover` and `/fi:fu-money-readout`. Capture per Step 4d in the SKILL procedure.*

### Stream: <name>

- **kind**: <pension | annuity | supplement | dividends | royalty | rental | trust-distribution | other-passive>
- **monthly-amount**: <amount> <ISO-currency>
- **status**: <active | future-activates-at-date | future-activates-at-event | expires-at-date | expires-at-event>
- **activation**: <YYYY-MM-DD | event description>  *(omit if status: active)*
- **expiration**: <YYYY-MM-DD | event description>  *(omit if no end)*
- **cola-adjusted**: <true | false>
- **taxable-treatment**: <free-form>
- **source**: <where the figure comes from>

### Stream: <name>
... (repeat per stream; capture each pension/SSA-claim-age scenario as its own stream)

## Non-investment assets

- **Real estate (primary residence)**: <value> <currency> (gross), as of YYYY-MM-DD, basis: <Zillow / appraisal / county-assessor / comp-sale>
- **Vehicles**: <value> <currency>, as of YYYY-MM-DD, basis: <KBB / NADA / appraisal>
- **Other saleable assets**:
  - <item description>: <estimated value> <currency>, basis: <appraisal / online comp / rough estimate>

## Liabilities

- **Mortgage**: -<amount> <currency>, rate: <X.XX>% APR-fixed, current-monthly-payment: <amount> <currency> (P&I only, excludes escrow), as of YYYY-MM-DD
- **Student loans**: -<amount> <currency>, rate: <X.XX>% APR-<fixed|variable>, current-monthly-payment: <amount> <currency>
- **Credit cards**: -<amount> <currency>, rate: <X.XX>% APR-variable  *(monthly payment varies; capture if user pays a fixed amount above minimum)*

*Why `current-monthly-payment`*: amortizing liabilities (mortgage, auto loan, student loan) need this field for `/fi:crossover` to compute amortization-based payoff dates ("trust the math, not lender-stated maturity"). Without it, crossover can't model the future-expense-reduction line that fires when the loan is paid off. Capture P&I only (principal + interest); escrow (taxes + insurance) is a separate ongoing expense and doesn't disappear at payoff — note that distinction in the readout if the user has it bundled.

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
| `/fi:track-flow` | Doesn't read holdings.md directly, but reads transactions/ which are gitignored alongside | n/a |

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

- [ ] Run the skill end-to-end on a first-user's real holdings.
- [ ] Write the two `examples/` files.
- [ ] Stress-test gitignore enforcement on a fresh repo.
- [ ] Verify FX-rate query against api.frankfurter.dev returns expected format.
- [ ] Test what happens when the user already has a holdings.md (Step 1 branch).

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1 of the 9-step program; the catch-up framing.
- **Marika Olson** (2026). 2026 generalization of the holdings-file structure. The FX-at-read-time rule comes from a real aggregator failure case: aggregator-frozen currency conversions silently stale between syncs, producing material misreport on non-base-currency holdings.
