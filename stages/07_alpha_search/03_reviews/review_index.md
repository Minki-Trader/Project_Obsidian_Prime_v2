# Stage 07 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
4. `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
5. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
6. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
7. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
8. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
9. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
10. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
11. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
12. `../../06_tiered_readiness_exploration/04_selected/selection_status.md`
13. `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 07 is now active because Stage 06 already fixed the readiness boundary, separate reporting interface, first v2-native baseline seed family, additive follow-up pack, and first shared keep42 reduced-context model clearly enough that later alpha-search work can move downstream without reopening the same readiness debate`
- lane read: the `Tier A main lane (Tier A 메인 레인)` remains the only current runtime-aligned line, while the separate `Tier B offline-only lane (Tier B 별도 오프라인 전용 레인)` now starts from the shared keep42 reduced-context model with separate reporting and info-only subtype tags
- do not confuse with operating line: `Stage 07 is an alpha-search stage and still does not imply MT5 readiness, simulated execution, or operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` remains closed
- `06_tiered_readiness_exploration` is now also closed as the first exploration-only readiness family closure
- the first Stage 06 readiness boundary, scorecard, baseline family, follow-up pack, and reduced-context model now give Stage 07 a durable bounded starting surface
- `Tier B` remains separate from `Tier A` and is still `offline-only (오프라인 전용)` at Stage 07 opening

## Open Questions

- what is the narrowest first `Stage 07 alpha-search pack (Stage 07 알파 탐색 팩)` across the `Tier A main lane` and the separate `Tier B` lane?
- should one optional `macro-aware (매크로 인지)` Tier B variant be materialized only after the shared keep42 lane receives its first Stage 07 search read?
- does the placeholder monthly-weight caveat still force a real-weight rerun before any later `simulated execution (가상 실행)` or `MT5-path expansion (MT5 경로 확장)`?
- does the separate `Tier B` lane survive the first Stage 07 alpha-search read strongly enough to stay open?
