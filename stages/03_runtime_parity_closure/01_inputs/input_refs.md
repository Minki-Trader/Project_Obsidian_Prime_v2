# Stage 03 Input Refs

## Required Contracts

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/policies/artifact_policy.md`

## Carry-Forward Evidence

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `stages/00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
- `stages/00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `stages/02_feature_dataset_closure/04_selected/selection_status.md`
- `docs/registers/artifact_registry.csv`

## Materialized Local Inputs

- raw export roots under `data/raw/mt5_bars/m5/`
- processed dataset outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- the first materialized freeze card and tracked dataset hashes
- bound fixture inventory under `stages/03_runtime_parity_closure/01_inputs/first_bound_runtime_minimum_fixture_inventory.md`
- stage-local fixture bindings under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json`
- stage-local Python snapshot under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`
- stage-local MT5 request pack under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- stage-local MT5 input set under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_audit_inputs.set`
- stage-local MT5 tester ini under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_tester_runtime_parity_pack_0001.ini`
- stage-local imported MT5 snapshot under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- stage-local machine-readable comparison summary under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- evaluated Stage 03 parity report under `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- MT5 window spec under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_target_windows_utc.txt`
- MT5 handoff note under `stages/03_runtime_parity_closure/01_inputs/mt5_runtime_snapshot_handoff.md`
- v2-native MT5 runner under `foundation/parity/run_fpmarkets_v2_runtime_parity_native.py`

## Immediate Missing Inputs

- no missing files remain for the first evaluated five-window pack
- a localized root-cause note or repaired rerun is still needed before any Stage 03 closure claim
- explicit embedded MT5-side identity fields remain a later Stage 04 artifact-identity follow-up
