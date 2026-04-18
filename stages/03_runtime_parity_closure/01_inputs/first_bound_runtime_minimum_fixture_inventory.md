# First Bound Runtime Minimum Fixture Inventory

## Identity

- fixture_set_id: `fixture_fpmarkets_v2_runtime_minimum_0001`
- created_on: `2026-04-18`
- owner: `Project_Obsidian_Prime_v2 workspace`
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- bundle_id: `bundle_fpmarkets_v2_runtime_minimum_0001`
- python_snapshot_id: `snapshot_fpmarkets_v2_runtime_python_0001`
- target_mt5_runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_0001`

## Contract Versions

- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## Required Minimum Fixture Set

### 1. Regular Closed-Bar Sample
- fixture_id: `fix_regular_closed_bar_0001`
- evaluated_timestamp_utc: `2022-09-02T17:00:00Z`
- evaluated_timestamp_america_new_york: `2022-09-02T13:00:00-04:00`
- symbol_scope: `US100 plus required external symbols`
- expected_contract_behavior: `all required inputs present and the row remains runtime-ready on a normal closed-bar sample`
- source_artifact_ref: `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

### 2. Session-Boundary Sample
- fixture_id: `fix_session_boundary_0001`
- evaluated_timestamp_utc: `2022-09-01T20:00:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T16:00:00-04:00`
- boundary_type: `cash-close semantics`
- expected_contract_behavior: `session flags, minutes_from_cash_open, and close-boundary fields stay exact on the contract surface`
- source_artifact_ref: `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

### 3. DST-Sensitive Sample
- fixture_id: `fix_dst_sensitive_0001`
- evaluated_timestamp_utc: `2022-11-09T21:00:00Z`
- evaluated_timestamp_america_new_york: `2022-11-09T16:00:00-05:00`
- dst_transition_context: `post-fall-DST transition week sample with stable 16:00 America/New_York semantics`
- expected_contract_behavior: `session features stay stable across the DST boundary with no timezone drift`
- source_artifact_ref: `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

### 4. External-Alignment Sample
- fixture_id: `fix_external_alignment_0001`
- evaluated_timestamp_utc: `2022-09-01T19:55:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T15:55:00-04:00`
- required_symbols: `VIX, US10YR, USDX, NVDA, AAPL, MSFT, AMZN, AMD, GOOGL.xnas, META, TSLA`
- exact_timestamp_match_expected: `yes`
- source_artifact_ref: `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

### 5. Negative Fixture
- fixture_id: `fix_negative_required_missing_0001`
- evaluated_timestamp_utc: `2022-09-01T13:35:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T09:35:00-04:00`
- missing_input_condition: `the 09:35 cash-open row is non-ready because the required equity external series are still missing on the exact US100 closed-bar timestamp`
- expected_non_ready_behavior: `all-or-skip; non-ready row and no silent substitution`
- source_artifact_ref: `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`

## Notes

- known_caveats: `the bound fixture timestamps and first Python snapshot artifact are materialized, but the MT5 snapshot artifact and evaluated parity metrics are still pending Stage 03 follow-up`
- mt5_request_ref: `../02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- mt5_window_spec_ref: `../02_runs/runtime_parity_pack_0001/mt5_target_windows_utc.txt`
- reuse_guidance: `this inventory now freezes the first Stage 03 five-window minimum pack; future MT5 snapshot export and parity comparison must reuse these same timestamps and ids rather than sampling a new window set`
