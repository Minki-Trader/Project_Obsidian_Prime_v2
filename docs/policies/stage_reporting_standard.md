# Stage Reporting Standard

This note turns the current experiment-review lessons into a reusable reporting rule set.

## Why This Exists

- Some stages need an early `structural_scout` read to learn rule behavior quickly.
- The same stage may still need a separate `regular_risk_execution` read before any operating decision is trustworthy.
- Selection notes are easier to re-enter when every stage uses the same sections and promotion gates.
- Governance telemetry becomes more useful when every comparison report exposes the same core fields.
- Run evidence becomes reusable when every reviewed run keeps measurement, managed identity, and lane-aware judgment.

## Dual Scoreboard Rule

For any stage that changes exit behavior, position sizing, or execution semantics, keep two scoreboards:

1. `structural_scout`
   - frozen scouting assumptions
   - usually fixed-lot or reduced execution complexity
   - goal: understand rule shape, clipping, containment, and interaction risk
2. `regular_risk_execution`
   - intended operating assumptions
   - live-like risk sizing and stop behavior
   - goal: decide the real incumbent / challenger relationship

Do not treat the `structural_scout` winner as `operating_promotion` unless the `regular_risk_execution` scoreboard agrees and the remaining hard gates are closed. It may become `promotion_candidate` evidence, but not `operating_promotion` by itself.

These scoreboard names are also part of `docs/policies/kpi_measurement_standard.md`. Stage reports may summarize them, but detailed machine-readable KPI evidence should live in each run's `kpi_record.json` when a run is reviewed.

## Selection Status Standard

Each active stage should keep `04_selected/selection_status.md` with these sections:

1. `Current Read`
2. `Promotion Gates`
3. `Scoreboards`
4. `Headline`
5. `Risk`
6. `Diagnostics`
7. `Execution`
8. `Decision`
9. `Follow-Up Bias`
10. `Report Refs`

The selection note should answer four questions quickly:

- What is the current incumbent?
- What is the current challenger?
- Under which scoreboard was that decision made?
- What evidence still has to improve before promotion is allowed?

## Review Index Standard

Each active later-stage review folder should keep `03_reviews/review_index.md` with:

- the review reading order
- the latest regular decision
- the latest structural-scout decision when it differs
- any closed diagnostic branches that should not be mistaken for the regular line

## Governance Summary Standard

Human-facing governance summaries should always expose a stable comparison core:

- `headline`: return, PF, DD, trades
- `risk`: ulcer / worst-week / other available stress metrics
- `diagnostics`: no-trade rate, long-short mix, key trade-shape diagnostics
- `execution`: external skip pressure, argmax concentration, entropy, overlay rate, top skip reasons, ready-row gap

If a value is unavailable, show `n/a` and say why. Do not silently emit `None`.

## Run Evidence Standard

For reviewed run outputs, keep three surfaces distinct:

- `run_manifest.json`: managed identity, lineage, inputs, and artifact references
- `kpi_record.json`: layered KPI evidence for machine reading
- `result_summary.md`: human readout and lane-aware judgment

Record the durable row in `docs/registers/run_registry.csv` when a run becomes reviewed, selected, archived, invalidated, or superseded.

Use `runtime_probe` for runtime observation without closure authority, and reserve `runtime_authority` for closure, handoff, or live-like readiness claims.

## Branch Re-entry Standard

When branch work is materially ahead of `main`, keep `docs/context/current_working_state.md` updated with:

- current branch name
- where the latest decisions live
- which diagnostics are closed and should not be reopened casually
- the current operating incumbent / challenger pair
