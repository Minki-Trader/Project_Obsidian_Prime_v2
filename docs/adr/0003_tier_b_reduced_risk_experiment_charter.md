# ADR-0003 Tier B Reduced-Risk Offline Experiment Charter

## Status

- `adr_id`: `0003`
- `reviewed_on`: `2026-04-21`
- `status`: `accepted`
- `scope`: `Stage 06` first `Tier B (부분 준비)` `offline-only (오프라인 전용)` `experiment charter (실험 헌장)` only; no `reduced-risk runtime family (축소위험 런타임 계열)` is materialized

## Intent

- open the first `Tier B` work as a separate `offline-only (오프라인 전용)` exploration after `scorecard_0001`
- keep the current strict `Tier A` runtime rule unchanged
- give the first `Tier B` question a durable home before any runtime implementation or operating claim

## Experiment Question

- can `Tier B` candidate rows add `offline coverage (오프라인 커버리지)` and separate `analysis value (분석 가치)` without claiming `contract equivalence (계약 동등성)` to `Tier A`?

## Default Model Hypothesis

- reuse the current `baseline model family (기준선 모델 계열)` and current `public input-contract surface (공용 입력 계약 표면)` as the first design hypothesis
- do not copy current `Tier A` trained outputs, thresholds, or calibration unchanged onto `Tier B`
- require `separate calibration (별도 보정)` or a separate `offline evaluation read (오프라인 평가 판독)` before any `Tier B` performance claim

## Allowed Changes

- `risk sizing (위험 크기)`
- `entry threshold (진입 임계값)`
- `exposure cap (노출 한도)`
- `reporting_lane (보고 레인)`
- `readiness_tier (준비도 등급)`

## Required Reporting Boundary

- record `strict_tier_a` and `tier_b_exploration` on separate `reporting lanes (보고 레인)`
- summarize `Tier B KPIs (핵심 지표)` separately from `Tier A`
- treat any `mixed aggregate (혼합 집계)` as `info-only (정보용)` and never as a promotion read
- keep the existing interface: `readiness_tier`, `missing_groups`, `missing_symbols`, `reporting_lane`

## What This Charter Does Not Open

- no `reduced-risk runtime family (축소위험 런타임 계열)`
- no `simulated execution (가상 실행)`
- no `MT5 real-environment path (MT5 실환경 경로)`
- no `operating promotion (운영 승격)`
- no new `public API (공용 API)` or `runtime input contract (런타임 입력 계약)`
- no `artifact_registry.csv` additions in this `docs-only (문서 전용)` pass

## Placeholder Weight Caveat

- `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` may remain in force for the first `offline-only (오프라인 전용)` `Tier B` exploration
- that `placeholder monthly-weight source (임시 월별 가중치 소스)` is not enough for `operating promotion (운영 승격)`, `simulated execution (가상 실행)`, or `MT5-path expansion (MT5 경로 확장)`

## Next Durable Outputs

- the first `Tier B offline evaluation pack (Tier B 오프라인 평가 팩)` or `report (평가 보고서)`
- the first separate `calibration (보정)` or `threshold read (임계값 판독)` for the reused baseline family on `Tier B` rows

## Related Docs

- `docs/policies/tiered_readiness_exploration.md`
- `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
