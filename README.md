# FI-skill-suite

> **Finance Tools Rot, Concepts Survive.**

A free, open, multi-skill suite for navigating towards financial independence — built on multiple frameworks, modernized for 2026 work modes, written to age well as the world keeps changing. Many thanks to the original authors of Your Money Or Your Life for setting the author on this journey, and to the other authors whose work will be added to the book audits in editions to come.

> **Status:** scaffold (2026-05-01). Active development. Not yet production-ready. Eventual home: a public GitHub repo under the `XerafinaTaleSedrin` GH account, posted as work by Marika Olson Consulting.

---

## What this is

A set of Claude Code skills (under the `/fi:` namespace, where **fi** stands for **financial independence**) that walk a user through the load-bearing mechanics of personal finance:

- Total lifetime earnings reconstruction
- Current net worth + holdings file
- Real hourly wage (life-energy math, work-mode-aware)
- Spending capture + monthly tabulation
- Values-fit consciousness check on each spending category
- Long-arc income/spending/passive-income wall chart
- Crossover-point math (when investment income exceeds expenses)
- Investment management as a question-asking discipline
- Daily FU money readout (optional)
- Book audit pipeline ("I read it so you didn't have to")

The skills derive their concepts from books — primarily Vicki Robin & Joe Dominguez's *Your Money or Your Life*, with refinements from Mike Michalowicz's *Profit First*, Morgan Housel's *The Psychology of Money*, Bill Perkins's *Die With Zero*, Nick Maggiulli's *Just Keep Buying*, and others as the audit pipeline grows. Books contribute to skills; books don't *own* skills.

## Who this is for

- **People who can read.** No motivational fluff. No bro-tone. No scarcity-tone. The skills assume you're already convinced personal finance matters.
- **People who like clean systems.** The architecture (see [ARCHITECTURE.md](./ARCHITECTURE.md)) is opinionated about layer separation and lifecycle hygiene. If that's appealing, you're in the right place.
- **People who want to own their data.** Holdings, transactions, lifetime earnings — all of it stays on your machine. Nothing syncs anywhere. Nothing phones home.
- **People in any country, with any tax regime.** Per-country tax reference files (community-contributed) let the skills adapt without being rewritten.
- **People at any work mode.** Fully remote, hybrid, on-site, gig — the skills ask before assuming.

## Who this isn't for

- Anyone looking for stock tips, market timing advice, or get-rich-quick patterns.
- Anyone looking for one-size-fits-all retirement age targets.
- Anyone allergic to discomfort in honest financial calculations (some of these skills will surface numbers that are genuinely uncomfortable; that's the point).

## License

Dual-licensed:

- **Content** (skills, audits, READMEs, examples, references): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) — attribution required, non-commercial only, derivatives must inherit the same license.
- **Code** (any scripts, agents, tool-register automation): [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) — non-commercial use only, source-available.

This is a deliberate choice. The repo is **explicitly free for everyone, forever, with no commercial appropriation.** Compare with [Kate Chapman's flywheel](https://github.com/Untangling-Systems/flywheel) which uses MIT (commercial-permissive) — that's a different goal. Both choices are right; they're just oriented at different outcomes.

## Getting started (when scaffold is done)

```bash
# Install as a Claude Code plugin
claude plugin install fi@https://github.com/XerafinaTaleSedrin/FI-skill-suite

# Or clone manually for customization
git clone https://github.com/XerafinaTaleSedrin/FI-skill-suite.git

# Run the foundation
/fi:holdings-scaffold      # builds your local holdings file
/fi:fu-money-readout       # daily ground-state report (optional)
```

After that, any of the YMOYL-step skills (`/fi:lifetime-earnings`, `/fi:hourly-wage`, `/fi:monthly-tabulation`, `/fi:three-questions`, `/fi:wallchart`, `/fi:crossover`, `/fi:investing`) read from the holdings file and produce their own analyses.

## Repo structure

```
FI-skill-suite/
├── .claude-plugin/
│   └── plugin.json               ← plugin manifest (name: "fi")
├── CLAUDE.md                     ← user-facing plugin instructions
├── README.md                     ← you are here
├── ARCHITECTURE.md               ← three-layer rule + half-life discipline
├── AGENTS.md                     ← cross-skill rules (DRY layer)
├── CONTRIBUTING.md               ← layer separation, license, contribution flow
├── _last-reviewed.md             ← freshness flag
├── skills/
│   ├── 00-overview.md            ← skill index + YMOYL → skill map
│   ├── holdings-scaffold/        ← /fi:holdings-scaffold — flagship #1
│   ├── fu-money-readout/         ← /fi:fu-money-readout — flagship #2
│   ├── lifetime-earnings/        ← /fi:lifetime-earnings — YMOYL Step 1a
│   ├── net-worth/                ← /fi:net-worth — YMOYL Step 1b
│   ├── hourly-wage/              ← /fi:hourly-wage — YMOYL Step 2a (mode-aware)
│   ├── track-spending/           ← /fi:track-spending — YMOYL Step 2b
│   ├── monthly-tabulation/       ← /fi:monthly-tabulation — YMOYL Step 3
│   ├── three-questions/          ← /fi:three-questions — YMOYL Step 4
│   ├── wallchart/                ← /fi:wallchart — YMOYL Step 5
│   ├── crossover/                ← /fi:crossover — YMOYL Step 8
│   ├── investing/                ← /fi:investing — YMOYL Step 9 (question-asking)
│   └── audit/                    ← /fi:audit — book audit pipeline
├── references/                   ← shared rules, per-country tax files
│   └── tax/                      ← community-contributed per-country tax content
├── tools/                        ← tool register, dated, replacement-shape
├── book-audits/                  ← outputs of /fi:audit
├── docs/                         ← Rogue Reads website (rendered from book-audits/)
└── examples/                     ← worked examples, dated
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for why the structure looks like this.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version:

- **Country tax files**: highest-leverage contribution surface. If your country doesn't have a `references/tax/<COUNTRY>.md` file, write one.
- **New tool entries**: add to `tools/` with `last-reviewed` frontmatter and a "if this dies, look for X-shape replacement" note.
- **Book audits**: run the `/fi:audit` skill on a finance/business book you've read; submit the output as a PR.
- **New skills**: less common — most concepts already have a home. If you think a new concept needs its own skill, open an issue first.

## Author / posting

- **Author**: [Marika Olson](https://marikaolson.com), via [Marika Olson Consulting](https://marikaolson.com).
- **GitHub owner**: `XerafinaTaleSedrin` (Marika's permanent code-handle; orthogonal to her professional brand).
- **Public face**: Marika Olson, MOC. Not under the Xerafina pen name (which is reserved for the Rogue Bureaucrat shelf — political commentary, separate altitude).

## Acknowledgments

- **Vicki Robin & Joe Dominguez** — *Your Money or Your Life*, the load-bearing source.
- **Kate Chapman ([@wonderchook](https://github.com/wonderchook), [Untangling Systems](https://github.com/Untangling-Systems))** — the [flywheel](https://github.com/Untangling-Systems/flywheel) skills are the architectural model. AGENTS.md / references/ / per-skill discipline patterns are all hers.
- **Morgan Housel, Bill Perkins, Nick Maggiulli, Mike Michalowicz** — concepts to be audited and folded in.
- **The federal civil service folks** who taught Marika what *enough* looks like in practice, before USAID was dismantled.
