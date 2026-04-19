# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-19_stage05_broader_sample_first_lane`
- `reviewed_on`: `2026-04-19`
- `owner`: `codex + user`
- `decision`: `freeze broader-sample parity as the first downstream Stage 05 validation lane and keep runtime-helper parity and Tier B exploration separate`

## What Was Decided

- adopted:
  - freeze `broader-sample parity` as the first downstream lane after the Stage 04 artifact-identity closure
  - treat that lane as a `pre-exploration validation lane` rather than as alpha or range exploration
  - keep the existing minimum-pack artifact family and widen it through a fixed broader-sample charter instead of inventing a new public runtime interface
  - keep `runtime-helper parity` as a separate later validation lane
  - keep `Tier B / Tier C readiness` as later exploration vocabulary only
- not adopted:
  - opening `runtime-helper parity` before broader-sample parity
  - opening a separate exploration charter before a broader-sample parity lane exists
  - treating the broader-sample lane as a replacement for the current strict Tier A runtime rule
  - opening alpha or range work in the same pass as this kernel-freeze decision

## Why

- the current Stage 03 closure already proves the minimum `5-window` pack on the contract surface, but it explicitly does not prove broader-sample parity beyond that first pack
- the current Stage 04 closure already proves the first-pack identity and required-hash discipline, so the next lowest-risk downstream question is whether the same contract-surface parity survives a wider, stratified sample
- `runtime-helper parity` remains a different question because it concerns helper-path equivalence rather than the already closed model-input parity surface
- `Tier B` reduced-risk work remains downstream-only by decision and would blur the current strict Tier A rule if opened before a wider strict-line validation lane exists

## What Remains Open

- the imported MT5 snapshot export, broader comparison summary, and rendered broader parity report on the already materialized `24-window` pack
- separate runtime-helper parity evaluation in v2
- any later `Tier B` reduced-risk line or alpha exploration

## Evidence Used

- `stages/05_exploration_kernel_freeze/04_selected/selection_status.md`
- `stages/04_artifact_identity_closure/04_selected/selection_status.md`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `docs/policies/tiered_readiness_exploration.md`
- `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`

## Operational Meaning

- `active_stage changed?`: `no, Stage 05 remains active`
- `first downstream lane frozen?`: `yes, broader-sample parity`
- `runtime-helper parity opened?`: `no`
- `Tier B exploration opened?`: `no`
- `strict Tier A runtime rule changed?`: `no`
- `workspace_state update needed?`: `yes, completed with the broader-sample-first Stage 05 freeze`
