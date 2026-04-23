# Bound Runtime Helper Fixture Inventory

## Identity

- profile: `helper_0001`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_helper_0001`
- created_on: `2026-04-20`
- owner: `Project_Obsidian_Prime_v2 workspace`
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- source_fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0002`
- source_bundle_id: `bundle_fpmarkets_v2_runtime_broader_0002`
- bundle_id: `bundle_fpmarkets_v2_runtime_helper_0001`
- python_snapshot_id: `snapshot_fpmarkets_v2_runtime_python_helper_0001`
- target_mt5_runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_helper_0001`
- report_id: `report_fpmarkets_v2_runtime_helper_parity_0001`

## Contract Versions

- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- parser_contract_version: `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## Coverage Summary

- pack_type: `helper-focused reuse subset`
- fixture_count: `8`
- ready_rows: `6`
- negative_non_ready_rows: `2`
- distinct_month_count_ny: `8`
- distinct_weekday_count_ny: `5`
- utc_offsets_present: `-300, -240`
- source_fixture_family: `runtime_broader_pack_0002`
- selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_helper_fixture_manifest_0001.json`

## regular_cash_session

### fix_regular_cash_session_0001
- stratum: `regular_cash_session`
- bucket: `regular_cash_session`
- evaluated_timestamp_utc: `2022-09-01T16:40:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T12:40:00-04:00`
- month_ny: `2022-09`
- weekday_ny: `Thursday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required inputs remain runtime-ready on a normal US cash-session middle-segment sample`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## cash_close_boundary

### fix_cash_close_boundary_1555_0002
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1555`
- evaluated_timestamp_utc: `2026-03-31T19:55:00Z`
- evaluated_timestamp_america_new_york: `2026-03-31T15:55:00-04:00`
- month_ny: `2026-03`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close pre-boundary semantics remain exact on a 15:55 America/New_York contract-surface sample`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

### fix_cash_close_boundary_1600_0002
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1600`
- evaluated_timestamp_utc: `2026-02-27T21:00:00Z`
- evaluated_timestamp_america_new_york: `2026-02-27T16:00:00-05:00`
- month_ny: `2026-02`
- weekday_ny: `Friday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close boundary semantics remain exact on a 16:00 America/New_York contract-surface sample`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## dst_sensitive

### fix_dst_sensitive_utc4_0001
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc4`
- evaluated_timestamp_utc: `2023-03-13T20:00:00Z`
- evaluated_timestamp_america_new_york: `2023-03-13T16:00:00-04:00`
- month_ny: `2023-03`
- weekday_ny: `Monday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-4 side without timezone drift`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

### fix_dst_sensitive_utc5_0002
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc5`
- evaluated_timestamp_utc: `2025-11-04T21:00:00Z`
- evaluated_timestamp_america_new_york: `2025-11-04T16:00:00-05:00`
- month_ny: `2025-11`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-5 side without timezone drift`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## full_external_alignment

### fix_full_external_alignment_0002
- stratum: `full_external_alignment`
- bucket: `full_external_alignment`
- evaluated_timestamp_utc: `2026-01-30T19:00:00Z`
- evaluated_timestamp_america_new_york: `2026-01-30T14:00:00-05:00`
- month_ny: `2026-01`
- weekday_ny: `Friday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `all required external symbols exact-timestamp match on a non-boundary afternoon sample`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## cash_open_missing_equities

### fix_negative_cash_open_missing_equities_0002
- stratum: `cash_open_missing_equities`
- bucket: `negative_cash_open_missing_equities`
- evaluated_timestamp_utc: `2025-12-31T14:35:00Z`
- evaluated_timestamp_america_new_york: `2025-12-31T09:35:00-05:00`
- month_ny: `2025-12`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `False`
- expected_contract_behavior: `equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## off_hours_external_alignment_missing

### fix_negative_off_hours_post_close_0002
- stratum: `off_hours_external_alignment_missing`
- bucket: `negative_off_hours_post_close`
- evaluated_timestamp_utc: `2025-09-30T20:55:00Z`
- evaluated_timestamp_america_new_york: `2025-09-30T16:55:00-04:00`
- month_ny: `2025-09`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `False`
- expected_contract_behavior: `off-hours external alignment missing keeps the post-close row non-ready with no reduced substitute`
- source_fixture_family: `runtime_broader_pack_0002`
- source_artifact_ref: `../02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`

## Notes

- known_caveats: `this helper-focused fixture inventory, selection manifest, Python snapshot, MT5 request, and MT5 helper pack are materialized, but helper-path closure is still pending the paired evaluation pass and later Stage 05 read update`
- mt5_request_ref: `../02_runs/runtime_helper_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_helper_0001.json`
- mt5_window_spec_ref: `../02_runs/runtime_helper_pack_0001/mt5_target_windows_utc.txt`
- selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_helper_fixture_manifest_0001.json`
- reuse_guidance: `this inventory freezes the first helper-focused Stage 05 subset derived from the active broader_0002 pack; the paired MT5 snapshot export and parity comparison must reuse these same timestamps and ids rather than sampling a new helper window set`
