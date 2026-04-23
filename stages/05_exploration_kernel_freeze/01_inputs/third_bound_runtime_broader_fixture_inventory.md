# Bound Runtime Broader Fixture Inventory

## Identity

- profile: `broader_0003`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0003`
- created_on: `2026-04-20`
- owner: `Project_Obsidian_Prime_v2 workspace`
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- bundle_id: `bundle_fpmarkets_v2_runtime_broader_0003`
- python_snapshot_id: `snapshot_fpmarkets_v2_runtime_python_broader_0003`
- target_mt5_runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_broader_0003`
- report_id: `report_fpmarkets_v2_runtime_broader_parity_0003`

## Contract Versions

- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- parser_contract_version: `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## Coverage Summary

- pack_type: `fixed stratified audit pack`
- fixture_count: `24`
- ready_rows: `16`
- negative_non_ready_rows: `8`
- distinct_month_count_ny: `22`
- distinct_weekday_count_ny: `5`
- utc_offsets_present: `-300, -240`
- selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/third_bound_runtime_broader_fixture_manifest_0003.json`

## Reinforcement Boundary

- reinforcement_role: `additional broader-sample coverage without reusing the active broader_0002 timestamps`
- excluded_source_selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json`

## regular_cash_session

### fix_regular_cash_session_0001
- stratum: `regular_cash_session`
- bucket: `regular_cash_session`
- evaluated_timestamp_utc: `2022-09-01T16:45:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T12:45:00-04:00`
- month_ny: `2022-09`
- weekday_ny: `Thursday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required inputs remain runtime-ready on a normal US cash-session middle-segment sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_regular_cash_session_0002
- stratum: `regular_cash_session`
- bucket: `regular_cash_session`
- evaluated_timestamp_utc: `2026-04-13T16:40:00Z`
- evaluated_timestamp_america_new_york: `2026-04-13T12:40:00-04:00`
- month_ny: `2026-04`
- weekday_ny: `Monday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required inputs remain runtime-ready on a normal US cash-session middle-segment sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_regular_cash_session_0003
- stratum: `regular_cash_session`
- bucket: `regular_cash_session`
- evaluated_timestamp_utc: `2024-06-21T16:40:00Z`
- evaluated_timestamp_america_new_york: `2024-06-21T12:40:00-04:00`
- month_ny: `2024-06`
- weekday_ny: `Friday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required inputs remain runtime-ready on a normal US cash-session middle-segment sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_regular_cash_session_0004
- stratum: `regular_cash_session`
- bucket: `regular_cash_session`
- evaluated_timestamp_utc: `2023-07-26T16:45:00Z`
- evaluated_timestamp_america_new_york: `2023-07-26T12:45:00-04:00`
- month_ny: `2023-07`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required inputs remain runtime-ready on a normal US cash-session middle-segment sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## cash_close_boundary

### fix_cash_close_boundary_1555_0001
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1555`
- evaluated_timestamp_utc: `2022-10-11T19:55:00Z`
- evaluated_timestamp_america_new_york: `2022-10-11T15:55:00-04:00`
- month_ny: `2022-10`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close pre-boundary semantics remain exact on a 15:55 America/New_York contract-surface sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_cash_close_boundary_1555_0002
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1555`
- evaluated_timestamp_utc: `2026-03-30T19:55:00Z`
- evaluated_timestamp_america_new_york: `2026-03-30T15:55:00-04:00`
- month_ny: `2026-03`
- weekday_ny: `Monday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close pre-boundary semantics remain exact on a 15:55 America/New_York contract-surface sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_cash_close_boundary_1600_0001
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1600`
- evaluated_timestamp_utc: `2022-11-02T20:00:00Z`
- evaluated_timestamp_america_new_york: `2022-11-02T16:00:00-04:00`
- month_ny: `2022-11`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close boundary semantics remain exact on a 16:00 America/New_York contract-surface sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_cash_close_boundary_1600_0002
- stratum: `cash_close_boundary`
- bucket: `cash_close_boundary_1600`
- evaluated_timestamp_utc: `2026-02-26T21:00:00Z`
- evaluated_timestamp_america_new_york: `2026-02-26T16:00:00-05:00`
- month_ny: `2026-02`
- weekday_ny: `Thursday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `cash-close boundary semantics remain exact on a 16:00 America/New_York contract-surface sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## dst_sensitive

