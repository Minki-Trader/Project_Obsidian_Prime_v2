# Stage 01 Dataset Contract Freeze

- stage: `01_dataset_contract_freeze`
- stage_type: `foundation_stage`
- updated_on: `2026-04-18`
- owner_path: `stages/01_dataset_contract_freeze/`

## Purpose

- convert the Stage 00 planning freeze into the first materialized dataset-contract evidence pack
- record the first durable row summary, source identities, and output hashes for `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- keep the dataset-contract surface explicit before any broader parser, parity, or alpha work

## Inherited Context

- `00_foundation_sprint` is closed as planning scaffold complete
- the first planning freeze card, planning gold fixture inventory, and planning runtime parity report already exist
- the contract-order `58`-feature fingerprint is fixed at `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- placeholder monthly weights remain an explicit caveat until real monthly weights are supplied

## Scope

- in scope:
  - first materialized row summary
  - source identity capture
  - output artifact hashes for the first reusable dataset freeze
  - registry backfill for the materialized dataset evidence
  - Stage 01 live read path and selection note
- not in scope:
  - evaluated runtime parity metrics
  - fixture timestamp binding
  - bundle or runtime identity closure beyond dataset artifacts
  - new alpha or range search

## Success Criteria

- the planning freeze card is upgraded with materialized row counts, invalid-reason breakdown, source identities, and output hashes
- the dataset artifact identity is durable and machine-readable in `docs/registers/artifact_registry.csv`
- the remaining parity and broader artifact-identity work is still explicit, but no longer blocks Stage 01 scope definition

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
- `../../00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
- `../../00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `../../../docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `../../../docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `../../../docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
- local raw export roots and first processed dataset outputs

## Required Outputs

- updated dataset freeze card with materialized dataset fields
- updated `docs/registers/artifact_registry.csv`
- `03_reviews/review_index.md`
- `04_selected/selection_status.md`

## Close Bias

- close Stage 01 only after materialized row summary, source identities, and dataset-output hashes are written back into the freeze card and registry
- do not let Stage 01 absorb runtime parity or broader artifact identity closure work
