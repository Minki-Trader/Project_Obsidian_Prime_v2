# Stage 05 Input Refs

## Required Contracts And Policies

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/artifact_registry_schema.md`
- `docs/policies/tiered_readiness_exploration.md`

## Carry-Forward Evidence

- `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
- `docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
- `docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
- `docs/decisions/2026-04-20_stage05_dual_followup_order.md`
- `docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
- `docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
- `docs/adr/0002_broader_sample_parity_charter.md`
- `docs/decisions/2026-04-19_stage04_close_and_stage05_open.md`
- `stages/04_artifact_identity_closure/03_reviews/review_index.md`
- `stages/04_artifact_identity_closure/04_selected/selection_status.md`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `docs/context/current_working_state.md`
- `docs/registers/artifact_registry.csv`

## Materialized Local Inputs

- Stage 03 MT5 request pack under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- Stage 03 imported MT5 snapshot under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- Stage 03 comparison summary under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- Stage 03 rendered parity report under `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- closed Stage 04 selection read under `stages/04_artifact_identity_closure/04_selected/selection_status.md`
- retained Stage 05 pre-alignment broader fixture inventory under `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_broader_fixture_inventory.md`
- retained Stage 05 pre-alignment broader selection manifest under `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_broader_fixture_manifest_0001.json`
- retained Stage 05 pre-alignment broader comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0001.json`
- retained Stage 05 pre-alignment broader parity report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0001.md`
- active Stage 05 broader fixture inventory under `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_inventory.md`
- active Stage 05 broader selection manifest under `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json`
- active Stage 05 broader fixture bindings under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/fixture_bindings_fpmarkets_v2_runtime_broader_0002.json`
- active Stage 05 broader Python snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/python_snapshot_fpmarkets_v2_runtime_broader_0002.json`
- active Stage 05 broader MT5 request under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_snapshot_request_fpmarkets_v2_runtime_broader_0002.json`
- active Stage 05 broader MT5 input helper under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_snapshot_audit_inputs.set`
- active Stage 05 broader MT5 tester config under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_tester_runtime_broader_pack_0002.ini`
- active Stage 05 imported MT5 snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl`
- active Stage 05 broader comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0002.json`
- active Stage 05 rendered broader parity report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
- first helper-focused Stage 05 fixture inventory under `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_helper_fixture_inventory.md`
- first helper-focused Stage 05 selection manifest under `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_helper_fixture_manifest_0001.json`
- first helper-focused Stage 05 fixture bindings under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/fixture_bindings_fpmarkets_v2_runtime_helper_0001.json`
- first helper-focused Stage 05 Python snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`
- first helper-focused Stage 05 MT5 request under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_helper_0001.json`
- first helper-focused Stage 05 MT5 input helper under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/mt5_snapshot_audit_inputs.set`
- first helper-focused Stage 05 MT5 tester config under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/mt5_tester_runtime_helper_pack_0001.ini`
- first helper-focused imported MT5 snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_helper_0001.jsonl`
- first helper-focused comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_helper_0001.json`
- first helper-focused rendered report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
- additive broader reinforcement inventory under `stages/05_exploration_kernel_freeze/01_inputs/third_bound_runtime_broader_fixture_inventory.md`
- additive broader reinforcement selection manifest under `stages/05_exploration_kernel_freeze/01_inputs/third_bound_runtime_broader_fixture_manifest_0003.json`
- additive broader reinforcement fixture bindings under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/fixture_bindings_fpmarkets_v2_runtime_broader_0003.json`
- additive broader reinforcement Python snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`
- additive broader reinforcement MT5 request under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/mt5_snapshot_request_fpmarkets_v2_runtime_broader_0003.json`
- additive broader reinforcement MT5 input helper under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/mt5_snapshot_audit_inputs.set`
- additive broader reinforcement MT5 tester config under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/mt5_tester_runtime_broader_pack_0003.ini`
- additive broader reinforcement imported MT5 snapshot under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0003.jsonl`
- additive broader reinforcement comparison summary under `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0003.json`
- additive broader reinforcement rendered report under `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
- ordered Stage 05 dual-lane follow-up plan under `stages/05_exploration_kernel_freeze/01_inputs/next_evidence_dual_lane_plan.md`

## Immediate Missing Inputs

- no missing file input remains for the closed Stage 05 kernel-freeze read
- the first downstream lane is frozen to `broader-sample parity`, and its ordered helper then additive reinforcement follow-up is now fully materialized and evaluated
- `broader_0001` remains retained pre-alignment mismatch evidence and is no longer the active pack
- the downstream home for any new reduced-risk or tiered-readiness artifact is now `stages/06_tiered_readiness_exploration/`
