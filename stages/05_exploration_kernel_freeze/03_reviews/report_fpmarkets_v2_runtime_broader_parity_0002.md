# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0002`
- report_id: `report_fpmarkets_v2_runtime_broader_parity_0002`
- reviewed_on: `2026-04-19`
- bundle_id: `bundle_fpmarkets_v2_runtime_broader_0002`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_broader_0002`
- stage: `05_exploration_kernel_freeze`

## Scope

- closure_scope: `first_evaluated_pack_mismatch_open`
- audited_window(s): `2022-09-01T16:40:00Z|2026-04-13T16:35:00Z|2024-06-21T16:35:00Z|2023-07-26T16:40:00Z|2022-10-04T19:55:00Z|2026-03-31T19:55:00Z|2022-11-01T20:00:00Z|2026-02-27T21:00:00Z|2023-03-13T20:00:00Z|2025-03-10T20:00:00Z|2023-11-06T21:00:00Z|2025-11-04T21:00:00Z|2022-12-01T19:00:00Z|2026-01-30T19:00:00Z|2024-07-01T18:00:00Z|2025-04-16T18:00:00Z|2023-01-03T14:35:00Z|2025-12-31T14:35:00Z|2024-08-01T13:35:00Z|2023-10-18T13:35:00Z|2023-02-01T05:00:00Z|2025-10-31T04:00:00Z|2022-09-01T00:00:00Z|2025-09-30T20:55:00Z`
- audited_row_count: `16 ready rows + 8 negative non-ready rows`

## Inputs

- python_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/python_snapshot_fpmarkets_v2_runtime_broader_0002.json`
- mt5_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:750c7f5223582f61b9aceec820419675142244df72c5cf3d8a1ddf93f44ca130|python_snapshot_sha256=sha256:b53ae1546a6fee6d13009948e541a4e3fc5ee9b0ca3d874bb9f04c4ca442eaf7|mt5_request_sha256=sha256:38867ff252edffa17f0584cf54417bf154478ece35bcab4f05be2eebba505ded|mt5_snapshot_sha256=sha256:db41f5f6880b473d44b0cde7c5c08bfb6b02b8ed5be585bdff2223e481c373e4`

## Identity Trace

- request_consistent: `true`
- mt5_identity_fields_present: `true`
- mt5_identity_values_match: `true`
- machine_readable_identity_trace: `true`

## Fixture Coverage

- fixture_strata: `cash_close_boundary=4|cash_open_missing_equities=4|dst_sensitive=4|full_external_alignment=4|off_hours_external_alignment_missing=4|regular_cash_session=4`
- fixture_buckets: `cash_close_boundary_1555=2|cash_close_boundary_1600=2|dst_sensitive_utc4=2|dst_sensitive_utc5=2|full_external_alignment=4|negative_cash_open_missing_equities=4|negative_off_hours_post_close=2|negative_off_hours_pre_open=2|regular_cash_session=4`
- negative_fixture_result: `matched_non_ready=8/8; skip_reasons=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=4,EXTERNAL_TIMESTAMP_MISMATCH_VIX=2,SESSION_CASH_OPEN_NOT_FOUND=2`

## Timestamp Identity

- evaluated_timestamp_utc: `2022-09-01T16:40:00Z|2026-04-13T16:35:00Z|2024-06-21T16:35:00Z|2023-07-26T16:40:00Z|2022-10-04T19:55:00Z|2026-03-31T19:55:00Z|2022-11-01T20:00:00Z|2026-02-27T21:00:00Z|2023-03-13T20:00:00Z|2025-03-10T20:00:00Z|2023-11-06T21:00:00Z|2025-11-04T21:00:00Z|2022-12-01T19:00:00Z|2026-01-30T19:00:00Z|2024-07-01T18:00:00Z|2025-04-16T18:00:00Z|2023-01-03T14:35:00Z|2025-12-31T14:35:00Z|2024-08-01T13:35:00Z|2023-10-18T13:35:00Z|2023-02-01T05:00:00Z|2025-10-31T04:00:00Z|2022-09-01T00:00:00Z|2025-09-30T20:55:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T12:40:00-04:00|2026-04-13T12:35:00-04:00|2024-06-21T12:35:00-04:00|2023-07-26T12:40:00-04:00|2022-10-04T15:55:00-04:00|2026-03-31T15:55:00-04:00|2022-11-01T16:00:00-04:00|2026-02-27T16:00:00-05:00|2023-03-13T16:00:00-04:00|2025-03-10T16:00:00-04:00|2023-11-06T16:00:00-05:00|2025-11-04T16:00:00-05:00|2022-12-01T14:00:00-05:00|2026-01-30T14:00:00-05:00|2024-07-01T14:00:00-04:00|2025-04-16T14:00:00-04:00|2023-01-03T09:35:00-05:00|2025-12-31T09:35:00-05:00|2024-08-01T09:35:00-04:00|2023-10-18T09:35:00-04:00|2023-02-01T00:00:00-05:00|2025-10-31T00:00:00-04:00|2022-08-31T20:00:00-04:00|2025-09-30T16:55:00-04:00`

## Results

- exact_parity: `false`
- tolerance_parity: `false`
- max_abs_diff: `3.021929825070319`
- dominant_drift_features: `us100_minus_top3_weighted_return_1=3.02193|top3_weighted_return_1=3.02193|nvda_xnas_log_return_1=2.37064|mega8_equal_return_1=1.13322|us100_minus_mega8_equal_return_1=1.13322`
- zero_shift_share: `0.1271551724137931`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `localized model-input mismatch remains on the evaluated runtime parity pack`
- what_this_does_not_prove: `no runtime-helper parity closure, no separate broader-sample parity closure read, no Tier B or Tier C readiness claim, and no operating promotion`
- what_remains_open: `inspect the broader-pack mismatch, update the Stage 05 blocker read, and rerun the same frozen 24-window pack before opening any new lane`

## Required Follow-Up

- next_sampling_plan: `inspect the broader-pack mismatch, update the Stage 05 mismatch-open read, and rerun the same frozen 24-window pack before opening any downstream lane`
- gate_before_closure: `Stage 05 state docs, review read, and registry rows must be updated in the same pass while keeping Stage 05 open; do not blur this evaluated pack into runtime-helper parity, Tier B or Tier C readiness, or operating promotion`
- owner: `Project_Obsidian_Prime_v2 workspace`
