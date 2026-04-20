# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_helper_0001`
- report_id: `report_fpmarkets_v2_runtime_helper_parity_0001`
- reviewed_on: `2026-04-20`
- bundle_id: `bundle_fpmarkets_v2_runtime_helper_0001`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_helper_0001`
- stage: `05_exploration_kernel_freeze`

## Scope

- closure_scope: `first_helper_focused_pack_tolerance_closed_identity_trace_materialized_exact_open`
- audited_window(s): `2022-09-01T16:40:00Z|2026-03-31T19:55:00Z|2026-02-27T21:00:00Z|2023-03-13T20:00:00Z|2025-11-04T21:00:00Z|2026-01-30T19:00:00Z|2025-12-31T14:35:00Z|2025-09-30T20:55:00Z`
- audited_row_count: `6 ready rows + 2 negative non-ready rows`

## Inputs

- python_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/python_snapshot_fpmarkets_v2_runtime_helper_0001.json`
- mt5_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_helper_0001.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:5dd8c0d16cd02b62f987c7c0376487d8daab5b9f1521bac1a48d25cb82f4887c|python_snapshot_sha256=sha256:90a00b50e06d8c91a966e14ac0af7a53e6bfd07f5dea495ab9b4c0f0324d4a87|mt5_request_sha256=sha256:a64cb195efe39b4befd55dc796a84ad6bdf9011a992ea711248483f09cbe0d50|mt5_snapshot_sha256=sha256:b73c0932419d7368b5ea084e6efcb990fca061a52cf45cacc973f8269d933e61`

## Identity Trace

- request_consistent: `true`
- mt5_identity_fields_present: `true`
- mt5_identity_values_match: `true`
- machine_readable_identity_trace: `true`

## Fixture Coverage

- fixture_strata: `cash_close_boundary=2|cash_open_missing_equities=1|dst_sensitive=2|full_external_alignment=1|off_hours_external_alignment_missing=1|regular_cash_session=1`
- fixture_buckets: `cash_close_boundary_1555=1|cash_close_boundary_1600=1|dst_sensitive_utc4=1|dst_sensitive_utc5=1|full_external_alignment=1|negative_cash_open_missing_equities=1|negative_off_hours_post_close=1|regular_cash_session=1`
- negative_fixture_result: `matched_non_ready=2/2; skip_reasons=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=1,EXTERNAL_TIMESTAMP_MISMATCH_VIX=1`

## Timestamp Identity

- evaluated_timestamp_utc: `2022-09-01T16:40:00Z|2026-03-31T19:55:00Z|2026-02-27T21:00:00Z|2023-03-13T20:00:00Z|2025-11-04T21:00:00Z|2026-01-30T19:00:00Z|2025-12-31T14:35:00Z|2025-09-30T20:55:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T12:40:00-04:00|2026-03-31T15:55:00-04:00|2026-02-27T16:00:00-05:00|2023-03-13T16:00:00-04:00|2025-11-04T16:00:00-05:00|2026-01-30T14:00:00-05:00|2025-12-31T09:35:00-05:00|2025-09-30T16:55:00-04:00`

## Results

- exact_parity: `false`
- tolerance_parity: `true`
- max_abs_diff: `3.9019953135266405e-06`
- dominant_drift_features: `ema50_ema200_diff=3.902e-06|ema20_ema50_diff=2.75114e-06|ema9_ema20_diff=2.26307e-06|rsi_14=1.99524e-06|atr_50=1.85118e-06`
- zero_shift_share: `0.1235632183908046`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `the evaluated pack stays within tolerance and the remaining exact mismatch is consistent with floating-point serialization drift`
- what_this_does_not_prove: `no runtime-helper parity closure yet, no separate broader-sample reinforcement closure read, no Tier B or Tier C readiness claim, and no operating promotion`
- what_remains_open: `an explicit Stage 05 helper-lane closure read, the ordered additional broader-sample coverage pass beyond the active broader_0002 pack, and any downstream exploration or operating promotion`

## Required Follow-Up

- next_sampling_plan: `update the Stage 05 helper-lane read from this first helper-focused evaluated pack, keep broader_0002 as the active broader evidence, and run the ordered additional broader-sample coverage follow-up`
- gate_before_closure: `follow the canonical same-pass sync norm in docs/policies/agent_trigger_policy.md (align workspace state + current working state + active-stage selection/review read, add a durable decision memo when meaning changes, and update artifact registry rows when identity changes); keep Stage 05 open for this evaluated pack and do not blur it into runtime-helper parity, Tier B or Tier C readiness, or operating promotion`
- owner: `Project_Obsidian_Prime_v2 workspace`
