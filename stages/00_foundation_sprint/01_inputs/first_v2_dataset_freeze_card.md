# First V2 Dataset Freeze Card

## Identity
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- created_on: `2026-04-18`
- owner: `Project_Obsidian_Prime_v2 workspace`

## Sources
- raw source roots: `FPMarkets terminal-native history export; path pending first collection`
- source_identities: `pending_first_materialized_export`
- symbols: `US100, VIX, US10YR, USDX, NVDA, AAPL, MSFT, AMZN, AMD, GOOGL.xnas, META, TSLA`
- timeframe: `M5`
- session/calendar assumptions: `closed-bar only, storage may be UTC, session features derive in America/New_York, and required external symbols must match the US100 bar-close timestamp exactly`

## Window
- window_start: `2022-08-01`
- window_end_inclusive: `2026-04-13`
- practical_modeling_start: `2022-09-01`
- warmup_bars: `300`
- preload_policy: `300 bars minimum; practical modeling start remains 2022-09-01`

## Feature Contract
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- parser_contract_version: `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `pending_first_materialized_export`
- weights_version: `foundation/config/top3_monthly_weights_fpmarkets_v2.csv@2026-04-16 (placeholder_equal_weight)`

## Row Summary
- raw_rows: `pending_first_materialized_export`
- valid_rows: `pending_first_materialized_export`
- invalid_rows: `pending_first_materialized_export`
- invalid_reason_breakdown: `pending_first_materialized_export`

## Output Artifacts
- main_output_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/features.parquet`
- validity_output_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`
- summary_json_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/dataset_summary.json`
- artifact_fingerprints: `feature_order_hash=pending_first_materialized_export|features_parquet_sha256=pending_first_materialized_export|dataset_summary_sha256=pending_first_materialized_export`

## Notes
- known weak periods: `not yet audited in v2`
- known symbol issues: `GOOGL.xnas is the contract Google symbol and exact timestamp matching remains required across all required external symbols`
- placeholder caveats: `top3 monthly weights remain an equal-weight placeholder, so this card is a planning freeze and not yet a materialized dataset freeze`
- reuse guidance: `safe for Stage 00 naming and identity planning; not sufficient for exploration-only mode until row summary, source identities, and feature fingerprint are materialized`
