# Stage 06 First Tier B Reduced-Context Model Review (Stage 06 첫 Tier B 축약 문맥 모델 검토)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- stage: `06_tiered_readiness_exploration`
- reduced_context_id: `reduced_context_model_fpmarkets_v2_tier_b_0001`
- report_id: `report_fpmarkets_v2_tier_b_reduced_context_0001`
- model_family_id: `gaussian_nb_3class_tier_b_reduced_context_keep42_0001`
- local_spec_ref: `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_reduced_context_local_spec.md@2026-04-22`
- schema_ref: `stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_safe_feature_schema_draft_0001.md@2026-04-22`
- anchor_ref: `stages/06_tiered_readiness_exploration/03_reviews/note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md@2026-04-22`

## Boundary Read (경계 판독)
- this pass materializes the first shared `Tier B reduced-context model (Tier B 공용 축약 문맥 모델)` while keeping all meaning `offline-only (오프라인 전용)`
- no `Stage 07 open (Stage 07 개시)`, no `simulated execution (가상 실행)`, no `MT5 path (MT5 경로)`, and no `operating promotion (운영 승격)` meaning is claimed here
- the current `strict Tier A runtime rule (엄격 Tier A 런타임 규칙)` remains unchanged
- the first shared reduced-context active set uses `42` `keep (유지)` features only and keeps all `conditional (조건부)` macro features out of this pass

## Feature Schema (피처 스키마)
- active feature count (활성 피처 수): `42`
- conditional feature count (조건부 피처 수): `6`
- dropped feature count (제외 피처 수): `10`
- deferred macro family (보류 매크로 계열): `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`
- dropped external family (제외 외부 계열): `nvda_xnas_log_return_1, aapl_xnas_log_return_1, msft_xnas_log_return_1, amzn_xnas_log_return_1, mega8_equal_return_1, top3_weighted_return_1, mega8_pos_breadth_1, mega8_dispersion_5, us100_minus_mega8_equal_return_1, us100_minus_top3_weighted_return_1`

## KPI Summary (핵심 지표 요약)
| split (분할) | lane (레인) | row_count (행 수) | class_balance (클래스 분포) | log_loss (로그 손실) | macro_f1 (매크로 F1) | balanced_accuracy (균형 정확도) | multiclass_brier_score (다중분류 브라이어 점수) | imputed_rows (대치 행 수) | mean_missing_feature_count (평균 누락 피처 수) |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | strict_tier_a | 34695 | short=11450, flat=11795, long=11450 | 2.336503 | 0.355380 | 0.393067 | 0.927199 | 0 | 0.000 |
| validation | strict_tier_a | 10618 | short=3396, flat=3798, long=3424 | 2.279542 | 0.405939 | 0.424995 | 0.818819 | 0 | 0.000 |
| validation | tier_b_exploration | 15866 | short=3618, flat=8919, long=3329 | 1.840824 | 0.390090 | 0.391556 | 0.727080 | 0 | 0.000 |
| holdout | strict_tier_a | 10144 | short=3130, flat=4096, long=2918 | 2.136729 | 0.421953 | 0.429897 | 0.771317 | 0 | 0.000 |
| holdout | tier_b_exploration | 17978 | short=3458, flat=11470, long=3050 | 1.503578 | 0.372836 | 0.371866 | 0.658588 | 0 | 0.000 |

## Comparison To Full Baseline Seed (전체 기준선 시드 대비 비교)
- `validation` / `strict_tier_a`: `delta_log_loss=-0.919599`, `delta_macro_f1=0.022508`, `delta_balanced_accuracy=0.006706`, `delta_brier=-0.101110`
- `validation` / `tier_b_exploration`: `delta_log_loss=-0.592837`, `delta_macro_f1=0.043750`, `delta_balanced_accuracy=0.002978`, `delta_brier=-0.036413`
- `holdout` / `strict_tier_a`: `delta_log_loss=-0.815506`, `delta_macro_f1=0.040512`, `delta_balanced_accuracy=0.012954`, `delta_brier=-0.094721`
- `holdout` / `tier_b_exploration`: `delta_log_loss=-0.460042`, `delta_macro_f1=0.036399`, `delta_balanced_accuracy=0.002576`, `delta_brier=-0.001578`

## Tier B Subtype Info-Only (Tier B 하위유형 정보용)
- `validation` / `b_eq_dark`: `row_count=13710`, `row_share_within_tier_b=0.864112`, `log_loss=1.819234`, `macro_f1=0.394987`, `balanced_accuracy=0.394863`
- `validation` / `b_macro_late`: `row_count=2156`, `row_share_within_tier_b=0.135888`, `log_loss=1.978116`, `macro_f1=0.307669`, `balanced_accuracy=0.358649`
- `holdout` / `b_eq_dark`: `row_count=16278`, `row_share_within_tier_b=0.905440`, `log_loss=1.480760`, `macro_f1=0.374008`, `balanced_accuracy=0.372453`
- `holdout` / `b_macro_late`: `row_count=1699`, `row_share_within_tier_b=0.094504`, `log_loss=1.722690`, `macro_f1=0.351804`, `balanced_accuracy=0.373819`
- `holdout` / `b_residual_sparse`: `row_count=1`, `row_share_within_tier_b=0.000056`, `log_loss=0.675853`, `macro_f1=0.333333`, `balanced_accuracy=0.333333`

## Calibration Read (보정 판독)
- `validation` / `strict_tier_a`: `ece=0.314469`, `mean_max_probability=0.750144`, `observed_top_class_accuracy=0.435675`
- `validation` / `tier_b_exploration`: `ece=0.248552`, `mean_max_probability=0.762229`, `observed_top_class_accuracy=0.513677`
- `validation` / `mixed_info_only`: `ece=0.274979`, `mean_max_probability=0.757384`, `observed_top_class_accuracy=0.482404`
- `holdout` / `strict_tier_a`: `ece=0.281826`, `mean_max_probability=0.739732`, `observed_top_class_accuracy=0.457906`
- `holdout` / `tier_b_exploration`: `ece=0.196830`, `mean_max_probability=0.739549`, `observed_top_class_accuracy=0.542719`
- `holdout` / `mixed_info_only`: `ece=0.227490`, `mean_max_probability=0.739615`, `observed_top_class_accuracy=0.512126`

## Notes (메모)
- this report is a `Stage 06 local read (Stage 06 로컬 판독)` only and does not update `workspace_state.yaml`, `current_working_state.md`, or the active `selection_status.md` by itself
- the first shared reduced-context model answers whether the `keep=42` feature surface is worth carrying forward before any optional `macro-aware (매크로 인지)` variant is opened
- any later threshold policy, control search, simulated execution, or `MT5` feasibility read still needs a separate explicit decision layer
