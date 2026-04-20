# Stage 06 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
4. `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
5. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
6. `../../../docs/policies/tiered_readiness_exploration.md`
7. `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
8. `../../../docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
9. `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
10. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
11. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
12. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
13. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 06 is now active, Stage 05 is closed, the strict Tier A runtime rule remains the only current runtime rule, and the first deterministic Tier B or Tier C boundary plus the first reporting interface are now fixed at the docs-only governance layer`
- do not confuse with regular line: `Stage 06 is exploration-only work and does not imply operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` is now closed
- the first downstream exploration boundary is frozen on `broader_0002 + helper_0001 + broader_0003`
- `Tier A / Tier B / Tier C` readiness already has a downstream policy boundary and now has an active stage home
- the first exact Tier B eligibility rule and the first reporting-boundary interface are now fixed for Stage 06
- the first Stage 06 row-level scorecard summary and review report are now materialized on the fixed readiness boundary
- `B-mixed-partial` now remains vocabulary only and is not an eligible first-boundary rule

## Open Questions

- does the first materialized scorecard justify opening a Tier B reduced-risk experiment immediately, or is additional helper-lane or broader-lane evidence still required before experimentation begins?
- should Tier B reuse the current model family with explicit readiness features, or require a separate model family and calibration path?
