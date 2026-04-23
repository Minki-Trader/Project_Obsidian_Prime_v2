# 2026-04-20 Stage 05 Helper_0001 First Focused Pack

## Status

- decided_on: `2026-04-20`
- stage: `05_exploration_kernel_freeze`
- decision_type: `first helper-focused Stage 05 pack materialized and evaluated`

## Decision

- freeze `helper_0001` as the first helper-focused Stage 05 identity family derived from the active `broader_0002` pack
- keep `helper_0001` bounded to a frozen `8-window` subset with `6 ready rows + 2 negative non-ready rows`
- treat `helper_0001` as the first separate helper-focused evaluated read, not as runtime-helper parity closure
- keep the active `broader_0002` pack as the current broader read and move `additional broader-sample coverage` to the next required Stage 05 follow-up lane

## Why

- the ordered dual-lane follow-up decision already fixed `runtime-helper parity` as the first next lane after the active broader tolerance-closed read existed
- a bounded helper-focused reuse subset from the active `broader_0002` family keeps Stage 05 additive instead of replacing the current broader evidence
- the selected helper-focused windows prioritize helper-driven areas that prior evidence had already localized, especially ATR, Stochastic, close-boundary timing, DST-sensitive timing, and one downstream helper-derived path
- the first helper-focused native MT5 run now produced a machine-readable report without reopening Stage 03 or Stage 04

## Evaluated Read

- fixture_set_id: `fixture_fpmarkets_v2_runtime_helper_0001`
- report_id: `report_fpmarkets_v2_runtime_helper_parity_0001`
- closure_scope: `first_helper_focused_pack_tolerance_closed_identity_trace_materialized_exact_open`
- matched_fixtures: `8`
- missing_fixtures: `[]`
- unexpected_record_count: `0`
- exact_parity: `false`
- tolerance_parity: `true`
- max_abs_diff: `3.9019953135266405e-06`

## What This Does Not Claim

- no runtime-helper parity closure yet
- no separate broader-sample reinforcement closure read yet
- no Stage 05 closure yet
- no operating promotion
- no Tier B or Tier C readiness change

## Consequences

- the active `broader_0002` pack remains the current broader Stage 05 read
- `helper_0001` now becomes the first separate helper-focused evaluated read inside Stage 05
- the next required Stage 05 follow-up is `additional broader-sample coverage`
- any future helper-closure claim must build on `helper_0001` or explicitly explain why a different helper-focused pack is needed

## Operational Meaning

- helper-focused pack materialized?: `yes`
- helper-focused pack evaluated?: `yes`
- runtime-helper parity closed?: `no`
- additional broader-sample coverage next?: `yes`
- workspace and Stage 05 state docs need the same-pass update?: `yes`
