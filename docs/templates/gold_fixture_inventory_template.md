# Gold Fixture Inventory

## Identity
- fixture_set_id:
- created_on:
- owner:
- dataset_id:
- bundle_id:

## Contract Versions
- feature_contract_version:
- parser_version:
- runtime_contract_version:
- feature_order_hash:

## Required Minimum Fixture Set

### 1. Regular Closed-Bar Sample
- fixture_id:
- evaluated_timestamp_utc:
- evaluated_timestamp_america_new_york:
- symbol_scope:
- expected_contract_behavior:
- source_artifact_ref:

### 2. Session-Boundary Sample
- fixture_id:
- evaluated_timestamp_utc:
- evaluated_timestamp_america_new_york:
- boundary_type:
- expected_contract_behavior:
- source_artifact_ref:

### 3. DST-Sensitive Sample
- fixture_id:
- evaluated_timestamp_utc:
- evaluated_timestamp_america_new_york:
- dst_transition_context:
- expected_contract_behavior:
- source_artifact_ref:

### 4. External-Alignment Sample
- fixture_id:
- evaluated_timestamp_utc:
- evaluated_timestamp_america_new_york:
- required_symbols:
- exact_timestamp_match_expected:
- source_artifact_ref:

### 5. Negative Fixture
- fixture_id:
- evaluated_timestamp_utc:
- evaluated_timestamp_america_new_york:
- missing_input_condition:
- expected_non_ready_behavior:
- source_artifact_ref:

## Notes
- known caveats:
- reuse guidance:
