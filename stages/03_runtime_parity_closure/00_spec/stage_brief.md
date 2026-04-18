# Stage 03 Runtime Parity Closure

- stage: `03_runtime_parity_closure`
- stage_type: `foundation_stage`
- updated_on: `2026-04-18`
- owner_path: `stages/03_runtime_parity_closure/`

## Purpose

- materialize the first evaluated Python to MT5 runtime parity pack on the frozen `58`-feature contract surface
- bind the first fixture timestamps and snapshot refs for the minimum parity fixture inventory
- keep model-input parity distinct from runtime-helper parity and broader artifact identity closure

## Inherited Context

- `00_foundation_sprint` is closed as planning scaffold complete
- `01_dataset_contract_freeze` is closed after the first materialized dataset-contract evidence pack
- `02_feature_dataset_closure` is closed after a deterministic rerun reproduced the same row summary and tracked output hashes
- the contract-order `58`-feature fingerprint is fixed at `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- placeholder monthly weights remain an explicit caveat until real monthly weights are supplied

## Scope

- in scope:
  - first bound fixture timestamps for `fixture_fpmarkets_v2_runtime_minimum_0001`
  - first Python snapshot and MT5 snapshot refs for the minimum parity pack
  - first evaluated parity report for `report_fpmarkets_v2_runtime_parity_0001`
  - explicit separation between model-input parity and runtime-helper parity
  - Stage 03 live read path and selection note
- not in scope:
  - broader artifact identity closure beyond the first parity pack
  - operating promotion
  - new alpha or range search

## Success Criteria

- the first runtime parity pack is backed by bound fixture timestamps, snapshot refs, and an evaluated parity read
- the active stage docs state clearly whether model-input parity is closed, partially closed, or still open
- helper/runtime parity is not conflated with model-input parity
- the remaining artifact identity and exploration-kernel work stays explicit downstream

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
- `../../00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `../../00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `../../02_feature_dataset_closure/04_selected/selection_status.md`
- `../../../docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `../../../docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `../../../docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## Required Outputs

- updated `03_reviews/review_index.md`
- updated `04_selected/selection_status.md`
- first evaluated parity read with bound fixture and snapshot refs

## Close Bias

- close Stage 03 only after an evaluated parity read exists with bound fixture timestamps and snapshot refs
- do not let Stage 03 absorb broader artifact identity closure or operating promotion
