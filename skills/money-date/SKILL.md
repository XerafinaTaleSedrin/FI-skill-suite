---
name: money-date
description: Weekly ~5-minute counterweight ritual to the hoarding instinct. Three honest questions — did you pay yourself, did you spend on ease, did you enjoy anything — surfaced once a week against the user's actual flow. Designed for owners whose risk pattern is *under*-spending, not over. Use weekly, or whenever the user wants a quick check against the "check the balance to feel safe" compulsion.
layer: pattern
ymoyl_step: cadence-companion
mode_aware: false
status: draft
status-history:
  - 2026-05-23: draft (initial scaffold from Hidden Profit / Jamie Trull seed + Ruler/Accumulator counterweight design intent)
sources:
  - book: Hidden Profit (Jamie Trull, 2024)
    contribution: "p.74 — the Weekly Money Date concept. ~5-minute weekly cash-flow check, in contrast to the heavier monthly tabulation. Cadence and lightness come from Trull's framing."
  - book: Your Money or Your Life
    contribution: "Monthly tabulation is the heavier sibling — the money-date is the weekly lighter version, same spirit. The shared principle: visibility on flow is the first lever."
  - author: Marika Olson
    contribution: "2026 design refinements — three-question counterweight structure aimed at the Ruler/Accumulator hoarding instinct. Designed against the failure mode of becoming another anxious balance-check ritual."
last-reviewed: 2026-05-23
---

# /fi:money-date

A money date is not a balance check. The risk pattern this skill is designed
against is the *Ruler / Accumulator* one: keep money in, watch the number, feel
safe by hoarding. That compulsion needs a counterweight ritual, not another
reinforcement of itself.

So the money-date is structured around three questions about money going **out**
— what got paid to the user, what got spent on ease, what got spent on joy. The
balance is mentioned in passing only as context for whether the outflows were
honest. The headline number is whether all three questions had real answers.

Output: a dated weekly file the user re-runs every Friday (or whatever cadence
they pick), with a trend over time as runs accrete. Short, honest, glance-able.

## Step 1 — Settle the cadence

Ask first: **"When's your money date — same day each week, or roving?"**

- **Fixed day** (e.g. every Friday morning) — the rhythm itself is the value.
  Skip the question on subsequent runs unless the user changes it.
- **Roving** — fine, but ask whether last run was within ~10 days. Longer gaps
  mean the cadence isn't holding; surface that gently and ask if a fixed slot
  would help.

Persist the cadence choice to `~/finances/profile/money-date-cadence.md`
(gitignored). Don't re-ask once set.

## Step 2 — Pull the week

Read the user's flow data for the period since the last money-date file
(default: last 7 days; longer if the cadence slipped). Sources, in priority:

1. The `/fi:track-flow` output if the user runs it — that's already classified
   by bucket / source / category.
2. A configured banking aggregator / file path if they use one.
3. Recent entries from `~/finances/transactions/`.
4. User self-report if nothing is automated.

If multiple sources exist, prefer the most-classified one. State which source
was used in the output. Never blend silently.

## Step 3 — The three questions

The whole skill turns on these three. Ask them **in order**, even if the user
expects to start with the balance. Starting with the balance reinforces the
hoarding compulsion this ritual is built to counter.

### Q1 — Did you pay yourself?

For a business owner: did money move from business to personal accounts this
week? An owner draw, a profit distribution, a salary equivalent — anything that
moves earned-by-the-business money into the user's personal life. If yes, how
much and on what cadence. If no, why not — was the week genuinely a low-income
week, or did the money sit in the business because pulling it felt unsafe?

For a salaried user: did your paycheck land, and did you treat any of it as
yours (separate from bill-paying)? Equivalent test, different surface.

If the answer is "no" for more than two consecutive weeks, name the pattern.
The Ruler/Accumulator instinct is strongest right here — money staying in the
business "for safety" is the most common form of self-underpayment. Don't
moralize. Just say so.

### Q2 — Did you spend on ease?

This is the harder one. Did the user spend money this week on something whose
explicit purpose was to reduce friction in their life? Categories that count:

- Hiring help (cleaner, VA, bookkeeper, gardener)
- A tool or subscription that removed a recurring annoyance
- Buying time (delivery instead of errand, prepared food on a low-spoons day,
  a service instead of DIY when DIY would have cost spoons)
- Replacing a frustrating object with one that works (the right-shape spoon
  energy — investment in friction-free daily use)

If the answer is "no," ask whether there was a moment this week where the user
*could* have spent on ease and didn't. That's the data point. Hoarding-pattern
owners reliably under-spend in this category; capturing the missed moment is
how the pattern surfaces over time.

### Q3 — Did you enjoy anything?

Did the user spend money this week on something whose explicit purpose was
joy? Not productivity, not health, not work-adjacent. Joy. Categories:

