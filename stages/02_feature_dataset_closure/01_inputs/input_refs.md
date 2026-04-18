# Stage 02 Input Refs

## Required Contracts

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
- `docs/policies/artifact_policy.md`

## Carry-Forward Evidence

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `stages/01_dataset_contract_freeze/01_inputs/first_raw_source_inventory.md`
- `stages/01_dataset_contract_freeze/04_selected/selection_status.md`
- `docs/registers/artifact_registry.csv`

## Materialized Local Inputs

- raw export roots under `data/raw/mt5_bars/m5/`
- processed dataset outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- `features.parquet`, `feature_order.txt`, `parser_manifest.json`, `row_validity_report.json`, `dataset_summary.json`, and `external_merge_report.json`

## Immediate Missing Inputs

- a second deterministic rerun record from the same raw roots
- an explicit coverage explanation note for the large exact-match `external_alignment_missing` share
- a Stage 02 read on whether output-hash equality is exact or subject only to deterministic formatting differences
