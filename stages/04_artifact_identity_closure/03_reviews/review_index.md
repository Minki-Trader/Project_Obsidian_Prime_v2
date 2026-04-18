# Stage 04 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
4. `../../03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
5. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 04 opened after Stage 03 closed model-input parity within tolerance and materialized a first machine-readable identity chain across the request, MT5 snapshot, and comparison summary, while the rendered report and registry already carry linked evidence for the same pack`
- do not confuse with regular line: `Stage 04 is still foundation work and does not compare alpha candidates`

## Closed Branches

- Stage 03 already closed the first model-input parity read on the five-window pack within the agreed tolerance
- the first MT5 snapshot rows now include machine-readable identity fields and the comparison summary confirms they match the request identities and tracked comparison-side hashes; the rendered report remains linked through `required_artifact_hashes_checked` and registry rows

## Open Questions

- does the first machine-readable identity chain plus the recorded hashes already satisfy the explicit Stage 04 closure read?
- if not, what is the smallest additional runtime self-check note needed to close Stage 04 without reopening Stage 03?
