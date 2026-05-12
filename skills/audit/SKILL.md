---
name: audit
description: Book audit pipeline — extracts the load-bearing mechanics from a finance/business book, separated by layer (concept / pattern / tool), with Hearth's verdict. Output is a long-form Markdown audit in `book-audits/`.
layer: concept+pattern
ymoyl_step: n/a
mode_aware: false
status: draft
sources:
  - book: (any finance/business book the user wants to audit)
  - author: Marika Olson
    contribution: "2026 design — load-bearing-mechanic + persona-strip + Hearth verdict format, multi-session resumability, layer tagging for downstream skill refinement"
worked_example: book-audits/2026-05-01-ymoyl.md
last-reviewed: 2026-05-12
---

# /fi:audit

The book audit skill. Strips persona, surfaces the load-bearing mechanics, separates concept-pattern-tool layers, and delivers Hearth's verdict on every book audited. Output feeds the rest of the suite — when a load-bearing mechanic shows up in an audit, it earns its way into a `fi-*` skill (or refines an existing one's `sources:`).

**Worked example**: `book-audits/2026-05-01-ymoyl.md` (Your Money or Your Life, audited 2026-05-01). That's the shape and depth a finished audit should reach. The 8-section template is the starting frame; the audit grows as deep as the book deserves.

---

## The concept (decades-stable)

Most finance books are 30% load-bearing mechanic, 70% rhetorical packaging. The audit pipeline strips the packaging and surfaces the mechanic in plain terms — separated by which layer it belongs in (concept / pattern / tool), so the time-sensitive parts can be tagged for replacement and the durable parts can be incorporated.

The 5-line takeaway is the deliverable. Everything else is supporting evidence.

---

## The pattern (~5-year stable)

Sequential prompt-driven extraction with a fixed output format. The skill asks the same questions of every book; the answers go into a structured audit file. Output is reusable: feeds `book-audits/` folder, the suite's READMEs, IG carousels, and concept refinements across skills.

The skill structures the user's voice; it does not author the audit. The user is the auditor of record (the audit file frontmatter names them). Claude's role is to ask the right questions, hold the structure, push back on hedging, and notice when the user's answer in one section contradicts another.

---

## What the skill does at runtime

### Setup (one-time per book)

1. **Capture book metadata.** Title, author, publication year, edition. If multiple editions are relevant (e.g., YMOYL 1992 + 2018), capture both — they often differ in ways that matter.
2. **Capture input mode.** Three options:
   - **Full read**: the user has read the book (or both editions) and is bringing their own reading.
   - **From notes**: the user has read it but is working from notes or memory, not the book in hand.
   - **From summary**: the user has not read the book and is working from publisher copy, Wikipedia, or a third-party summary. Flag this in the audit's `auditor:` frontmatter (e.g., "Marika Olson, from summary only"). Some audits don't survive this — be honest in the verdict.
3. **Confirm or create the audit file** at `book-audits/YYYY-MM-DD-<book-slug>.md` using `book-audits/_audit-template.md` as the starting frame.

### Extraction (walk through sequentially; resumable across sessions)

Each step writes to the audit file before moving to the next. The user can stop at any point; the next session re-reads the file, summarizes what's done, and resumes at the first unfilled section.

3a. **§0 — Reader's note (optional, 3-4 sentences max).** Ask: *Is there a story behind why you picked up this book — who recommended it, where you got it, what other reading led here, what made you want to write this audit specifically?* If yes, write it as a tight 3-4 sentence preface. If no genuine motivation story exists, skip §0 entirely — not every book has one. The point is to make the auditor-of-record visible from the start when there's a real reason to; not to manufacture autobiography. Cap at 4 sentences; if it's running longer, the substance probably belongs in §6 (verdict) or as a callout inside another section.

4. **§1 — The premise in one paragraph.** Strip the persona. Ask: *What is the actual claim?* Two to four sentences, no jargon, no marketing copy. If the book has historical significance (founding document, first to name something), note that briefly here.
5. **§2 — Load-bearing mechanics.** Ask: *What does the book actually want the reader to do?* Strip the chapter sequence, strip the worksheets, strip the rhetorical framing. List the 1-3 concrete moves underneath. If the book has a deeper single mechanic that the surface structure is wrapped around, name it.
6. **§3 — What aged well.** Concepts and patterns that survive their era. Be specific: cite which step or chapter holds up, and why.
7. **§4 — What aged poorly.** Specific numerical assumptions, named tools, era-bound math, vibes-based claims. Be blunt. Cite chapters or step numbers, not page numbers (those edition-drift). If the book is older than 5 years, translate every dollar figure into [current year] purchasing power and flag any rate or return assumption that no longer holds.
8. **§5 — What's missing.** What does a [current year] reader need to think about that the book doesn't address? Common gaps: AI displacement, HSAs / post-ACA healthcare, gig income, geographic arbitrage, generational wealth disparity, structural cost asymmetries (Vimes Boots), non-US readers. Don't limit to that list — surface anything missing that matters for this book's claim.
9. **§6 — The honest verdict.** Who should read it, who should skip it. Use specific reader profiles, not "everyone" or "depends on your situation." If the book is useful for parts but not whole, say which parts and which to skip.
10. **§7 — The 5-line takeaway.** The smallest version of the book's advice worth keeping. If a reader does only these things and skips everything else, do they get the load-bearing benefit? Cross-reference any `fi-*` skill that already implements one of the takeaways (e.g., "this is `/fi:track-flow`").
11. **§8 — Hearth's verdict.** Mandatory. One-line cat-take in Hearth's voice. Tonal range: `nap-worthy` / `hiss-worthy` / `windowsill-approved` / `would-knock-off-the-desk`. Hearth speaks for herself — she is not a tagline machine. If the book is mixed (good tools, bad framing or vice versa), Hearth can split the verdict.

