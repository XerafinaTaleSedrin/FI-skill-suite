---
name: three-questions
description: Walks the user through YMOYL's three-questions consciousness check on each spending category — values-fit, life-energy-fit, FI-fit. Slow, reflective, energy-aware. Reads the most recent monthly tab from /fi:track-flow and (when available) the real hourly wage from /fi:hourly-wage so "life energy" is a real number, not abstract.
layer: concept+pattern
ymoyl_step: 4
mode_aware: false
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 4 — the three questions that will transform your life. Original phrasing preserved (with optional modernization) because the original carries weight in the YMOYL community and gentle paraphrase loses substance."
  - book: Profit First (Michalowicz, 2017)
    contribution: "Business-side mirror of the YMOYL expense-awareness discipline. The Profit First OpEx 'cut what you don't need, be aware' move is the business-cash version of the YMOYL spending-awareness question 4. Surfaces in this skill for users who run a business — apply the same three questions to OpEx line items."
  - author: Marika Olson
    contribution: "2026 design refinements: energy-aware pacing (resumable mid-walk), real-hourly-wage anchoring (life-energy in actual hours not abstract concept), pattern-surfacing from /fi:track-flow as scaffolding for each category prompt, AuDHD-aware support for users who can't sit through 30+ category prompts in one go."
last-reviewed: 2026-05-12
---

# /fi:three-questions

Reads the user's most recent monthly tab (from `/fi:track-flow`) and walks them through YMOYL's three questions for each spending category. The skill captures a per-category response (`-` / `=` / `+`) plus optional notes, writes a values-overlay file alongside the original tab, and surfaces the categories that scored `-` as candidates for `/fi:redirect` (or future `/fi:spending-minimize`) work.

This is the highest-friction skill in the suite by design. The friction *is* the consciousness. The skill supports breaking it into multiple sessions so the friction doesn't become a wall.

---

## The concept (decades-stable)

Tracking spending without a values check is mechanical bookkeeping. Knowing where every dollar goes is necessary; knowing whether you're glad it went there is the thing that converts data into living.

The three questions:

