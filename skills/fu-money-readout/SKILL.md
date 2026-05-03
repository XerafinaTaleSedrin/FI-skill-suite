---
name: fu-money-readout
description: Optional daily ground-state report — net direction, runway, recurring passive income, crossover %, nuclear runway. Reads from holdings.md. ("FU" in the skill name is intentional FI-community slang for "fuck-you money" — having enough to walk away from any situation. Not a typo of "FI money.")
layer: concept+pattern
ymoyl_step: 8
mode_aware: true
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Crossover-point concept (Step 8) — when investment income covers expenses"
last-reviewed: 2026-05-02
---

# /fi:fu-money-readout

> **About the name** — "FU money" is established FI-community slang for **"fuck-you money"**: the amount of money that gives you the freedom to walk away from any situation you don't want to be in (a bad job, a bad client, a bad relationship structure, a bad city). It's not a typo of "FI money" — it's a specific, deliberate term that captures the *agency* aspect of financial independence rather than the retirement-age aspect. James Altucher, Suze Orman, and the broader FI community have all used the term. This skill is named to keep the ethos visible.

Optional daily check-in skill. Produces a brief ground-state report from `holdings.md` so the user has a regular pulse on their financial position. Inspired by YMOYL's crossover-point model, modernized for a 2026 rate environment and any user-defined "retirement" frame.

---

## The concept (decades-stable)

The financial brain operates on a small number of orientation questions: *Am I gaining ground or losing it? How long can I sustain this? What's the worst case if everything fails?* When those questions are unanswered, anxiety fills the gap. When they're answered honestly and regularly, anxiety has nothing to feed on.

The reading should feel like a weather report — short, factual, no drama. Not "you're ahead by 12%!" Not "you'll never retire." Just the numbers, in a tone the user picked.

---

## The pattern (~5-year stable)

A short daily readout, rendered in the terminal or saved to a log file, produced from the user's local `holdings.md` file. NOT an interactive dashboard; NOT a real-time market ticker. The cadence is daily-or-less; the data updates only as fast as the user updates `holdings.md` (typically monthly). What changes day-to-day is the date, the freshness flag, and any recent events — not the underlying numbers.

---

## What the skill does at runtime

1. **Reads `holdings.md`.** Validates schema. Reports if the file is missing — points at `/fi:holdings-scaffold` to create one.
2. **Checks freshness.** Flags warm if last-updated is >14 days ago; flags stale if >30 days.
3. **Pulls the user's "retirement frame"** from a saved profile. Frame options:
   - **Full stop**: traditional retirement, all income from passive sources.
   - **Location-time flexibility**: working, but able to choose where and when.
   - **Income downshift**: working, but at lower income because non-money values are weighted higher.
   - **Coast FI**: invested enough that compounding alone gets to FI by traditional retirement age, even with no further contributions.
4. **Computes the readout fields:**
   - **Net positive/negative direction** (this month vs. last month, expenses-vs-income).
   - **Runway** in months from liquid savings if all income stopped.
   - **Recurring passive income** (dividends, rental net, interest) — list sources.
   - **Crossover %** of monthly expenses currently covered by passive income.
   - **Nuclear runway** — if all income stopped AND all liquid savings exhausted, how many years could the user sustain by drawing down sequentially (cash → brokerage → Roth contributions → IRA penalty-eligible → etc.) before depletion. Also reports the user's age at depletion.
5. **Renders the readout** in the user's chosen tone (matter-of-fact / warm / blunt).
6. **Logs it** to `~/finances/fu-money-log/YYYY-MM-DD.md` so the user has a history.

---

## Output format

```
--- FU Money Readout (YYYY-MM-DD) ---

Right now:    [Net positive/negative direction] ([+/-]$X,XXX/mo)
Runway:       XX months from liquid savings
Recurring:    $X,XXX/mo passive (list sources)
Crossover %:  XX% of monthly expenses covered passively
Nuclear:      XX years at full burn, zero income, before depleted (age you'd be: XX)

[One grounding sentence — chosen from user's tone preference]
---
```

---

## Architectural features

- **Mandatory Nuclear line.** This is the anxiety answer. Even if everything fails, here's how long the user lasts. Not a plan — a grounding number. Calculated from the full draw-down sequence the user defines (savings → cash → brokerage → Roth contributions → Trad IRA penalty-eligible → real estate liquidation → etc.).
- **Tone selectable**: matter-of-fact / warm / blunt. User picks at setup. The skill offers grounding sentence variants in the chosen tone (kept in `tone-options.md` per the skill folder).
- **Runtime freshness**: pulls `holdings.md`'s `last-updated` date; flags if stale.
- **Pluggable into session start**: optional; default OFF. User opts in. If opted in, the readout fires on first session of the day after any other session-start rituals.
- **Mode-aware**: readout adjusts based on the user's retirement frame. The crossover math is different for each variant.
  - Full stop: crossover% target is 100%.
  - Location-time flexibility: crossover% target is 60-80% (working partially).
  - Income downshift: crossover% target is 40-60% (downshift while working).
  - Coast FI: crossover% target is 0% (just need invested enough to compound).

---

## Headless behavior

This skill is **explicitly designed to run headlessly** as a session-start ritual or a daily cron. When fired with no human present:

- Reads `holdings.md` as normal.
- Computes the readout.
- Writes it to `~/finances/fu-money-log/YYYY-MM-DD.md`.
- Does NOT print to stdout (no human there to read it).
- Does NOT block on any interactive prompt.
- If `holdings.md` is missing or malformed: writes an error note to the log file with a clear next step (run `/fi:holdings-scaffold`), exits cleanly.

---

## Mode-aware retirement frames

The user picks one frame at setup; the skill stores the choice in a profile file. Frame definitions:

### Full stop
Traditional retirement. All income from passive sources. Crossover target = 100% of expenses.

### Location-time flexibility
Working, but with full freedom to choose where and when. Crossover target = 60-80% (partial work fills the gap).

### Income downshift
Working in a deliberately lower-income role aligned with values, not maximization. Crossover target = 40-60% (work fills more than half).

### Coast FI
Invested enough that compounding alone reaches FI by traditional retirement age, even with zero further contributions. Crossover target = 0% (the math is "is the existing invested amount × expected real return enough to compound to target by year N?").

For each frame, the readout uses different language and different math. The output fields stay the same; the targets differ.

---

## TODO

- [ ] Define the schema for the user's profile file (retirement frame + tone preference + draw-down sequence).
- [ ] Build the headless cron-friendly entry point.
- [ ] Implement the four retirement-frame variants of the crossover math.
- [ ] Define the tone-options.md content (grounding-sentence pool per tone).
- [ ] Worked examples in `examples/` for each retirement frame.
- [ ] Cross-skill: define how `/fi:track-flow` feeds the monthly-expense baseline this skill needs.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Crossover point as Step 8.
- **Marika Olson** (2026). The "Nuclear runway" concept is an addition not in YMOYL — captures a worst-case grounding number that addresses anxiety more than crossover% alone does.
