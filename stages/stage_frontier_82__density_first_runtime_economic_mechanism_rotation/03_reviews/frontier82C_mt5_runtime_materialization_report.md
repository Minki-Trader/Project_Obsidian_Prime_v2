# F82C MT5 Runtime Materialization Report(F82C MT5 런타임 물질화 보고서)

Updated(갱신): 2026-06-18T05:50:31Z

- run id(실행 ID): `frontier82C_mt5_runtime_materialization_v1`
- parent run(부모 실행): `frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1`
- target(대상): `f82b_07295` / `extra_trees_d7_l120`
- status(상태): `completed_mt5_runtime_materialization_observation_no_authority`
- judgment(판정): `runtime_materialization_completed_gap_attribution_required_no_authority`
- attempt count(시도 수): `2`
- completed attempt count(완료 시도 수): `2`
- claim boundary(주장 경계): `runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F82B materialization target(F82B 물질화 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 거부 테이프), Strategy Tester attempt(전략 테스터 시도)로 물질화하고 실행을 시도했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)을 같은 후보 표면으로 연결했지만, 결과는 runtime materialization observation(런타임 물질화 관찰)만 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `3`
- signal parity rows(신호 동등성 행): `3`
- feature readiness rows(피처 준비 행): `1`
- source reproduction rows(원천 재현 행): `2`
- best runtime(최선 런타임): `{'run_id': 'frontier82C_mt5_runtime_materialization_v1', 'attempt_name': 'f82c_runtime_materialization_oos', 'candidate_id': 'f82c_runtime_f82b_07295', 'axis_id': 'long_h12_tp15.0_sl9.0_trend_density_extra_trees_d7_l120_all_intent_release_q0.68', 'split': 'oos', 'test_period_start': '2025-10-01', 'test_period_end': '2026-04-14', 'calendar_days_exclusive': 195, 'tester_status': 'completed', 'runtime_status': 'completed', 'report_status': 'completed', 'expected_rows': 7584, 'feature_ready_count': 7584, 'feature_ready_diff': 0, 'expected_signal_count': 1340, 'signal_count': 1340, 'signal_count_diff': 0, 'expected_selected_trade_count': 1340, 'order_attempt_count': 1339, 'order_fill_count': 1338, 'order_fill_rate': 0.9992531740104555, 'trade_count': 1338, 'trades_per_day': 6.861538461538461, 'long_trade_count': 1338, 'short_trade_count': 0, 'winning_trade_count': 492, 'losing_trade_count': 846, 'net_profit': -55.21, 'gross_profit': 772.43, 'gross_loss': -827.64, 'profit_factor': 0.93, 'expectancy': -0.04, 'win_rate_percent': 36.77, 'average_win': 1.5699796747967478, 'average_loss': -0.9782978723404255, 'payoff_ratio': 1.6048074100793204, 'recovery_factor': -0.52, 'max_drawdown_amount': 105.43, 'max_drawdown_percent': 20.36, 'proxy_net_profit': 190.97504260071986, 'proxy_profit_factor': 1.312138066226088, 'proxy_trades_per_day': None, 'proxy_dd_percent': 2.4483866090271933, 'dd_delta_runtime_minus_proxy': 17.911613390972807, 'gap_cause_summary': 'order_fill_gap_after_signal_parity', 'report_path': 'C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/02_runs/frontier82C_mt5_runtime_materialization_v1/mt5/reports/Project_Obsidian_Prime_v2_frontier82C_mt5_runtime_materialization_v1_f82c_runtime_materialization_oos.htm', 'telemetry_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier82C_mt5_runtime_materialization/telemetry/f82c_runtime_materialization_oos_telemetry.csv', 'summary_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier82C_mt5_runtime_materialization/telemetry/f82c_runtime_materialization_oos_summary.csv', 'claim_boundary': 'runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
