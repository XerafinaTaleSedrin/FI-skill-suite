# Design log — Suite reorder + capture-skill restructure

**Date**: 2026-05-02 (Saturday evening session)
**Status**: Decisions captured; encoding pending tomorrow morning.
**Trigger**: Phase 2 of plugin packaging began as "run /fi:holdings-scaffold end-to-end on Marika's data." Evolved into substantive suite redesign as the design friction surfaced from real use.

---

## Decisions

### 1. Suite ordering — canonical sequence

YMOYL's original ordering puts the most shocking number (real hourly wage, Step 2) before the most orienting number (crossover, Step 8). That works for early-career low-net-worth readers whose threshold question is theoretical and whose wage shock is the motivating force. For mid-career readers with substantial holdings, the ordering inverts: the threshold answer determines what the wage exercise even means.

Canonical reordered sequence:

```
1.  /fi:holdings-scaffold     What I have
2.  /fi:track-flow            Money in + money out (one skill, two outputs)
3.  /fi:monthly-tabulation    Categorize the spending side
4.  /fi:fu-money-readout      Daily/weekly orienting view: % of FI
5.  /fi:crossover             Formal threshold math, mode-aware
6.  /fi:hourly-wage           Does my work close the gap? (uses /fi:track-time)
7.  /fi:three-questions       Values check per category
8.  /fi:wallchart             Long-arc trend
9.  /fi:investing             Allocation strategy

Capture-layer skills (feed everything above):
- /fi:track-flow              Dollars in/out
- /fi:track-time              Hours by client/project (NEW)
```

### 2. Capture-layer split

Two capture skills feed the analytical layer:

- **`/fi:track-flow`** (renamed from `/fi:track-spending`, broader scope) — captures both income and expense rows from a single data source (aggregator CSV, bank statements, walkthrough). Auto-classifies. Outputs monthly income total, monthly expense total, by-month time series.
- **`/fi:track-time`** (NEW) — captures hours by client/project. Auto-track-from-conversation pattern; light periodic confirmation; end-of-day total; weekly aggregation in Saturday review.

Why combined `/fi:track-flow` instead of parallel `/fi:track-income` + `/fi:track-spending`: aggregator exports include both income and expense rows in one file. Two parallel skills would force the user to import the same file twice. The combined skill handles classification internally.

### 3. "Everything flowing" interrogation pattern

After CSV import (or walkthrough), `/fi:track-flow` runs an explicit pass to surface flow that aggregators systematically miss:

