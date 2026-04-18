# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_stage01_close_stage02_open`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `close Stage 01 as first materialized dataset-contract evidence complete and open Stage 02 for deterministic feature-dataset closure`

## What Was Decided

- adopted:
  - close `01_dataset_contract_freeze` after the first row summary, invalid-reason breakdown, and processed-output hashes were written back into the freeze card and artifact registry
  - keep the first materialized freeze rooted at `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
  - open `02_feature_dataset_closure` as the active stage
  - move deterministic rerun checks and exact-match coverage explanation into Stage 02
  - keep evaluated runtime parity and broader artifact identity closure assigned to later foundation stages
- not adopted:
  - treating Stage 01 materialization as runtime parity closure
  - treating the first valid-row share as broader parser readiness without a Stage 02 coverage explanation
  - reopening alpha or range stages while Stages 02 to 05 foundation gates remain open

## Why

- Stage 01 owns the first materialized dataset-contract evidence rather than broader parser closure
- that evidence now exists with tracked row counts, invalid-reason breakdown, source identities, and processed-output hashes
- the remaining questions are no longer about whether the first freeze exists, but whether it reruns deterministically and how the sparse exact-match overlap should be interpreted honestly

## What Remains Open

- deterministic rerun and repeatability checks for the first materialized freeze
- an explicit coverage explanation for the large `external_alignment_missing` share under exact timestamp alignment
- bound fixture timestamps and evaluated runtime parity results for `03_runtime_parity_closure`
- later `04_artifact_identity_closure` and `05_exploration_kernel_freeze` gates

## Evidence Used

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `stages/01_dataset_contract_freeze/01_inputs/first_raw_source_inventory.md`
- local-only outputs under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- `stages/01_dataset_contract_freeze/04_selected/selection_status.md`
- `docs/registers/artifact_registry.csv`

## Operational Meaning

- `current_operating_reference updated?`: `no`
- `shadow updated?`: `no`
- `automatic carry-forward from legacy?`: `no`
- `workspace_state update needed?`: `yes, completed with the Stage 01 close and Stage 02 open transition`
- `next mandatory follow-up`: `rerun and explain the first materialized freeze inside 02_feature_dataset_closure`
