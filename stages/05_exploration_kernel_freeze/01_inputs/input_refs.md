# Stage 05 Input Refs

## Required Contracts And Policies

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/artifact_registry_schema.md`
- `docs/policies/tiered_readiness_exploration.md`

## Carry-Forward Evidence

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

## Immediate Missing Inputs

- no missing file input remains for the first Stage 05 kernel-freeze pass
- the explicit Stage 05 blocker read is now written from the closed Stage 04 evidence and the downstream exploration boundary policies
- the remaining blocker is a durable ordering decision, not a missing file input
