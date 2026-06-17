# F80D MT5 Runtime Probe Quality Report(F80D MT5 런타임 탐침 품질 보고서)

Updated(갱신): 2026-06-17T15:36:49Z

- run id(실행 ID): `frontier80D_mt5_runtime_probe_quality_v1`
- parent run(부모 실행): `frontier80C_wfo_aware_surface_selection_v1`
- target(대상): `f80b_13315` / `extra_trees_d6_l120`
- status(상태): `completed_mt5_runtime_probe_quality_observation_no_authority`
- judgment(판정): `runtime_probe_quality_completed_gap_attribution_required_no_authority`
- attempt count(시도 수): `1`
- completed attempt count(완료 시도 수): `1`
- claim boundary(주장 경계): `runtime_probe_quality_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F80C(전선80C)의 materialization target(물질화 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 거부 테이프), Strategy Tester attempt(전략 테스터 시도)로 물질화하고 실행을 시도했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)을 같은 후보 표면으로 연결했지만, 결과는 runtime probe quality observation(런타임 탐침 품질 관찰)만 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `3`
- signal parity rows(신호 동등성 행): `3`
- feature readiness rows(피처 준비 행): `1`
- source reproduction rows(원천 재현 행): `2`
- best runtime(최선 런타임): `{'run_id': 'frontier80D_mt5_runtime_probe_quality_v1', 'attempt_name': 'f80d_runtime_probe_quality_validation', 'candidate_id': 'f80d_runtime_f80b_13315', 'axis_id': 'long_h18_tp22.0_sl11.0_micro_reversal_extra_trees_d6_l120_chop_liquidity_release_q0.7', 'split': 'validation', 'test_period_start': '2025-01-02', 'test_period_end': '2025-10-01', 'calendar_days_exclusive': 272, 'tester_status': 'completed', 'runtime_status': 'completed', 'report_status': 'completed', 'expected_rows': 9844, 'feature_ready_count': 9844, 'feature_ready_diff': 0, 'expected_signal_count': 396, 'signal_count': 396, 'signal_count_diff': 0, 'expected_selected_trade_count': 396, 'order_attempt_count': 394, 'order_fill_count': 394, 'order_fill_rate': 1.0, 'trade_count': 394, 'trades_per_day': 1.4485294117647058, 'long_trade_count': 394, 'short_trade_count': 0, 'winning_trade_count': 129, 'losing_trade_count': 265, 'net_profit': -14.61, 'gross_profit': 296.77, 'gross_loss': -311.38, 'profit_factor': 0.95, 'expectancy': -0.04, 'win_rate_percent': 32.74, 'average_win': 2.3005426356589145, 'average_loss': -1.1750188679245284, 'payoff_ratio': 1.9578771868765248, 'recovery_factor': -0.48, 'max_drawdown_amount': 30.75, 'max_drawdown_percent': 6.09, 'proxy_net_profit': 89.72893373785989, 'proxy_profit_factor': 1.3786494266857832, 'proxy_trades_per_day': None, 'proxy_dd_percent': 4.056337901607913, 'dd_delta_runtime_minus_proxy': 2.033662098392087, 'gap_cause_summary': 'runtime_economics_gap_after_signal_and_feature_parity', 'report_path': 'C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/02_runs/frontier80D_mt5_runtime_probe_quality_v1/mt5/reports/Project_Obsidian_Prime_v2_frontier80D_mt5_runtime_probe_quality_v1_f80d_runtime_probe_quality_validation.htm', 'telemetry_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier80D_mt5_runtime_probe_quality/telemetry/f80d_runtime_probe_quality_validation_telemetry.csv', 'summary_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier80D_mt5_runtime_probe_quality/telemetry/f80d_runtime_probe_quality_validation_summary.csv', 'claim_boundary': 'runtime_probe_quality_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
