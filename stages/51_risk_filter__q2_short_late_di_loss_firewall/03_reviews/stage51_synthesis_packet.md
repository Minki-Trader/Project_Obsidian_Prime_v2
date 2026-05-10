# Stage51 Synthesis Packet(51단계 종합 패킷)

- judgment(판정): `reviewed_completed_positive_q2_loss_firewall_runtime_probe_only`
- reason(이유): `firewall_improved_q2_kept_wfo_and_routed_cost_survival`
- best_tier_a(최상 Tier A): `{'run_id': 'run45A_q2_loss_firewall_broad_mt5_wfo_v1', 'variant_id': 'fw02_block_di_short_mild', 'route_view': 'tier_a_firewall_separate', 'tested_windows': 4, 'positive_windows': 4, 'negative_windows': 0, 'total_net_profit': 364.18, 'q2_net_profit': 56.07, 'worst_window': 'w01_2025q2', 'worst_window_net_profit': 56.07, 'median_profit_factor': 1.395, 'total_trades': 407, 'robustness_status': 'passed'}`
- control(대조군): `{'run_id': 'run45A_q2_loss_firewall_broad_mt5_wfo_v1', 'variant_id': 'fw00_adx_reference', 'route_view': 'tier_a_firewall_separate', 'tested_windows': 4, 'positive_windows': 3, 'negative_windows': 1, 'total_net_profit': 414.75, 'q2_net_profit': -28.05, 'worst_window': 'w01_2025q2', 'worst_window_net_profit': -28.05, 'median_profit_factor': 1.465, 'total_trades': 469, 'robustness_status': 'passed'}`
- routed_for_best(최상 라우팅): `{'run_id': 'run45B_firewall_routed_tier_b_eligibility_mt5_v1', 'variant_id': 'fw02_block_di_short_mild', 'route_view': 'tier_a_primary_tier_b_firewall_fallback_routed_total', 'tested_windows': 4, 'positive_windows': 3, 'negative_windows': 1, 'total_net_profit': 375.92, 'q2_net_profit': 84.63, 'worst_window': 'w03_2025q4', 'worst_window_net_profit': -18.09, 'median_profit_factor': 1.56, 'total_trades': 508, 'robustness_status': 'passed'}`
- cost_05_for_best(최상 비용 0.5): `{'run_id': 'run45C_firewall_cost_overlap_attribution_v1', 'source_label': 'run45A_tier_a_firewall', 'variant_id': 'fw02_block_di_short_mild', 'route_view': 'tier_a_firewall_separate', 'extra_cost_per_trade': 0.5, 'tested_windows': 4, 'positive_windows': 4, 'total_adjusted_net_profit': 160.68, 'worst_window': 'w03_2025q4', 'worst_window_adjusted_net_profit': 10.43, 'cost_status': 'passed'}`
- mt5_attempts(MT5 시도): `64`
- alpha_rows(알파 장부 행): `99`
- boundary(주장 경계): `stage51_q2_loss_firewall_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`
