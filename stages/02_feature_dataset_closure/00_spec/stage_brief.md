# Stage 02 Feature Dataset Closure

- stage: `02_feature_dataset_closure`
- stage_type: `foundation_stage`
- updated_on: `2026-04-18`
- owner_path: `stages/02_feature_dataset_closure/`

## Purpose

- verify that the first materialized freeze reruns deterministically from the same raw `M5` source roots
- keep the frozen `58`-feature contract surface explicit while testing repeatability on the first materialized dataset freeze
- explain the sparse valid-row share honestly under exact timestamp alignment before any parity or alpha work

## Inherited Context

- `00_foundation_sprint` is closed as planning scaffold complete
- `01_dataset_contract_freeze` is closed after materializing the first reusable dataset-contract evidence pack
- the contract-order `58`-feature fingerprint is fixed at `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- placeholder monthly weights remain an explicit caveat until real monthly weights are supplied
- the first materialized freeze currently reports `raw_rows=261344`, `valid_rows=24280`, `invalid_rows=237064`

## Scope

- in scope:
  - deterministic rerun of the first materialized freeze from the same raw source roots
  - repeatability check for row summary and invalid-reason breakdown
  - repeatability check for the frozen `58`-feature contract surface and output hashes
  - explicit explanation of the large exact-match `external_alignment_missing` share
  - Stage 02 live read path and selection note
- not in scope:
  - evaluated runtime parity metrics
  - fixture timestamp binding
  - bundle or runtime identity closure beyond dataset artifacts
  - new alpha or range search

## Success Criteria

- a second deterministic pass can reproduce the same `58`-feature contract surface, row summary, and invalid-reason breakdown from the same raw roots
- any output-hash differences are either absent or explained as deterministic formatting-only differences
- the large exact-match `external_alignment_missing` share is documented honestly and no longer left as an implicit surprise
- the remaining parity and broader artifact-identity work is still explicit, but no longer blocks Stage 02 scope definition

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `../../01_dataset_contract_freeze/01_inputs/first_raw_source_inventory.md`
- `../../01_dataset_contract_freeze/04_selected/selection_status.md`
- `../../../docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `../../../docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `../../../docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
- local raw export roots and first processed dataset outputs

## Required Outputs

- updated `03_reviews/review_index.md`
- updated `04_selected/selection_status.md`
- an explicit Stage 02 read on deterministic rerun stability and coverage explanation

## Close Bias

- close Stage 02 only after deterministic rerun behavior and the exact-match coverage explanation are written back into the active stage documents
- do not let Stage 02 absorb evaluated runtime parity or broader artifact identity closure work
