# Stage 07 Input Refs

## Required Contracts And Policies

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/artifact_registry_schema.md`
- `docs/policies/tiered_readiness_exploration.md`

## Carry-Forward Evidence

- `docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
- `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- `docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md`
- `docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
- `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
- `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
- `docs/context/current_working_state.md`
- `docs/registers/artifact_registry.csv`

## Materialized Upstream Inputs

- Stage 07 dual-verdict local spec under `stages/07_alpha_search/01_inputs/stage07_tier_b_dual_verdict_local_spec.md`
- Stage 06 closed selection read under `stages/06_tiered_readiness_exploration/04_selected/selection_status.md`
- Stage 06 baseline-seed local spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md`
- Stage 06 follow-up-pack local spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_followup_pack_local_spec.md`
- Stage 06 reduced-context local spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_reduced_context_local_spec.md`
- Stage 06 readiness row labels under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- Stage 06 scorecard summary under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`
- Stage 06 baseline evaluation summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- Stage 06 baseline calibration read under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_calibration_read_fpmarkets_v2_tier_b_offline_eval_0001.json`
- Stage 06 follow-up-pack manifest under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/followup_pack_manifest_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 calibration-fit summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_calibration_fit_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 control-sensitivity summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_control_sensitivity_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 robustness summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_robustness_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 weight-verdict summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_weight_verdict_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 reduced-context manifest under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_manifest_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 reduced-context probability table under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_probability_table_fpmarkets_v2_tier_b_reduced_context_0001.parquet`
- Stage 06 reduced-context evaluation summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_evaluation_summary_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 reduced-context calibration read under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_calibration_read_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 readiness review report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- Stage 06 Tier B offline evaluation report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- Stage 06 calibration-fit report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- Stage 06 control-sensitivity report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- Stage 06 robustness report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
- Stage 06 weight-verdict report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
- Stage 06 reduced-context report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`

## Stage 07 Boundary Interface

- keep `readiness_tier`: `tier_a | tier_b | tier_c`
- keep `missing_groups`: `g1_contract_base | g2_session_semantics | g3_macro_proxy | g4_leader_equity | g5_breadth_extension`
- keep `missing_symbols`: symbol-level missing explanation
- keep `reporting_lane`: `strict_tier_a | tier_b_exploration`
- keep all mixed aggregates `info-only (정보용)` rather than promotive
- keep `tier_b_subtype_tag` `info-only (정보용)` only
- add packet verdict fields:
  - `separate_lane_verdict`: `keep | prune`
  - `mt5_candidate_verdict`: `yes | no | blocked`
  - `weights_source_status`: user-weight validation status
  - `weights_version`: stable label for the validated user-weight source

## Immediate Missing Inputs

- the first `Stage 07 Tier B dual verdict packet (Stage 07 Tier B 이중 판정 팩)` does not exist yet
- the validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)` for that packet does not exist in the repo yet
- the first Stage 07 decision on whether the separate `Tier B` lane should continue after that packet does not exist yet
- the first Stage 07 decision on whether the packet may move forward as an `MT5 feasibility candidate (MT5 가능성 후보)` does not exist yet
- no optional `macro-aware (매크로 인지)` Tier B variant is required for Stage 07 opening, but no such variant exists yet either
- placeholder monthly weights still remain insufficient for an opened `MT5 path (MT5 경로)` or a promoted operating-line claim (승격 운영선 주장)
