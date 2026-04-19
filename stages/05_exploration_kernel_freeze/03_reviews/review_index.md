# Stage 05 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
4. `../../../docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
5. `../../../docs/adr/0002_broader_sample_parity_charter.md`
6. `../../../docs/policies/tiered_readiness_exploration.md`
7. `report_fpmarkets_v2_runtime_broader_parity_0002.md`
8. `report_fpmarkets_v2_runtime_broader_parity_0001.md`
9. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 05 remains open, the first downstream lane is frozen to broader-sample parity, broader_0001 is retained as pre-alignment mismatch evidence, and the active contract-aligned broader_0002 twenty-four-window pack now reaches the first broader tolerance-closed read with identity trace materialized and exact-open bounded to floating-point serialization drift; that first broader evaluated pack still does not by itself close broader-sample parity as a separate stage read`
- do not confuse with regular line: `Stage 05 is still foundation work and does not compare alpha candidates`

## Closed Branches

- Stage 04 already closed the first explicit artifact-identity read on the v2-native five-window pack
- Stage 05 already froze `broader-sample parity` as the first downstream validation lane and kept `runtime-helper parity` separate
- Stage 05 already retained `broader_0001` as pre-alignment mismatch evidence instead of overwriting that first evaluated broader pack
- Stage 05 already rebound `broader_0002` on the same fixed `24-window` charter shape after the localized contract-alignment fixes landed
- Stage 05 already imported the active `broader_0002` MT5 snapshot and rendered the active broader comparison summary plus report on the same frozen `24-window` pack
- Stage 05 already reran the active `broader_0002` pack to a first tolerance-closed exact-open report on the same frozen `24-window` charter without reopening Stage 03 or Stage 04
- the strict Tier A runtime rule remains the only current runtime rule; future Tier B and Tier C paths remain downstream-only exploration vocabulary

## Open Questions

- should the next Stage 05 evidence extend broader-sample coverage again or open a separate runtime-helper parity lane while keeping the first broader tolerance-closed pack as the active read?
- does the remaining exact-open float drift require tighter serialization discipline before any later explicit broader-sample closure read, or is the current tolerance boundary sufficient?
- what minimum reporting and registry boundary must any future Tier B reduced-risk line carry so it never blurs with the strict Tier A runtime rule?
