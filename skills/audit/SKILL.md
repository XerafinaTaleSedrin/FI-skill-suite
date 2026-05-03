---
name: audit
description: Book audit pipeline — extracts the load-bearing mechanics from a finance/business book, separated by layer (concept / pattern / tool), with Hearth's verdict.
layer: concept+pattern
ymoyl_step: n/a
mode_aware: false
status: scaffold
sources:
  - book: (any finance/business book the user wants to audit)
last-reviewed: 2026-05-01
---

# /fi:audit

The book audit skill. Strips persona, surfaces the load-bearing mechanics, separates concept-pattern-tool layers, and delivers Hearth's verdict on every book audited. Output feeds the rest of the suite — when a load-bearing mechanic shows up in an audit, it earns its way into a `fi-*` skill (or refines an existing one's `sources:`).

---

## The concept (decades-stable)

Most finance books are 30% load-bearing mechanic, 70% rhetorical packaging. The audit pipeline strips the packaging and surfaces the mechanic in plain terms — separated by which layer it belongs in (concept / pattern / tool), so the time-sensitive parts can be tagged for replacement and the durable parts can be incorporated.

The 5-line takeaway is the deliverable. Everything else is supporting evidence.

---

## The pattern (~5-year stable)

Sequential prompt-driven extraction with a fixed output format. The skill asks the same questions of every book; the answers go into a structured audit file. Output is reusable: feeds book-audits/ folder, the suite's READMEs, IG carousels, and concept refinements across skills.

---

## What the skill does at runtime

1. Asks: which book? (Title, author, publication year, edition.)
2. Asks: have you read it, or are you working from notes?
3. Walks through the extraction prompts (see below).
4. Captures the user's responses verbatim where blunt; structures the output to the fixed audit format.
5. Asks for Hearth's verdict (one-line cat-take, mandatory).
6. Writes the audit to `book-audits/YYYY-MM-DD-<book-slug>.md`.
7. **Privately** (not in the audit itself): notes for Marika which existing `fi-*` skills should add this book to their `sources:`. The audit stays clean for the business-interested reader; repo-wiring lives in the SKILL.md files where it belongs.

---

## Audit output format (per book)

```
1. The premise in one paragraph (no jargon)
2. The load-bearing mechanic — the 1-3 actual moves the book proposes
3. What aged well (still applicable in 2026)
4. What aged poorly (era-bound math, dead assumptions, vibes-based claims)
5. What's missing (things the book ignores that matter now)
6. The honest verdict — who should read it, who should skip it
7. The 5-line takeaway you'd actually run
8. **Hearth's verdict** — one-line cat-take. Mandatory. Tonal range:
   nap-worthy / hiss-worthy / windowsill-approved / would-knock-off-the-desk.
   Hearth speaks for herself; she's not a tagline machine.
```

The audit is for the business-interested reader. Repo-internal mappings (which `fi-*` skills this book contributes to, deletion records, refinement notes for existing source lists) live in the SKILL.md files of the relevant skills, NOT in the audit. Keep the two surfaces separate.

---

## Extraction prompts

**System frame:**

> You are evaluating a personal finance / business finance book on behalf of a reader who is sharp, financially literate, and allergic to bro-tone, scarcity-tone, and outdated math. The reader does not need to be sold on the importance of money management. They want the load-bearing ideas separated from the rhetorical packaging. Be blunt. If the math is dated, say so. If the premise no longer holds in [current year], say so. If the author is performing a persona that gets in the way of the substance, name it. Do not soften.

**Per-book extraction prompts:**

- *"Strip the persona. What is the actual claim?"*
- *"What numerical assumptions does this book make? Which of them are still true in [current year]?"*
- *"What does this book ignore that a reader in [current year] needs to think about?"* (high-deductible health plans, HSAs, gig income, AI displacement, geographic arbitrage, etc.)
- *"What survives if you remove every motivational paragraph?"*
- *"Who is this book actually written for, and is that person the same as the reader today?"*
- *"What's the smallest version of this book's advice — the 5-bullet operating manual?"*
- *"Which load-bearing mechanic from this book belongs in the concept layer? Which belongs in the pattern layer? Which is purely a tool-of-the-moment that will rot?"*

**Output guardrails:**
- No hedging language ("it depends", "everyone's different") — pick a side
- No promotional copy from the author's marketing — work only from the book's actual claims
- Cite chapter titles (or step numbers, for stepwise books) for every load-bearing claim. Page numbers are optional — they edition-drift quickly and aren't load-bearing.
- Translate every dollar figure into [current year] purchasing power if the book is >5 years old
- For each surviving mechanic, tag the layer it belongs in (concept / pattern / tool)

---

## Headless behavior

Not headless — extraction requires interaction. Future option: read from a structured input file (book metadata + user's pre-written notes) and run the extraction non-interactively.

---

## TODO

- [ ] Build the IG-carousel slice — auto-generate a 5-slide carousel from the audit.
- [ ] Build the cross-reference detection (suggest privately to Marika which `fi-*` skills should add this book to `sources:` — the audit stays clean of repo-mapping).
- [ ] Worked audits in `book-audits/` for YMOYL, Profit First, Psychology of Money, Just Keep Buying, Die With Zero.

---

## Sources

The sources for this skill are the books that get audited. The skill itself derives from observation of common patterns in finance-book persona vs. substance, with notes from Marika Olson's reading list (2026).
