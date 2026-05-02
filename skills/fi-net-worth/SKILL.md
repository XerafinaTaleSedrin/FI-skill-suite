---
name: fi-net-worth
description: Computes the user's current net worth from the holdings.md sentinel file. The "where do I actually stand right now?" half of YMOYL Step 1.
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 1b — current net worth as half of 'making peace with the past'"
last-reviewed: 2026-05-01
---

# fi-net-worth

Reads `holdings.md` (created by `fi-holdings-scaffold`) and produces the user's current net worth, with the YMOYL Step 1 catch-up framing comparing total lifetime earnings (`fi-lifetime-earnings` output) against current net worth.

---

## The concept (decades-stable)

Net worth = what you own minus what you owe. Run honestly, this includes hard-to-value assets (real estate, vehicles), debts that never feel "real" (mortgages, student loans), and all currencies you hold. The catch-up framing — *I earned $X across my life; I have $Y now* — surfaces the gap that motivates every later step in the YMOYL program.

---

## The pattern (~5-year stable)

Read-only skill. It does not capture anything new from the user; it reads from the sentinel files (`holdings.md`, `lifetime-earnings.md`) that other skills populate. Output is a clean section in the user's existing `holdings.md`, OR a separate readout if the user prefers.

---

## What the skill does at runtime

1. Reads `holdings.md`. Validates schema.
2. Reads `lifetime-earnings.md` if present (optional).
3. Computes:
   - Asset side: investment account balances + real estate (gross) + vehicles + other assets
   - Liability side: mortgage + other loans + credit card balances + other debt
   - Net = assets - liabilities
4. If `lifetime-earnings.md` present: computes the catch-up framing (lifetime earnings vs current net worth, with both nominal and inflation-adjusted views).
5. Writes the result to a "Net Worth" section in `holdings.md` OR to a separate `~/finances/net-worth.md` readout per user preference.

---

## Headless behavior

Fully supported. Reads the sentinel files, computes net worth, writes to the configured output location. Useful for cron-driven monthly snapshots.

---

## TODO

- [ ] Define schema for "non-investment assets" section in `holdings.md`.
- [ ] Multi-currency net-worth handling (read native, convert at runtime).
- [ ] Catch-up framing presentation: how to display the gap between lifetime earnings and net worth without being moralistic.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1b.
