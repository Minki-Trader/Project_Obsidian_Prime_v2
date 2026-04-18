# First V2 Runtime Parity Report

## Identity
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_minimum_0001`
- report_id: `report_fpmarkets_v2_runtime_parity_0001`
- reviewed_on: `2026-04-18`
- bundle_id: `pending_first_materialized_export`
- runtime_id: `pending_first_materialized_export`
- stage: `00_foundation_sprint`

## Scope
- closure_scope: `planning_scaffold_only`
- audited_window(s): `pending_first_materialized_export`
- audited_row_count: `pending_first_materialized_export`

## Inputs
- python_snapshot_artifact: `pending_first_materialized_export`
- mt5_snapshot_artifact: `pending_first_materialized_export`
- parser_version: `pending_first_materialized_export`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `not_applicable`

## Fixture Coverage
- regular_closed_bar_sample: `fix_regular_closed_bar_0001`
- session_boundary_sample: `fix_session_boundary_0001`
- dst_sensitive_sample: `fix_dst_sensitive_0001`
- external_alignment_sample: `fix_external_alignment_0001`
- negative_fixture_result: `pending_first_materialized_export`

## Timestamp Identity
- evaluated_timestamp_utc: `pending_first_materialized_export`
- evaluated_timestamp_america_new_york: `pending_first_materialized_export`

## Results
- exact_parity: `not_yet_evaluated`
- tolerance_parity: `not_yet_evaluated`
- max_abs_diff: `not_applicable`
- dominant_drift_features: `not_applicable`
- zero_shift_share: `not_applicable`
- decision_flip_count: `not_applicable`

## Interpretation
- likely root cause: `not yet evaluated; this report exists to freeze identity fields before the first snapshot-backed parity pass`
- what this does NOT prove: `no Python to MT5 parity claim, no helper-path closure, and no exploration-ready runtime claim yet`
- what remains open: `materialized dataset row summary, source identities, Python snapshot, MT5 snapshot, evaluated fixture timestamps, parity metrics, and artifact-identity registry rows beyond planning drafts`

## Required Follow-Up
- next_sampling_plan: `materialize the first dataset export, bind exact timestamps into fixture_fpmarkets_v2_runtime_minimum_0001, then evaluate localized parity on that fixture set`
- gate before closure: `snapshot-backed parity results and machine-readable artifact identity must exist before 03_runtime_parity_closure can close`
- owner: `Project_Obsidian_Prime_v2 workspace`
