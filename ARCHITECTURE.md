# Architecture

The architectural choices in `FI-skill-suite` exist to solve one specific problem: **personal finance content rots.** YMOYL was published in 1992, last meaningfully updated in 2018. By 2026 — a 5-year-or-less gap — significant chunks of its math no longer hold (bond yields, contribution limits, tools that no longer exist, work modes that didn't exist when it was written). Profit First (2014) is starting to show similar gaps. Any book or skill written today will face the same drift in 5-10 years.

Rather than write skills that will rot, this repo enforces a discipline that lets the durable parts persist while the time-sensitive parts get replaced.

---

## The three-layer rule (the YMOYL-mistake fix)

Every concept, pattern, and tool reference in this repo lives at one of three layers, with explicit half-lives:

### Layer 1 — Concept (decades)

The principles. The mental models. The questions worth asking. The mechanics that survive across economic regimes.

Examples:
- "Reduce ownership weight in proportion to your real life-energy cost."
- "Calculate real hourly wage by subtracting work-related costs from gross income, and adding work-related hours to the denominator."
- "Track every dollar — automation if available, manual capture if not."
- "Run a values-fit filter on every spending category at least quarterly."
- "Plot life energy on an arc to see whether spending and investment income cross."

**Where it lives:** inside each skill's `SKILL.md`. Concepts are the heart of the skill; they shouldn't move.

**Half-life:** decades. If a concept's half-life turns out to be < 10 years, it was probably actually a *pattern* and got mis-promoted. Demote and re-think.

### Layer 2 — Pattern (~5 years)

The shape of an implementation, abstracted from the specific tool. The kind of solution that keeps working even as specific tools rotate underneath it.

Examples:
- "Use a low-friction resale platform with buyer-trust mechanisms" (not "use Mercari").
- "Automate transaction capture so tracking doesn't require willpower" (not "use Monarch").
- "Bucket your operating cash inside one bank that supports purpose-tagged sub-accounts" (not "split across 5 separate banks à la Profit First").
- "Hold an emergency fund in a high-yield account that's accessible within 2 business days" (not "use Marcus by Goldman Sachs at 4.4%").
- "Use a brokerage that supports automated dividend reinvestment, low-cost index funds, and tax-loss harvesting" (not "use Vanguard").

**Where it lives:** inside each skill's `SKILL.md` alongside the concept. Patterns are slower-changing than tools but faster-changing than concepts.

**Half-life:** ~5 years. If the shape of a solution category changes (e.g., the rise of decentralized finance, the death of physical banks), the pattern needs revision.

### Layer 3 — Tool (1-3 years)

The specific named thing. Today's app, today's bank, today's tax threshold, today's contribution limit, today's bond yield.

Examples:
- "Mercari, Depop, Flip" (resale platforms, mid-2026).
- "Monarch, Copilot, Lunch Money" (transaction aggregators, mid-2026).
- "Ally, BlueVine, Relay, Found" (banks supporting buckets, mid-2026).
- "$23,500 401(k) contribution limit; $7,000 IRA" (US 2025 limits).
- "10-year Treasury yield ~4.2%" (mid-2026).

**Where it lives:** in `tools/` — separate files, dated frontmatter, replacement-shape notes.

**Half-life:** 1-3 years. By design, tool entries go stale. The discipline is *making the staleness obvious* — every file has `last-reviewed: YYYY-MM-DD` and an "if this dies, look for X-shape replacement" hint that points back to the pattern layer.

---

## Why this matters in practice

**Skills don't reach down to tools directly.** A skill like `/fi:hourly-wage` operates at the concept + pattern layer ("subtract work-related costs"; "use category-based capture"). It doesn't say "use Monarch." It says "use a transaction aggregator (current options: see tools/aggregators.md)."

**Tools don't bleed up into skills.** When Monarch dies (and one day it will), `/fi:hourly-wage` doesn't break. The tool register gets updated, a new aggregator gets named, the skill keeps working.

**The README always tells the reader: read concepts first, then patterns, then tools.** Descend the layers. Don't start at tools — they're the most likely to be dated.

**Old tool snapshots stay in git history (version-tag releases)** so a 2031 reader can see what was named in 2026, dated, and judge for themselves.

---

## Per-country tax content lives in the tool layer

Tax rules are tool-layer (1-3 year half-life — rates change yearly, structures every few years). They live in `references/tax/` so contributors can add their own country without touching the concept-layer skills.

Schema: each `references/tax/<COUNTRY>.md` file follows a uniform structure (account types available, contribution limits, tax-deferred vs. tax-free vs. taxable hierarchy, current rates, last-reviewed date) so concept-layer skills can read any country file structurally.

Concept-layer skills like `/fi:hourly-wage` and `/fi:crossover` are **tax-agnostic** — they don't reach into the tax files at all. Only `/fi:redirect`, the eventual `/fi:allocation-buckets`, and the placement-audit skill care about the tax layer.

This is the natural community-contribution surface. Marika authors `US.md` (her actual expertise). Other contributors author their own country files. Pin a "Country tax files needed — community contributions welcome" issue.

---

## Per-skill structure

Every skill folder has at minimum:

```
skills/<concept>/
├── SKILL.md            ← concept + pattern + frontmatter
└── (optional) examples/  ← worked examples specific to this skill
```

Skill folder names use the bare concept (e.g., `holdings-scaffold/`, `hourly-wage/`). The `fi` namespace is applied automatically by the plugin manifest, so skills are invoked as `/fi:<concept>` (e.g., `/fi:holdings-scaffold`).

The SKILL.md frontmatter declares:

```yaml
---
name: <concept>
description: One-line purpose.
layer: concept | concept+pattern | concept+pattern+tool
ymoyl_step: 1 | 2 | 3 | … | n/a
mode_aware: true | false
sources:
  - book: Your Money or Your Life
    contribution: short note on what this book contributes
  - book: Profit First
    contribution: short note
last-reviewed: 2026-05-01
---
```

The body of `SKILL.md` covers:

1. **The concept** — what's the load-bearing idea (decades-stable).
2. **The pattern** — what shape of implementation (5-year stable).
3. **What the skill actually does at runtime** — the agentic flow.
4. **Headless behavior** — what the skill does when fired by a cron / pipeline with no human.
5. **Mode-awareness** — if applicable, branching logic for user circumstances (work mode, country, life stage).
6. **Runtime freshness checks** — what the skill verifies vs. what it pulls from disk.
7. **User-extensible categories** — if applicable, capture loop + community submission.
8. **Sources** — books that contributed concepts.
9. **Cross-references** — which other skills this one reads from / writes to.

---

## Runtime freshness — first-class architectural feature

Every skill that touches anything time-sensitive (rates, thresholds, platforms, account types, regulatory limits) must include a runtime "is this still true?" loop the agent runs at invocation. **Skills should *ask* and *verify* current state, not hard-code numbers.**

Killer example: YMOYL-era bond yields were ~15%, making "park your savings in long-term Treasuries and live off the interest" sound math. 2026 yields are ~4%. A skill that hard-coded the 15% assumption would silently mislead a 2026 user into financial ruin. A skill that asks "what's the current 10-year Treasury yield?" — or queries it via WebFetch when MCP/web tools are available — stays honest forever.

Three checks every relevant skill should run:

1. **Does the named tool/platform/institution still exist?** ("Does Ally Bank still offer buckets-within-account?")
2. **What's the current value of the rate/threshold/limit this calculation depends on?** ("What's the current 401(k) contribution limit? Bond yield? Inflation rate?")
3. **What does the user have available?** ("Which bank do you use? Does it support buckets natively, or do you need workarounds?")

The first two are external-state checks. The third is the user-state loop. Together they're the **concept + current-state pattern.**

---

## User-extensible categories with community-learning loop

Distinct architectural feature. This pattern lets users contribute back to canonical content with maintainer curation:

1. Skill asks user about custom categories or line items at runtime.
2. Captures user's custom inputs locally (in their session, in their own repo).
3. At session end, surfaces an opt-in prompt: *"If you think this category would help others, share it via [GitHub Discussions / issue link]."* User decides whether to submit. Never automatic.
4. Maintainer (Marika initially) periodically reviews submissions. When the same custom category recurs across multiple users, it's signal worth promoting to canonical — with attribution.
5. Promotion happens via normal PR flow into the relevant skill, with the user-suggested category added to the core list and a credit line.

This pattern stays out of any data-collection / privacy minefield (no auto-telemetry, no analytics, fully opt-in user-initiated submission), while giving the project a path to *learn* from collective use without the maintainer having to predict every category in advance.

---

## What's deliberately NOT in this architecture

- **No telemetry, no analytics, no phone-home.** The skills run locally and stay local.
- **No cloud sync of user data.** Holdings, transactions, all financial files — gitignored or off-repo. The user owns it.
- **No platform lock-in.** Country-aware, bank-agnostic, aggregator-agnostic. If your tools change, the skills adapt.
- **No "premium tier."** It's all free. CC BY-NC-SA 4.0 ensures it stays free.
- **No motivational framing.** The skills are operational tools, not affirmations.

---

## Open architectural questions

Listed for future iterations:

- **How does the suite handle joint finances?** Two-person households with combined holdings + separate values-fit filters need careful design.
- **How does the suite handle non-USD primary currencies?** First-class multi-currency design vs. base-currency mode toggle.
- **How does the suite handle inheritance flows?** Receiving an estate is a real transition that breaks the assumption of "all your wealth came from work."
- **Hearth integration** — Marika's companion-cat figure has an explicit role in book audits (mandatory verdict line). Does Hearth show up across other skills, or stay scoped to audits?
