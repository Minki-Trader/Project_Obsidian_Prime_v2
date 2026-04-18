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

## Immediate Missing Inputs

- bound fixture timestamps for `fixture_fpmarkets_v2_runtime_minimum_0001`
- first Python snapshot and MT5 snapshot refs
- evaluated runtime parity results for `report_fpmarkets_v2_runtime_parity_0001`
