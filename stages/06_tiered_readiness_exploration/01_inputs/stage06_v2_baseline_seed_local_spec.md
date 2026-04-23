# Stage 06 v2 Baseline Seed Local Spec

## Scope (범위)

- this `local spec (로컬 규격)` defines the first `v2-native baseline seed (v2 고유 기준선 시드)` for `Stage 06`
- it does not change any global `contract (계약)` under `docs/contracts/**`
- it stays `offline-only (오프라인 전용)` and does not open `simulated execution (가상 실행)`, `MT5 path (MT5 경로)`, or `operating promotion (운영 승격)`

## Inputs (입력)

- `data/raw/mt5_bars/m5/**` rebuilt through the current `build_feature_frame() (특성 프레임 재구성)` parser identity because `features.parquet (특성 파케이)` excludes `Tier B (부분 준비)` rows
- `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- carry-forward boundary and reporting rules from:
  - `docs/policies/tiered_readiness_exploration.md`
  - `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
  - `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`

## Split Rule (분할 규칙)

- `train (학습)`: `2022-09-01` through `2024-12-31` inclusive
- `validation (검증)`: `2025-01-01` through `2025-08-31` inclusive
- `holdout (보류 평가)`: `2025-09-01` through `2026-04-13` inclusive
- only `Tier A (엄격 준비)` rows may enter model fitting
- `Tier B (부분 준비)` rows are evaluation-only
- `Tier C (스킵 준비)` rows remain excluded

## Label Rule (라벨 규칙)

- target: `future_log_return_1 (다음 1개 확정봉 로그수익률)`
- fit `q33/q67 quantile (33/67 분위수)` on `Tier A train (Tier A 학습)` rows only
- apply:
  - `x <= q33 -> short`
  - `q33 < x < q67 -> flat`
  - `x >= q67 -> long`
- the last row with missing future return remains excluded

## Model Rule (모델 규칙)

- model family: first `3-class Gaussian Naive Bayes (3분류 가우시안 나이브 베이즈)`
- implementation dependency surface: `numpy/pandas (넘파이/판다스)` only
- output order: `[p_short, p_flat, p_long]`
- fit lane: `strict_tier_a_only`
- inference-time missing features on evaluation rows use `Tier A train mean fill (Tier A 학습 평균 대치)` only
- this pass records a `calibration read (보정 판독)` only and does not fit a separate `calibration model (보정 모델)`

## Required Outputs (필수 산출물)

- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_seed_manifest_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_probability_table_fpmarkets_v2_tier_b_offline_eval_0001.parquet`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_calibration_read_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`

## Reporting Boundary (보고 경계)

- separate `strict_tier_a (엄격 Tier A)` and `tier_b_exploration (Tier B 탐색)` on distinct `reporting lanes (보고 레인)`
- keep any `mixed aggregate (혼합 집계)` as `info-only (정보용)` only
- minimum lane metrics:
  - `row_count (행 수)`
  - `class_balance (클래스 분포)`
  - `log_loss (로그 손실)`
  - `macro_f1 (매크로 F1)`
  - `balanced_accuracy (균형 정확도)`
  - `multiclass_brier_score (다중분류 브라이어 점수)`

## Not Opened Here (이번 패스에서 열지 않는 것)

- no legacy `model (모델)` or `bundle (번들)` inheritance
- no `threshold sweep (임계값 스윕)`
- no `calibration fit (보정 적합)`
- no runtime-family claim
- no promotion claim
