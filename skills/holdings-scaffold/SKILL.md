---
name: holdings-scaffold
description: Builds the user's local holdings.md from scratch — accounts, holdings, asset-class roll-up, net worth, gitignore enforcement.
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 1 framing — current net worth as half of 'making peace with the past'"
last-reviewed: 2026-05-01
---

# /fi:holdings-scaffold

The flagship onboarding skill. Walks the user through populating a `holdings.md` file from scratch, account by account, with privacy enforcement built in. Every other skill in the suite reads from this file; without it, nothing else has data.

---

## The concept (decades-stable)

Knowing what you own is the prerequisite for any conscious financial decision. Most people don't know — their assets are scattered across employer-managed retirement accounts they barely look at, brokerages with auto-deposits they forgot about, foreign currency holdings, retirement contributions from old jobs, real estate equity they don't track, debts whose balances are stale. The catch-up framing of YMOYL Step 1 names this honestly: most adults are running their financial lives on partial information.

A consolidated holdings file resolves this — not as a planning tool, but as a security-blanket artifact you can read like a weather report.

---

## The pattern (~5-year stable)

A single, hand-curated, locally-owned markdown file with structured sections per account. NOT an auto-aggregated dashboard pulled from a third-party service (those go stale, lose accounts, mis-categorize, and lock you to a vendor). The hand-curated approach means:

- Updates happen on a deliberate cadence (monthly typically), not in real time.
- The file exists offline. No service can take it away.
- Schema is portable — if Claude Code goes away, the markdown still reads.
- Asset-class tagging is user-controlled, not vendor-imposed.

---

## What the skill does at runtime

1. **Picks the file location.** Default suggestions: `~/finances/holdings.md` or `<current-repo>/finances/holdings.md`. User chooses; the skill writes to wherever they pick.
2. **Enforces no-commit posture.** If the chosen location is inside a git repo, the skill adds the file path to `.gitignore` automatically. If not in a git repo, writes a clear "DO NOT COMMIT — sensitive financial data" warning header at the top of the file.
3. **Walks the user through populating it**, account by account:
   - Account name + type (Taxable / IRA / Roth / 401k / TSP / HSA / Brokerage / Foreign / Crypto / Real Estate / Debt / etc.)
   - Account balance (current; user enters, skill records)
   - Per-fund holdings (ticker, shares, value)
   - Asset-class tag per holding (US equity / intl equity / bonds / REIT / cash / commodity / crypto / other) — skill suggests based on ticker, user confirms
4. **Generates the asset-class roll-up.** Sums by tag across all accounts.
5. **Computes net worth** including non-investment assets (real estate gross value, vehicles, mortgage debt, other loans, credit card balances, foreign-currency holdings converted at runtime FX rate).
6. **Adds the catch-up framing.** YMOYL Step 1 has two halves — lifetime earnings (TODO pointer to `/fi:lifetime-earnings`) and current net worth (just populated). Skill sets up both sections of the file.
7. **Outputs a clean, structured markdown file** the user can read like a security blanket. Sections are predictable; updates can be made in any text editor.
8. **Tells the user how to keep it updated.** Monthly refresh suggested; offer to schedule the refresh as a recurring agent invocation if the harness supports it.

---

## Privacy posture

Per [AGENTS.md](../../AGENTS.md):

- File is NEVER auto-committed to git.
- File is NEVER auto-synced to cloud.
- File is NEVER sent anywhere by the skill.
- Skill validates `.gitignore` coverage before writing or warns if no git repo exists.
- Account balances, ticker holdings, and net-worth figures NEVER appear in error messages or debug output.

---

## Multi-currency / international support

- **Account types are typed, not enumerated.** Don't hard-code "Taxable / Trad IRA / Roth / TSP / Fundrise" — accept arbitrary account-type tags. TSP is a federal-employee thing; HSA is a US-employer thing; ISA is a UK thing; non-US users have RRSP / TFSA / SIPP / pension equivalents.
- **Asset classes are typed, not enumerated.** Common: US equity / intl equity / bonds / REIT / cash. User can add: crypto, commodities, private equity, direct real estate, others.
- **Currency-aware.** Each holding stored in native currency in the file. Conversion to base currency happens at read-time using a freshly-queried FX rate (not stored in the file).

**Real-world failure mode**: Aggregators (Monarch, Copilot) that pre-convert FX freeze the conversion at sync time. By the next read it's stale by potentially hundreds of dollars. Lesson for the skill: **never trust aggregator-converted figures for foreign-currency holdings; always store native currency, convert at read-time.**

---

## Schema

The skill writes to `holdings.md` using a stable schema. See [SCHEMA.md](./SCHEMA.md) (TODO: write this file) for the exact YAML/markdown structure other skills can read from.

Roughly:

```markdown
---
last-updated: YYYY-MM-DD
base-currency: USD
---

# Holdings

## Account: [name]
- type: [tag]
- balance: [native amount + currency]
- holdings:
  - [ticker]: [shares] @ [price native] = [value native]
    asset-class: [tag]

(repeat per account)

## Asset-class roll-up
- US equity: $X (XX%)
- ... (computed)

## Net worth (current)
- Investment accounts: $X
- Real estate (gross): $X
- Vehicles: $X
- Cash: $X
- Debt: -$X
- **Net: $X**
```

---

## Headless behavior

Not generally headless — this is an interactive walkthrough by design. If invoked headlessly, the skill should fail loudly with an error explaining it requires interactive input.

Future option: read from a YAML manifest file (`holdings-input.yaml`) and skip prompts when the manifest is present. Allows scripted re-population for users with hundreds of accounts. Not yet implemented.

---

## TODO

- [ ] Write `SCHEMA.md` documenting the exact `holdings.md` structure other skills read.
- [ ] Implement runtime FX conversion (likely WebFetch to ECB / FRED).
- [ ] Define the manifest-input schema for batch population.
- [ ] Worked example: full session run for a typical 5-account US user (in `examples/`).
- [ ] Worked example: full session run for a multi-currency UK+US user (in `examples/`).
- [ ] Cross-skill data contract section: explicit schema for `/fi:net-worth`, `/fi:fu-money-readout`, `/fi:crossover` to read.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1 of the 9-step program; the catch-up framing.
- **Marika Olson** (2026). The holdings-file structure was built for personal use first, then generalized into this skill.
