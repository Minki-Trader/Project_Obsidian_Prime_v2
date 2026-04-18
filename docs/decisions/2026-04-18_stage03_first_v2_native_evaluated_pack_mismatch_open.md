# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_stage03_first_v2_native_evaluated_pack_mismatch_open`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `keep Stage 03 open after the first v2-native evaluated five-window pack leaves a localized mismatch open`

## What Was Decided

- adopted:
  - treat the first v2-native MT5 audit export on `runtime_parity_pack_0001` as the current Stage 03 materialized evidence line
  - keep the first evaluated report explicit as `first_evaluated_pack_mismatch_open`
  - record that the first v2-native evaluated pack already reproduces the expected `4 ready rows + 1 negative non-ready row`
  - keep model-input parity, runtime-helper parity, and Stage 04 artifact identity as separate open gates
- not adopted:
  - claiming model-input parity closure from the first v2-native evaluated pack
  - claiming runtime-helper parity closure from the current evidence
  - claiming Stage 04 artifact-identity closure from the current JSONL export alone

## Why

- the first v2-native evaluated pack now exists, so Stage 03 no longer depends on a pending MT5-side export
- the current comparison still fails both exact and tolerance parity, with the dominant drift concentrated in `ema50_ema200_diff` and smaller mismatches in `rsi_50`, `atr_50`, `atr_14_over_atr_50`, and `ema20_ema50_diff`
- the ready or non-ready outcomes and the negative-fixture skip reason already match, so the remaining issue is localized rather than a total pack failure
- the MT5 JSONL export still omits explicit embedded identity fields such as `dataset_id`, `bundle_id`, and `runtime_id`, so Stage 04 remains separate and open

## What Remains Open

- the localized Stage 03 feature mismatch root cause and a repaired rerun on the same five-window pack
- separate runtime-helper parity evaluation in v2
- `04_artifact_identity_closure`
- `05_exploration_kernel_freeze`

## Evidence Used

- `foundation/mt5/ObsidianPrimeV2_RuntimeParityAuditEA.mq5`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_tester_runtime_parity_pack_0001.ini`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`

## Operational Meaning

- `active_stage changed?`: `no`
- `first v2-native MT5 snapshot artifact materialized?`: `yes`
- `first evaluated parity report written?`: `yes`
- `model-input parity closed?`: `no`
- `runtime-helper parity closed?`: `no`
- `Stage 03 status?`: `open`
- `workspace_state update needed?`: `yes, to reflect the first v2-native evaluated mismatch-open read`
