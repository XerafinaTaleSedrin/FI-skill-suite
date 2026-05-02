# Skill index

Map of every `fi-*` skill in the suite, with status, source, and reading dependencies.

---

## YMOYL → skills (Vicki Robin & Joe Dominguez, 1992 / 2018)

| YMOYL step | Concept | Skill | Status |
|---|---|---|---|
| 1 — Make peace with the past (a) | Total lifetime earnings | [`fi-lifetime-earnings`](fi-lifetime-earnings/SKILL.md) | scaffold |
| 1 — Make peace with the past (b) | Current net worth | [`fi-net-worth`](fi-net-worth/SKILL.md) | scaffold |
| 2 — Be in the present (a) | Real hourly wage (life-energy math) | [`fi-hourly-wage`](fi-hourly-wage/SKILL.md) | scaffold |
| 2 — Be in the present (b) | Track every dollar | [`fi-track-spending`](fi-track-spending/SKILL.md) | scaffold |
| 3 — Where is it all going? | Monthly tabulation by category | [`fi-monthly-tabulation`](fi-monthly-tabulation/SKILL.md) | scaffold |
| 4 — Three questions that will transform your life | Per-category values check | [`fi-three-questions`](fi-three-questions/SKILL.md) | scaffold |
| 5 — Make life energy visible | Long-arc wall chart | [`fi-wallchart`](fi-wallchart/SKILL.md) | scaffold |
| 6 — Minimizing spending | (chapter of tactics — likely splits across multiple skills) | TBD per tactic | not started |
| 7 — Maximizing income | (chapter of tactics — likely splits across multiple skills) | TBD per tactic | not started |
| 8 — Capital and the crossover point | FI threshold | [`fi-crossover`](fi-crossover/SKILL.md) | scaffold |
| 9 — Managing your finances | Investment management (question-asking) | [`fi-investing`](fi-investing/SKILL.md) | scaffold |

---

## Flagship skills (built first, gateway to everything else)

| Skill | Purpose | Status |
|---|---|---|
| [`fi-holdings-scaffold`](fi-holdings-scaffold/SKILL.md) | Builds the user's local `holdings.md` from scratch — every account, every holding, asset-class roll-up, net worth, gitignore enforcement | scaffold |
| [`fi-fu-money-readout`](fi-fu-money-readout/SKILL.md) | Optional daily ground-state report: net direction, runway, recurring passive income, crossover %, nuclear runway | scaffold |

`fi-holdings-scaffold` is the prerequisite for almost every other skill. `fi-fu-money-readout` is the engagement habit that keeps the holdings file fresh.

---

## Pipeline skills

| Skill | Purpose | Status |
|---|---|---|
| [`fi-audit`](fi-audit/SKILL.md) | Book audit pipeline — extracts the load-bearing mechanics from a finance/business book, separated by layer (concept / pattern / tool), with Hearth's verdict | scaffold |

---

## Cross-book derivatives

Concepts named in books OTHER than YMOYL that earn their own skill:

| Source book | Concept | Skill | Status |
|---|---|---|---|
| Mike Michalowicz, *Profit First* (2014) | Purpose-bound allocation buckets | `fi-allocation-buckets` (planned) | not started |
| Bill Perkins, *Die With Zero* (2020) | Time-buckets for life-stage spending | TBD | not started |
| Morgan Housel, *Psychology of Money* (2020) | Tail-event awareness in investing | TBD (likely folds into `fi-investing`) | not started |
| Nick Maggiulli, *Just Keep Buying* (2022) | Front-loading vs. dollar-cost averaging | TBD (likely folds into `fi-investing`) | not started |

When a book's load-bearing concept doesn't already have a home, it earns a new `fi-*` skill. When the concept refines an existing skill, the skill's `sources:` frontmatter gets the new book added — no rename, no fork.

---

## Reading dependency graph

Roughly: do these in order. Some skills can run independently once `fi-holdings-scaffold` is done.

```
fi-holdings-scaffold ─┬─→ fi-fu-money-readout (daily, optional)
                     │
                     ├─→ fi-net-worth
                     ├─→ fi-investing
                     └─→ fi-crossover ←─┐
                                        │
fi-lifetime-earnings ───→ (catch-up framing for fi-net-worth)
                                        │
fi-track-spending ─→ fi-monthly-tabulation ─→ fi-three-questions
                                       └────→ fi-wallchart ────┘

fi-hourly-wage (mode-aware, runs independently)

fi-audit (runs on any book; outputs to book-audits/)
```

---

## Status legend

- **scaffold**: SKILL.md stub exists with frontmatter + outline; not yet implementable.
- **draft**: SKILL.md is complete enough to run; needs review and testing.
- **alpha**: skill runs and produces output; rough edges remain.
- **stable**: skill is reliable; tool-register entries are current.
- **not started**: no SKILL.md yet; planned but unwritten.

---

*Last updated: 2026-05-01 (scaffold complete).*
