# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-20_stage05_close_stage06_open`
- `reviewed_on`: `2026-04-20`
- `owner`: `codex + user`
- `decision`: `close Stage 05 after the explicit broader_0002 + helper_0001 + broader_0003 kernel-freeze read and open Stage 06 for tiered-readiness exploration`

## What Was Decided

- adopted:
  - close `05_exploration_kernel_freeze` because the combined `broader_0002`, `helper_0001`, and additive `broader_0003` evidence family now freezes the first downstream exploration boundary clearly enough that later exploration work cannot drift open by implication
  - keep the remaining `exact_parity=false` notes bounded as floating-point serialization drift rather than as a Stage 05 blocker
  - keep separate `runtime-helper parity` closure and separate `broader-sample parity` closure outside the Stage 05 closure claim
  - open `06_tiered_readiness_exploration` as the new active stage
  - align workspace state and current working state to the actual branch `codex/stage06-tiered-readiness-open`
- not adopted:
  - claiming runtime-helper parity closure from `helper_0001`
  - claiming a separate broader-sample parity closure read from `broader_0002` plus `broader_0003`
  - relaxing the current strict Tier A runtime rule
  - claiming operating promotion or opening alpha or range search in the same pass as this Stage 05 closure

## Why

- Stage 05 owns the exploration-kernel freeze boundary, not separate helper-lane closure, separate broader-sample closure, or operating promotion
- the active `broader_0002` twenty-four-window pack already provided the first broader tolerance-closed exact-open read on the contract-aligned Stage 05 family
- the first helper-focused `helper_0001` pack already provided a separate eight-window tolerance-closed exact-open read without replacing the active broader evidence
- the additive `broader_0003` reinforcement pack now reproduced a native MT5 tolerance-closed exact-open read on a non-overlapping twenty-four-window charter pack with `matched_fixtures=24`, `unexpected_record_count=0`, `tolerance_parity=true`, and `max_abs_diff=7.160007811535252e-06`
- together those three evidence families now make the downstream exploration boundary explicit enough that a later exploration-only stage can open without pretending that helper closure, broader closure, or operating promotion already happened
- the accepted `Tier A / Tier B / Tier C` readiness framework already had a downstream policy home, so the first natural post-foundation exploration stage is now the explicit tiered-readiness exploration stage rather than an implied alpha-search stage

## What Remains Open

- the first explicit Stage 06 Tier B or Tier C readiness boundary and reporting identity
- whether any reduced-risk Stage 06 line needs additional helper-lane or broader-lane evidence before experimentation begins
- whether Tier B should reuse the current model family with explicit readiness features or require a separate model family and calibration path
- any later operating promotion or alpha/range search

## Evidence Used

- `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
- `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0002.json`
- `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
- `stages/05_exploration_kernel_freeze/02_runs/runtime_helper_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_helper_0001.json`
- `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
- `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0003/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0003.json`
- `docs/policies/tiered_readiness_exploration.md`
- `docs/registers/artifact_registry.csv`

## Operational Meaning

- `active_stage changed?`: `yes, Stage 05 closed and Stage 06 opened`
- `exploration-kernel freeze closed?`: `yes, on the explicit broader_0002 + helper_0001 + broader_0003 read`
- `runtime-helper parity closed?`: `no`
- `broader-sample parity separately closed?`: `no`
- `strict Tier A runtime rule changed?`: `no`
- `operating promotion happened?`: `no`
- `workspace_state update needed?`: `yes, completed with the Stage 05 close and Stage 06 open transition`
