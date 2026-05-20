---
name: hourly-wage
description: Compute the user's real hourly wage — life-energy math. Takes income, subtracts the true cost of earning it, divides by every hour the work actually consumes (not just billed hours). Handles a single job or several income streams at different effective rates. Mode-aware — remote, hybrid, on-site, or gig. Use when a user wants to know what an hour of their life is really worth, or which of several engagements is actually paying well.
layer: concept+pattern
ymoyl_step: 2
mode_aware: true
status: draft
sources:
  - book: Your Money or Your Life
    contribution: "Step 2 — the real-hourly-wage calculation. Subtract every cost incurred because of the job; add every hour spent because of the job; divide. The classic on-site line items carry forward; the 1992 list assumed an office commuter."
  - book: Profit First (Michalowicz, 2017)
    contribution: "Owner-as-key-employee principle and purpose-bound treatment of business expenses — informs the shared-expense allocation across multiple income streams, and naturalizes a real wage for the business-owner case where 'wage' might otherwise be conflated with owner draw."
  - author: Marika Olson
    contribution: "2026 design refinements — work-mode branching (remote/hybrid/on-site/gig), AI/SaaS OpEx as a load-bearing line item, contracted-vs-cash income basis, explicit denominator-policy capture, load-phase tagging, shared-expense allocation, multi-stream per-engagement wages with a blended number, pro bono reported as its own line, dated-output trend tracking, headless pipeline mode."
last-reviewed: 2026-05-20
---

# /fi:hourly-wage

The number on a paycheck or an invoice is not the wage. The real hourly wage is
what's left after the costs of earning the money come out, divided by every hour
the work truly consumes — commute, prep, tooling upkeep, the always-on tax of
working from home. This skill walks the user to that number. Stay blunt: a
flattering number that ignores real costs is worse than no number.

Output: a dated wage file the user can re-run quarterly or after a major
work-mode change, with trend-over-time analysis as runs accrete.

## Step 1 — One stream or several?

Ask first: **"Do you earn from one job, or several income streams?"**

- **One** — run the single-stream path: Steps 2–7 once, skip the allocation and
  blending logic. Don't make a salaried user wade through per-engagement math.
- **Several** — run Steps 2–6 once per stream, then Step 7 produces a
  per-engagement wage for each plus a blended wage across all of them. The
  per-engagement numbers are the point: they reveal which work underpays.

For each stream the user names, also ask its **type**: paid, or pro bono /
civic / unpaid. Pro bono streams are carried through every step but reported
separately (Step 7) — never blended into the wage as if zero pay were a
failure. Unpaid work the user chose is life energy spent on purpose, and the
report says so.

## Step 2 — Work mode

Per stream, ask: **"What's the work mode — fully remote, hybrid (how many days
on-site), fully on-site, or gig/freelance multi-job?"** The mode decides which
expense and hour line items in Steps 4–5 are relevant. Don't assume remote.

## Step 3 — Income, and over what period

For each stream, get gross income **and pin the period** (a month, a quarter, a
year). Income and hours must cover the *same* window — Step 6 will refuse to
compute if they don't.

Ask which income figure the user means:

- **Contracted / accrued** — what the work earns for the period, billed or not.
- **Cash received** — what actually landed in the account.

These differ. A monthly retainer is earned every month even if an invoice is
late or stuck in a payment processor. If the user is pulling from an accounting
tool, that tool usually shows cash received — flag that it may understate a
period where income is earned but unpaid, and let the user choose which basis
to use. Apply the same basis to every stream.

### Step 3b — Employer-paid benefits (employee streams)

For any W-2 / employee stream, gross pay understates what the employer actually
spends on the user. Capture employer-paid benefits and add them to the
compensation side — otherwise a W-2 stream looks worse than an equivalent gig
that has to buy all of this out of pocket.

Ask, for each employee stream: **"Beyond gross pay, what employer-paid benefits
do you get? Give an annual value or 'none' for each."** Walk the main categories:

- Health, dental, vision premiums — the employer's share (W-2 box 12 code DD is
  the health figure; code D is the 401(k) amount, W is the employer HSA).
- 401(k)/403(b) match and any HSA employer contribution — employer dollars only,
  not the user's.
- Life and disability insurance premiums.
- Stipends and reimbursements — phone/internet, equipment, tuition, wellness.
- Paid time off — only when comparing across streams with different PTO levels;
  otherwise leave PTO inside declared hours (Step 4) and don't double-count.

