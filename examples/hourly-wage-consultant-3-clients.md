# Worked example — /fi:hourly-wage: consultant, 3 clients

> Anonymized illustration. All figures are invented to show the skill's logic —
> not anyone's real client data.

A freelance consultant runs `/fi:hourly-wage` for **Q1** (a one-quarter period).
She wants to know which engagements actually pay well per hour of life energy.

## Step 1 — Streams

Three streams:

- **Client A** — ongoing retainer. Type: paid.
- **Client B** — project engagement. Type: paid.
- **Client C** — nonprofit advisory. Type: pro bono.

Multi-stream path: Steps 2–6 run per stream; Step 7 produces a per-engagement
wage plus a blended number.

## Step 2 — Work mode

All three are **gig / freelance** (remote, no employer). No employer-benefits
section (Step 3b is empty by design for gig streams).

## Step 3 — Income and period

Basis chosen: **contracted / accrued**. Client B's Q1 invoice is still unpaid in
the payment processor, but the work was delivered — it counts at the accrued
basis, applied to all three streams.

| Stream | Contracted income (Q1) |
|---|---|
| Client A | $6,000 |
| Client B | $4,500 |
| Client C | $0 (pro bono) |

## Step 4 — Hours (denominator)

Denominator policy: **all job-related hours**, billable plus unbilled overhead
(admin, business development, tooling upkeep).

| Stream | Billed hours | Real hours (all job-related) |
|---|---|---|
| Client A | 90 | 140 |
| Client B | 60 | 85 |
| Client C | — | 30 |

**Load-phase check.** Client A's Q1 included a one-time CRM migration (~25
hours) that won't recur. Client A's quarter is tagged **project-load**; B and C
are **steady-state**.

## Step 5 — Subtract the cost of earning

Direct (per-stream) expenses:

| Stream | Direct expenses |
|---|---|
| Client A | travel $200 + stream-specific software $60 = $260 |
| Client B | platform fee $135 |

Shared expenses (serve every paid stream) for Q1: AI/SaaS $480 + home internet
work-portion $90 + electricity work-portion $75 = **$645**.

Allocation basis chosen **once**: **by share of hours** (paid streams only —
225 real hours total: A 140, B 85).

- Client A: 140 / 225 = 62.2% → **$401**
- Client B: 85 / 225 = 37.8% → **$244**

## Step 6 — Custom categories, verify

No extra categories. Income and hours both cover Q1 — periods match. Both sides
are fully tracked. Proceed.

## Step 7 — Compute and report

```
real hourly wage = (income − direct expenses − allocated shared expenses) ÷ real hours
```

| Stream | Income | Direct | Allocated shared | Real pay | Real hours | Real hourly |
|---|---|---|---|---|---|---|
| Client A | $6,000 | $260 | $401 | $5,339 | 140 | **$38.14/hr** |
| Client B | $4,500 | $135 | $244 | $4,121 | 85 | **$48.48/hr** |

Context lines:

- **Client A** bills at $66.67/billed-hr ($6,000 ÷ 90) but earns **$38.14/hr**
  of real life energy. The gap is unbilled overhead — 140 real hours against 90
  billed.
- **Client B** bills at $75.00/billed-hr ($4,500 ÷ 60); real **$48.48/hr**.

**Blended real hourly (paid streams):** ($5,339 + $4,121) ÷ 225 = **$42.04/hr**.

**Client C (pro bono):** 30 hours, reported on its own line — life energy spent
by choice, never blended into the wage.

**Load-phase caveat:** Client A's quarter is project-load. The one-time
migration inflated its hours; a steady-state quarter (~115 real hours) would put
Client A's real wage near $46/hr. **Do not reprice Client A off this single
project-load reading** — re-run after a normal quarter first.

**One-line read:** Client B is the strongest engagement per hour of real life
energy. Client A's retainer *feels* like the anchor, but even adjusting for
project-load it trails B — it's the reprice-or-cap candidate once a
steady-state quarter confirms the pattern.

## Output

Written to `~/finances/hourly-wage/2026-03-31.md` with a Trend table seeded for
future quarterly re-runs.
