---
name: fi-lifetime-earnings
description: Reconstructs total lifetime earnings — the YMOYL Step 1 catch-up artifact. Used as the "what did all that work add up to?" anchor for everything else.
layer: concept+pattern
ymoyl_step: 1
mode_aware: false
status: scaffold
sources:
  - book: Your Money or Your Life
    contribution: "Step 1a — total lifetime earnings as half of 'making peace with the past'"
last-reviewed: 2026-05-01
---

# fi-lifetime-earnings

Walks the user through reconstructing total lifetime earnings — every dollar of W-2, 1099, self-employment, and other earned income they've ever received. Pairs with `fi-net-worth` (Step 1b) to deliver YMOYL's full Step 1.

---

## The concept (decades-stable)

Most adults can't say with confidence how much money has flowed through their hands across their working life. The number is psychologically powerful: it's both larger than people guess (decades of compounding paychecks add up) and humbling against current net worth (where did it all go?). Surfacing the gap is the foundation of every conscious financial choice that follows.

The skill is not for tax purposes. It's for orientation.

---

## The pattern (~5-year stable)

Build the number from authoritative sources, in the order they're easiest to retrieve:

1. **Most recent decade**: pull from tax returns (the user's own records).
2. **Pre-records era**: pull from the country's social security or equivalent earnings record (US: SSA earnings statement; UK: HMRC; Canada: CPP statement of contributions).
3. **Gaps**: estimate honestly with documented assumptions (e.g., "first job $X/yr 1996-1998, no records remain").

Result is a `lifetime-earnings.md` file in the user's `~/finances/` directory (gitignored), structured by year, with sources cited.

---

## What the skill does at runtime

1. Confirms the user's country (drives which earnings-record source to use).
2. Walks the user through retrieving the latest version of their country's earnings record.
3. Captures year-by-year earned income.
4. Adds non-W-2 income sources (1099, self-employment, foreign earnings, royalties) the official record might miss.
5. Generates a year-by-year table with running total + a "current dollars" column (each year's nominal earnings inflation-adjusted to current purchasing power).
6. Writes the result to `~/finances/lifetime-earnings.md`, gitignored.

---

## Headless behavior

Not generally headless — interactive walkthrough by design. Optional manifest-input mode planned (similar to `fi-holdings-scaffold`).

---

## TODO

- [ ] Per-country earnings-record retrieval guidance (delegated to `references/earnings-records/` per country).
- [ ] Inflation-adjustment math; pull source rates dynamically (BLS / ONS / StatsCan / etc.).
- [ ] Schema for the output file so `fi-net-worth` can read the lifetime total for the catch-up framing.

---

## Sources

- **Vicki Robin & Joe Dominguez**, *Your Money or Your Life* (1992; rev. 2018). Step 1a.
