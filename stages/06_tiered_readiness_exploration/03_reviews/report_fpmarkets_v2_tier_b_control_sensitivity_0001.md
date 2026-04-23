# Stage 06 Tier B Control Sensitivity Read (Stage 06 Tier B 제어 민감도 판독)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- followup_pack_id: `followup_pack_fpmarkets_v2_tier_b_0001`
- probability_source: `lane_specific_temperature_fit`

## Boundary Read (경계 판독)
- this pass runs a coarse `threshold / exposure / sizing (임계값 / 노출 / 사이징)` grid as an `offline proxy (오프라인 프록시)` only
- no `best alpha setting (최적 알파 설정)` is claimed; this report only asks whether the current seed is directionally fragile or stable under conservative controls

## Grid (탐색 격자)
- entry_threshold (진입 임계값): `[0.35, 0.4, 0.45, 0.5, 0.55]`
- exposure_cap (노출 상한): `[0.25, 0.5, 0.75]`
- risk_size_multiplier (위험 사이징 배수): `[0.5, 0.75, 1.0]`

## Holdout Best Proxy Configs (보류 평가 최고 프록시 구성)
- `strict_tier_a`: `{"entry_threshold": 0.55, "exposure_cap": 0.25, "risk_size_multiplier": 0.5, "active_rows": 121, "participation_rate": 0.011928233438485805, "mean_abs_exposure": 0.0014910291798107256, "proxy_log_return_sum": -0.0015543897200844172, "proxy_return_pct": -0.0015531822820742391, "proxy_mean_log_return": -1.5323242508718625e-07, "active_mean_log_return": -1.2846196033755516e-05, "active_hit_rate": 0.47107438016528924, "proxy_max_drawdown": 0.0024375924635237746}`
- `tier_b_exploration`: `{"entry_threshold": 0.55, "exposure_cap": 0.75, "risk_size_multiplier": 1.0, "active_rows": 139, "participation_rate": 0.0077316720436088554, "mean_abs_exposure": 0.004696608900918374, "proxy_log_return_sum": 0.007715484041552114, "proxy_return_pct": 0.007745325085212196, "proxy_mean_log_return": 4.291625342948111e-07, "active_mean_log_return": 5.5507079435626705e-05, "active_hit_rate": 0.5467625899280576, "proxy_max_drawdown": 0.008519998200333875}`

## Draft Takeaway (초안 해석)
- holdout / strict_tier_a: `no positive offline proxy control configuration appeared on this slice`
- holdout / tier_b_exploration: `positive offline proxy control configurations appeared, but only on sparse low-participation slices`
- the coarse control grid does not replace a later `threshold policy (임계값 정책)` or `risk policy (위험 정책)` decision

## Notes (메모)
- the proxy uses future `log_return_1 (로그수익률 1)` with lane-specific temperature-scaled probabilities and should not be read as a runtime PnL claim (손익 주장)
- a later decision pass must still decide whether any Stage 07 control search should open, and if so on which lane (레인)
