# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-20_stage06_first_readiness_boundary`
- `reviewed_on`: `2026-04-20`
- `owner`: `codex + user`
- `decision`: `fix the first Stage 06 deterministic readiness boundary (결정형 준비도 경계) as a docs-only governance lock (문서 전용 거버넌스 잠금) without changing the current strict Tier A runtime rule`

## What Was Decided

- adopted:
  - replace heuristic Tier B wording with a conservative deterministic boundary for the first Stage 06 read
  - fix the canonical rule as:
    - if `Group 1` or `Group 2` fails -> `tier_c`
    - else if `Group 3`, `Group 4`, and `Group 5` are all complete -> `tier_a`
    - else if exactly `1` or `2` of `Group 3` to `Group 5` are complete -> `tier_b`
    - else -> `tier_c`
  - fix `group complete` to mean that the group's required symbols and required fields exist at the exact timestamp, no forward-fill or fabricate path is used, and the group's required semantics are computable
  - fix the first Stage 06 artifact and report interface as `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane`
  - keep `B-mixed-partial` as vocabulary only and not as an eligible materialized readiness rule in the first Stage 06 boundary
  - keep this pass as a docs-only governance lock with no new dataset, runtime, or report identity rows added to `artifact_registry.csv`
- not adopted:
  - a readiness score or quorum-based rule
  - treating `B-mixed-partial` as an eligible first-boundary rule
  - deciding whether Tier B reuses the current model family or requires a separate model family
  - materializing the first scorecard, report, or reduced-risk runtime family in the same pass
  - changing the current strict Tier A runtime rule
  - claiming operating promotion

## Why

- the accepted Stage 06 purpose is to make the exploration boundary explicit before any reduced-risk artifact materializes
- the prior policy wording still carried heuristic phrases such as `materially present`, `not fully collapsed`, Tier B subprofiles, and starting-risk defaults alongside the boundary itself
- leaving those phrases in the normative rule would allow interpretation drift across the policy, the Stage 06 read, and later artifacts
- a conservative deterministic rule keeps strict Tier A unchanged while still giving Tier B and Tier C a first durable downstream home
- fixing the Stage 06 interface now closes the minimum artifact and report boundary at the governance level without pretending that scorecards, reports, or runtime artifacts already exist

## What Remains Open

- the first materialized Stage 06 scorecard or report artifact that will carry the fixed `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane` interface
- whether any first Stage 06 reduced-risk experiment needs additional helper-lane or broader-lane evidence beyond `broader_0002 + helper_0001 + broader_0003`
- whether Tier B should reuse the current model family with explicit readiness features or require a separate model family and calibration path

## Evidence Used

- `docs/policies/tiered_readiness_exploration.md`
- `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
- `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
- `stages/06_tiered_readiness_exploration/00_spec/stage_brief.md`
- `stages/06_tiered_readiness_exploration/04_selected/selection_status.md`
- `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/row_validity_report.json`

## Operational Meaning

- `active_stage changed?`: `no`
- `current strict Tier A runtime rule changed?`: `no`
- `Tier B eligibility boundary fixed?`: `yes`
- `tier-specific reporting boundary fixed?`: `yes`
- `B-mixed-partial eligible in the first boundary?`: `no`
- `first scorecard or report artifact materialized?`: `no`
- `reduced-risk runtime family materialized?`: `no`
- `artifact_registry.csv update needed in this pass?`: `no, because this pass changes governance wording only and does not add or supersede dataset, bundle, runtime, or report identity artifacts`
- `workspace_state update needed?`: `yes, completed in the same pass to align the Stage 06 deterministic boundary read`