### fix_dst_sensitive_utc4_0001
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc4`
- evaluated_timestamp_utc: `2024-03-12T20:00:00Z`
- evaluated_timestamp_america_new_york: `2024-03-12T16:00:00-04:00`
- month_ny: `2024-03`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-4 side without timezone drift`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_dst_sensitive_utc4_0002
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc4`
- evaluated_timestamp_utc: `2026-03-09T20:00:00Z`
- evaluated_timestamp_america_new_york: `2026-03-09T16:00:00-04:00`
- month_ny: `2026-03`
- weekday_ny: `Monday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-4 side without timezone drift`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_dst_sensitive_utc5_0001
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc5`
- evaluated_timestamp_utc: `2024-11-04T21:00:00Z`
- evaluated_timestamp_america_new_york: `2024-11-04T16:00:00-05:00`
- month_ny: `2024-11`
- weekday_ny: `Monday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-5 side without timezone drift`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_dst_sensitive_utc5_0002
- stratum: `dst_sensitive`
- bucket: `dst_sensitive_utc5`
- evaluated_timestamp_utc: `2022-11-08T21:00:00Z`
- evaluated_timestamp_america_new_york: `2022-11-08T16:00:00-05:00`
- month_ny: `2022-11`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `the same contract surface survives a DST transition-week 16:00 sample on the UTC-5 side without timezone drift`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## full_external_alignment

### fix_full_external_alignment_0001
- stratum: `full_external_alignment`
- bucket: `full_external_alignment`
- evaluated_timestamp_utc: `2022-12-01T19:05:00Z`
- evaluated_timestamp_america_new_york: `2022-12-01T14:05:00-05:00`
- month_ny: `2022-12`
- weekday_ny: `Thursday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `all required external symbols exact-timestamp match on a non-boundary afternoon sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_full_external_alignment_0002
- stratum: `full_external_alignment`
- bucket: `full_external_alignment`
- evaluated_timestamp_utc: `2026-01-30T19:05:00Z`
- evaluated_timestamp_america_new_york: `2026-01-30T14:05:00-05:00`
- month_ny: `2026-01`
- weekday_ny: `Friday`
- utc_offset_minutes: `-300`
- expected_row_ready: `True`
- expected_contract_behavior: `all required external symbols exact-timestamp match on a non-boundary afternoon sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_full_external_alignment_0003
- stratum: `full_external_alignment`
- bucket: `full_external_alignment`
- evaluated_timestamp_utc: `2024-07-01T18:05:00Z`
- evaluated_timestamp_america_new_york: `2024-07-01T14:05:00-04:00`
- month_ny: `2024-07`
- weekday_ny: `Monday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required external symbols exact-timestamp match on a non-boundary afternoon sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_full_external_alignment_0004
- stratum: `full_external_alignment`
- bucket: `full_external_alignment`
- evaluated_timestamp_utc: `2025-04-16T18:05:00Z`
- evaluated_timestamp_america_new_york: `2025-04-16T14:05:00-04:00`
- month_ny: `2025-04`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `True`
- expected_contract_behavior: `all required external symbols exact-timestamp match on a non-boundary afternoon sample`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## cash_open_missing_equities

