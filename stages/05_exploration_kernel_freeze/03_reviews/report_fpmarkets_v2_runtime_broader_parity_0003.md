# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0003`
- report_id: `report_fpmarkets_v2_runtime_broader_parity_0003`
- reviewed_on: `2026-04-20`
- bundle_id: `bundle_fpmarkets_v2_runtime_broader_0003`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_broader_0003`
- stage: `05_exploration_kernel_freeze`

## Scope

- closure_scope: `additional_broader_reinforcement_pack_tolerance_closed_identity_trace_materialized_exact_open`
- audited_window(s): `2022-09-01T16:45:00Z|2026-04-13T16:40:00Z|2024-06-21T16:40:00Z|2023-07-26T16:45:00Z|2022-10-11T19:55:00Z|2026-03-30T19:55:00Z|2022-11-02T20:00:00Z|2026-02-26T21:00:00Z|2024-03-12T20:00:00Z|2026-03-09T20:00:00Z|2024-11-04T21:00:00Z|2022-11-08T21:00:00Z|2022-12-01T19:05:00Z|2026-01-30T19:05:00Z|2024-07-01T18:05:00Z|2025-04-16T18:05:00Z|2023-01-04T14:35:00Z|2025-12-30T14:35:00Z|2024-08-02T13:35:00Z|2023-10-19T13:35:00Z|2023-02-01T05:05:00Z|2025-11-26T05:00:00Z|2022-09-01T01:05:00Z|2025-10-31T20:55:00Z`
- audited_row_count: `16 ready rows + 8 negative non-ready rows`

## Inputs

- python_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/python_snapshot_fpmarkets_v2_runtime_broader_0003.json`
- mt5_snapshot_artifact: `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0003.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:84dea94a9a63388a715e8d60b29ae356038e03d80d77259c0a9952663229ff05|python_snapshot_sha256=sha256:395e694ca641b94970bc806d2d880de20a4929f048736221c0116afd6dc2ecc1|mt5_request_sha256=sha256:73e401029c8b16d0c9e7424743de989a48fac3354f0d20e8eee1371387691fb8|mt5_snapshot_sha256=sha256:2fc15fb3920eaffb45e7d29e75c9ebb18a2039faa47c36f8108b53728ff0f9e7`

## Identity Trace

- request_consistent: `true`
- mt5_identity_fields_present: `true`
- mt5_identity_values_match: `true`
- machine_readable_identity_trace: `true`

## Fixture Coverage

- fixture_strata: `cash_close_boundary=4|cash_open_missing_equities=4|dst_sensitive=4|full_external_alignment=4|off_hours_external_alignment_missing=4|regular_cash_session=4`
- fixture_buckets: `cash_close_boundary_1555=2|cash_close_boundary_1600=2|dst_sensitive_utc4=2|dst_sensitive_utc5=2|full_external_alignment=4|negative_cash_open_missing_equities=4|negative_off_hours_post_close=2|negative_off_hours_pre_open=2|regular_cash_session=4`
- negative_fixture_result: `matched_non_ready=8/8; skip_reasons=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=4,EXTERNAL_TIMESTAMP_MISMATCH_US10YR=2,EXTERNAL_TIMESTAMP_MISMATCH_USDX=1,EXTERNAL_TIMESTAMP_MISMATCH_VIX=1`

## Timestamp Identity

- evaluated_timestamp_utc: `2022-09-01T16:45:00Z|2026-04-13T16:40:00Z|2024-06-21T16:40:00Z|2023-07-26T16:45:00Z|2022-10-11T19:55:00Z|2026-03-30T19:55:00Z|2022-11-02T20:00:00Z|2026-02-26T21:00:00Z|2024-03-12T20:00:00Z|2026-03-09T20:00:00Z|2024-11-04T21:00:00Z|2022-11-08T21:00:00Z|2022-12-01T19:05:00Z|2026-01-30T19:05:00Z|2024-07-01T18:05:00Z|2025-04-16T18:05:00Z|2023-01-04T14:35:00Z|2025-12-30T14:35:00Z|2024-08-02T13:35:00Z|2023-10-19T13:35:00Z|2023-02-01T05:05:00Z|2025-11-26T05:00:00Z|2022-09-01T01:05:00Z|2025-10-31T20:55:00Z`
- evaluated_timestamp_america_new_york: `2022-09-01T12:45:00-04:00|2026-04-13T12:40:00-04:00|2024-06-21T12:40:00-04:00|2023-07-26T12:45:00-04:00|2022-10-11T15:55:00-04:00|2026-03-30T15:55:00-04:00|2022-11-02T16:00:00-04:00|2026-02-26T16:00:00-05:00|2024-03-12T16:00:00-04:00|2026-03-09T16:00:00-04:00|2024-11-04T16:00:00-05:00|2022-11-08T16:00:00-05:00|2022-12-01T14:05:00-05:00|2026-01-30T14:05:00-05:00|2024-07-01T14:05:00-04:00|2025-04-16T14:05:00-04:00|2023-01-04T09:35:00-05:00|2025-12-30T09:35:00-05:00|2024-08-02T09:35:00-04:00|2023-10-19T09:35:00-04:00|2023-02-01T00:05:00-05:00|2025-11-26T00:00:00-05:00|2022-08-31T21:05:00-04:00|2025-10-31T16:55:00-04:00`

## Results

- exact_parity: `false`
- tolerance_parity: `true`
- max_abs_diff: `7.160007811535252e-06`
- dominant_drift_features: `ema50_ema200_diff=7.16001e-06|rsi_14=2.30835e-06|atr_50=1.9025e-06|ema20_ema50_diff=1.79579e-06|rsi_50=1.63035e-06`
- zero_shift_share: `0.13685344827586207`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `the evaluated pack stays within tolerance and the remaining exact mismatch is consistent with floating-point serialization drift`
- what_this_does_not_prove: `no runtime-helper parity closure, no separate broader-sample parity closure read, no Tier B or Tier C readiness claim, and no operating promotion`
- what_remains_open: `an explicit Stage 05 closure read that keeps broader_0002 as the first broader pack, helper_0001 as the first helper-focused pack, this broader reinforcement pass as additive evidence, and any downstream exploration or operating promotion`

## Required Follow-Up

- next_sampling_plan: `update the Stage 05 read from this broader reinforcement pack, keep broader_0002 plus helper_0001 as retained evidence, and evaluate whether the exploration boundary is now explicit enough for a same-pass Stage 05 closure read`
- gate_before_closure: `follow the canonical same-pass sync norm in docs/policies/agent_trigger_policy.md (align workspace state + current working state + active-stage selection/review read, add a durable decision memo when meaning changes, and update artifact registry rows when identity changes); keep Stage 05 open for this evaluated pack and do not blur it into runtime-helper parity, Tier B or Tier C readiness, or operating promotion`
- owner: `Project_Obsidian_Prime_v2 workspace`
