# First V2 Gold Fixture Inventory

## Identity
- fixture_set_id: `fixture_fpmarkets_v2_runtime_minimum_0001`
- created_on: `2026-04-18`
- owner: `Project_Obsidian_Prime_v2 workspace`
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- bundle_id: `pending_first_materialized_export`

## Contract Versions
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- parser_version: `pending_first_materialized_export`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## Required Minimum Fixture Set

### 1. Regular Closed-Bar Sample
- fixture_id: `fix_regular_closed_bar_0001`
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`
- symbol_scope: `US100 plus required external symbols`
- expected_contract_behavior: `all required inputs present, row remains valid and runtime-ready on the same closed-bar timestamp`
- source_artifact_ref: `pending_first_materialized_export`

### 2. Session-Boundary Sample
- fixture_id: `fix_session_boundary_0001`
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`
- boundary_type: `cash-open or cash-close semantics`
- expected_contract_behavior: `session flags, minutes_from_cash_open, and overnight_return all match the America/New_York contract interpretation`
- source_artifact_ref: `pending_first_materialized_export`

### 3. DST-Sensitive Sample
- fixture_id: `fix_dst_sensitive_0001`
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`
- dst_transition_context: `same contract surface across a daylight-saving transition week`
- expected_contract_behavior: `session features stay stable across the DST boundary with no timezone drift`
- source_artifact_ref: `pending_first_materialized_export`

### 4. External-Alignment Sample
- fixture_id: `fix_external_alignment_0001`
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`
- required_symbols: `VIX, US10YR, USDX, NVDA, AAPL, MSFT, AMZN, AMD, GOOGL.xnas, META, TSLA`
- exact_timestamp_match_expected: `yes`
- source_artifact_ref: `pending_first_materialized_export`

### 5. Negative Fixture
- fixture_id: `fix_negative_required_missing_0001`
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`
- missing_input_condition: `at least one required external source or runtime prerequisite is missing for the target closed-bar timestamp`
- expected_non_ready_behavior: `all-or-skip; non-ready row and no silent substitution`
- source_artifact_ref: `pending_first_materialized_export`

## Notes
- known caveats: `planning inventory only; exact timestamps and source artifact refs must be materialized from the first reusable export or snapshot set`
- reuse guidance: `fixture ids and contract intent are frozen here; sample timestamps remain open until the first materialized export and runtime snapshots exist`
