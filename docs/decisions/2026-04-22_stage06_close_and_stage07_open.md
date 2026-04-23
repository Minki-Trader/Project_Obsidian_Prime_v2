# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-22_stage06_close_and_stage07_open`
- `reviewed_on`: `2026-04-22`
- `owner`: `codex + user`
- `decision`: `close Stage 06 (Stage 06 종료) as the first exploration-only (탐색 전용) readiness family closure and open Stage 07 (Stage 07 개시) as the first alpha search stage (알파 탐색 단계) with one `Tier A main lane (Tier A 메인 레인)` plus one separate `Tier B offline-only lane (Tier B 별도 오프라인 전용 레인)` without changing the current strict Tier A runtime rule (엄격 Tier A 런타임 규칙)`

## What Was Decided

- adopted:
  - treat the first Stage 06 readiness boundary, scorecard family, v2-native baseline seed, additive follow-up pack, and first shared reduced-context model as sufficient `materialized evidence (물질화 근거)` to stop treating Stage 06 as the active stage
  - open `07_alpha_search` as the next active stage with two bounded lanes:
    - `Tier A main lane (Tier A 메인 레인)`: full contract-surface alpha search home
    - `Tier B separate lane (Tier B 별도 레인)`: keep42 shared reduced-context lane with separate reporting and `offline-only (오프라인 전용)` meaning
  - keep `b_eq_dark`, `b_macro_late`, and `b_residual_sparse` as `info-only (정보용)` subtype tags only
  - keep the current strict `Tier A` runtime rule unchanged while Stage 07 remains an exploration stage rather than an operating promotion read
  - move threshold, exposure, sizing, and coarse control search questions into Stage 07 as downstream alpha-search questions rather than leaving them as Stage 06 ambiguity
- not adopted:
  - any `simulated execution (가상 실행)` authorization
  - any `MT5 path (MT5 경로)` expansion
  - any `operating promotion (운영 승격)`
  - any `Tier B runtime family (Tier B 런타임 계열)` claim
  - any requirement that an optional `macro-aware (매크로 인지)` Tier B variant must exist before Stage 07 can open
  - treating `placeholder monthly weights (임시 월별 가중치)` as sufficient for anything beyond separate offline exploration

## Why

- Stage 06 now has an explicit readiness boundary, separate reporting interface, row-label scorecard, first v2-native baseline family, follow-up pack, and first shared reduced-context model, so the readiness-family question no longer needs the active-stage slot
- the first shared reduced-context read improves the current `Tier B holdout (Tier B 보류 평가)` probabilistic read from `log_loss=1.963620` to `log_loss=1.503578` while preserving separate Tier A and Tier B reporting lanes
- the additive follow-up pack already made the main Stage 07 design pressure explicit: separate calibration improvement exists, positive Tier B proxy slices exist only on low-participation settings, dominant missingness remains concentrated in `g4_leader_equity|g5_breadth_extension`, and placeholder weights remain `offline-only`
- opening Stage 07 now gives those bounded alpha-search questions a durable home without implying runtime safety, MT5 readiness, or operating promotion

## What Remains Open

- the first bounded `Stage 07 alpha-search pack (Stage 07 알파 탐색 팩)` across the `Tier A main lane` and the separate `Tier B` offline lane
- whether a later optional `macro-aware (매크로 인지)` Tier B variant adds enough value after the first keep42 reduced-context alpha-search read exists
- whether the placeholder monthly-weight caveat still forces a real-weight rerun before any later `simulated execution (가상 실행)` or `MT5-path expansion (MT5 경로 확장)`
- whether the separate `Tier B` lane survives the first Stage 07 alpha-search read strongly enough to remain open as a bounded downstream family

## Evidence Used

- `docs/policies/tiered_readiness_exploration.md`
- `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`

## Operational Meaning

- `active_stage changed?`: `yes, from Stage 06 to Stage 07`
- `Stage 06 closed?`: `yes`
- `Stage 07 opened?`: `yes`
- `current strict Tier A runtime rule changed?`: `no`
- `Tier B separate alpha-search lane opened?`: `yes, but offline-only`
- `simulated execution or MT5 path authorized?`: `no`
- `operating promotion claimed?`: `no`
- `artifact_registry.csv update needed?`: `no, because this same-pass sync changes durable stage meaning but adds no new dataset, bundle, runtime, or report identity rows beyond the already-registered Stage 06 artifacts`
- `workspace_state update needed?`: `yes and completed in the same pass so the active-stage truth no longer lags the materialized Stage 06 evidence family`
