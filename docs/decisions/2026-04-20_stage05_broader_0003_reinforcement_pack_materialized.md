# 2026-04-20 Stage 05 Broader_0003 Reinforcement Pack Materialized

## Status

- decided_on: `2026-04-20`
- stage: `05_exploration_kernel_freeze`
- decision_type: `additional broader-sample reinforcement pack materialized pending native evaluation`

## Decision

- freeze `broader_0003` as the first additive Stage 05 broader-sample reinforcement family after `helper_0001`
- keep `broader_0003` on the same fixed `24-window` charter shape as `broader_0002`
- require `broader_0003` to exclude every timestamp already frozen into the active `broader_0002` manifest
- treat `broader_0003` as materialized Stage 05 evidence only until a native MT5 evaluation pass exists

## Why

- the ordered dual-lane follow-up already fixed `additional broader-sample coverage` as the next required lane after the first helper-focused pass
- a new broader reinforcement family answers the remaining Stage 05 question more directly than reusing the already evaluated `broader_0002` timestamps
- excluding the active `broader_0002` timestamps keeps the reinforcement lane additive instead of rewriting the current broader read

## Materialized Read

- fixture_set_id: `fixture_fpmarkets_v2_runtime_broader_0003`
- bundle_id: `bundle_fpmarkets_v2_runtime_broader_0003`
- report_id: `report_fpmarkets_v2_runtime_broader_parity_0003`
- pack_shape: `24 windows`
- ready_rows: `16`
- negative_non_ready_rows: `8`
- distinct_month_count_ny: `22`
- distinct_weekday_count_ny: `5`
- utc_offsets_present: `-300|-240`
- selection_method: `balance_first_global_and_bucket_greedy_excluding_active_broader_0002_v1`

## What This Does Not Claim

- no MT5 native evaluation yet
- no broader-sample parity closure yet
- no runtime-helper parity closure
- no Stage 05 closure yet
- no operating promotion

## Consequences

- `broader_0002` remains the active broader evaluated pack
- `helper_0001` remains the first helper-focused evaluated pack
- the next required Stage 05 step is now the native MT5 evaluation of `broader_0003`
- any later Stage 05 closure read must name whether `broader_0003` reproduced tolerance closure or why a different reinforcement pack replaced it

## Operational Meaning

- broader reinforcement pack materialized?: `yes`
- broader reinforcement pack evaluated?: `no`
- active_stage changed?: `no`
- Stage 05 remains open?: `yes`
- workspace and Stage 05 state docs need the same-pass update?: `yes`
