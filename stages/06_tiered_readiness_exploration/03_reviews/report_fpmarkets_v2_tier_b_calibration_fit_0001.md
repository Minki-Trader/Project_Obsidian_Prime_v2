# Stage 06 Tier B Calibration Fit Follow-Up (Stage 06 Tier B 보정 적합 후속)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- stage: `06_tiered_readiness_exploration`
- baseline_seed_id: `baseline_seed_fpmarkets_v2_tier_b_offline_eval_0001`
- followup_pack_id: `followup_pack_fpmarkets_v2_tier_b_0001`
- local_spec_ref: `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_followup_pack_local_spec.md@2026-04-22`

## Boundary Read (경계 판독)
- this pass fits separate `temperature scaling (온도 스케일링)` candidates on `validation (검증)` only and keeps all meaning `offline-only (오프라인 전용)`
- no `runtime family (런타임 계열)`, no `simulated execution (가상 실행)`, and no `MT5 path (MT5 경로)` work is materialized here
- class ordering stays `[p_short, p_flat, p_long]`; temperature scaling changes confidence only, not the class-order contract (계약)

## Candidate Fits (후보 적합)
- `identity_read_only`: `temperature=1.000000`, `fit_split=None`, `fit_lane=None`, `fit_row_count=0`
- `strict_tier_a_temperature_fit`: `temperature=16.000000`, `fit_split=validation`, `fit_lane=strict_tier_a`, `fit_row_count=10618`
- `tier_b_exploration_temperature_fit`: `temperature=7.000000`, `fit_split=validation`, `fit_lane=tier_b_exploration`, `fit_row_count=15866`

## Holdout Read (보류 평가 판독)
- `holdout / strict_tier_a / identity_read_only`: `row_count=10144`, `log_loss=2.952236`, `multiclass_brier_score=0.866039`, `ece=0.380169`, `mean_max_probability=0.837089`, `observed_top_class_accuracy=0.456920`
- `holdout / strict_tier_a / strict_tier_a_temperature_fit`: `row_count=10144`, `log_loss=1.051182`, `multiclass_brier_score=0.633000`, `ece=0.052142`, `mean_max_probability=0.418424`, `observed_top_class_accuracy=0.456920`
- `holdout / tier_b_exploration / identity_read_only`: `row_count=17978`, `log_loss=1.963620`, `multiclass_brier_score=0.660165`, `ece=0.296914`, `mean_max_probability=0.921789`, `observed_top_class_accuracy=0.624875`
- `holdout / tier_b_exploration / strict_tier_a_temperature_fit`: `row_count=17978`, `log_loss=1.004383`, `multiclass_brier_score=0.599967`, `ece=0.211715`, `mean_max_probability=0.413466`, `observed_top_class_accuracy=0.624875`
- `holdout / tier_b_exploration / tier_b_exploration_temperature_fit`: `row_count=17978`, `log_loss=0.937521`, `multiclass_brier_score=0.546947`, `ece=0.106207`, `mean_max_probability=0.519113`, `observed_top_class_accuracy=0.624875`

## Draft Takeaway (초안 해석)
- tier_b_reuse_check: `tier_b_temperature_fit improves holdout log_loss and expected_calibration_error over strict_tier_a_temperature_fit on tier_b_exploration`
- tier_a_calibration_takeaway: `strict_tier_a_temperature_fit improves the strict_tier_a holdout calibration read without changing class prediction order`

## Notes (메모)
- this report is a `follow-up artifact (후속 산출물)` only and does not update the official `selection_status (선정 상태)` or open Stage 07 by itself
- the separate `Tier B calibration fit (Tier B 보정 적합)` now exists, but any later threshold or runtime meaning still needs a separate decision layer (결정 레이어)
