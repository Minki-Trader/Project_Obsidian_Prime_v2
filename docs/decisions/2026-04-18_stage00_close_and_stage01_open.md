# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_stage00_close_stage01_open`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `close Stage 00 as planning scaffold complete and open Stage 01 for the first materialized dataset-contract evidence`

## What Was Decided

- adopted:
  - close `00_foundation_sprint` as a completed planning and governance stage
  - keep the first planning freeze card, first planning gold fixture inventory, and first planning runtime parity report as durable Stage 00 scaffold artifacts
  - open `01_dataset_contract_freeze` as the active stage
  - move row summary, source identity, and first materialized dataset-hash work into Stage 01
  - keep runtime parity metrics and broader artifact-identity closure assigned to later foundation stages
- not adopted:
  - treating the Stage 00 planning artifacts as materialized dataset evidence
  - claiming runtime parity closure from planning artifacts alone
  - reopening alpha or range stages while Stage 01 to 05 foundation gates remain open

## Why

- Stage 00 was charter and scaffold work by design, and those planning outputs now exist
- leaving Stage 00 open for downstream materialization would blur the difference between planning closure and evidence closure
- opening Stage 01 makes the next required work explicit without pretending parity or artifact identity are already closed

## What Remains Open

- the first materialized row summary, source identities, and output hashes for `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- the first bound fixture timestamps and snapshot refs for `fixture_fpmarkets_v2_runtime_minimum_0001`
- the first evaluated runtime parity results for `report_fpmarkets_v2_runtime_parity_0001`
- the later `04_artifact_identity_closure` and `05_exploration_kernel_freeze` gates

## Evidence Used

- `stages/00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `stages/00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
- `stages/00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `stages/00_foundation_sprint/04_selected/selection_status.md`
- `docs/workspace/workspace_state.yaml`

## Operational Meaning

- `current_operating_reference updated?`: `no`
- `shadow updated?`: `no`
- `automatic carry-forward from legacy?`: `no`
- `workspace_state update needed?`: `yes, completed with the Stage 00 close and Stage 01 open transition`
- `next mandatory follow-up`: `materialize the first dataset-contract evidence inside 01_dataset_contract_freeze`
