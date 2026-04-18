# Stage 01 Input Refs

## Required Contracts

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
- `docs/policies/artifact_policy.md`

## Stage 00 Carry-Forward Evidence

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `stages/00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
- `stages/00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `docs/registers/artifact_registry.csv`

## Local-Only Inputs Needed

- first raw export roots for `US100, VIX, US10YR, USDX, NVDA, AAPL, MSFT, AMZN, AMD, GOOGL.xnas, META, TSLA`
- first processed dataset outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- first `row_validity_report.json` and `dataset_summary.json`

## Immediate Missing Inputs

- materialized `raw_rows`, `valid_rows`, `invalid_rows`, and `invalid_reason_breakdown`
- durable `source_identities` for the first reusable dataset freeze
- output hashes for `features.parquet`, `row_validity_report.json`, and `dataset_summary.json`
- an explicit note if placeholder equal-weight monthly weights are still the only available weights source
