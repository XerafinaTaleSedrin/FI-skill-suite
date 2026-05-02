# Contributing to FI-skill-suite

Thank you for considering a contribution. Read this end-to-end before opening a PR — most review feedback comes from missed conventions, not bad code.

---

## Where contributions are welcome

In rough order of value to the project:

1. **Per-country tax reference files** (`references/tax/<COUNTRY>.md`). The highest-leverage surface. If your country isn't represented, please contribute. Schema in [`references/tax/_country-template.md`](references/tax/_country-template.md).
2. **Tool register entries** (`tools/`). New aggregators, banks, brokerages, or platforms that fit one of the existing tool categories. Each entry needs `last-reviewed: YYYY-MM-DD` and a "if this dies, look for X-shape replacement" hint.
3. **Book audits** (`book-audits/`). Run the `/fi:audit` skill on a finance/business book and submit the output. Use the audit template; include Hearth's verdict.
4. **User-extensible category submissions**. After running a skill, if you added a custom category that you think generalizes (e.g., a work-related expense category that wasn't in the canonical list), open an issue or discussion to suggest promotion. Maintainer reviews; if the same category recurs across submissions, it gets promoted with attribution.
5. **Documentation fixes, typo corrections, link updates**. Always welcome.
6. **New skills**. Less common — most concepts already have a home. **Open an issue first** to discuss before writing the skill.

---

## What's NOT welcome

- Telemetry or analytics of any kind. The privacy posture is non-negotiable.
- Cloud-sync features that move user data off-device.
- "Premium" features locked behind a paywall.
- AI-generated content that hasn't been reviewed by a human contributor (see "AI assistance" below).
- Promotional content for specific paid services or financial advisors.
- Content that assumes a single country, currency, or work mode without flagging the assumption.

---

## License

By contributing, you agree your contribution will be released under:

- **Content**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **Code**: [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/)

If your contribution can't be released under those terms, please don't submit it.

---

## The layer-separation rule

All content in this repo lives at one of three layers (full detail in [ARCHITECTURE.md](./ARCHITECTURE.md)):

- **Concept (decades)** — the principles. Lives in `SKILL.md`.
- **Pattern (~5 years)** — the shape of an implementation, abstracted from the specific tool. Lives in `SKILL.md` alongside concepts.
- **Tool (1-3 years)** — specific named platforms, current rates, current contribution limits. Lives in `tools/` with explicit `last-reviewed` dates.

**Before submitting a PR, identify which layer your contribution belongs in.** Mis-layered content is the most common rejection reason.

Quick rule of thumb:

| You're submitting… | Layer | Goes in |
|---|---|---|
| A principle that's true regardless of country, era, or tools | Concept | `skills/<skill>/SKILL.md` |
| An implementation pattern that survives tool changes | Pattern | `skills/<skill>/SKILL.md` (alongside concept) |
| A specific app, bank, rate, or limit | Tool | `tools/<category>.md` |
| Country-specific tax content | Tool (with structure) | `references/tax/<COUNTRY>.md` |
| A book extraction | n/a (audit format) | `book-audits/<date>-<slug>.md` |

If you're not sure, open a discussion before opening a PR.

---

## Style conventions

### Naming convention — capital FI vs lowercase fi

- **`FI`** (capital) is the proper-noun acronym for **Financial Independence** — used in the project name, repo name, and suite-level branding (`FI-skill-suite`).
- **`fi`** (lowercase) is the **plugin name** declared in `.claude-plugin/plugin.json`, which Claude Code automatically applies as the slash-command namespace. So skills are invoked as `/fi:hourly-wage`, `/fi:crossover`, etc. — same shape as Kate Chapman's `/fw:` flywheel namespace and `/sw:` switch namespace.
- **Skill folder names** drop any prefix (just `hourly-wage/`, `crossover/`, etc.) — the `fi` namespace is applied automatically by the plugin manifest, so prefixing the folder names would create redundant `/fi:fi-hourly-wage` invocations.

When in doubt: project / repo / brand context = capital FI. Plugin name / slash-command namespace = lowercase fi. Skill folder name = bare concept (no prefix).

### File naming

- All `SKILL.md` files live at `skills/<skill-name>/SKILL.md`. The folder name is the bare concept (e.g., `hourly-wage`, NOT `fi-hourly-wage`). The skill is invoked as `/fi:<skill-name>`.
- Tool register files use kebab-case category names: `tools/transaction-aggregators.md`, `tools/high-yield-savings.md`.
- Country tax files use ISO country codes: `references/tax/US.md`, `references/tax/GB.md`, `references/tax/CA.md`.
- Book audit files: `book-audits/YYYY-MM-DD-<book-slug>.md` (date is audit date, not publication date).

### Frontmatter

Every Markdown file with structured metadata has YAML frontmatter at the top:

```yaml
---
key: value
last-reviewed: 2026-05-01
---
```

Required fields per file type:

| File type | Required fields |
|---|---|
| `SKILL.md` | `name`, `description`, `layer`, `ymoyl_step`, `mode_aware`, `sources`, `last-reviewed` |
| `tools/<category>.md` | `category`, `last-reviewed` |
| `references/tax/<COUNTRY>.md` | `country`, `country_code`, `last-reviewed` |
| `book-audits/<file>.md` | `book`, `author`, `published`, `audited`, `auditor`, `hearth_verdict` |

### Headings

- **Don't put attribution or version info in headings.** See [AGENTS.md](./AGENTS.md) §Heading discipline.
- Use `##` for top-level sections, `###` for subsections. `#` is reserved for the document title.
- Headings should be readable as instructions to an AI agent — clear, concrete, no rhetorical flourishes.

### Tone

- Direct, blunt, no hedging.
- No motivational language.
- No pitch stories "let me tell you about user X..."
- Honest numbers, even when uncomfortable.
- Acknowledge when source material is dated or wrong.
- See [AGENTS.md](./AGENTS.md) §Tone for the full rule.

---

## AI assistance in contributions

This project is built using Claude Code, and contributors may use AI assistance. Two ground rules:

1. **Disclose AI assistance in your PR description.** Not as a disqualifier — just so reviewers know the provenance of the content. "Drafted with Claude, edited by hand" is fine. "Generated wholesale by an LLM and not read" is not fine.
2. **Validate any factual claims yourself.** Especially in tool register entries and tax reference files. AI gets contribution limits, current rates, and platform features wrong constantly. If you write that the 2026 401(k) limit is $23,500, verify it against the IRS's published limits before submitting.

---

## PR workflow

1. **Open an issue first** for non-trivial changes (new skills, schema changes, removed content). Quick fixes (typos, broken links, doc updates) can skip this step.
2. **Fork + branch.** Branch name should describe the change concisely: `add-tax-NL`, `fix-hourly-wage-headless`, `audit-housel`.
3. **One logical concern per PR.** If the diff needs an "AND" or "+" in the title, split it.
4. **Run any tests / validations specified in `AGENTS.md`.** When validation tooling exists for SKILL.md schemas, it'll be referenced here.
5. **Update the structure diagram in `README.md`** if you're adding a new sentinel file or directory.
6. **Bump version + add CHANGES entry** if applicable (see versioning section below).
7. **Open the PR with a clear description**: what changed, why, what layer, any AI assistance disclosed.
8. **Be responsive to review.** Maintainer is Marika Olson initially; review cadence is "weekly when possible." Patient PRs get merged; abandoned ones get closed after 60 days.

---

## Versioning + releases

(To be defined when the repo goes public. Initial scaffold is pre-versioning.)

Planned approach:
- Semantic versioning (`MAJOR.MINOR.PATCH`).
- Tagged releases when meaningful changes ship.
- `CHANGES.md` (or `CHANGELOG.md`) maintained at the repo root.
- Tool-register snapshots tagged at minor releases so old snapshots are recoverable for historical reference.

---

## Reporting issues

- **Bug reports**: open a GitHub issue with reproduction steps. Don't include any of your personal financial data in the report.
- **Privacy concerns**: open a GitHub issue tagged `privacy`. Privacy is non-negotiable; valid concerns get prioritized.
- **Conceptual disagreements**: open a GitHub Discussion. The architectural choices are opinionated; we welcome challenge but don't always change them.

---

## Conduct

Be a good colleague. The audience for this project is people who are sometimes anxious about money, sometimes ashamed of past decisions, sometimes trying to undo years of bad financial advice. They may have never considered their financial situation in detail, or realized they they had agency in improving it. Reviewers and contributors should be patient, specific, and humane. Check your priviledge. 

Specifically NOT welcome:
- Bro-y tone in PRs or issues
- "Why don't you just" responses to genuine confusion
- Mocking of country-specific quirks (e.g., "lol Americans and your 401(k)s")
- Performative cleverness in code reviews
- Gatekeeping based on financial sophistication
- Pitches or inclusion of unproven, unstable assets. This is not the audience for your cryptocurrency pitch. 

---

## Acknowledgments

Patterns adapted from Kate Chapman's [flywheel](https://github.com/Untangling-Systems/flywheel) repo. If you've contributed there, the patterns will feel familiar.
