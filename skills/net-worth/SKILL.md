---
name: net-worth
description: Read-only roll-up of holdings.md — surfaces the user's current net worth and the YMOYL Step 1 framing without re-walking the inventory. Use when the user wants the "where do I stand right now?" snapshot but doesn't want to re-run the full holdings scaffold.
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 1 — current net worth as 'making peace with the past'. (YMOYL prescribes a second half — lifetime earnings reconstruction — which this suite deliberately does not implement; see book-audits/2026-05-01-ymoyl.md §8 for reasoning.)"
last-reviewed: 2026-05-02
---

# /fi:net-worth

Reads `holdings.md` (created by `/fi:holdings-scaffold`) and produces a read-only net-worth snapshot with the YMOYL Step 1 framing language. **Does not modify the holdings file.**

> **Open question (logged 2026-05-02)**: with Step 1a (lifetime earnings) deliberately not implemented in this suite, the distinct value of `/fi:net-worth` versus the closing block of `/fi:holdings-scaffold` is thin. Both render the same Step 1 framing against the same numbers. Consider merging this skill into `/fi:holdings-scaffold` before promoting either to `alpha`. See YMOYL audit §8.

---

## The concept (decades-stable)

Net worth = what you own minus what you owe. Honest accounting includes hard-to-value assets (real estate, vehicles), debts that don't feel "real" (mortgages, student loans), and any non-base currencies the user holds. The number is data, not a verdict.

---

## The pattern (~5-year stable)

**Read-only.** Reads from `holdings.md`. Does not capture anything new from the user. Output is either a clean readout to chat OR a "Net Worth" section appended to the holdings file at the user's preference.

---

## What the skill does at runtime

1. Reads `holdings.md`. Validates schema (`holdings-schema-version: 1`).
2. Computes:
   - Asset side: investment + real estate + vehicles + saleable inventory + cash + CDs
   - Liability side: mortgage + other loans + credit-card balances + other debt
   - Net = assets - liabilities
3. Multi-currency conversion at runtime (FX-at-read-time rule from holdings-scaffold) — query `api.frankfurter.dev` for current rates; never trust frozen aggregator conversions.
4. Renders the YMOYL Step 1 framing block:

   > *This file completes Step 1 of Your Money or Your Life — what Vicki Robin calls "making peace with the past." Read it like a weather report. Not a verdict on your self-worth. The past is just data. It does not determine the future. We build on this.*

5. Output destination per user preference:
   - Chat readout only (default for re-runs)
   - Append a "Net Worth (snapshot YYYY-MM-DD)" section to `holdings.md`
   - Separate `~/finances/net-worth-YYYY-MM-DD.md` file

---

## Headless behavior

Fully supported. Reads `holdings.md`, computes net worth, writes to configured output. Useful for cron-driven monthly snapshots feeding into `/fi:fu-money-readout` or external dashboards the user maintains.

---

## TODO

- [ ] Decide: merge into `/fi:holdings-scaffold` closing block, or keep as separate skill? (Open question above; resolve before `alpha`.)
- [ ] Multi-currency net-worth handling — confirm FX-at-read-time pattern is consistent with `/fi:holdings-scaffold`.
- [ ] Snapshot diffing: when the skill runs against a holdings file that has changed since the last snapshot, surface the delta cleanly.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1.
