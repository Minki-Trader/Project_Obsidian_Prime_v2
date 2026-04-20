# Stage 05 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../01_inputs/next_evidence_dual_lane_plan.md`
4. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
5. `../../../docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
6. `../../../docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
7. `../../../docs/decisions/2026-04-20_stage05_dual_followup_order.md`
8. `../../../docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
9. `../../../docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
10. `../../../docs/adr/0002_broader_sample_parity_charter.md`
11. `report_fpmarkets_v2_runtime_helper_parity_0001.md`
12. `report_fpmarkets_v2_runtime_broader_parity_0002.md`
13. `report_fpmarkets_v2_runtime_broader_parity_0003.md`
14. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 05 is now closed because the first downstream exploration boundary is explicit on the combined broader_0002 + helper_0001 + broader_0003 evidence family; Stage 06 now owns downstream tiered-readiness exploration while the strict Tier A runtime rule remains unchanged`
- do not confuse with regular line: `the closed Stage 05 read is still foundation evidence and does not compare alpha candidates`

## Closed Branches

- Stage 04 already closed the first explicit artifact-identity read on the v2-native five-window pack
- Stage 05 already froze `broader-sample parity` as the first downstream validation lane and kept `runtime-helper parity` separate
- Stage 05 already retained `broader_0001` as pre-alignment mismatch evidence instead of overwriting that first evaluated broader pack
- Stage 05 already rebound `broader_0002` on the same fixed `24-window` charter shape after the localized contract-alignment fixes landed
- Stage 05 already imported the active `broader_0002` MT5 snapshot and rendered the active broader comparison summary plus report on the same frozen `24-window` pack
- Stage 05 already reran the active `broader_0002` pack to a first tolerance-closed exact-open report on the same frozen `24-window` charter without reopening Stage 03 or Stage 04
- Stage 05 already materialized and evaluated `helper_0001` as the first helper-focused eight-window subset derived from the active broader_0002 pack
- Stage 05 already advanced the ordered follow-up plan from `runtime-helper parity first, then additional broader-sample coverage` to `helper_0001 evaluated, then broader_0003 materialized for additive reinforcement`
- Stage 05 already evaluated `broader_0003` as the first additive non-overlapping broader reinforcement pack on the native MT5 path
- the strict Tier A runtime rule remains the only current runtime rule; future Tier B and Tier C paths remain separate downstream exploration vocabulary

## Open Questions

- none inside the closed Stage 05 read; the downstream home is now `06_tiered_readiness_exploration`
