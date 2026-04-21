# Stage 06 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
4. `../01_inputs/stage06_v2_baseline_seed_local_spec.md`
5. `../03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
6. `../../../docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
7. `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
8. `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
9. `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
10. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
11. `../../../docs/policies/tiered_readiness_exploration.md`
12. `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
13. `../../../docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
14. `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
15. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
16. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
17. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
18. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 06 is now active, Stage 05 is closed, the strict Tier A runtime rule remains the only current runtime rule, the first deterministic Tier B or Tier C boundary plus the first reporting interface are fixed, the first scorecard is materialized, and the first v2-native baseline seed plus Tier B offline evaluation report now exist on separate Tier A and Tier B reporting lanes without inheriting legacy model artifacts`
- do not confuse with regular line: `Stage 06 is exploration-only work and does not imply operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` is now closed
- the first downstream exploration boundary is frozen on `broader_0002 + helper_0001 + broader_0003`
- `Tier A / Tier B / Tier C` readiness already has a downstream policy boundary and now has an active stage home
- the first exact Tier B eligibility rule and the first reporting-boundary interface are now fixed for Stage 06
- the first Stage 06 row-level scorecard summary and review report are now materialized on the fixed readiness boundary
- the first Stage 06 offline-only Tier B charter remains accepted, but its baseline-family reuse hypothesis is now superseded by a first `Tier A`-trained v2-native baseline seed with separate `tier_b_exploration` reporting
- the first Stage 06 `Tier B offline evaluation report` now exists and carries separate `validation`, `holdout`, and `calibration read` summaries without claiming runtime-family or promotion meaning
- `B-mixed-partial` now remains vocabulary only and is not an eligible first-boundary rule

## Open Questions

- what is the narrowest first follow-up for the v2-native baseline seed family: a separate `threshold read` or a separate `calibration fit`?
- does the placeholder monthly-weight caveat require a real-weight rerun before any later simulated execution or MT5-path expansion?
