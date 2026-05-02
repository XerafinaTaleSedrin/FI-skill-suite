# FI-skill-suite — Claude Code plugin instructions

> **Tools rot. Concepts survive.**

This file is loaded automatically when Claude Code reads a project where the `fi` plugin is installed. It tells Claude how to use the suite.

---

## What this plugin does

A multi-skill suite for navigating financial independence. Each skill walks the user through one load-bearing mechanic of personal finance — calculating real hourly wage, tracking every penny, computing crossover point, auditing finance books — with the source concepts deliberately separated from the tools that come and go.

The architectural rule (full detail in [`ARCHITECTURE.md`](./ARCHITECTURE.md)): every concept, pattern, and tool reference in this suite has a declared half-life. **Concepts last decades. Patterns last ~5 years. Tools last 1–3.** Skills only reach down to tools through a tool register, so when tools rot the concepts don't.

## Available skills

All skills are invoked under the `fi` namespace. The 12 currently defined:

### Foundation (start here)

| Skill | Invocation | Purpose |
|---|---|---|
| Holdings scaffold | `/fi:holdings-scaffold` | Build the user's local `holdings.md` from scratch — accounts, holdings, asset-class roll-up, net worth, gitignore enforcement |
| FU money readout | `/fi:fu-money-readout` | Optional daily ground-state report: net direction, runway, recurring passive, crossover %, nuclear runway |

### YMOYL nine-step program

| Skill | Invocation | YMOYL Step |
|---|---|---|
| Lifetime earnings | `/fi:lifetime-earnings` | 1a — total earnings reconstruction |
| Net worth | `/fi:net-worth` | 1b — current net worth |
| Hourly wage | `/fi:hourly-wage` | 2a — real hourly wage (work-mode-aware) |
| Track spending | `/fi:track-spending` | 2b — every-penny capture |
| Monthly tabulation | `/fi:monthly-tabulation` | 3 — category aggregation with life-energy cost |
| Three questions | `/fi:three-questions` | 4 — values-fit consciousness check |
| Wall chart | `/fi:wallchart` | 5 — long-arc income/spending/passive chart |
| Crossover | `/fi:crossover` | 8 — FI threshold (mode-aware) |
| Investing | `/fi:investing` | 9 — investment management as question-asking |

### Editorial pipeline

| Skill | Invocation | Purpose |
|---|---|---|
| Book audit | `/fi:audit` | Run a finance/business book through the audit format. Produces a `book-audits/YYYY-MM-DD-<slug>.md` artifact. Hearth's verdict mandatory. |

## Privacy posture (every skill)

Strict, non-negotiable rules enforced across all skills:

1. **Never auto-commit user financial files to git.** Skills validate `.gitignore` coverage before writing or warn if no git repo exists.
2. **Never auto-sync user data anywhere.** No phone-home, no telemetry, no cloud backup unless the user explicitly invokes one.
3. **Never log sensitive content to debug output.** Account balances, ticker holdings, net-worth figures NEVER appear in error messages or stack traces.
4. **Holdings, transactions, lifetime earnings stay on the user's machine.** Period.

## Where outputs go

Skills write to predictable, gitignored locations on the user's machine. Default paths (user can override):

- Holdings: `~/finances/holdings.md`
- Lifetime earnings: `~/finances/lifetime-earnings.md`
- Transactions: `~/finances/transactions/YYYY-MM.csv`
- Monthly tabs: `~/finances/monthly-tabs/YYYY-MM.md`
- Wall chart: `~/finances/wallchart.md`
- FU money log: `~/finances/fu-money-log/YYYY-MM-DD.md`

Book audits (NOT user-private) go in the plugin's own repo at `book-audits/`.

## Reading order if you're new to the user's setup

1. Check whether `~/finances/holdings.md` exists. If not, `/fi:holdings-scaffold` is the gateway — every other skill reads from that file.
2. After holdings exists, `/fi:fu-money-readout` provides daily orientation. Other skills (`/fi:net-worth`, `/fi:crossover`, `/fi:investing`) all read from holdings.
3. The YMOYL Step 2-5 skills (hourly-wage, track-spending, monthly-tabulation, three-questions, wallchart) chain together: each reads from the previous.

## Runtime freshness

Every skill that touches time-sensitive content (rates, contribution limits, platform availability) MUST run a "is this still true?" check at invocation time rather than hard-coding values. See [`AGENTS.md`](./AGENTS.md) §Runtime freshness for the full rule.

## Cross-skill rules

See [`AGENTS.md`](./AGENTS.md) for the DRY layer — privacy posture, headless mode, schema discipline, file operations, cross-skill data contracts.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Short version: country tax files and tool register entries are the highest-leverage contribution surface. Audits are CLOSED to community submissions (voice integrity).

## License

- **Content** (skills, audits, READMEs, references): CC BY-NC-SA 4.0
- **Code** (any scripts, tooling): PolyForm Noncommercial 1.0.0

This is a deliberate choice. The repo is **explicitly free for everyone, forever, with no commercial appropriation.**

## Author

Marika Olson, via [Marika Olson Consulting](https://marikaolson.com). Plugin hosted on [`XerafinaTaleSedrin/FI-skill-suite`](https://github.com/XerafinaTaleSedrin/FI-skill-suite).
