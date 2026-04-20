# Stage 06 Input Refs

## Required Contracts And Policies

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/artifact_registry_schema.md`
- `docs/policies/tiered_readiness_exploration.md`

## Carry-Forward Evidence

- `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
- `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
- `docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
- `docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
- `docs/decisions/2026-04-20_stage05_dual_followup_order.md`
- `docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
- `docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
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
- dataset validity source under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`
- Stage 06 row-level readiness labels under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- Stage 06 machine-readable scorecard summary under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`
- Stage 06 first scorecard review report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`

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
- `tier_c` remains a skip classification rather than a reporting lane
- the first materialized Stage 06 scorecard family now exists and is registered as `readiness_row_labels`, `readiness_scorecard_summary`, and `readiness_scorecard_report`

## Immediate Missing Inputs

- no Stage 06-specific reduced-risk runtime family exists yet
- no Stage 06-specific reduced-risk experiment charter exists yet
- model-family choice for any future Tier B runtime family remains open by decision
- the next missing durable artifact is either the first Tier B reduced-risk experiment charter or an explicit evidence decision that says additional helper-lane or broader-lane support is still required before experimentation
