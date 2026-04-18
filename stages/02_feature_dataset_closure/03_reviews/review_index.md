# Stage 02 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../00_foundation_sprint/01_inputs/first_v2_dataset_freeze_card.md`
4. `../../01_dataset_contract_freeze/04_selected/selection_status.md`
5. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 02 closed after a second rerun reproduced the same row summary, invalid-reason breakdown, and tracked output hashes`
- do not confuse with regular line: `Stage 02 is still foundation work and does not compare alpha candidates`

## Closed Branches

- Stage 01 already materialized the first dataset-contract evidence pack
- a second deterministic pass reproduced the same row summary and invalid-reason breakdown from the same raw roots
- the tracked output hashes for `features.parquet`, `row_validity_report.json`, and `dataset_summary.json` matched exactly on rerun
- the exact-match coverage explanation is now explicit: sparse overlap is expected because US100 is near-continuous while required external symbols trade on narrower overlapping sessions

## Open Questions

- none inside Stage 02 scope
- downstream home: `03_runtime_parity_closure` now owns bound fixture timestamps, snapshot refs, and evaluated parity results
