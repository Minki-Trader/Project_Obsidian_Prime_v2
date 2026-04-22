# Stage 06 Input Refs

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
- `docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
- `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
- `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
- `docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
- `docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
- `docs/decisions/2026-04-20_stage05_dual_followup_order.md`
- `docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
- `docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
- `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
- `docs/adr/0002_broader_sample_parity_charter.md`
- `docs/context/current_working_state.md`
- `docs/registers/artifact_registry.csv`

## Materialized Local Inputs

- Stage 05 closed selection read under `stages/05_exploration_kernel_freeze/04_selected/selection_status.md`
- Stage 05 active broader comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0002.json`
- Stage 05 active broader parity report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
- Stage 05 helper-focused comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_helper_0001.json`
- Stage 05 helper-focused parity report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
- Stage 05 additive broader reinforcement comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0003.json`
- Stage 05 additive broader reinforcement parity report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
- Stage 05 broader fixture manifests under `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json` and `stages/05_exploration_kernel_freeze/01_inputs/third_bound_runtime_broader_fixture_manifest_0003.json`
- Stage 05 helper fixture manifest under `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_helper_fixture_manifest_0001.json`
- Stage 06 local baseline-seed spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md`
- Stage 06 local follow-up-pack spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_followup_pack_local_spec.md`
- Stage 06 local reduced-context spec under `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_reduced_context_local_spec.md`
- dataset validity source under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`
- Stage 06 row-level readiness labels under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- Stage 06 machine-readable scorecard summary under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`
- Stage 06 first scorecard review report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- Stage 06 baseline-seed manifest under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_seed_manifest_fpmarkets_v2_tier_b_offline_eval_0001.json`
- Stage 06 baseline evaluation summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- Stage 06 baseline calibration read under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_calibration_read_fpmarkets_v2_tier_b_offline_eval_0001.json`
- Stage 06 Tier B offline evaluation report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- Stage 06 follow-up-pack manifest under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/followup_pack_manifest_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 calibration-fit summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_calibration_fit_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 control-sensitivity summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_control_sensitivity_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 robustness summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_robustness_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 weight-verdict summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001/tier_b_weight_verdict_summary_fpmarkets_v2_tier_b_followup_pack_0001.json`
- Stage 06 calibration-fit report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- Stage 06 control-sensitivity report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- Stage 06 robustness report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
- Stage 06 weight-verdict report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
- Stage 06 reduced-context manifest under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_manifest_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 reduced-context probability table under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_probability_table_fpmarkets_v2_tier_b_reduced_context_0001.parquet`
- Stage 06 reduced-context evaluation summary under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_evaluation_summary_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 reduced-context calibration read under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_calibration_read_fpmarkets_v2_tier_b_reduced_context_0001.json`
- Stage 06 reduced-context report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
- Stage 07 alpha design draft under `stages/06_tiered_readiness_exploration/03_reviews/stage07_alpha_design_draft_0001.md`
- Stage 06 close / Stage 07 open readout draft under `stages/06_tiered_readiness_exploration/03_reviews/stage06_close_stage07_open_readout_draft_0001.md`

## Draft-Only Planning Inputs

- Stage 06 reduced-context modeling anchor under `stages/06_tiered_readiness_exploration/03_reviews/note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md`
- Stage 06 Tier B-safe feature schema draft under `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_safe_feature_schema_draft_0001.md`
- both draft-only planning inputs remain `planning scaffold (계획 비계)` only and do not update `workspace_state.yaml`, `current_working_state.md`, or the active `selection_status.md`

## Stage 06 Boundary Interface

- canonical readiness rule:
  - if `Group 1` or `Group 2` fails -> `tier_c`
  - else if `Group 3`, `Group 4`, and `Group 5` are all complete -> `tier_a`
  - else if exactly `1` or `2` of `Group 3` to `Group 5` are complete -> `tier_b`
  - else -> `tier_c`
- `group complete` means that the group's required symbols and required fields exist at the exact timestamp, no forward-fill or fabricate path is used, and the group's required semantics are computable
- future Stage 06 artifacts must use:
  - `readiness_tier`: `tier_a | tier_b | tier_c`
  - `missing_groups`: `g1_contract_base | g2_session_semantics | g3_macro_proxy | g4_leader_equity | g5_breadth_extension`
  - `missing_symbols`: symbol-level missing explanation
  - `reporting_lane`: `strict_tier_a | tier_b_exploration`
- future Tier B offline evaluation artifacts must summarize KPI reads separately for `strict_tier_a` and `tier_b_exploration`, and any mixed aggregate remains info-only
- `tier_c` remains a skip classification rather than a reporting lane
- the first materialized Stage 06 scorecard family now exists and is registered as `readiness_row_labels`, `readiness_scorecard_summary`, and `readiness_scorecard_report`

## Immediate Missing Inputs

- no Stage 06-specific reduced-risk runtime family exists yet
- the first Stage 06-specific reduced-risk experiment charter now exists under `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
- the first charter now reads through `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`, which replaces baseline-family reuse with legacy non-inheritance plus a first `Tier A`-trained v2-native baseline seed
- the additive follow-up pack and reduced-context model are now reflected into the official Stage 06 close and Stage 07 open decision
- the first shared `Tier B reduced-context model` now exists on the `keep=42` active surface, and no optional `macro-aware` variant is required for the official Stage 07 opening
- placeholder monthly weights are allowed only for offline Tier B exploration and not for promotion, simulated execution, or MT5-path expansion
- the next missing downstream artifact is the first bounded Stage 07 alpha-search pack across the Tier A main lane and the separate Tier B offline-only lane
