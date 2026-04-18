# First V2 Dataset Freeze Card

## Identity
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- created_on: `2026-04-18`
- owner: `Project_Obsidian_Prime_v2 workspace`

## Sources
- raw source roots: `data/raw/mt5_bars/m5/`
- source_identities: `see stages/01_dataset_contract_freeze/01_inputs/first_raw_source_inventory.md and the local-only materialized dataset summary for full per-symbol csv/manifest identities`
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
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- weights_version: `foundation/config/top3_monthly_weights_fpmarkets_v2.csv@2026-04-16 (placeholder_equal_weight)`

## Row Summary
- raw_rows: `261344`
- valid_rows: `24280`
- invalid_rows: `237064`
- invalid_reason_breakdown: `warmup_incomplete=300|main_symbol_missing=0|external_alignment_missing=236979|session_semantics_missing=12490|numeric_invalid=0|weights_unavailable=0|contract_version_mismatch=0`

## Output Artifacts
- main_output_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/features.parquet`
- validity_output_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`
- summary_json_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/dataset_summary.json`
- parser_manifest_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/parser_manifest.json`
- external_merge_report_path: `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/external_merge_report.json`
- deterministic_rerun_status: `rerun on 2026-04-18 reproduced the same row summary and the same tracked output hashes`
- artifact_fingerprints: `feature_order_hash=fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2|features_parquet_sha256=64f1be5c1457fc16edaa8a940b7d4dec83f090fe4625a1661071c931bf29a26c|row_validity_report_sha256=802eda0ceb2c6298f79c2ff5aa4f4aea7ca3d4d2858f89f7583caade964639bf|dataset_summary_sha256=0ed52742806982598715aee12759bfc39bcbc6b5942e1341d397a8844a6aafdb|feature_order_txt_sha256=18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb|parser_manifest_sha256=17158f60865b7c19baa357c09774f12d99564a350eccaf1023a0fb55735f5c7f|external_merge_report_sha256=81221ded7a400712654c05ec4312492e7cc248fbb6f62aefd57a97bf7d75c387`

## Notes
- known weak periods: `exact-match coverage is sparse by contract because US100 contributes near-continuous M5 bars while required external symbols, especially the equity set, trade on narrower overlapping sessions; this drives the large external_alignment_missing share without implying numeric corruption`
- known symbol issues: `GOOGL.xnas is the contract Google symbol and exact timestamp matching remains required across all required external symbols`
- placeholder caveats: `top3 monthly weights remain an equal-weight placeholder and the raw-source time binding still rests on the explicit UTC epoch assumption captured in the materialized dataset summary`
- reuse guidance: `this card now records the first materialized dataset-contract evidence pack with a deterministic rerun read from Stage 02, but it is still not runtime parity closure, broader artifact identity closure, or exploration-ready operating truth`
