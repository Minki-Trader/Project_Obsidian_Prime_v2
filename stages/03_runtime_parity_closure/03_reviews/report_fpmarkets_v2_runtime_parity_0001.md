# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_minimum_0001`
- report_id: `report_fpmarkets_v2_runtime_parity_0001`
- reviewed_on: `2026-04-19`
- bundle_id: `bundle_fpmarkets_v2_runtime_minimum_0001`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_0001`
- stage: `03_runtime_parity_closure`

## Scope

- closure_scope: `first_evaluated_pack_tolerance_closed_identity_trace_materialized_exact_open`
- audited_window(s): `2022-09-02T17:00:00Z|2022-09-01T20:00:00Z|2022-11-09T21:00:00Z|2022-09-01T19:55:00Z|2022-09-01T13:35:00Z`
- audited_row_count: `4 ready rows + 1 negative non-ready row`

## Inputs

- python_snapshot_artifact: `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`
- mt5_snapshot_artifact: `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:bd7b41719deabf9c2500af48a14f1f12e5981ff9e8489341ba5065c9037238f2|python_snapshot_sha256=sha256:2f91f2b5d93fd855efbfa8c4ba7c100d7eac207740e5ab3c2d1eb3deb5021cc4|mt5_request_sha256=sha256:5b6bd9ab215c2d2141a8472d5b2f4ae41373f7b06f80cdc9a8acec1f49b55077|mt5_snapshot_sha256=sha256:45da1471056c7c1ede56288466ce03faeae769aeef60691ad50b673ff1cfd3b2`

## Identity Trace

- request_consistent: `true`
- mt5_identity_fields_present: `true`
- mt5_identity_values_match: `true`
- machine_readable_identity_trace: `true`

## Fixture Coverage

- regular_closed_bar_sample: `fix_regular_closed_bar_0001`
- session_boundary_sample: `fix_session_boundary_0001`
- dst_sensitive_sample: `fix_dst_sensitive_0001`
- external_alignment_sample: `fix_external_alignment_0001`
- negative_fixture_result: `MT5-side non-ready evidence is materialized at 2022-09-01T13:35:00Z with skip_reason=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas`

## Timestamp Identity

- evaluated_timestamp_utc: `2022-09-02T17:00:00Z|2022-09-01T20:00:00Z|2022-11-09T21:00:00Z|2022-09-01T19:55:00Z|2022-09-01T13:35:00Z`
- evaluated_timestamp_america_new_york: `2022-09-02T13:00:00-04:00|2022-09-01T16:00:00-04:00|2022-11-09T16:00:00-05:00|2022-09-01T15:55:00-04:00|2022-09-01T09:35:00-04:00`

## Results

- exact_parity: `false`
- tolerance_parity: `true`
- max_abs_diff: `1.6846210968424202e-06`
- dominant_drift_features: `ema50_ema200_diff=1.68462e-06|atr_14=1.46268e-06|ema20_ema50_diff=1.4553e-06|rsi_14=9.94534e-07|di_spread_14=8.83391e-07`
- zero_shift_share: `0.13793103448275862`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `the first pack stays within tolerance and the remaining exact mismatch is consistent with floating-point serialization drift`
- what_this_does_not_prove: `no runtime-helper parity closure, no broader-sample parity claim, and no Stage 04 artifact-identity closure yet`
- what_remains_open: `runtime-helper parity, broader-sample parity beyond the first five windows, and the explicit Stage 04 artifact-identity closure read`

## Required Follow-Up

- next_sampling_plan: `close the Stage 03 model-input parity read, hand the machine-readable identity chain to Stage 04, and decide whether the next sample is broader-sample parity or explicit runtime self-check closure`
- gate_before_closure: `Stage 03 selection docs and workspace state must be updated in the same pass before any closure claim is made from this evaluated pack`
- owner: `Project_Obsidian_Prime_v2 workspace`
