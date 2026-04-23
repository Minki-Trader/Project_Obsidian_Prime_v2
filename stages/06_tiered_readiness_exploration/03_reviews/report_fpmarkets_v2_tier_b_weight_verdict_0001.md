# Stage 06 Tier B Placeholder Weight Verdict (Stage 06 Tier B 임시 가중치 판정)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- followup_pack_id: `followup_pack_fpmarkets_v2_tier_b_0001`
- weights_version: `foundation/config/top3_monthly_weights_fpmarkets_v2.csv@2026-04-16 (placeholder_equal_weight)`

## Scenario Read (시나리오 판독)
- `equal_placeholder`: weights `{'msft_xnas_weight': 0.3333333333333333, 'nvda_xnas_weight': 0.3333333333333333, 'aapl_xnas_weight': 0.3333333333333333}`, `holdout_tier_b_log_loss=1.963620`, `holdout_tier_b_macro_f1=0.336437`, `holdout_tier_b_brier=0.660165`
- `nvda_tilt_60`: weights `{'msft_xnas_weight': 0.2, 'nvda_xnas_weight': 0.6, 'aapl_xnas_weight': 0.2}`, `holdout_tier_b_log_loss=1.955990`, `holdout_tier_b_macro_f1=0.336803`, `holdout_tier_b_brier=0.659864`
- `msft_tilt_60`: weights `{'msft_xnas_weight': 0.6, 'nvda_xnas_weight': 0.2, 'aapl_xnas_weight': 0.2}`, `holdout_tier_b_log_loss=1.955706`, `holdout_tier_b_macro_f1=0.336491`, `holdout_tier_b_brier=0.658371`
- `aapl_tilt_60`: weights `{'msft_xnas_weight': 0.2, 'nvda_xnas_weight': 0.2, 'aapl_xnas_weight': 0.6}`, `holdout_tier_b_log_loss=1.964346`, `holdout_tier_b_macro_f1=0.336370`, `holdout_tier_b_brier=0.660333`

## Spread Summary (변동 폭 요약)
- tier_b_holdout_log_loss_spread: `0.008640`
- tier_b_holdout_brier_spread: `0.001962`
- tier_b_holdout_macro_f1_spread: `0.000433`

## Draft Verdict (초안 판정)
- offline_screen_sufficient: `True`
- real_weight_rerun_required_before_simulated_or_mt5: `True`
- verdict_text: `placeholder weights look stable enough for Stage 06 offline screening because the coarse tilt scenarios keep Tier B holdout metrics in a narrow band, but a real-weight rerun still remains required before any simulated execution, MT5-path expansion, or operating promotion claim`

## Notes (메모)
- this report does not replace the contract fact that the current monthly weights file is still `placeholder (임시값)`
- the read here is only that coarse offline conclusions do not swing wildly under obvious tilt scenarios (기울기 시나리오)
