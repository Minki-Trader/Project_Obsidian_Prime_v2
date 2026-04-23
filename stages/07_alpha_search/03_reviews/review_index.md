# Stage 07 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../01_inputs/stage07_tier_b_dual_verdict_local_spec.md`
4. `../../../docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md`
5. `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
6. `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
7. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
8. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
9. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
10. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
11. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
12. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
13. `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
14. `../../06_tiered_readiness_exploration/04_selected/selection_status.md`
15. `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: Stage 07 is now active and its first bounded packet is fixed as the `Tier B dual verdict packet (Tier B 이중 판정 팩)` on a validated user-weight rerun rather than as a generic opening alpha-search pack
- lane read: the `Tier A main lane (Tier A 메인 레인)` remains the only current runtime-aligned line, while the separate `Tier B lane (Tier B 별도 레인)` now starts from the shared keep42 reduced-context model and must earn both `separate lane survival (별도 레인 생존)` and `MT5 feasibility candidate handoff (MT5 가능성 후보 이관)` explicitly
- do not confuse with operating line: Stage 07 remains an alpha-search stage and the dual-verdict packet does not imply an opened `MT5 path (MT5 경로)` or a promoted operating-line claim (승격 운영선 주장)

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` remains closed
- `06_tiered_readiness_exploration` is now also closed as the first exploration-only readiness family closure
- the first Stage 06 readiness boundary, scorecard, baseline family, follow-up pack, and reduced-context model now give Stage 07 a durable bounded starting surface
- `Tier B` remains separate from `Tier A` and is still `offline-only (오프라인 전용)` at Stage 07 opening
- the first Stage 07 packet shape is now fixed as the validated user-weight `Tier B dual verdict packet (Tier B 이중 판정 팩)`

## Open Questions

- after the validated user-weight rerun, does the separate `Tier B lane (Tier B 별도 레인)` survive as `keep` or close as `prune`?
- after the validated user-weight rerun, does the packet earn `MT5 feasibility candidate (MT5 가능성 후보)` status as `yes` or `no`?
- should one optional `macro-aware (매크로 인지)` Tier B variant be materialized only after the dual-verdict packet closes with `separate_lane_verdict=keep`?
