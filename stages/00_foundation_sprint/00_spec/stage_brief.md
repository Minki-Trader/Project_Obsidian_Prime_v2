# Stage 00 Foundation Sprint

- stage: `00_foundation_sprint`
- stage_type: `foundation_stage`
- updated_on: `2026-04-16`
- owner_path: `stages/00_foundation_sprint/`

## Purpose

- make v2 re-entry fast and safe before any new alpha search
- establish the first v2 state, policy, registry, and durable-decision skeleton
- define the first v2 dataset freeze and parity harness path

## Inherited Context

- legacy regular reference: `34D_29s_outbarlong_0001`
- legacy contract-aligned operating candidate: `34D min_margin=0.06000` after the Stage 42 helper-path cleanup
- legacy parity lesson: localized model-input parity closed only after replacing MT5 built-in ATR and Stochastic paths with contract-matching logic

## Scope

- in scope:
  - workspace state
  - restart decision memo
  - branch, promotion, artifact, and stage-type policies
  - artifact, assumption, and negative-result registers
  - Stage 00 read path and selection status
  - define the first dataset-freeze and parity-harness to-do surface
- not in scope:
  - new alpha search
  - new training runs
  - threshold or sidecar experiments
  - claiming v2 parity closure from legacy evidence alone

## Success Criteria

- a new thread can re-enter by reading fewer than ten documents
- current state lives in one obvious file
- durable artifact identity has an obvious home in Git
- Stage 00 makes the next required foundation tasks explicit

## Required Outputs

- `docs/workspace/workspace_state.yaml`
- `docs/decisions/2026-04-16_v2_restart_decision.md`
- `docs/registers/*`
- `stages/00_foundation_sprint/03_reviews/review_index.md`
- `stages/00_foundation_sprint/04_selected/selection_status.md`

## Close Bias

- close Stage 00 only after the first v2 dataset-freeze plan and parity-harness plan are explicit
- do not let Stage 00 turn into a broad design rabbit hole
