# F81C MT5 Runtime Materialization Report(F81C MT5 런타임 물질화 보고서)

Updated(갱신): 2026-06-18T03:54:17Z

- run id(실행 ID): `frontier81C_mt5_runtime_materialization_v1`
- parent run(부모 실행): `frontier81B_mt5_native_order_intent_cost_shape_proxy_scout_v1`
- target(대상): `f81b_01107` / `extra_trees_d6_l160`
- status(상태): `completed_mt5_runtime_materialization_observation_no_authority`
- judgment(판정): `runtime_materialization_completed_gap_attribution_required_no_authority`
- attempt count(시도 수): `2`
- completed attempt count(완료 시도 수): `2`
- claim boundary(주장 경계): `runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F81B(전선81B)의 materialization target(물질화 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 거부 테이프), Strategy Tester attempt(전략 테스터 시도)로 물질화하고 실행을 시도했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)을 같은 후보 표면으로 연결했지만, 결과는 runtime materialization observation(런타임 물질화 관찰)만 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `3`
- signal parity rows(신호 동등성 행): `3`
- feature readiness rows(피처 준비 행): `1`
- source reproduction rows(원천 재현 행): `2`
- best runtime(최선 런타임): `{'run_id': 'frontier81C_mt5_runtime_materialization_v1', 'attempt_name': 'f81c_runtime_materialization_oos', 'candidate_id': 'f81c_runtime_f81b_01107', 'axis_id': 'long_h14_tp18.0_sl8.0_price_vol_session_extra_trees_d6_l160_trend_liquidity_release_q0.72', 'split': 'oos', 'test_period_start': '2025-10-01', 'test_period_end': '2026-04-14', 'calendar_days_exclusive': 195, 'tester_status': 'completed', 'runtime_status': 'completed', 'report_status': 'completed', 'expected_rows': 7584, 'feature_ready_count': 7584, 'feature_ready_diff': 0, 'expected_signal_count': 670, 'signal_count': 670, 'signal_count_diff': 0, 'expected_selected_trade_count': 670, 'order_attempt_count': 670, 'order_fill_count': 670, 'order_fill_rate': 1.0, 'trade_count': 670, 'trades_per_day': 3.4358974358974357, 'long_trade_count': 670, 'short_trade_count': 0, 'winning_trade_count': 170, 'losing_trade_count': 500, 'net_profit': -115.71, 'gross_profit': 318.13, 'gross_loss': -433.84, 'profit_factor': 0.73, 'expectancy': -0.17, 'win_rate_percent': 25.37, 'average_win': 1.8713529411764707, 'average_loss': -0.8676799999999999, 'payoff_ratio': 2.156731676627871, 'recovery_factor': -0.97, 'max_drawdown_amount': 119.43, 'max_drawdown_percent': 23.72, 'proxy_net_profit': 120.89973397988815, 'proxy_profit_factor': 1.396125563144892, 'proxy_trades_per_day': None, 'proxy_dd_percent': 2.050967333359029, 'dd_delta_runtime_minus_proxy': 21.66903266664097, 'gap_cause_summary': 'runtime_economics_gap_after_signal_and_feature_parity', 'report_path': 'C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/02_runs/frontier81C_mt5_runtime_materialization_v1/mt5/reports/Project_Obsidian_Prime_v2_frontier81C_mt5_runtime_materialization_v1_f81c_runtime_materialization_oos.htm', 'telemetry_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier81C_mt5_runtime_materialization/telemetry/f81c_runtime_materialization_oos_telemetry.csv', 'summary_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier81C_mt5_runtime_materialization/telemetry/f81c_runtime_materialization_oos_summary.csv', 'claim_boundary': 'runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