- **Cash flow**: cash income (tips, side gigs paid in cash, farmer's market sales, cash gifts), cash expenses (in-person spending not on a card)
- **Recurring family / partner support** (load-bearing — most aggregators classify this opaquely): monthly transfers from parents, parental subsidies (childcare, college contributions, paid bills), partner contributions to shared expenses, ongoing financial support framed as "loans" for tax-shielding even when no repayment is expected. *This category alone can be $500-2000+/mo for many users and is usually invisible to the aggregator.*
- **Non-cash value flow**: bartering / in-kind exchange, non-monetary benefits received (free housing, employer-provided meals, comped services), crypto activity not in aggregator
- **Missed accounts/channels**: Venmo / Cash App / Zelle / PayPal flows that don't auto-classify; old/foreign/business accounts not connected; reimbursements (income? expense reversal? neutral?); loans in/out
- **Forgotten/dormant accounts** (parallel pattern, also applies to `/fi:holdings-scaffold`): *"Do you have any account you've forgotten about, or haven't checked in months?"* Examples: old TSP/401k from a previous job, ESOPs, foreign bank accounts, dormant brokerage accounts, custodial/UTMA accounts from when you were a minor, gift accounts you opened for someone else, savings bonds from grandparents, company stock plans never claimed, accounts whose aggregator connection broke and never got re-fixed (Marika's TSP is the exemplar — disconnected for months at a time when she "can't be bothered to hook it back up").
- **One-time / annual flows**: tax refunds, bonuses, RSU vesting, insurance reimbursements, settlements, lump-sum inheritance, one-time gifts received

Skill captures these as monthly-equivalent, flags them, folds into totals. Documenting "considered and zero" is honest data. Bartering specifically belongs here — YMOYL doesn't address it; rural/PNW/homestead/mutual-aid communities use it heavily; ignoring it understates true life-energy flow. Family support specifically belongs here — YMOYL doesn't address it; for early-career, between-jobs, and partial-retirement users, recurring family transfers are extremely common and meaningfully change the FU readout when included.

This is a generalizable capture-skill pattern, also applies retroactively to `/fi:holdings-scaffold` (where the "everything saleable" prompt is the structural parallel). Should become an AGENTS.md rule.

### 4. `/fi:fu-money-readout` — tone + format

**Output structure (gap-first):**

```
=== FU Money Readout (YYYY-MM-DD) ===

THE GAP
You are at:       XX% of your FI target
At retirement:    YY% (Coast FI projection)
Status:           on track / behind / crossed

WHAT WOULD CLOSE THE REMAINING GAP
- $X,XXX/mo more income, OR
- $Y,YYY/mo less spending, OR
- $Z,ZZZ/mo more passive income

THE NUMBERS (decomposed)
Recurring passive:  $X,XXX/mo (list sources)
Monthly expenses:   $X,XXX/mo
Net direction:      [+/-]$X,XXX/mo
Runway:             XX months liquid + Y years sequential drawdown
Coast FI status:    crossed (✓) / on track / behind
```

**Tone principle**: honest about position, precise about distinctions, neither patronizing nor depressing. Reference example: *"You're financially free in the way that matters; you're just not free to never work again. Those are two different questions."*

**No mode-jargon labels.** Internally the skill knows about full-stop / location-time / income-downshift / Coast FI variants — but the user-facing readout shows just "% of your target." User picks the target percentage at setup; the skill never surfaces the labels in daily output.

### 5. `/fi:crossover` — division of labor with readout

- **`/fi:fu-money-readout`** (daily UX): simple math (passive ÷ expenses); single % display; three-state status; next-step guidance. Run frequently.
- **`/fi:crossover`** (formal deep-dive): same gap number with sensitivity analysis (real return ±1%, spending ±10%, mode-variant), drawdown-sequence modeling, bridge-years math, sequence-of-returns risk. Run when sitting down to plan.

Both compute the same fundamental gap. Readout is the daily interface; crossover is when planning depth is needed.

### 6. AGENTS.md additions

Three new rules / posture clarifications:

1. **Capture skills must include an outside-the-data interrogation pass.** Aggregators / spreadsheets / time-trackers all systematically miss certain categories. The skill's job is to surface those categories explicitly so the user can fill them in. Otherwise the skill is a CSV parser inheriting the aggregator's blind spots.

2. **Assume the user is interested.** They downloaded the skill suite. Don't gate offerings or truncate based on assumed disengagement. Coast-FI users are arguably MORE likely to want the deep diagnostic, not less. Offer the full picture; let the user choose.

3. **Tone principle for readouts**: honest about position, precise about distinctions, neither patronizing nor depressing. Numbers honest, even when uncomfortable. No false motivation; no false comfort. Match what the math actually says.

### 7. YMOYL audit §5 — refinement

Add paragraph capturing:
- The ordering critique (threshold-before-wage for mid-career readers)
- The accessibility-bias correction (data-readiness branch + working-estimate path)
- The assumed-engagement posture (don't truncate based on assumed user state)

This is a substantive audit-level refinement, similar in weight to the §4 lifetime-earnings critique already shipped.

### 8. Data-readiness branch (UX)

After `/fi:holdings-scaffold` (Step 1), the suite asks:

> *"For your spending side, three options:*
> - *Drag in your CSV (Monarch / Copilot / Tiller / Empower / bank export) — I'll parse it. ~5 min.*
> - *Bank statements last 3 months — I'll walk you through extracting totals. ~15 min.*
> - *Working estimate — give me your gut number. We'll get directional now and refine later.*
>
> *If you want to start tracking and don't yet have a tool: free options exist (Tiller free trial, Empower / Personal Capital free tier, Google Sheets templates). Tracking helps. Not tracking is fine for a directional read but caps your precision long-term."*

Marika has a Google Sheets annual-budget template she likes; will add the name to this language when she finds it.

---

## Encoding queue (tomorrow morning)

1. Rename `/fi:track-spending` → `/fi:track-flow` with broader scope (income + expense, single data source, "everything flowing" interrogation pass)
2. New `/fi:track-time` skill scaffold (hours capture; parallel to track-flow; auto-from-conversation; weekly aggregation)
3. Reorder skills in `00-overview.md` + `CLAUDE.md` to canonical sequence
4. Update `/fi:fu-money-readout` SKILL.md: gap-first output, three-state status, tone guideline, no-jargon-labels, % now + projected % at retirement
5. Update `/fi:crossover` SKILL.md: clarify division of labor with readout
6. Update YMOYL audit §5: ordering refinement + accessibility correction + assumed-engagement posture
7. AGENTS.md updates: outside-the-data rule, assume-user-engaged posture, readout tone principle
8. Komorebi-side: time-tracker rule + agent (auto-track-from-context system; replaces Xero-reminder rule)
9. Add Marika's preferred Google Sheets budget template name to data-readiness branch language (when she finds it)

Net suite change: −2 skills (lifetime-earnings, net-worth, both deleted prior commits) + 1 effective skill (track-time as net-new; track-flow is rename + scope expansion). Same or smaller skill count, meaningfully cleaner structure.

---

## Validation — the redesign was discovered, not designed

This redesign emerged from running the existing scaffolds against real data:

- `/fi:holdings-scaffold` was tested end-to-end on Marika's Monarch export. Surfaced the rate / maturity-date / progressive-enrichment / update-mode patterns.
- `/fi:hourly-wage` was tested conceptually against Marika's actual MOC numbers. Surfaced: compensation-structure-first ordering, multi-stream complexity, severance bracket-stacking, ramp vs. steady-state distinction, ADHD-aware always-on tax. Real hourly came out at $10.64/hr 2026, $14.57/hr 2027 with no-severance, ~$30/hr at 2x MOC scale.
- `/fi:crossover` was previewed conceptually. Surfaced: Coast FI crossed for Marika, full-stop FI ~16%, location-time flex variant ~20-27%, the "you're financially free in the way that matters" framing.
- The skill-ordering critique surfaced when the hourly-wage shock landed without context. The FU readout would have made the shock meaningful; running it after the hourly wage was backwards.

Marika's instinct on the reorder was correct. The skills work better in this sequence. The encoding tomorrow makes it canonical.

---

*Design log entry. Implementation pending. Encoding queue above.*