Sum these into an employer-benefits total. **Total compensation = income
(Step 3) + employer-benefits total.** For employee streams the rest of the skill
computes off total compensation, not gross pay alone.

Gig / freelance streams: this section is mostly empty by design — the gig worker
pays for all of it themselves, and those payments show up as subtractions in
Step 5. That contrast is the point: a gig gross that looks higher than a W-2 is
often carrying the cost of everything an employer would otherwise provide.

Unvested equity (RSUs, options): default to **not counting it** — the real
hourly wage is what time is worth now, in this configuration. If the user wants
it tracked, record it on a separate "optionality" line, out of the wage math.

## Step 4 — Hours: the denominator

This is where most calculations cheat. Get **every hour the work consumes**, not
just billable hours.

First, settle the denominator policy — ask: **"What counts as work hours for
you? Just client/billable time, or also unbilled overhead — admin, business
development, tooling upkeep, learning?"** There is no universal answer; capture
the user's choice and apply it consistently. For a real hourly wage, unbilled
overhead that exists *only because of the job* belongs in the denominator even
when the user wouldn't bill it.

Then, by work mode, add to the hour count:

- **On-site / hybrid (classic):** commute time, prep time (getting ready,
  packing), decompression time after work, work-related errands and shopping.
- **Remote / hybrid (modern):** blurred-boundary hours — the always-on tax of
  working where you live; cognitive context-switching when home and work share
  space; time spent maintaining the tooling itself (software updates, prompt
  engineering, debugging integrations).
- **Gig / multi-job:** unpaid time between gigs that the work requires —
  searching, bidding, scheduling, platform admin.

If the user tracks time in a log or tool, read it for the period and total the
hours per stream. If not, walk them through estimating each bucket. Either way,
surface the total and let them correct it before continuing.

**Load-phase check.** Ask whether the period contained a one-time project load
unusual for the stream — a migration, a setup build, a one-off overhaul. If so,
tag the period as project-load, not steady-state. A wage measured during a
project-load month is real but unrepresentative; the report (Step 7) must say
which kind of month it is, and a pricing decision should never rest on a single
project-load reading.

## Step 5 — Subtract the cost of earning

Per stream and work mode, subtract job-related expenses from income. Surface
only the line items the mode makes relevant.

- **On-site / hybrid (classic):** commuting costs, work clothing, work meals
  out, decompression spending, "escape" entertainment, job-related health costs.
- **Remote / hybrid (modern):**
  - Home internet — work-attributed portion.
  - Home electricity — work-attributed portion (desk, monitors, heating/cooling
    during work hours).
  - Home-office space — depreciation or rent allocation.
  - Ergonomic furniture and equipment, amortized over useful life.
  - **AI / SaaS operating expense** — subscriptions and metered API spend for
    the tools the work runs on. This line is growing and routinely ignored;
    ignoring it pretends the wage is higher than it is.
  - Equipment refresh cycle (laptop, monitor, headset), amortized.
  - Isolation costs — anything that replaces the incidental social contact and
    movement of an office (gym, body work, therapy, co-working day passes).
- **Gig / multi-job:** platform fees, self-employment tax delta, unreimbursed
  supplies, equipment.

**Shared-expense allocation (multi-stream only).** Some costs — AI/SaaS, home
internet, electricity — serve every stream and can't be charged to one. Ask the
user to pick an allocation basis **once**: by share of hours, or by share of
revenue. Apply it to every shared cost and every stream consistently. State the
basis in the report.

## Step 6 — User-extensible categories, then verify

Ask: **"Any other costs or hours specific to your situation we should factor
in?"** Capture each addition against the stream it belongs to. Persist these to
`~/finances/profile/hourly-wage-custom-categories.md` (gitignored) so subsequent
runs offer them instead of re-asking from scratch.

Before computing, verify both sides cover the same period (Step 3) and that
neither side is suspiciously thin (e.g. income logged but almost no hours, or a
period only partly tracked). If a side is incomplete, say so plainly and either
narrow the period to what's solid or flag the result as provisional. Never
compute silently over a gap.

## Step 7 — Compute and report

Per stream:

