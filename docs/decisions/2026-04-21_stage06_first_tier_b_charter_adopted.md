# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-21_stage06_first_tier_b_charter_adopted`
- `reviewed_on`: `2026-04-21`
- `owner`: `codex + user`
- `decision`: `adopt the first Stage 06 offline-only (오프라인 전용) Tier B (부분 준비) reduced-risk experiment charter (축소위험 실험 헌장) as a separate exploration design (탐색 설계) using the current baseline model family (기준선 모델 계열) with separate calibration (별도 보정) and separate reporting (별도 보고) without changing the current strict Tier A runtime rule (실행 규칙)`

## What Was Decided

- adopted:
  - treat `scorecard_0001` as sufficient to open the first `offline-only (오프라인 전용)` `Tier B` charter
  - adopt `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md` as the durable charter home
  - keep the first `Tier B` charter `offline-only (오프라인 전용)` with no `simulated execution (가상 실행)`, no `MT5 real-environment path (MT5 실환경 경로)`, and no `operating promotion (운영 승격)`
  - reuse the current `baseline model family (기준선 모델 계열)` and current `public input-contract surface (공용 입력 계약 표면)` as the first `Tier B` design hypothesis
  - require `separate calibration (별도 보정)` or a separate `offline evaluation read (오프라인 평가 판독)` before any `Tier B` performance claim
  - keep `strict_tier_a` and `tier_b_exploration` on separate `reporting lanes (보고 레인)` with separate `KPI summaries (핵심 지표 요약)`; any `mixed aggregate (혼합 집계)` remains `info-only (정보용)`
  - allow the `placeholder monthly-weight source (임시 월별 가중치 소스)` only for `offline-only (오프라인 전용)` exploration with an explicit caveat
- not adopted:
  - any `reduced-risk runtime family (축소위험 런타임 계열)`
  - any `public API (공용 API)` or `runtime input contract (런타임 입력 계약)` change
  - any `artifact_registry.csv` additions
  - treating `Tier B` as `contract-equivalent (계약 동등)` to `Tier A`
  - any decision that the `placeholder monthly-weight source (임시 월별 가중치 소스)` is sufficient for later `simulated execution (가상 실행)` or `MT5-path expansion (MT5 경로 확장)`
  - choosing a separate `model family (모델 계열)` as the first charter default

## Why

- the first materialized `scorecard_0001` already fixed the row-label and reporting boundary, so the next missing durable artifact was the first `Tier B` charter rather than a runtime implementation
- adopting the charter now gives later `Tier B` evaluation work a durable boundary before any runtime or promotion claims can drift open by implication
- reusing the current `baseline model family (기준선 모델 계열)` is the narrowest first hypothesis, but the policy still forbids assuming that a `Tier A`-trained path is automatically safe on `Tier B` inputs
- keeping the placeholder weight caveat explicit prevents the charter from being misread as permission for `simulated execution (가상 실행)`, `MT5-path expansion (MT5 경로 확장)`, or `operating promotion (운영 승격)`

## What Remains Open

- the first `Tier B offline evaluation pack (Tier B 오프라인 평가 팩)` or `report (평가 보고서)` on the separate `tier_b_exploration` lane
- the narrowest separate `calibration read (보정 판독)` and `threshold read (임계값 판독)` for the reused baseline family on `Tier B` rows
- whether the `placeholder monthly-weight caveat (임시 월별 가중치 단서)` requires a real-weight rerun before any later `simulated execution (가상 실행)` or `MT5-path expansion (MT5 경로 확장)`

## Evidence Used

- `docs/policies/tiered_readiness_exploration.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- `stages/06_tiered_readiness_exploration/04_selected/selection_status.md`

## Operational Meaning

- `active_stage changed?`: `no`
- `current strict Tier A runtime rule changed?`: `no`
- `first Tier B offline-only charter adopted?`: `yes`
- `reduced-risk runtime family materialized?`: `no`
- `simulated execution or MT5 path authorized?`: `no`
- `operating promotion claimed?`: `no`
- `artifact_registry.csv update needed?`: `no, because this is a docs-only pass that adds no dataset, bundle, runtime, or report identity artifact`
- `workspace_state update needed?`: `yes and completed in the same pass so the active Stage 06 read stays aligned with the adopted charter`
