# Stage 05 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-19_stage04_close_and_stage05_open.md`
4. `../../../docs/policies/tiered_readiness_exploration.md`
5. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `not used`
- diagnostic read: `Stage 05 opened after Stage 04 closed the first explicit artifact-identity read, and it is now explicitly blocked because no durable ordering decision has frozen which downstream lane may open first`
- do not confuse with regular line: `Stage 05 is still foundation work and does not compare alpha candidates`

## Closed Branches

- Stage 04 already closed the first explicit artifact-identity read on the v2-native five-window pack
- the strict Tier A runtime rule remains the only current runtime rule; future Tier B and Tier C paths remain downstream-only exploration vocabulary

## Open Questions

- which downstream lane should open first once Stage 05 is frozen: broader-sample parity, runtime-helper parity, or a separate exploration charter?
- what minimum reporting boundary is required before any future Tier B reduced-risk line can open without blurring into the strict Tier A line?
