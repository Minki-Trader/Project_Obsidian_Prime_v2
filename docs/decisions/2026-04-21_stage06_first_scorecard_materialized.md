# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-21_stage06_first_scorecard_materialized`
- `reviewed_on`: `2026-04-21`
- `owner`: `codex + user`
- `decision`: `materialize the first Stage 06 scorecard (점수표) as row-level labels (행 단위 라벨) plus a machine-readable summary (기계가독 요약) plus a review report (리뷰 보고서) on the fixed deterministic readiness boundary (결정형 준비도 경계) without changing the current strict Tier A runtime rule (실행 규칙)`

## What Was Decided

- adopted:
  - reuse `build_feature_frame()` from the Stage 01 dataset materializer (`데이터셋 생성기`) instead of reading `features.parquet`
  - materialize the first Stage 06 row-label artifact under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
  - materialize the first Stage 06 machine-readable summary under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`
  - materialize the first Stage 06 review report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
  - keep the fixed readiness interface as `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane`
  - append the first Stage 06 registry rows as `readiness_row_labels`, `readiness_scorecard_summary`, and `readiness_scorecard_report`
- not adopted:
  - any reduced-risk runtime family (`축소위험 런타임 계열`)
  - any operating promotion (`운영 승격`)
  - any decision on whether Tier B reuses the current model family or requires a separate model family
  - any claim that `B-mixed-partial` became an eligible rule

## Materialized Read

- shared window (`공유 구간`) counts:
  - `tier_a=56988`
  - `tier_b=88303`
  - `tier_c=116053`
- practical window (`실전 구간`) counts:
  - `tier_a=55457`
  - `tier_b=86192`
  - `tier_c=113352`
- top missing groups (`상위 누락 그룹`) in the shared window:
  - `g5_breadth_extension=190434`
  - `g4_leader_equity=190431`
  - `g3_macro_proxy=126987`
  - `g2_session_semantics=12490`
- top missing symbols (`상위 누락 심볼`) in the practical window:
  - `NVDA.xnas=185791`
  - `MSFT.xnas=184925`
  - `TSLA.xnas=184921`
  - `META.xnas=184919`

## Why

- the first deterministic Stage 06 boundary was already fixed at the governance layer and the next missing durable artifact was a scorecard or report that actually used that boundary
- materializing row-level labels plus summary plus report closes the first Stage 06 artifact boundary without pretending that a reduced-risk runtime family already exists
- the scorecard now gives the next experiment question a concrete evidence base instead of a policy-only boundary
- same-pass registry rows were required because the first durable Stage 06 artifact identities now exist

## What Remains Open

- whether scorecard_0001 is enough to open a first Tier B reduced-risk experiment or whether additional helper-lane or broader-lane evidence is still required first
- whether Tier B should reuse the current model family with explicit readiness features or require a separate model family and calibration path
- whether any first Tier B experiment can proceed under the placeholder monthly-weight source or should wait for a real source

## Evidence Used

- `docs/policies/tiered_readiness_exploration.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `foundation/pipelines/materialize_fpmarkets_v2_tiered_readiness_scorecard.py`
- `tests/test_materialize_fpmarkets_v2_tiered_readiness_scorecard.py`
- `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`

## Operational Meaning

- `active_stage changed?`: `no`
- `current strict Tier A runtime rule changed?`: `no`
- `first scorecard materialized?`: `yes`
- `first scorecard reviewed?`: `yes`
- `reduced-risk runtime family materialized?`: `no`
- `operating promotion claimed?`: `no`
- `artifact_registry.csv update needed?`: `yes and completed in the same pass because the first durable Stage 06 artifact identities now exist`
- `workspace_state update needed?`: `yes and completed in the same pass so the active Stage 06 read stays aligned with the materialized scorecard`