### fix_negative_cash_open_missing_equities_0001
- stratum: `cash_open_missing_equities`
- bucket: `negative_cash_open_missing_equities`
- evaluated_timestamp_utc: `2023-01-04T14:35:00Z`
- evaluated_timestamp_america_new_york: `2023-01-04T09:35:00-05:00`
- month_ny: `2023-01`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `False`
- expected_contract_behavior: `equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_cash_open_missing_equities_0002
- stratum: `cash_open_missing_equities`
- bucket: `negative_cash_open_missing_equities`
- evaluated_timestamp_utc: `2025-12-30T14:35:00Z`
- evaluated_timestamp_america_new_york: `2025-12-30T09:35:00-05:00`
- month_ny: `2025-12`
- weekday_ny: `Tuesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `False`
- expected_contract_behavior: `equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_cash_open_missing_equities_0003
- stratum: `cash_open_missing_equities`
- bucket: `negative_cash_open_missing_equities`
- evaluated_timestamp_utc: `2024-08-02T13:35:00Z`
- evaluated_timestamp_america_new_york: `2024-08-02T09:35:00-04:00`
- month_ny: `2024-08`
- weekday_ny: `Friday`
- utc_offset_minutes: `-240`
- expected_row_ready: `False`
- expected_contract_behavior: `equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_cash_open_missing_equities_0004
- stratum: `cash_open_missing_equities`
- bucket: `negative_cash_open_missing_equities`
- evaluated_timestamp_utc: `2023-10-19T13:35:00Z`
- evaluated_timestamp_america_new_york: `2023-10-19T09:35:00-04:00`
- month_ny: `2023-10`
- weekday_ny: `Thursday`
- utc_offset_minutes: `-240`
- expected_row_ready: `False`
- expected_contract_behavior: `equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## off_hours_external_alignment_missing

### fix_negative_off_hours_pre_open_0001
- stratum: `off_hours_external_alignment_missing`
- bucket: `negative_off_hours_pre_open`
- evaluated_timestamp_utc: `2023-02-01T05:05:00Z`
- evaluated_timestamp_america_new_york: `2023-02-01T00:05:00-05:00`
- month_ny: `2023-02`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `False`
- expected_contract_behavior: `off-hours external alignment missing keeps the pre-open row non-ready with no reduced substitute`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_off_hours_pre_open_0002
- stratum: `off_hours_external_alignment_missing`
- bucket: `negative_off_hours_pre_open`
- evaluated_timestamp_utc: `2025-11-26T05:00:00Z`
- evaluated_timestamp_america_new_york: `2025-11-26T00:00:00-05:00`
- month_ny: `2025-11`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-300`
- expected_row_ready: `False`
- expected_contract_behavior: `off-hours external alignment missing keeps the pre-open row non-ready with no reduced substitute`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_off_hours_post_close_0001
- stratum: `off_hours_external_alignment_missing`
- bucket: `negative_off_hours_post_close`
- evaluated_timestamp_utc: `2022-09-01T01:05:00Z`
- evaluated_timestamp_america_new_york: `2022-08-31T21:05:00-04:00`
- month_ny: `2022-08`
- weekday_ny: `Wednesday`
- utc_offset_minutes: `-240`
- expected_row_ready: `False`
- expected_contract_behavior: `off-hours external alignment missing keeps the post-close row non-ready with no reduced substitute`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

### fix_negative_off_hours_post_close_0002
- stratum: `off_hours_external_alignment_missing`
- bucket: `negative_off_hours_post_close`
- evaluated_timestamp_utc: `2025-10-31T20:55:00Z`
- evaluated_timestamp_america_new_york: `2025-10-31T16:55:00-04:00`
- month_ny: `2025-10`
- weekday_ny: `Friday`
- utc_offset_minutes: `-240`
- expected_row_ready: `False`
- expected_contract_behavior: `off-hours external alignment missing keeps the post-close row non-ready with no reduced substitute`
- source_artifact_ref: `../02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`

## Notes

- known_caveats: `this broader-sample fixture inventory, selection manifest, Python snapshot, MT5 request, and MT5 helper pack are materialized, but the MT5 snapshot export, comparison summary, and rendered broader parity report remain pending the paired evaluation pass`
- mt5_request_ref: `../02_runs/runtime_broader_pack_0003/mt5_snapshot_request_fpmarkets_v2_runtime_broader_0003.json`
- mt5_window_spec_ref: `../02_runs/runtime_broader_pack_0003/mt5_target_windows_utc.txt`
- selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/third_bound_runtime_broader_fixture_manifest_0003.json`
- excluded_source_selection_manifest_ref: `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json`
- reuse_guidance: `this inventory now freezes the selected Stage 05 broader-sample twenty-four-window pack; the paired MT5 snapshot export and parity comparison must reuse these same timestamps and ids rather than sampling a new window set`
