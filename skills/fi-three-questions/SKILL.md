---
name: fi-three-questions
description: Walks the user through YMOYL's three-questions consciousness check on each spending category — values-fit, life-energy-fit, FI-fit.
layer: concept+pattern
ymoyl_step: 4
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 4 — the three questions that will transform your life"
last-reviewed: 2026-05-01
---

# fi-three-questions

Reads a monthly tab (from `fi-monthly-tabulation`) and walks the user through YMOYL's three questions for each category:

1. **Did I receive fulfillment, satisfaction, and value in proportion to life energy spent?** (Life-energy fit)
2. **Is this expenditure of life energy in alignment with my values and life purpose?** (Values fit)
3. **How might this expenditure change if I didn't have to work for a living?** (FI fit)

---

## The concept (decades-stable)

Tracking spending without a values check is mechanical bookkeeping. The three questions are the thing that converts bookkeeping into living. Run quarterly at minimum; monthly if you can stand the friction. The friction *is* the consciousness.

---

## The pattern (~5-year stable)

Sequential, category-by-category prompt. Capture user's response per category (-, =, or +) plus optional notes. Output is a values-overlay added to the monthly tab.

---

## What the skill does at runtime

1. Reads the monthly tab.
2. For each category: present total dollars + life-energy cost; ask the three questions; capture response.
3. Tag responses: `-` (out of alignment), `=` (neutral), `+` (in alignment).
4. Surfaces the categories with `-` ratings as candidates for `fi-spending-minimize` (planned).
5. Writes the values-overlay to `~/finances/monthly-tabs/YYYY-MM-with-values.md`.

---

## Headless behavior

Not headless — this skill is the values check. Removing the human removes the point.

---

## TODO

- [ ] Three-questions wording — preserve YMOYL phrasing or modernize? (Most users find the original a little stilted; gentle modernization without losing the substance.)
- [ ] Cross-skill: what does `fi-spending-minimize` need from this output?

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 4.
