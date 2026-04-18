# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-18_tiered_readiness_exploration_boundary`
- `reviewed_on`: `2026-04-18`
- `owner`: `codex + user`
- `decision`: `accept Tier A / Tier B / Tier C readiness as a future separate exploration framework without changing the current strict Tier A runtime rule`

## What Was Decided

- adopted:
  - define `Tier A / Tier B / Tier C readiness` as project vocabulary for a future reduced-risk partial-context line
  - keep `Tier A` equal to the current strict contract-aligned line
  - keep `Tier B` explicitly downstream and separate from the current operating rule
  - keep `Tier C` as hard skip whenever contract-base or session semantics fail
- not adopted:
  - replacing current `all-or-skip` semantics for the strict line
  - treating Tier B as contract-equivalent to Tier A
  - opening Tier B during current Stages `03` to `05`

## Why

- the first materialized v2 dataset showed that invalidation is dominated by `external_alignment_missing`, especially on equity symbols
- that creates a real gray zone between fully contract-aligned rows and completely unusable rows
- legacy behavior effectively stayed in a binary `ready / not ready` split
- the tiered framework preserves the strict line while creating space for later reduced-risk exploration without blurring current parity or current contract truth

## What Remains Open

- whether Tier B should be defined by group quorums, exact symbol sets, or a later readiness score
- whether Tier B needs its own model family or can use explicit readiness features with separate calibration
- the exact reporting and registry conventions for tier-specific outputs once later exploration opens

## Evidence Used

- local `row_validity_report.json` from `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- `stages/03_runtime_parity_closure/04_selected/selection_status.md`
- `docs/context/current_working_state.md`

## Operational Meaning

- `current strict runtime rule changed?`: `no`
- `current active stage changed?`: `no`
- `current parity scope changed?`: `no`
- `workspace_state update needed?`: `yes, completed to mark Tier B as downstream-only`
- `next mandatory follow-up`: `finish Stage 03 runtime parity work before opening any tiered-readiness exploration stage`
