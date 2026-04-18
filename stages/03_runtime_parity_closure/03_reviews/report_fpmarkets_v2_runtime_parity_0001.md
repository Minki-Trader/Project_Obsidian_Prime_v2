# Runtime Parity Report

## Identity

- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- fixture_set_id: `fixture_fpmarkets_v2_runtime_minimum_0001`
- report_id: `report_fpmarkets_v2_runtime_parity_0001`
- reviewed_on: `2026-04-18`
- bundle_id: `bundle_fpmarkets_v2_runtime_minimum_0001`
- runtime_id: `runtime_fpmarkets_v2_mt5_snapshot_0001`
- stage: `03_runtime_parity_closure`

## Scope

- closure_scope: `first_evaluated_pack_mismatch_open`
- audited_window(s): `2022-09-02T17:00:00Z|2022-09-01T20:00:00Z|2022-11-09T21:00:00Z|2022-09-01T19:55:00Z|2022-09-01T13:35:00Z`
- audited_row_count: `4 ready rows + 1 negative non-ready row`

## Inputs

- python_snapshot_artifact: `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`
- mt5_snapshot_artifact: `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- parser_version: `fpmarkets_v2_stage01_materializer_v1`
- feature_contract_version: `docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16`
- runtime_contract_version: `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16`
- feature_order_hash: `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:bd7b41719deabf9c2500af48a14f1f12e5981ff9e8489341ba5065c9037238f2|python_snapshot_sha256=sha256:2f91f2b5d93fd855efbfa8c4ba7c100d7eac207740e5ab3c2d1eb3deb5021cc4|mt5_request_sha256=sha256:a47fe98b26977ad97d8af12870f25fd7ce35aeb3e83fc9b9178f68bc0f10b260|mt5_snapshot_sha256=sha256:3e009a56464e6bdd6ab8a15bd32019dabbcc61a8b333a49b7727da0e4aba4248`

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
- tolerance_parity: `false`
- max_abs_diff: `7.285655212821098`
- dominant_drift_features: `ema50_ema200_diff=7.28566|rsi_50=0.286924|atr_50=0.0397433|atr_14_over_atr_50=0.00184555|ema20_ema50_diff=0.000600701`
- zero_shift_share: `0.13793103448275862`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `localized model-input mismatch remains on the first pack`
- what_this_does_not_prove: `no runtime-helper parity closure, no broader-sample parity claim, and no Stage 04 artifact-identity closure yet`
- what_remains_open: `inspect the dominant drift features, re-check timestamp identity, and confirm whether the mismatch is localized or systemic before any closure claim`

## Required Follow-Up

- next_sampling_plan: `repair the localized MT5 export or feature mismatch, rerun the five-window comparison, and only then revisit the Stage 03 closure read`
- gate_before_closure: `Stage 03 selection docs and workspace state must be updated in the same pass before any closure claim is made from this evaluated pack`
- owner: `Project_Obsidian_Prime_v2 workspace`
