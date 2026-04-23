# Stage 06 First v2 Baseline Seed Review (Stage 06 첫 v2 기준선 시드 리뷰)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- stage: `06_tiered_readiness_exploration`
- baseline_seed_id: `baseline_seed_fpmarkets_v2_tier_b_offline_eval_0001`
- report_id: `report_fpmarkets_v2_tier_b_offline_evaluation_0001`
- model_family_id: `gaussian_nb_3class_tier_a_seed_0001`
- local_spec_ref: `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md@2026-04-22`
- decision_ref: `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md@2026-04-22`

## Boundary Read (경계 판독)
- this pass keeps the current strict `Tier A (엄격 준비)` runtime rule unchanged and still treats `Tier B (부분 준비)` as `offline-only (오프라인 전용)` exploration work
- no `reduced-risk runtime family (축소위험 런타임 계열)`, no `simulated execution (가상 실행)`, and no `operating promotion (운영 승격)` are materialized here
- no legacy `model (모델)`, `threshold (임계값)`, or `calibration (보정)` artifact is inherited in this `v2-native baseline seed (v2 고유 기준선 시드)` pass
- the model is fit on `Tier A (엄격 준비)` train rows only and evaluates `strict_tier_a (엄격 Tier A)` and `tier_b_exploration (Tier B 탐색)` on separate `reporting lanes (보고 레인)`

## Label And Split Rule (라벨 및 분할 규칙)
- train window (학습 구간): `2022-09-01T00:00:00+00:00` -> `2024-12-31T23:55:00+00:00` on `Tier A (엄격 준비)` only
- validation window (검증 구간): `2025-01-01T00:00:00+00:00` -> `2025-08-31T23:55:00+00:00`
- holdout window (보류 평가 구간): `2025-09-01T00:00:00+00:00` -> `2026-04-13T23:55:00+00:00`
- label rule (라벨 규칙): `q33=-0.000350872479`, `q67=0.000404955664`, `x <= q33 -> short; q33 < x < q67 -> flat; x >= q67 -> long`
- imputation policy (대치 규칙): missing features are filled with `Tier A train mean (Tier A 학습 평균)` before inference only

## KPI Summary (핵심 지표 요약)
| split (분할) | lane (레인) | row_count (행 수) | class_balance (클래스 분포) | log_loss (로그 손실) | macro_f1 (매크로 F1) | balanced_accuracy (균형 정확도) | multiclass_brier_score (다중분류 브라이어 점수) | imputed_rows (대치 행 수) | mean_missing_feature_count (평균 누락 특성 수) |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | strict_tier_a | 34695 | short=11450, flat=11795, long=11450 | 3.560762 | 0.339340 | 0.389127 | 1.033700 | 0 | 0.000 |
| validation | strict_tier_a | 10618 | short=3396, flat=3798, long=3424 | 3.199141 | 0.383431 | 0.418289 | 0.919930 | 0 | 0.000 |
| validation | tier_b_exploration | 15866 | short=3618, flat=8919, long=3329 | 2.433661 | 0.346341 | 0.388578 | 0.763493 | 15866 | 8.065 |
| holdout | strict_tier_a | 10144 | short=3130, flat=4096, long=2918 | 2.952236 | 0.381442 | 0.416943 | 0.866039 | 0 | 0.000 |
| holdout | tier_b_exploration | 17978 | short=3458, flat=11470, long=3050 | 1.963620 | 0.336437 | 0.369290 | 0.660165 | 17977 | 8.346 |

## Mixed Aggregate Info-Only (혼합 집계 정보용)
- `validation`: row_count (행 수) `26484`, log_loss (로그 손실) `2.740558`, macro_f1 (매크로 F1) `0.379846`, balanced_accuracy (균형 정확도) `0.412704`, multiclass_brier_score (다중분류 브라이어 점수) `0.826212`
- `holdout`: row_count (행 수) `28122`, log_loss (로그 손실) `2.320228`, macro_f1 (매크로 F1) `0.375181`, balanced_accuracy (균형 정확도) `0.403543`, multiclass_brier_score (다중분류 브라이어 점수) `0.734427`

## Calibration Read (보정 판독)
- `validation` / `strict_tier_a`: `ece=0.412621`, `mean_max_probability=0.843211`, `observed_top_class_accuracy=0.430590`
- `validation` / `tier_b_exploration`: `ece=0.349659`, `mean_max_probability=0.917036`, `observed_top_class_accuracy=0.567377`
- `validation` / `mixed_info_only`: `ece=0.374902`, `mean_max_probability=0.887438`, `observed_top_class_accuracy=0.512536`
- `holdout` / `strict_tier_a`: `ece=0.380169`, `mean_max_probability=0.837089`, `observed_top_class_accuracy=0.456920`
- `holdout` / `tier_b_exploration`: `ece=0.296914`, `mean_max_probability=0.921789`, `observed_top_class_accuracy=0.624875`
- `holdout` / `mixed_info_only`: `ece=0.326945`, `mean_max_probability=0.891237`, `observed_top_class_accuracy=0.564291`

## Notes (메모)
- the first `Tier B offline evaluation report (Tier B 오프라인 평가 보고서)` now exists, but it remains a `stage-local read (단계 로컬 판독)` rather than a `promotion read (승격 판독)`
- the first `calibration read (보정 판독)` is descriptive only; this pass does not fit a new `calibration model (보정 모델)`
- a later packet must still decide whether the next narrow step is a `threshold read (임계값 판독)` or a `calibration fit (보정 적합)` follow-up
