# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0001`
- report_id: `report_fpmarkets_v2_runtime_broader_parity_0001`
- reviewed_on: `2026-04-19`
- bundle_id: `bundle_fpmarkets_v2_runtime_broader_0001`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_broader_0001`
- stage: `05_exploration_kernel_freeze`

## Scope

- closure_scope: `first_evaluated_pack_mismatch_open`
- audited_window(s): `2022-09-02T17:00:00Z|2026-04-13T16:35:00Z|2024-08-06T16:35:00Z|2023-08-10T17:05:00Z|2022-10-05T19:55:00Z|2026-03-31T19:55:00Z|2022-11-01T20:00:00Z|2026-02-20T21:00:00Z|2023-03-13T20:00:00Z|2025-03-10T20:00:00Z|2023-11-09T21:00:00Z|2025-11-13T21:00:00Z|2022-12-01T19:00:00Z|2026-01-30T19:00:00Z|2024-06-21T18:00:00Z|2025-04-11T18:00:00Z|2023-01-03T14:35:00Z|2025-12-31T14:35:00Z|2024-07-02T13:35:00Z|2023-10-03T13:35:00Z|2023-02-01T05:00:00Z|2025-10-31T04:00:00Z|2022-09-01T00:00:00Z|2025-09-30T20:05:00Z`
- audited_row_count: `16 ready rows + 8 negative non-ready rows`

## Inputs

- python_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/python_snapshot_fpmarkets_v2_runtime_broader_0001.json`
- mt5_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0001.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:68d98bc4ebe5c4b00dac8a4abd99f41cccdfe04ec080c591f6b30bf4c371e247|python_snapshot_sha256=sha256:071c74b2c222b938eec3cac5fc8c83ec0c5e54add3479de31c1a7ccc60686bf6|mt5_request_sha256=sha256:fff98495590983d0ac3ae1ee1cca1220c5d52c1b31a06b7142f4168a9d13383a|mt5_snapshot_sha256=sha256:7c752782c2be57eed0ef957a770786d989901e97b1a3980cbadc5f5869179e60`

## Identity Trace

- request_consistent: `true`
- mt5_identity_fields_present: `true`
- mt5_identity_values_match: `true`
- machine_readable_identity_trace: `true`

## Fixture Coverage

- fixture_strata: `cash_close_boundary=4|cash_open_missing_equities=4|dst_sensitive=4|full_external_alignment=4|off_hours_external_alignment_missing=4|regular_cash_session=4`
- fixture_buckets: `cash_close_boundary_1555=2|cash_close_boundary_1600=2|dst_sensitive_utc4=2|dst_sensitive_utc5=2|full_external_alignment=4|negative_cash_open_missing_equities=4|negative_off_hours_post_close=2|negative_off_hours_pre_open=2|regular_cash_session=4`
- negative_fixture_result: `matched_non_ready=7/8; skip_reasons=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=2,EXTERNAL_TIMESTAMP_MISMATCH_VIX=2,SESSION_CASH_OPEN_NOT_FOUND=2,RATES_NOT_READY_AAPL.xnas=1; missing=fix_negative_off_hours_post_close_0002`

## Timestamp Identity

- evaluated_timestamp_utc: `2022-09-02T17:00:00Z|2026-04-13T16:35:00Z|2024-08-06T16:35:00Z|2023-08-10T17:05:00Z|2022-10-05T19:55:00Z|2026-03-31T19:55:00Z|2022-11-01T20:00:00Z|2026-02-20T21:00:00Z|2023-03-13T20:00:00Z|2025-03-10T20:00:00Z|2023-11-09T21:00:00Z|2025-11-13T21:00:00Z|2022-12-01T19:00:00Z|2026-01-30T19:00:00Z|2024-06-21T18:00:00Z|2025-04-11T18:00:00Z|2023-01-03T14:35:00Z|2025-12-31T14:35:00Z|2024-07-02T13:35:00Z|2023-10-03T13:35:00Z|2023-02-01T05:00:00Z|2025-10-31T04:00:00Z|2022-09-01T00:00:00Z|2025-09-30T20:05:00Z`
- evaluated_timestamp_america_new_york: `2022-09-02T13:00:00-04:00|2026-04-13T12:35:00-04:00|2024-08-06T12:35:00-04:00|2023-08-10T13:05:00-04:00|2022-10-05T15:55:00-04:00|2026-03-31T15:55:00-04:00|2022-11-01T16:00:00-04:00|2026-02-20T16:00:00-05:00|2023-03-13T16:00:00-04:00|2025-03-10T16:00:00-04:00|2023-11-09T16:00:00-05:00|2025-11-13T16:00:00-05:00|2022-12-01T14:00:00-05:00|2026-01-30T14:00:00-05:00|2024-06-21T14:00:00-04:00|2025-04-11T14:00:00-04:00|2023-01-03T09:35:00-05:00|2025-12-31T09:35:00-05:00|2024-07-02T09:35:00-04:00|2023-10-03T09:35:00-04:00|2023-02-01T00:00:00-05:00|2025-10-31T00:00:00-04:00|2022-08-31T20:00:00-04:00|2025-09-30T16:05:00-04:00`

## Results

- exact_parity: `false`
- tolerance_parity: `false`
- max_abs_diff: `185.0`
- dominant_drift_features: `minutes_from_cash_open=185|rsi_14=74.535|rsi_50=61.7834|adx_14=30.1747|di_spread_14=26.2792`
- zero_shift_share: `0.1228448275862069`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `localized mismatch remains on the contract surface; inspect the warning list and dominant drift features before any closure claim`
- what_this_does_not_prove: `no runtime-helper parity closure, no separate broader-sample parity closure read, no Tier B or Tier C readiness claim, and no operating promotion`
- what_remains_open: `inspect the broader-pack mismatch, update the Stage 05 blocker read, and rerun the same frozen 24-window pack before opening any new lane`

## Required Follow-Up

- next_sampling_plan: `inspect the broader-pack mismatch, update the Stage 05 mismatch-open read, and rerun the same frozen 24-window pack before opening any downstream lane`
- gate_before_closure: `Stage 05 state docs, review read, and registry rows must be updated in the same pass while keeping Stage 05 open; do not blur this evaluated pack into runtime-helper parity, Tier B or Tier C readiness, or operating promotion`
- owner: `Project_Obsidian_Prime_v2 workspace`
