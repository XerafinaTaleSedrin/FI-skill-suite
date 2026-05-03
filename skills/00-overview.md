# Skill index

Map of every skill in the suite, with status, source, and reading dependencies.

All skills are namespaced under the `fi` plugin and invoked as `/fi:<skill-name>` (e.g., `/fi:holdings-scaffold`).

---

## YMOYL → skills (Vicki Robin & Joe Dominguez, 1992 / 2018)

| YMOYL step | Concept | Skill | Status |
|---|---|---|---|
| 1 — Make peace with the past | Current net worth (the "weather report" framing) | [`/fi:holdings-scaffold`](holdings-scaffold/SKILL.md) | draft |
| 2 — Be in the present (a) | Real hourly wage (life-energy math) | [`/fi:hourly-wage`](hourly-wage/SKILL.md) | scaffold |
| 2 + 3 — Track every dollar / Monthly tabulation | Unified flow capture + categorization + tabulation + neutral pattern detection | [`/fi:track-flow`](track-flow/SKILL.md) | scaffold |
| 4 — Three questions that will transform your life | Per-category values check | [`/fi:three-questions`](three-questions/SKILL.md) | scaffold |
| 5 — Make life energy visible | Long-arc wall chart | [`/fi:wallchart`](wallchart/SKILL.md) | scaffold |
| 6 — Minimizing spending | (chapter of tactics — likely splits across multiple skills) | TBD per tactic | not started |
| 7 — Maximizing income | (chapter of tactics — likely splits across multiple skills) | TBD per tactic | not started |
| 8 — Capital and the crossover point | FI threshold (incl. SSA-benefit projection input) | [`/fi:crossover`](crossover/SKILL.md) | scaffold |
| 5 + 9 — Redirect surplus / Manage capital | Debt paydown AND investment deployment, weighed against each other (question-asking) | [`/fi:redirect`](redirect/SKILL.md) | scaffold |

> **YMOYL Step 1 — what we don't implement.** YMOYL prescribes Step 1 as having two halves: current net worth AND total lifetime earnings reconstruction. We implement only the first. The lifetime-earnings half was load-bearing in 1992 (single career, regular paycheck, motivated by guilt-prompted action) but lands in 2026 as a shame mechanic that distorts dignified non-paycheck years (caregiving, immigration, illness, recovery, RIF, federal service capped at the SSA wage base). See `book-audits/2026-05-01-ymoyl.md` §8 for full reasoning. The operational pieces survive elsewhere: SSA benefit projection folds into `/fi:crossover` as a single prompt; SSA earnings-record audit is a one-time task documented but not skilled.

---

## Flagship skills (built first, gateway to everything else)

| Skill | Purpose | Status |
|---|---|---|
| [`/fi:holdings-scaffold`](holdings-scaffold/SKILL.md) | Builds the user's local `holdings.md` from scratch — every account, every holding, asset-class roll-up, net worth, gitignore enforcement | **draft** ← first runnable skill |
| [`/fi:fu-money-readout`](fu-money-readout/SKILL.md) | Optional daily ground-state report: net direction, runway, recurring passive income, crossover %, nuclear runway. **"FU" is intentional — established FI slang for "fuck-you money" (enough to walk away from any situation). Not a typo of "FI."** | scaffold |

`/fi:holdings-scaffold` is the prerequisite for almost every other skill. `/fi:fu-money-readout` is the engagement habit that keeps the holdings file fresh.

---

## Pipeline skills

| Skill | Purpose | Status |
|---|---|---|
| [`/fi:audit`](audit/SKILL.md) | Book audit pipeline — extracts the load-bearing mechanics from a finance/business book, separated by layer (concept / pattern / tool), with Hearth's verdict | scaffold |

---

## Cross-book derivatives

Concepts named in books OTHER than YMOYL that earn their own skill:

| Source book | Concept | Skill | Status |
|---|---|---|---|
| Mike Michalowicz, *Profit First* (2014) | Purpose-bound allocation buckets | `/fi:allocation-buckets` (planned) | not started |
| Bill Perkins, *Die With Zero* (2020) | Time-buckets for life-stage spending | TBD | not started |
| Morgan Housel, *Psychology of Money* (2020) | Tail-event awareness in investing | TBD (likely folds into `/fi:redirect`) | not started |
| Nick Maggiulli, *Just Keep Buying* (2022) | Front-loading vs. dollar-cost averaging | TBD (likely folds into `/fi:redirect`) | not started |

When a book's load-bearing concept doesn't already have a home, it earns a new skill under the `fi` namespace. When the concept refines an existing skill, the skill's `sources:` frontmatter gets the new book added — no rename, no fork.

---

## Reading dependency graph

Roughly: do these in order. Some skills can run independently once `/fi:holdings-scaffold` is done.

```
/fi:holdings-scaffold ─┬─→ /fi:fu-money-readout (daily, optional)
                      │
                      ├─→ /fi:hourly-wage  (the natural Step-2 forward-look)
                      ├─→ /fi:redirect
                      └─→ /fi:crossover
                                          │
/fi:track-flow ─→ /fi:three-questions
              └─→ /fi:wallchart

/fi:audit (runs on any book; outputs to book-audits/)
```

---

## Status legend

- **scaffold**: SKILL.md stub exists with frontmatter + outline; not yet implementable.
- **draft**: SKILL.md is complete enough to run; needs review and testing.
- **alpha**: skill runs and produces output; rough edges remain.
- **stable**: skill is reliable; tool-register entries are current.
- **not started**: no SKILL.md yet; planned but unwritten.

---

*Last updated: 2026-05-02 (folder rename + plugin packaging — all skills now namespaced under `/fi:`).*
