# Stage 06 Input Refs

## Required Contracts And Policies

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/artifact_registry_schema.md`
- `docs/policies/tiered_readiness_exploration.md`

## Carry-Forward Evidence

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

## Immediate Missing Inputs

- no Stage 06-specific readiness-label artifact exists yet
- no Stage 06-specific missing-group-summary artifact exists yet
- no Stage 06-specific report or registry convention has been materialized yet for Tier B or Tier C work
- the next missing durable artifact is the first explicit Stage 06 boundary read for readiness labels and reporting lanes