- A meal out chosen because it sounded good
- A book, a record, a subscription that brings delight
- Something for the home that's purely for pleasure
- An experience (movie, concert, class, trip)
- A gift to a friend or family member chosen with care

If "no," same data point. The pattern over time is more important than any
single week — a Ruler/Accumulator who logs three weeks of no-joy spending is
seeing their own compulsion clearly, which is the point.

If "yes," capture what it was. The skill will surface joy-spending patterns in
the trend section — what the user actually enjoys is data they can use.

## Step 4 — The balance, briefly

Only after the three questions, mention the balance — as **context** for
whether the outflows were honest, not as the headline.

- If outflows were minimal and balance grew: name it. "Balance up, no payment
  to self, no ease, no joy. That's hoarding, not saving."
- If outflows were substantial and balance dropped: name that too. "Balance
  down. Was the spending in line with values? (Use `/fi:three-questions` for a
  full check.)"
- If outflows and inflows roughly matched: that's the steady state — fine.

The point is the asymmetry: the skill says more when the balance moved in the
hoarding direction than when it moved in the spending direction. That's
deliberate.

## Step 5 — Trend

Read prior `~/finances/money-date/*.md` files. Surface a short trend on the
three questions:

- **Pay yourself** — frequency over the last 8 weeks (e.g. "5 of 8 weeks").
- **Ease** — count of weeks with ease-spending, plus most common category.
- **Joy** — count of weeks with joy-spending, plus most common category.

If any of the three are running below 50% over 8 weeks, name it gently in the
output. Don't recommend a fix — that's the user's call. The data is the
intervention.

## Output

Write each run to `~/finances/money-date/YYYY-MM-DD.md`. One file per run, a
dated snapshot, never overwritten. Validate `.gitignore` coverage before
writing; warn if the path is not ignored.

```markdown
---
date: YYYY-MM-DD
cadence: weekly | roving
days-covered: 7
source: /fi:track-flow | aggregator | transactions | self-report
generated-by: /fi:money-date
---

# Money date — YYYY-MM-DD

## The three questions

### Did you pay yourself?
- <yes / no, amount, cadence>
- <one-line context>

### Did you spend on ease?
- <yes / no, what + amount>
- <missed moment if applicable>

### Did you enjoy anything?
- <yes / no, what + amount>
- <one-line context>

## Balance (context only)
- Period flow: in $... / out $...
- Net: up / down / steady
- <honest one-liner about whether outflows match values>

## Trend (last 8 weeks)
| Question | Yes / 8 weeks | Notes |
|---|---|---|
| Pay self | n/8 | most recent date |
| Ease | n/8 | most common category |
| Joy | n/8 | most common category |

## What this week showed
- <2-3 honest lines — not advice, just naming what's visible>
```

On later runs, read prior money-date files and recompute the trend table.
Don't modify prior files — each is a snapshot.

## Pipeline mode (headless)

When invoked by another agent or a scheduled run with no human present:

- Read flow data from the configured source(s).
- Treat any week with no logged outflow on a question as a no.
- Default the cadence to weekly unless overridden.
- Write the dated file with whatever the data shows. The trend table is the
  durable artifact in headless mode — the prose may be sparse without user
  input, and that's fine.
- If no source has any data for the period, write a clear note to the file and
  exit. Never hang.

## What this skill is NOT

A balance-check ritual. The first instinct a Ruler/Accumulator owner will have
is to open this and immediately ask "what's my balance?" The skill is
structured against that instinct on purpose. If the user routinely jumps
straight to Step 4 and treats the three questions as obstacles, that's the
diagnostic — name it and ask whether the money-date is doing its job or
becoming another anxiety surface.

If the cadence stops holding (no run in 3+ weeks), don't enforce it. Ask the
user what's getting in the way. The ritual is a counterweight, not a duty.

## Privacy

User-specific data — payment amounts, vendor names, categories, balances — is
never embedded in this skill file or committed to the plugin repo. All user
data writes go to gitignored paths on the user's machine (`~/finances/`). See
`AGENTS.md` for the cross-skill privacy posture.

## Cross-refs

- `/fi:track-flow` — the heavier classification + tabulation skill; money-date
  is its weekly companion.
- `/fi:three-questions` — the values check; pair with money-date when an
  outflow surprised the user.
- `/fi:fu-money-readout` — the daily ground-state report. Money-date is the
  weekly outflow-focused complement; the readout is the balance-state complement.

## Sources

- **Hidden Profit**, Jamie Trull — p.74, the Weekly Money Date concept.
  Cadence and lightness come from Trull's framing.
- **Your Money or Your Life**, Vicki Robin & Joe Dominguez — the monthly
  tabulation is the heavier sibling; the money-date is its weekly lighter
  version.
- **2026 design refinements** (Marika Olson) — the three-question counterweight
  structure aimed at the Ruler/Accumulator hoarding instinct. Designed against
  the failure mode of becoming another anxious balance-check.
