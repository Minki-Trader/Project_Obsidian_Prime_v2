# run44D_cost_spread_sensitivity_v1 Packet(패킷)

- purpose(목적): cost/spread sensitivity(비용/스프레드 민감도)
- reference_cost_1_00(기준 변형 추가 비용 1.00): `{'run_id': 'run44D_cost_spread_sensitivity_v1', 'source_label': 'run44A_tier_a_reference', 'route_view': 'tier_a_separate', 'extra_cost_per_trade': 1.0, 'tested_windows': 4, 'positive_windows': 2, 'total_adjusted_net_profit': -54.25, 'worst_window': 'w01_2025q2', 'worst_window_adjusted_net_profit': -111.05, 'cost_status': 'failed'}`
- cost_model(비용 모델): actual MT5 trades(실제 MT5 거래)에 extra_cost_per_trade(거래당 추가 비용)를 차감한 post-MT5 sensitivity(사후 MT5 민감도)다.
- boundary(주장 경계): `stage50_followup_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`
