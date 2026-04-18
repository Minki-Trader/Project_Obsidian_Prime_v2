# Stage 04 Input Refs

## Required Contracts

- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/policies/artifact_policy.md`
- `docs/policies/artifact_registry_schema.md`

## Carry-Forward Evidence

- `stages/03_runtime_parity_closure/04_selected/selection_status.md`
- `stages/03_runtime_parity_closure/03_reviews/review_index.md`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `docs/registers/artifact_registry.csv`
- `docs/context/current_working_state.md`

## Materialized Local Inputs

- stage-local MT5 request pack under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- stage-local MT5 input set under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_audit_inputs.set`
- stage-local MT5 tester ini under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_tester_runtime_parity_pack_0001.ini`
- stage-local imported MT5 snapshot under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- stage-local machine-readable comparison summary under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- Stage 03 parity report under `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- fixture bindings under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json`
- Python snapshot under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

## Immediate Missing Inputs

- no missing file input remains for the first machine-readable identity chain
- the explicit Stage 04 closure read and any one-line runtime self-check conclusion still need to be written from the existing artifacts