### Citations + close-out

12. **Citations.** Chapter-level (or step number for stepwise books) for every load-bearing claim. Also list any external sources brought into the audit (other books, indicators, popularized concepts). Note which editions were read and where the reading copy came from if relevant.
13. **Auditor signature line.** "Audit by [Name], YYYY-MM-DD." Set `status: complete` in frontmatter.
14. **Cross-reference report (PRIVATE — strictly NOT in the audit file).** Tell Marika which existing `fi-*` skills should add this book to their `sources:` frontmatter. **DO NOT write this report into the audit's markdown file under any heading.** The cross-skill mapping is repo-internal book-keeping that breaks the audit's public-facing voice; audits are published to Rogue Reads (Substack) and the public GitHub repo, and any "wiring" or "private" framing in the audit body is a leak. Instead, after the audit is otherwise complete: (a) edit each relevant skill's `SKILL.md` to add the book to its `sources:` frontmatter directly; (b) surface the mapping to Marika in the chat response only — never in the audit file. If a load-bearing mechanic from this book doesn't have a `fi-*` home and earns one, propose the new skill (name + one-sentence purpose) in chat — don't create it inside this skill's run, and don't write it into the audit body.

---

## Audit output format (per book)

See `book-audits/_audit-template.md` for the frontmatter and section headers. The 8 sections are the frame; depth grows as the book warrants. The YMOYL audit (`book-audits/2026-05-01-ymoyl.md`) demonstrates a fully developed run — §4 and §5 there have sub-sections for distinct critiques, citations are chapter-level with edition disambiguation, and Hearth's verdict is split because the book and its tools earn different ratings.

---

## System frame for extraction

> You are evaluating a personal finance / business finance book on behalf of a reader who is sharp, financially literate, and allergic to bro-tone, scarcity-tone, and outdated math. The reader does not need to be sold on the importance of money management. They want the load-bearing ideas separated from the rhetorical packaging. Be blunt. If the math is dated, say so. If the premise no longer holds in [current year], say so. If the author is performing a persona that gets in the way of the substance, name it. Do not soften.

---

## Per-section extraction prompts (ask one at a time)

- *Premise:* "Strip the persona. What is the actual claim of this book, in 2-4 sentences?"
- *Load-bearing mechanics:* "If you removed every motivational paragraph and every chapter-opener anecdote, what 1-3 things does the book actually want the reader to do? Is there a deeper single mechanic that those surface moves are angles on?"
- *Aged well:* "Which concepts or patterns from this book still hold up in [current year]? Cite the chapter or step."
- *Aged poorly:* "Which numerical assumptions, named tools, or era-specific frames no longer hold? Cite chapters. Translate dollar figures into [current year] purchasing power."
- *Missing:* "What does a [current year] reader need to think about that this book doesn't address? Examples to consider but not be limited to: AI displacement, HSAs and post-ACA healthcare, gig and multi-employer income, structural cost asymmetries (Vimes Boots), geographic arbitrage, non-US contexts, generational wealth, accessibility tax on financial infrastructure."
- *Verdict:* "Who should read this book — specific reader profile. Who should skip it. Are there parts worth taking and parts worth leaving?"
- *Takeaway:* "If a reader did only the smallest version of this book's advice and skipped everything else, what would they do? Which `fi-*` skills (if any) already implement these moves?"
- *Hearth:* "Hearth's one-line cat-take. Tonal range: nap-worthy, hiss-worthy, windowsill-approved, would-knock-off-the-desk. She speaks for herself — don't write her a tagline."

---

## Output guardrails

- No hedging language ("it depends," "everyone's different") — pick a side.
- No promotional copy from the author's marketing — work only from the book's actual claims.
- Cite chapter titles (or step numbers, for stepwise books) for every load-bearing claim. Page numbers are optional — they edition-drift quickly and aren't load-bearing.
- Translate every dollar figure into [current year] purchasing power if the book is older than 5 years.
- For each surviving mechanic, tag the layer it belongs in (concept / pattern / tool).
- If working from summary only, the audit must say so in the frontmatter and the verdict. Don't dress up a summary-only audit as a full read.

---

## Headless behavior

Not headless — extraction requires interaction. The user is the auditor of record; the skill structures their voice. A future option is to read from a structured input file (book metadata + user's pre-written notes) and run extraction non-interactively, but the first version stays interactive.

---

## Cross-reference detection (private to Marika, not in the audit)

After the audit is complete, scan the load-bearing mechanics against the existing `fi-*` skills. For each match:

- If the skill already exists and the book is in its `sources:` — no action.
- If the skill exists but the book is missing from its `sources:` — propose an update to that SKILL.md's `sources:` frontmatter.
- If the mechanic doesn't have a home — propose a new skill name + one-sentence purpose. Do not create it inside this run.

The audit file itself stays clean of repo-mapping. The wiring report goes to Marika as a separate post-audit summary.

---

## TODO (deferred, not blocking draft status)

- [ ] IG-carousel slice — auto-generate a 5-slide carousel from the audit.
- [ ] Worked audits beyond YMOYL: Profit First (next), Psychology of Money, Just Keep Buying, Die With Zero.
- [ ] Non-interactive mode that reads from a notes file.

---

## Sources

The sources for this skill are the books that get audited. The skill itself derives from observation of common patterns in finance-book persona vs. substance, with notes from Marika Olson's reading list (2026).
