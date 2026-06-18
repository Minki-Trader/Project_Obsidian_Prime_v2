# F83E Short-Side Density Runtime Materialization Report(F83E 숏 방향 밀도 런타임 물질화 보고서)

Updated(갱신): 2026-06-18T08:26:26Z

- run id(실행 ID): `frontier83E_short_side_density_runtime_materialization_v1`
- parent run(부모 실행): `frontier83D_two_sided_density_expansion_or_rotation_decision_v1`
- target(대상): `f82b_10355` / `extra_trees_d7_l120`
- status(상태): `completed_mt5_short_density_runtime_materialization_observation_no_authority`
- judgment(판정): `f83e_runtime_materialization_completed_gap_attribution_required_no_authority`
- attempt count(시도 수): `2`
- completed attempt count(완료 시도 수): `2`
- claim boundary(주장 경계): `mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F83D selected short density target(F83D 선택 숏 밀도 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 차단 테이프), MT5 Strategy Tester attempt(MT5 전략 테스터 시도)로 물질화했다.

Effect(효과): F83C long-only runtime clue(F83C 롱 전용 런타임 단서)를 short density axis(숏 밀도 축)로 확장해 proxy/runtime gap(프록시/런타임 간극)을 관찰할 준비를 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `3`
- signal parity rows(신호 동등성 행): `3`
- feature readiness rows(피처 준비 행): `1`
- source reproduction rows(원천 재현 행): `2`
- best runtime(최선 런타임): `{'run_id': 'frontier83E_short_side_density_runtime_materialization_v1', 'attempt_name': 'f83e_short_density_runtime_materialization_oos', 'candidate_id': 'f83e_runtime_f82b_10355', 'axis_id': 'short_h18_tp20.0_sl10.0_density_core_extra_trees_d7_l120_all_intent_release_q0.68', 'split': 'oos', 'test_period_start': '2025-10-01', 'test_period_end': '2026-04-14', 'calendar_days_exclusive': 195, 'tester_status': 'completed', 'runtime_status': 'completed', 'report_status': 'completed', 'expected_rows': 7584, 'feature_ready_count': 7584, 'feature_ready_diff': 0, 'expected_signal_count': 1620, 'signal_count': 1620, 'signal_count_diff': 0, 'expected_selected_trade_count': 1620, 'order_attempt_count': 1613, 'order_fill_count': 1612, 'order_fill_rate': 0.9993800371977681, 'trade_count': 1612, 'trades_per_day': 8.266666666666667, 'long_trade_count': 0, 'short_trade_count': 1612, 'winning_trade_count': 537, 'losing_trade_count': 1075, 'net_profit': -37.17, 'gross_profit': 1114.06, 'gross_loss': -1151.23, 'profit_factor': 0.97, 'expectancy': -0.02, 'win_rate_percent': 33.31, 'average_win': 2.0745996275605214, 'average_loss': -1.0709116279069768, 'payoff_ratio': 1.9372276605261853, 'recovery_factor': -0.36, 'max_drawdown_amount': 103.69, 'max_drawdown_percent': 19.24, 'proxy_net_profit': 401.02621043351246, 'proxy_profit_factor': 1.4727443088117345, 'proxy_trades_per_day': None, 'proxy_dd_percent': 4.6767732618809985, 'dd_delta_runtime_minus_proxy': 14.563226738118999, 'gap_cause_summary': 'order_fill_gap_after_signal_parity', 'report_path': 'C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83E_short_side_density_runtime_materialization_v1/mt5/reports/Project_Obsidian_Prime_v2_frontier83E_short_side_density_runtime_materialization_v1_f83e_short_density_runtime_materialization_oos.htm', 'telemetry_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier83E_short_density_runtime_materialization/telemetry/f83e_short_density_runtime_materialization_oos_telemetry.csv', 'summary_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier83E_short_density_runtime_materialization/telemetry/f83e_short_density_runtime_materialization_oos_summary.csv', 'claim_boundary': 'mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`

## Runtime Closeout KPI(런타임 마감 핵심 지표)

- `validation`: net(순손익) `-285.66`, gross profit/loss(총이익/총손실) `1394.4`/`-1680.06`, PF(수익 팩터) `0.83`, DD(손실폭) `58.86%`, trades/day(일 거래 수) `8.213235294117647`, win rate(승률) `30.04%`, avg win/loss(평균 이익/손실) `2.078092399403875`/`-1.07489443378119`, payoff(손익비) `1.9332990609075014`, expectancy(기대값) `-0.13`, recovery(회복 계수) `-0.97`, long/short(롱/숏) `0`/`2234`.
- `oos`: net(순손익) `-37.17`, gross profit/loss(총이익/총손실) `1114.06`/`-1151.23`, PF(수익 팩터) `0.97`, DD(손실폭) `19.24%`, trades/day(일 거래 수) `8.266666666666667`, win rate(승률) `33.31%`, avg win/loss(평균 이익/손실) `2.0745996275605214`/`-1.0709116279069768`, payoff(손익비) `1.9372276605261853`, expectancy(기대값) `-0.02`, recovery(회복 계수) `-0.36`, long/short(롱/숏) `0`/`1612`.

Unavailable fields(미확보 항목): time under water(회복 전 체류 시간) and max consecutive loss(최대 연속 손실)은 현재 MT5 normalized receipt(정규화 영수증)에 없다.

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
