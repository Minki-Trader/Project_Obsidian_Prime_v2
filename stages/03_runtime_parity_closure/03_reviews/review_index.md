# Stage 03 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../01_inputs/first_bound_runtime_minimum_fixture_inventory.md`
4. `report_fpmarkets_v2_runtime_parity_0001.md`
5. `../../00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
6. `../../00_foundation_sprint/01_inputs/first_v2_gold_fixture_inventory.md`
7. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 03 has now evaluated the first v2-native five-window parity pack; ready and non-ready matching holds, but model-input parity remains mismatch open`
- do not confuse with regular line: `Stage 03 is still foundation work and does not compare alpha candidates`

## Closed Branches

- Stage 02 already closed deterministic feature-dataset repeatability
- the smallest honest first parity pack is now bound and evaluated against a v2-native MT5 snapshot export, but the result still leaves a localized mismatch open

## Open Questions

- which contract or MT5 path explains the localized drift led by `ema50_ema200_diff` on the first v2-native evaluated pack?
- does a repaired v2-native rerun on the same five-window pack close model-input parity without changing the already matched ready / non-ready outcomes?