```
compensation = income for the period
             + employer-paid benefits      (employee streams; 0 for gig — Step 3b)

real hourly wage = (compensation − job-related expenses − allocated shared expenses)
                 ÷ (all job-related hours for the period)
```

Report, per stream:

- The **real hourly wage** as a computed result — not a target the user typed.
  State it directly. If it's far below or above what the user expected, say so.
- **Gross hourly** (income ÷ hours, before expenses and before benefits)
  alongside it, so the cost of earning is visible as the gap between the two.
- Where employer benefits apply, a **total-comp hourly** line (compensation ÷
  hours) — what the employer actually pays per hour, before subtractions hit it.
- The load phase of the period (steady-state or project-load).

For multiple streams, add:

- A **blended real hourly wage** across all paid streams.
- Pro bono / civic streams reported on their own line as life energy spent by
  choice — hours shown, wage not blended in.
- A one-line read on which stream pays best and worst per hour, and — where the
  data supports it — why.

Keep the output short and concrete. The user should be able to act on it: raise
a rate, cap hours on a stream, drop or reprice the worst performer, or decide a
low number is a price worth paying. The number is descriptive, not prescriptive
— whether the wage is "too low" is the user's call, and the values check is
`/fi:three-questions`' job. If the wage surprised the user, `/fi:redirect` and
`/fi:fu-money-readout` may need a re-run, since the surplus and runway shift
when real income shifts.

## Output

Write each run to `~/finances/hourly-wage/YYYY-MM-DD.md` (create the directory
if needed). One file per run — a dated snapshot, never overwritten. Validate
`.gitignore` coverage before writing; warn if the path is not ignored.

```markdown
---
date: YYYY-MM-DD
mode: remote | hybrid | on-site | gig | mixed
streams: [stream-name, ...]
income-basis: contracted | cash
load-phase: steady-state | project-load
generated-by: /fi:hourly-wage
---

# Real hourly wage — YYYY-MM-DD

## <stream name>
| | Gross | Total comp | Real |
|---|---|---|---|
| Hourly | $... | $... | $... |
| For the period | $... | $... | $... |
| Hours | ... | ... | ... |

### Employer benefits (added to compensation)
| Category | Value |
|---|---|
| ... | ... |

### Subtractions (job-related costs)
| Category | Amount |
|---|---|
| ... | ... |

### Additions (job-related hours) / custom categories
- ...

## Blended (paid streams)
- Blended real hourly: $...
- Pro bono / civic: <hours>, reported separately

## Trend
| Date | Mode | Real hourly | Delta from prior |
|---|---|---|---|
| YYYY-MM-DD | ... | $... | first run |
```

On later runs, read prior `hourly-wage/*.md` files and append a row to the Trend
table of the newest run. Don't modify prior files — each is a snapshot.

## Pipeline mode (headless)

When invoked by another agent or a scheduled run with no human present:

- Read income and hours from the file paths or tool the user configured.
- Default to the **contracted/accrued** income basis, **all-hours** denominator,
  and **steady-state** load phase unless overrides are passed.
- Use the last-saved allocation basis; if none exists, default to share-of-hours.
- Write the per-stream and blended results to the configured output path. Do not
  block on input. If a required source is missing, write a clear error to the
  output and exit — never hang.

## Privacy

User-specific data — income, expense amounts, employer names, vendor patterns —
is never embedded in this skill file or committed to the plugin repo. All user
data writes go to gitignored paths on the user's machine (`~/finances/`). The
skill validates `.gitignore` coverage before writing, and warns if no git repo
exists. See `AGENTS.md` for the cross-skill privacy posture.

## Sources

- **Your Money or Your Life**, Vicki Robin & Joe Dominguez — Step 2 originated
  the real-hourly-wage calculation: subtract job-related costs from pay, add
  job-related hours to the denominator. The classic line items in Steps 4–5
  come from here.
- **Profit First**, Mike Michalowicz — purpose-bound treatment of business
  expenses informs the shared-expense allocation in Step 5, and the
  owner-as-key-employee principle naturalizes a real wage for business owners.
- **2026 modernization** — remote/hybrid line items (AI/SaaS OpEx, home-utility
  work-portions, blurred-boundary hours), the employer-benefits numerator, and
  the multi-stream / per-engagement structure are additions to the original
  single-job framework.
- **Community-contributed categories** — added via the user-extensible step
  (Step 6); promoted to this list with attribution when they recur.
