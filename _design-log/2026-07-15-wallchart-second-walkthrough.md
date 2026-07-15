# Wallchart second walkthrough — 2026-07-15

The clean-second-walkthrough that 00-overview named as wallchart's outstanding draft-gate item (recorded 2026-07-14). Executed end-to-end as a fresh reader, following each SKILL.md step literally, on **synthetic data invented for the run** (8 months of `_trend-totals.csv` — one partial month, one deliberately miscategorized $31,900 bonus month — plus a holdings.md with a $412,000 investment total and $440,500 net worth, chosen unequal on purpose). No real user data anywhere in the run.

**Verdict: runnable end-to-end.** Every step produced its artifact — source check, stream aggregation, outlier detection (fired correctly on the planted spike), SWR prompt with real-dollar anchoring, crossover determination, all five Step 4b deterministic checks computable and passing, ASCII render, wallchart.md written to the full Step 6 schema, closing copy. No step dead-ends, contradicts another, or references a missing input. The blockers found are ambiguity, not runnability.

**Note on the alpha gate**: the status legend requires *real-run* evidence for alpha. A synthetic walkthrough is procedure evidence, not real-run evidence — status stays `draft`; whether this plus the 2026-05-28 QA pass satisfies the gate (or a real-data run is still wanted first) is the author's call.

---

## Fixed during the pass (small + unambiguous; one commit each)

1. **Outlier baseline undefined under 12 months** — and the 3-SD test computed with the candidate in-sample masks itself (the planted 5.5× spike scored z = 2.46). Now: all-available-months fallback, candidate-excluded stats.
2. **"Portfolio value" ambiguous** between investment-accounts total ($412,000) and net worth ($440,500) — 7% swing in the reference line; worse for homeowners. Now pinned to the investment-accounts total on both the wallchart and holdings-scaffold sides (non-investment assets aren't SWR-drawable).
3. **Stream named `business_income`, formula was net** — the CSV already carries `business_net`, invariant-guarded by track-flow. Now read directly.
4. **Partial month in trailing stats** — dragged the synthetic spending median $3,872 → $3,765 (a fake spending drop); and Step 4's "flat baseline" named no level. Now: stats and projection baseline over complete months (partial months still always plot), baseline = the At-a-glance trailing-6 median.
5. **"ASCII" chart isn't ASCII** — the Unicode markers raise encode errors on a default cp1252 Windows console (hit live). Plain-ASCII fallback set documented.

## Flagged, deliberately NOT fixed (design calls)

- **The not-yet-crossed projection ignores growth.** Step 4 grows the reference line "at the user's recent contribution rate" only. Synthetic case: contribution-only says ~52 years to crossover; the same inputs at a 5% real return say ~15. That is materially misleading pessimism for anyone mid-journey. Options: borrow `/fi:crossover`'s real-return assumption, or keep contribution-only and say so in a caveat. Either works; picking one is a design decision.
- **Windfall treatment is inconsistent by detection path.** A track-flow-classified `personal_windfall` (a $500 one in the synthetic data) never appears on the chart at all, while an outlier the user routes via option 3 becomes a rendered "windfall marker." Same concept, two treatments. Suggest rendering the `personal_windfall` column with the same marker device — but that changes what the chart shows, so it's a call, not a fix.
- **Outlier scan target is loose.** "Scan the income data" — per-stream, TOTAL, or both? (Ran both; the active stream is where miscategorization lives.) One sentence would fix it, but it interacts with the windfall question above; settle them together.
- **Option 3's replacement value is unstated.** Moving an outlier to a marker leaves a hole in the trend — filled it with the median of the other months; option 2's language implies trailing-median. Same cluster.
- **No algorithmic rendering spec.** Full-height vs half-height, band resolution, and collision behavior when two series land in the same band (hit concretely: TOTAL ~$6.5K and active $5.75K collide at a $2K band) are left to the renderer's judgment. Two fresh readers will draw different charts from identical data. Fine for a draft; worth a spec pass before beta. Cosmetic sibling: the Step 5 example legend gives personal-active and business the same `··` marker.

## What worked cleanly (worth keeping as-is)

Path resolution (four-step order, no hesitation about where anything lives); the include-all-months + dashed-partial plotting rule; the Step 3 flow-vs-reference conceptual clarification (prevented the classic capacity/cash confusion before it started); the SWR prompt's real-dollar anchoring + explicit Q&A invitation; all five deterministic checks being exactly computable as written; the Step 6 schema being complete enough to write the artifact without inventing anything.
