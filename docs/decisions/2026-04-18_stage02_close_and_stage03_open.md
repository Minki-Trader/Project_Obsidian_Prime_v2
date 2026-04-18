# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_stage02_close_stage03_open`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `close Stage 02 after a deterministic rerun match and open Stage 03 for the first evaluated runtime parity pack`

## What Was Decided

- adopted:
  - close `02_feature_dataset_closure` after a second rerun reproduced the same row summary, invalid-reason breakdown, and tracked output hashes
  - record the exact-match coverage explanation as part of the Stage 02 closure read
  - open `03_runtime_parity_closure` as the active stage
  - move bound fixture timestamps, snapshot refs, and evaluated parity results into Stage 03
- not adopted:
  - treating Stage 02 closure as runtime parity closure
  - treating the deterministic rerun match as artifact identity closure
  - reopening alpha or range stages while Stages 03 to 05 foundation gates remain open

## Why

- Stage 02 owns deterministic feature-dataset closure rather than runtime parity
- the second rerun matched the first materialized freeze on row summary and tracked output hashes, so repeatability no longer blocks the next gate
- the next open questions are now about runtime snapshots, fixture binding, and evaluated Python to MT5 comparison results

## What Remains Open

- bound fixture timestamps for `fixture_fpmarkets_v2_runtime_minimum_0001`
- first runtime snapshot refs and evaluated parity results for `report_fpmarkets_v2_runtime_parity_0001`
- later `04_artifact_identity_closure` and `05_exploration_kernel_freeze` gates

## Evidence Used

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- local-only outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- `stages/02_feature_dataset_closure/03_reviews/review_index.md`
- `stages/02_feature_dataset_closure/04_selected/selection_status.md`

## Operational Meaning

- `current_operating_reference updated?`: `no`
- `shadow updated?`: `no`
- `automatic carry-forward from legacy?`: `no`
- `workspace_state update needed?`: `yes, completed with the Stage 02 close and Stage 03 open transition`
- `next mandatory follow-up`: `materialize the first evaluated runtime parity pack inside 03_runtime_parity_closure`
