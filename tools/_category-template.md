---
category: (Category name — e.g., "Transaction aggregators", "High-yield savings", "Resale platforms")
last-reviewed: YYYY-MM-DD
contributors:
  - (GitHub handle of last reviewer)
---

# [Category Name]

> Tool-layer file. 1-3 year half-life. The category itself (what kind of thing this is) is stable; the specific named tools rotate. Update whenever a major player enters/exits or terms change materially.

---

## What this category covers

One or two sentences about what role tools in this category play in the FI suite. Which skills read from this file. What user-need this category serves.

Example: *"Transaction aggregators consolidate bank, credit card, and brokerage transactions into a single view that the `fi-track-spending` skill can import. Without an aggregator, the user falls back to manual capture from each financial institution's website."*

---

## Current entries (last-reviewed YYYY-MM-DD)

For each tool currently named:

```
### [Tool Name]

- **Purpose**: brief
- **Pricing**: free / freemium / paid (with current $ figures)
- **Strengths**: 1-2 sentences
- **Weaknesses**: 1-2 sentences
- **Platforms**: (Web / iOS / Android / desktop / etc.)
- **Last verified working**: YYYY-MM-DD
- **Notes**: anything that might affect a user's choice (e.g., "owned by Empower, may shift toward wealth-management upsell over time")
```

---

## Replacement-shape notes

What does the category-shape look like, abstracted from any specific tool?

Example for "Transaction aggregators":

> *Replacement-shape: a service that connects to N financial institutions via Plaid (or equivalent), consolidates transactions into a single inbox, allows user-defined categories, exports CSV, doesn't sell data, costs <$15/mo. If a current named tool dies or pivots, the next entry in this category should fit this shape.*

---

## Tools no longer recommended (with reason)

Keep a short tail of tools that USED to be in this category but were removed. Document why so future readers don't accidentally re-add them.

Example:

```
- **Mint (RIP)** — sunset by Intuit Jan 2024. Was the dominant US aggregator for ~15 years.
- **Personal Capital** — pivoted to Empower Wealth-Management upsell; aggregator-only use no longer the product focus.
```

---

## What this file does NOT cover

Be explicit about scope.

Example: *"This file does NOT cover budgeting apps (separate category — see `tools/budgeting.md`). Aggregators consolidate transactions; budgeting apps add planning logic on top."*

---

## How to add an entry

If you want to add a tool to this category:

1. Verify it's been working as advertised for at least 3 months.
2. Check it fits the replacement-shape above.
3. Add an entry following the schema in "Current entries."
4. Update `last-reviewed` to today.
5. Add yourself to `contributors` in the frontmatter.
6. Open a PR with the addition; describe in the PR body why this tool deserves a slot in this category vs. existing options.

---

*Schema version: 1.0.*
