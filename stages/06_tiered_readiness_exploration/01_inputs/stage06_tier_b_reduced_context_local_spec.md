# Stage 06 Tier B Reduced-Context Local Spec (Stage 06 Tier B 축약 문맥 로컬 규격)

## Scope (범위)

- this `local spec (로컬 규격)` defines the first shared `Tier B reduced-context model (Tier B 공용 축약 문맥 모델)` pass for `Stage 06`
- it stays inside the current `offline-only (오프라인 전용)` exploration boundary and does not open `Stage 07 (07단계)` by itself
- it does not change any global `contract (계약)` under `docs/contracts/**`

## Inputs (입력)

- `data/raw/mt5_bars/m5/**` rebuilt through the current `build_feature_frame() (특성 프레임 재구성)` parser identity
- `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_safe_feature_schema_draft_0001.md`
- `stages/06_tiered_readiness_exploration/03_reviews/note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md`
- carry-forward boundary and reporting rules from:
  - `docs/policies/tiered_readiness_exploration.md`
  - `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
  - `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`

## Split And Label Rule (분할 및 라벨 규칙)

- reuse the same `train / validation / holdout (학습 / 검증 / 보류 평가)` windows as `tier_b_offline_eval_0001`
- reuse the same `q33 / q67 (33 / 67 분위수)` label rule fit on `Tier A train (Tier A 학습)` rows only
- only `Tier A (엄격 준비)` rows may enter model fitting
- `Tier B (부분 준비)` rows remain evaluation-only
- `Tier C (스킵 준비)` rows remain excluded

## Feature Rule (피처 규칙)

- first shared active set (첫 공용 활성 세트): use the `42` `keep (유지)` features from `stage06_tier_b_safe_feature_schema_draft_0001.md` only
- deferred macro set (보류 매크로 세트): keep the `6` `conditional (조건부)` `g3_macro_proxy` features out of the first active surface
- dropped context set (제외 문맥 세트): keep the `10` `drop (제외)` `g4_leader_equity` + `g5_breadth_extension` features out of this pass
- no forward-fill (전방 채우기), fabricate path (조작 경로), or relaxed contract semantics are allowed

## Model Rule (모델 규칙)

- model family: first shared `3-class Gaussian Naive Bayes (3분류 가우시안 나이브 베이즈)` reduced-context pass
- implementation dependency surface: `numpy / pandas (넘파이 / 판다스)` only
- output order: `[p_short, p_flat, p_long]`
- fit lane: `strict_tier_a_only_reduced_context_keep42`
- inference-time missing features on evaluation rows use `Tier A train mean fill (Tier A 학습 평균 대치)` on the active `42` features only
- subtype tags (하위유형 태그) remain `reporting-only (보고 전용)`:
  - `b_eq_dark`
  - `b_macro_late`
  - `b_residual_sparse`

## Required Outputs (필수 산출물)

- `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_manifest_fpmarkets_v2_tier_b_reduced_context_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_probability_table_fpmarkets_v2_tier_b_reduced_context_0001.parquet`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_evaluation_summary_fpmarkets_v2_tier_b_reduced_context_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_calibration_read_fpmarkets_v2_tier_b_reduced_context_0001.json`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`

## Reporting Boundary (보고 경계)

- keep `strict_tier_a (엄격 Tier A)` and `tier_b_exploration (Tier B 탐색)` separated across `validation (검증)` and `holdout (보류 평가)` reads
- keep `Tier B subtype tags (Tier B 하위유형 태그)` as `info-only (정보용)` reporting slices only
- compare the reduced-context read against the existing full-feature `tier_b_offline_eval_0001` baseline as `info-only (정보용)` delta lines only

## Not Opened Here (이번 패스에서 열지 않는 것)

- no `threshold sweep (임계값 스윕)`
- no `control search (제어 탐색)`
- no `macro-aware optional schema (매크로 인지 선택 스키마)` follow-up
- no reduced-risk runtime-family claim
- no `simulated execution (가상 실행)`, `MT5 path (MT5 경로)`, or `operating promotion (운영 승격)` claim
