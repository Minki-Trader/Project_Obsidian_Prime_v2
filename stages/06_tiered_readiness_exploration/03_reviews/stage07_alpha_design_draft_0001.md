# Stage 07 Alpha Design Draft (Stage 07 알파 설계 초안)

## Draft Status (초안 상태)
- this file is a `draft (초안)` only and does not open `Stage 07 (07단계)` by itself
- no `workspace_state (워크스페이스 상태)` or `selection_status (선정 상태)` reflection is performed in this pass

## Inputs Used (사용 입력)
- reviewed_on: `2026-04-22`
- calibration_followup: `report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- control_followup: `report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- robustness_followup: `report_fpmarkets_v2_tier_b_robustness_0001.md`
- weight_followup: `report_fpmarkets_v2_tier_b_weight_verdict_0001.md`

## Draft Lane Proposal (초안 레인 제안)
- `Tier A main lane (Tier A 메인 레인)`: candidate `yes` for Stage 07 alpha search because the strict Tier A line remains the only current runtime-aligned line
- `Tier B separate lane (Tier B 별도 레인)`: candidate `yes`, but `offline-only (오프라인 전용)` and still separate from any MT5-path meaning
- `Tier B MT5 feasibility gate (Tier B MT5 가능성 게이트)`: candidate `hold`, not opened in this pass

## Draft Scoreboard (초안 점수판)
- primary probabilistic metrics: `log_loss (로그 손실)`, `multiclass_brier_score (다중분류 브라이어 점수)`, `expected_calibration_error (기대 보정 오차)`
- stability checks: missing-pattern split, month split, and coarse control sensitivity read
- kill rule candidate: stop a Tier B branch when coarse control configurations stay negative and subgroup drift concentrates too narrowly

## Draft Supporting Read (초안 보조 판독)
- tier_b_reuse_check: `tier_b_temperature_fit improves holdout log_loss and expected_calibration_error over strict_tier_a_temperature_fit on tier_b_exploration`
- holdout_tier_b_control_positive_config_count: `21`
- dominant_holdout_pattern: `g4_leader_equity|g5_breadth_extension`
- offline_screen_sufficient_under_placeholder_weights: `True`

## Draft Guardrails (초안 가드레일)
- keep `strict Tier A runtime rule (엄격 Tier A 실행 규칙)` unchanged until a later explicit exploration read changes it
- do not treat this draft as permission for `simulated execution (가상 실행)` or `MT5 path (MT5 경로)` work
- keep `Tier B (Tier B)` reporting separate from `Tier A (Tier A)` in all later Stage 07 artifacts
