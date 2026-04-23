# 2026-04-20 Stage 05 Dual Follow-Up Order

## Status

- decided_on: `2026-04-20`
- stage: `05_exploration_kernel_freeze`
- decision_type: `ordered dual-lane follow-up after the first broader tolerance-closed read`

## Decision

- keep the existing `broader-sample parity` first-lane freeze exactly as written
- after the first active `broader_0002` tolerance-closed exact-open read, open `runtime-helper parity` as the primary next Stage 05 evidence lane
- require `additional broader-sample coverage` as the follow-up reinforcement lane after the first separate runtime-helper pass is materialized
- keep both lanes inside Stage 05 and keep both separate from operating promotion, Tier B exploration, and any fresh alpha or range opening

## Why

- the active `broader_0002` pack already exists as materialized Stage 05 evidence and now has a repeated native MT5 rerun that reproduces the same first broader tolerance-closed exact-open read
- `runtime-helper parity` still remains explicitly unevaluated in v2, so it is now the lowest-ambiguity separate gap after the first broader tolerance-closed read exists
- extra broader coverage still has value, but it no longer answers the most distinct remaining open gate by itself
- ordering the two lanes explicitly reduces state drift and keeps Stage 05 from re-opening the same lane-choice question on every pass

## What This Does Not Claim

- no `runtime-helper parity` closure yet
- no separate `broader-sample parity` closure yet
- no Stage 05 closure yet
- no operating promotion
- no Tier B or Tier C readiness change

## Consequences

- the next planning or materialization work inside Stage 05 should target a first v2 runtime-helper parity lane brief, inputs, and pack materialization path
- once that helper lane produces a first evaluated read, the next follow-up should extend broader-sample coverage again rather than jump directly to exploration or operating promotion
- the active `broader_0002` pack stays the current broader read while the new helper lane opens separately
- Stage 03 and Stage 04 stay closed and do not reopen unless a new contradiction appears

## Operational Meaning

- active_stage changed?: `no`
- Stage 05 remains open?: `yes`
- broader-sample first-lane freeze changed?: `no`
- runtime-helper parity opened as the primary next lane?: `yes, as ordered follow-up only`
- additional broader-sample coverage retained after helper work?: `yes`
- workspace and Stage 05 state docs need the same-pass update?: `yes`