1. **Did I receive fulfillment, satisfaction, and value in proportion to life energy spent?** (Life-energy fit — was it worth the hours?)
2. **Is this expenditure of life energy in alignment with my values and life purpose?** (Values fit — does it fit who I'm trying to be?)
3. **How might this expenditure change if I didn't have to work for a living?** (FI fit — would it go up, stay the same, or go down?)

The questions get modernized in delivery (YMOYL-1992 phrasing reads stilted in 2026), but the substance is preserved: a fulfillment check, an alignment check, and a hypothetical-FI check.

Run quarterly at minimum. Monthly if you can stand the friction. Friction is the cost of consciousness; not a flaw in the design.

---

## The pattern (~5-year stable)

Sequential, category-by-category prompt loop. Capture user's response per category (`-`, `=`, `+`) plus optional one-line note. Output is a values-overlay added to the monthly tab.

The skill is **resumable** — if the user runs it on a 47-category month and only gets through 15 categories before stopping, the next invocation picks up where they left off. State persists in the values-overlay file itself (categories not yet rated have a placeholder).

---

## What the skill does at runtime

### Step 1 — Source data check

Look for the most recent `~/finances/monthly-tabs/YYYY-MM.md` file. If multiple are available, ask:

> *"I see monthly tabs for [list of months]. Which one are we walking?"*

Default to the most recently complete (`complete: true`) month. Offer the most recent partial month as an alternative if the user explicitly wants the current snapshot.

If no monthly tab is present, instruct the user to run `/fi:track-flow` first and stop.

### Step 2 — Anchor in life-energy hours (if available)

Look for the most recent `~/finances/hourly-wage/*.md` file. If present, read the real hourly wage. Use it to anchor each category prompt:

> *"At your real hourly wage of $R/hr, a $X expense in [category] cost you W hours of life energy this month. Holding that number in mind for the questions."*

If no hourly-wage file is present, ask:

> *"Have you run `/fi:hourly-wage` recently? Having that number makes the questions sharper. If you'd like a quick anchor without running the full skill, give me a rough estimate of your real hourly wage; if not, we'll do the questions without the dollar-to-hours translation."*

Allow either path. Without the anchor, the skill still works but loses some of its bite.

### Step 3 — Pacing pre-check

Count the categories in the monthly tab. Ask:

> *"This month has N spending categories. Walking each carefully is ~2-3 minutes per category, so this is roughly a [N × 2.5]-minute session. Three options:*
> - *Walk all N now (one focused session)*
> - *Walk the top M by dollar amount now, save the rest for next session (pareto-aware — typically 5-10 categories cover 80%+ of spend)*
> - *Walk a custom subset — pick which categories you want to think about today"*

Default offer: top-M-by-dollar pareto split. Most users find this less daunting and most of the values-fit signal lives in the high-dollar categories anyway.

For users who picked "all" but show energy fading mid-walk (e.g., terse responses, skip-no-note patterns), gently offer:

> *"You've been at this a while — want to save the rest for another session? The skill picks up where you left off."*

### Step 4 — Per-category walk

For each category in the chosen subset, present:

```
=== [Category name] ===
This month:
  Total: $X
  Hours of life energy (at $R/hr): W hours
  Top vendor: [vendor], [% of category]
  Recurring: [Y / N]
  Patterns from /fi:track-flow: [any flagged patterns for this category]
```

Then ask the three questions. Default modernized phrasing:

> **Q1.** *Was this worth the hours? Did this give you fulfillment, satisfaction, or real value in proportion to the W hours of life energy it cost?*
>
> **Q2.** *Does this fit who you're trying to be? Is the spending in this category aligned with your actual values and life direction (not the version of you that you think you should be)?*
>
> **Q3.** *If you didn't have to work for a living, what would happen to this category — would it go up, stay the same, or go down?*

Offer the original YMOYL phrasing as a footnote on first category:

> *(YMOYL original: "Did I receive fulfillment, satisfaction, and value in proportion to life energy spent?" / "Is this expenditure of life energy in alignment with my values and life purpose?" / "How might this expenditure change if I didn't have to work for a living?" — say "use original" anytime you'd prefer the unmodernized phrasing.)*

For each question, capture the user's response. Use a 3-letter shorthand to keep pacing fast:

- `-` = out of alignment (one or more questions answered "no" / "not really" / "I'd cut this in FI")
- `=` = neutral / mixed (some yes some no, or genuinely indifferent)
- `+` = in alignment (all three questions answered with conviction)

Single composite rating per category, NOT per question. The skill is values-fit overall, not micro-scored.

After the rating, offer:

> *"One-line note? (optional — just to give your future self context when you re-read this in 6 months)"*

Capture verbatim if given. Skip if user says "no" / hits enter / declines.

### Step 5 — Mid-walk break support

After every 5 categories, gently check in:

> *"5 done. [If pareto-mode] X of M to go in this session. Want to keep going, take a break, or wrap?"*

If the user says break:

- Save state to the values-overlay file (categories rated so far, in-progress flag on the next one).
- Show a brief summary of what's been rated.
- Offer to resume on next invocation.

### Step 6 — Pattern surfacing (post-walk)

After all chosen categories are rated, surface the picture:

```
=== Values overlay summary ===

In alignment (+): N categories, $X total
Neutral (=): M categories, $Y total
Out of alignment (-): K categories, $Z total

Out-of-alignment categories worth thinking about:
  1. [Category] — $X (W hours) — note: [user note]
  2. ...

In-alignment categories that are quietly working:
  1. [Category] — $X (W hours)
  2. ...
```

Then offer:

> *"The minus-rated categories are candidates for `/fi:redirect` work — the freed-up dollars from minimizing those go to debt paydown or investment per your priority. Want to look at those now, save for a future session, or just sit with the data?"*

Default offer: save. The skill's job is awareness, not action — `/fi:redirect` does the deployment math.

### Step 7 — Write output

Write to `~/finances/monthly-tabs/YYYY-MM-with-values.md`. Schema:

```markdown
---
month: YYYY-MM
source-tab: YYYY-MM.md
hourly-wage-anchor: $R/hr (from YYYY-MM-DD wage file, or "none" / "user-estimate $X")
categories-walked: N of M total
generated-by: /fi:three-questions
last-updated: 2026-MM-DD
---

# Values overlay — YYYY-MM

## Summary
- In alignment (+): N categories, $X total
- Neutral (=): M categories, $Y total
- Out of alignment (-): K categories, $Z total
- Not yet walked: P categories, $Q total *(pick up where you left off)*

## Per-category ratings

| Category | Spend | Hours @ $R | Rating | Note |
|---|---|---|---|---|
| housing | $X | W | + | "Mortgage feels right" |
| food | $X | W | = | "Mixed — groceries good, restaurants drift" |
| subscription-streaming | $X | W | - | "Don't watch most of these" |
| ... | ... | ... | ... | ... |

## Patterns surfaced
- ... (carried from /fi:track-flow's _patterns-detected.md, marked with values overlay)

## Categories pending (resume next session)
- [Category]
- [Category]
```

### Step 8 — Closing

Show:

> *"Saved to ~/finances/monthly-tabs/[month]-with-values.md.*
>
> *No directive ending. The data's the data. A few useful next steps if you want them:*
>
> - *`/fi:redirect` — for the minus-rated categories, where do those freed-up dollars go?*
> - *`/fi:hourly-wage` — if the dollar-to-hours math felt sharp and you haven't run it lately, refresh.*
> - *`/fi:track-flow` again next month — the values overlay is more useful with multiple months stacked next to each other (drift becomes visible).*
>
> *Skip me until you can sit with the data. The work is half-done if you don't let the answers settle."*

---

## Output schema

### `~/finances/monthly-tabs/YYYY-MM-with-values.md`

(Per Step 7. Frontmatter declares source tab + anchor + walk progress; per-category ratings table; patterns; pending list for resume.)

The skill writes ALONGSIDE the original `YYYY-MM.md` from `/fi:track-flow`. Never modifies the original.

---

## Tone and pacing

The skill is slow on purpose. The three questions are not a checkbox exercise; they're a contemplative practice. Pacing should match:

- **Don't rush**: when the user takes 60 seconds before responding, leave the silence.
- **Don't add commentary**: after the user rates a category, just confirm the rating and move on. Don't editorialize ("That seems right!" / "Interesting choice"). The questions do the work.
- **Don't moralize the rating**: a `-` rating in entertainment isn't bad; a `+` rating in housing isn't good. The rating is the user's. The skill records it.
- **Default to the user's framing**: if the user goes off the question and gives a long contextual answer, capture it as a note rather than re-asking the question literally. The note is more useful than a forced rating.
- **Honor breaks**: the AuDHD-aware framing is real — some users genuinely cannot sit through 30+ category prompts in one go. The resumable design exists for them. Don't penalize multi-session use.

Common reactions and how to handle:

- *"All my categories are bad."* — Probably not true. Probe gently: *"This came up for almost every category — is it that the spending really is out of alignment, or is something else going on (low energy, low mood, recent big stress)?"* If the user confirms it's a state thing, suggest pausing the skill and resuming on a different day.
- *"I don't know."* — Capture as `=` (neutral). The user not knowing is itself a useful signal — the category isn't conscious yet. Note it: "didn't know — revisit when more aware."
- *"Why are you asking me this?"* — Frame: the questions are YMOYL Step 4. The math (hours of life energy spent) doesn't have meaning without the values overlay. The skill is a structured way to do the overlay.

---

## Headless behavior

Not headless. This skill is the values check. Removing the human removes the point.

A "rate-from-prior-month" flag is conceivable (carry over last month's ratings as defaults, only walk categories where the spend changed >Q%) — useful for users running monthly cadence. Park as TODO.

---

## Resumable-walk implementation note

The skill stores walk state in the values-overlay file itself, not a separate state file:

- **First invocation**: creates `YYYY-MM-with-values.md` with all categories listed, all ratings empty, walks chosen subset, fills ratings as it goes.
- **Subsequent invocations on the same month**: reads the file, identifies pending categories (rating empty), offers to resume.
- **All-walked invocations**: detects all ratings filled, offers to add notes / re-rate / move on.

User can edit the file directly (e.g., change a rating after reflection). Skill respects edits on next read.

---

## Why this matters

Track-flow without three-questions is bookkeeping. Hourly-wage without three-questions is a number on a screen. The values overlay is the thing that turns financial consciousness into something that informs how you actually live.

The skill is friction-by-design because the substance is friction. A user who can rate 47 categories in 8 minutes is checking boxes, not reflecting. Build the pacing in.

For AuDHD users specifically: the resumable structure isn't a fallback for "lazy" or "low-discipline" users. It's the correct shape for the cognitive realities of the work. The values check is contemplative; contemplative work doesn't always fit in a 60-minute block. Three sessions of 15 minutes each is a better cognitive fit than one 45-minute slog.

---

## TODO

- [ ] Validate against multiple users — refine modernized phrasing based on what feels natural vs forced
- [ ] Carryover-mode: rate-from-prior-month defaults for users running monthly cadence
- [ ] Cross-skill: define what `/fi:redirect` reads from this output (probably the minus-rated category list with dollar amounts)
- [ ] Drift-detection: when a category's rating shifts month-over-month (was `+`, now `-`), surface the change as a pattern worth thinking about
- [ ] Per-question scoring mode (optional, for users who want micro-scoring instead of composite) — captured but defaults off
- [ ] Worked examples in `examples/` showing different reaction patterns

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 4 — the three questions that will transform your life. Original phrasing preserved (with optional modernization) because the original carries weight in the YMOYL community and gentle paraphrase loses substance for users who've read the book.
- **Marika Olson** (2026). Energy-aware pacing (resumable mid-walk), real-hourly-wage anchoring (life-energy in actual hours not abstract concept), pattern-surfacing from `/fi:track-flow` as scaffolding for each category prompt, AuDHD-aware support for users who can't sit through 30+ category prompts in one go.
