---
name: hourly-wage
description: Computes real hourly wage — the YMOYL life-energy math, modernized for 2026 work modes (remote, hybrid, on-site, gig).
layer: concept+pattern
ymoyl_step: 2
mode_aware: true
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 2 — real hourly wage formula (life-energy math)"
last-reviewed: 2026-05-01
---

# /fi:hourly-wage

Walks the user through computing their *real* hourly wage — gross pay minus work-related costs, divided by total hours including commute, prep, decompression, and tooling-maintenance. This is YMOYL's life-energy math; the 2026 update makes it work-mode-aware so it doesn't flatter remote workers and overstate on-site costs (or vice versa).

---

## The concept (decades-stable)

What you actually earn per hour of life energy spent on work is almost never what your paycheck says. The YMOYL formula:

- **Subtract** from gross pay: every cost incurred *because* you have this job.
- **Add** to total hours: every hour spent *because* you have this job.
- Divide.

The result is your real hourly wage — and it's almost always shocking.

The 1992 version assumed an office commuter. The 2026 version has to handle remote, hybrid, on-site, and gig workers, each with completely different line items. The skill is **mode-aware** so it doesn't apply the wrong subset.

---

## The pattern (~5-year stable)

Branching walk-through based on work mode. For each mode, surface the relevant subset of subtractions and additions. Capture user-specific custom categories at runtime. Compute and report.

---

## What the skill does at runtime

1. **Asks first**: "What's your current work mode? Fully remote / hybrid (X days in office) / fully on-site / gig or freelance / other?"
2. Surfaces the relevant subset of YMOYL classic adjustments + 2026 additions (see below).
3. Captures the user's specific numbers per line item.
4. Asks the **user-extensible question**: "Are there categories specific to your situation we should factor in?"
5. Runs the math: gross pay − sum(subtractions) divided by official hours + sum(additional hours).
6. Reports the real hourly wage with full decomposition (which subtractions hit hardest, which hours dominated).
7. Optional: writes the result to `~/finances/hourly-wage-YYYY-MM-DD.md` for tracking over time.
8. Surfaces the opt-in community-submission prompt for any custom categories the user added.

---

## YMOYL-classic adjustments (still load-bearing for on-site and hybrid)

**Subtract from wages:**
- Commuting costs (gas, transit, parking, vehicle wear)
- Work clothes
- Work meals out (lunches you wouldn't eat if you weren't there)
- Decompression spending (the post-work drink, the "I deserve this" purchase)
- Escape entertainment (the streaming service that's really a "I'm too tired to do anything else" subscription)
- Job-related sickness costs (stress-related healthcare)

**Add to denominator:**
- Commute hours
- Prep hours (getting ready, getting there)
- Decompression hours (the wind-down after work)
- Work-related shopping hours (errands you only do because of work)

These do **not** disappear in 2026 — they apply to anyone whose job still requires showing up in person, even part-time.

---

## 2026 remote / hybrid additions (additive, not replacements)

**Subtract from wages:**
- Home internet (work-attributed portion — typically 30-70% depending on role)
- Home electricity (work-attributed portion — desk + monitors + heating/cooling during work hours)
- Home office depreciation / rent allocation
- Ergonomic furniture amortized over its useful life
- **AI / SaaS OpEx — Claude Code, ChatGPT, Notion, the full stack.** Meaningful and growing line item; ignoring it pretends the wage is higher than it is.
- Equipment refresh cycle (laptop, monitor, headset)
- Work-from-home isolation costs (therapy, body work, social re-entry, gym membership replacing the incidental walking of office life)

**Add to denominator:**
- Blurred-boundary hours — the "always-on" tax of working from where you live
- Cognitive context-switching cost when home/work share physical space
- Time spent maintaining the tooling itself (AI prompt engineering, software updates, MCP debugging)

**New category:** AI tooling that increases output but eats margin. Has to be amortized into the wage calc honestly. A consultant pulling $200/hr who spends $400/mo on AI subscriptions is not actually pulling $200/hr — but most people don't do the subtraction.

---

## Why this matters

A 2026 fully-remote consultant who runs YMOYL's classic-only calc gets a flattering number — no commuting subtraction, work clothes near zero, work meals minimal. The number reads high. But the modern line items (AI OpEx, home utilities work-portion, blurred-boundary hours) often more than replace what 1992-office-worker line items used to cost. The honest 2026 number is often **lower than the YMOYL-1992-only calc would suggest** for remote workers — and equally honest for hybrid and on-site workers because the classic items still apply.

That honesty across all work modes is the whole point.

---

## Headless behavior

Not generally headless — interactive walkthrough by design. Manifest-input mode planned for batch recomputation.

---

## TODO

- [ ] Mode branching logic in detail; capture each path.
- [ ] User-extensible category capture flow (writes to local `custom-categories.md`, surfaces opt-in submission at session end).
- [ ] Output schema for the dated wage file so trend-over-time analysis is possible.
- [ ] Tone-aware reporting (matter-of-fact / blunt / contextual).
- [ ] Worked examples for each work mode in `examples/`.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 2 real hourly wage formula.
- **Marika Olson** (2026). 2026 work-mode additions and the AI/SaaS OpEx line item are additions not in YMOYL.
