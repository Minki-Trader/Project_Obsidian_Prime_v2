# Stage 06 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
4. `../../../docs/policies/tiered_readiness_exploration.md`
5. `../../../docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
6. `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
7. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
8. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
9. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
10. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 06 is now active, Stage 05 is closed, the strict Tier A runtime rule remains the only current runtime rule, and tiered-readiness work now has an explicit exploration-stage home`
- do not confuse with regular line: `Stage 06 is exploration-only work and does not imply operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` is now closed
- the first downstream exploration boundary is frozen on `broader_0002 + helper_0001 + broader_0003`
- `Tier A / Tier B / Tier C` readiness already has a downstream policy boundary and now has an active stage home

## Open Questions

- what exact Tier B eligibility rule should Stage 06 materialize first: group quorums, family-presence rules, or a more explicit readiness score?
- what minimum artifact, report, and registry boundary must every Tier B or Tier C exploration artifact carry so it never blurs with the strict Tier A line?
- does any first Stage 06 reduced-risk experiment need additional helper-lane or broader-lane evidence beyond the frozen Stage 05 evidence family before experimentation begins?
- should Tier B reuse the current model family with explicit readiness features, or require a separate model family and calibration path?
