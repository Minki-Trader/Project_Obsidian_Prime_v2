# Frontier22 Shock PF Source Lock Spec(전선22 충격 수익 팩터 원천 잠금 명세)

Locks(잠금):
- novelty_delta: shock-anchored cross-family entry states(충격 고정 교차군 진입 상태)
- mandatory_rule_shape: one shock condition plus one non-shock context condition(충격 조건 1개와 비충격 문맥 조건 1개)
- search_cap: family_condition_cap<=8, pair_depth=2, max_candidates<=200(군별 조건 8개 이하, 깊이 2, 후보 200개 이하)
- side_hypothesis: two locked lanes: shock_continuation and shock_fade(고정 2개 방향: 충격 지속과 충격 되돌림)
- exit_proxy: future_log_return_12 minus rough proxy cost only(12봉 미래 수익률에서 거친 비용만 차감)
- f20_duplicate_guard: F20 vix_zscore_20+close_ema50_ratio duplicate cannot be scout clue(F20 중복은 탐색 단서 금지)
- f21_guard: no lifecycle repair in first proxy(F22B 첫 프록시에는 생명주기 수리 금지)

Buckets(버킷):
- shock: `return_zscore_20, log_return_1, return_1_over_atr_14, gap_percent, close_prev_close_ratio`
- volatility: `atr_14_over_atr_50, historical_vol_5_over_20, vix_zscore_20, hl_zscore_50`
- trend_chop: `adx_14, ema20_ema50_diff, ema20_ema50_spread_zscore_50, bb_squeeze`
- session_age: `minutes_from_cash_open, is_first_30m_after_open, is_last_30m_before_cash_close, is_us_cash_open`
- breadth: `mega8_pos_breadth_1, mega8_dispersion_5, us100_minus_mega8_equal_return_1, us100_minus_top3_weighted_return_1`
