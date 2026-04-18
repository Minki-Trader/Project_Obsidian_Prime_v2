# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_stage03_bound_minimum_fixture_pack`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `bind the first five-window Stage 03 minimum parity pack and materialize the first Python-side snapshot artifact before the MT5-side parity pass`

## What Was Decided

- adopted:
  - bind exact timestamps for `fixture_fpmarkets_v2_runtime_minimum_0001`
  - materialize the first Python-side snapshot artifact under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/`
  - materialize an MT5 request artifact and exact UTC window spec for the same five fixtures
  - keep the first Stage 03 parity report explicit as `not_yet_evaluated` until the MT5 snapshot artifact exists
- not adopted:
  - claiming Python-only fixture binding as full runtime parity closure
  - claiming artifact identity closure from the Python-side pack alone
  - reopening alpha or range stages while Stage 03 still lacks MT5-side parity evidence

## Why

- the active Stage 03 blocker was still the smallest honest first parity pack
- the local workspace already had enough materialized dataset evidence to bind exact timestamps deterministically
- the repo still has no v2-native MT5 snapshot artifact, so the next safest move is to freeze the window set and Python-side truth first

## What Remains Open

- the first MT5 snapshot artifact for `runtime_fpmarkets_v2_mt5_snapshot_0001`
- the first evaluated feature-vector comparison results for `report_fpmarkets_v2_runtime_parity_0001`
- the later `04_artifact_identity_closure` and `05_exploration_kernel_freeze` gates

## Evidence Used

- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- local raw exports under `data/raw/mt5_bars/m5/`
- local processed dataset outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`

## Operational Meaning

- `active_stage changed?`: `no`
- `fixture timestamps bound?`: `yes`
- `first Python snapshot artifact materialized?`: `yes`
- `first MT5 snapshot artifact materialized?`: `no`
- `model-input parity closed?`: `no`
- `workspace_state update needed?`: `yes, to reflect the bound pack and the remaining MT5-side gap`
