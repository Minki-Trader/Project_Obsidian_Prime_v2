# F84C MT5 Runtime-Realized Winrate Materialization Report(F84C MT5 런타임 실현 승률 물질화 보고서)

Updated(갱신): 2026-06-18T10:08:52Z

- run id(실행 ID): `frontier84C_mt5_runtime_realized_winrate_materialization_v1`
- parent run(부모 실행): `frontier84B_runtime_realized_winrate_proxy_scout_v1`
- target(대상): `f84b_00287` / `extra_trees_d7_l120`
- source best(원천 최선): `f84b_01151` / `histgbm_density_shallow`
- status(상태): `completed_mt5_runtime_realized_winrate_materialization_observation_no_authority`
- judgment(판정): `f84c_runtime_materialization_completed_gap_attribution_required_no_authority`
- attempt count(시도 수): `2`
- completed attempt count(완료 시도 수): `2`
- claim boundary(주장 경계): `mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F84B runtime-realized winrate proxy(런타임 실현 승률 프록시) 후보 중 현재 ONNX runtime path(온엑스 런타임 경로)로 exportable(내보내기 가능)한 첫 materialization candidate(물질화 후보)를 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 차단 테이프), MT5 Strategy Tester attempt(MT5 전략 테스터 시도)로 물질화했다.

Effect(효과): HistGBM best clue(히스토그램 그래디언트 부스팅 최선 단서)는 preserved clue(보존 단서)로 남기고, ExtraTrees/Logistic(엑스트라트리/로지스틱) runtime handoff(런타임 인계) 가능 후보만 실제 MT5 runtime probe(MT5 런타임 탐침)로 관찰한다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `3`
- signal parity rows(신호 동등성 행): `3`
- feature readiness rows(피처 준비 행): `1`
- source reproduction rows(원천 재현 행): `2`
- best runtime(최선 런타임): `{'run_id': 'frontier84C_mt5_runtime_realized_winrate_materialization_v1', 'attempt_name': 'f84c_runtime_realized_winrate_materialization_oos', 'candidate_id': 'f84c_runtime_f84b_00287', 'axis_id': 'long_h10_tp14.0_sl7.0_density_core_extra_trees_d7_l120_high_vol_intent_release_q0.66', 'split': 'oos', 'test_period_start': '2025-10-01', 'test_period_end': '2026-04-14', 'calendar_days_exclusive': 195, 'tester_status': 'completed', 'runtime_status': 'completed', 'report_status': 'completed', 'expected_rows': 7584, 'feature_ready_count': 7584, 'feature_ready_diff': 0, 'expected_signal_count': 1805, 'signal_count': 1805, 'signal_count_diff': 0, 'expected_selected_trade_count': 1805, 'order_attempt_count': 1802, 'order_fill_count': 1801, 'order_fill_rate': 0.9994450610432852, 'trade_count': 1801, 'trades_per_day': 9.235897435897435, 'long_trade_count': 1801, 'short_trade_count': 0, 'winning_trade_count': 556, 'losing_trade_count': 1245, 'net_profit': -133.51, 'gross_profit': 818.96, 'gross_loss': -952.47, 'profit_factor': 0.86, 'expectancy': -0.07, 'win_rate_percent': 30.87, 'average_win': 1.4729496402877698, 'average_loss': -0.7650361445783133, 'payoff_ratio': 1.9253333985934185, 'recovery_factor': -0.88, 'max_drawdown_amount': 151.26, 'max_drawdown_percent': 29.27, 'proxy_net_profit': 288.0970393819249, 'proxy_profit_factor': 1.4246374556585157, 'proxy_trades_per_day': 9.304123711340207, 'proxy_dd_percent': 2.930967158052863, 'dd_delta_runtime_minus_proxy': 26.339032841947137, 'gap_cause_summary': 'order_fill_gap_after_signal_parity', 'report_path': 'C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/mt5/reports/Project_Obsidian_Prime_v2_frontier84C_mt5_runtime_realized_winrate_materialization_v1_f84c_runtime_realized_winrate_materialization_oos.htm', 'telemetry_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier84C_runtime_realized_winrate_materialization/telemetry/f84c_runtime_realized_winrate_materialization_oos_telemetry.csv', 'summary_path': 'C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/Common/Files/Project_Obsidian_Prime_v2/frontier84C_runtime_realized_winrate_materialization/telemetry/f84c_runtime_realized_winrate_materialization_oos_summary.csv', 'claim_boundary': 'mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`

## Runtime Closeout KPI(런타임 마감 핵심 성과 지표)

- `validation`: net(순손익) `-378.76`, gross profit/loss(총이익/총손실) `937.22`/`-1315.98`, PF(수익 팩터) `0.71`, DD(손실폭) `75.89%`, trades/day(일 거래 수) `8.551470588235293`, win rate(승률) `27.43%`, avg win/loss(평균 이익/손실) `1.4689968652037617`/`-0.7796090047393365`, payoff ratio(손익비) `1.884273855578314`, expectancy(기대값) `-0.16`, recovery factor(회복 계수) `-0.99`, long/short(롱/숏) `2326`/`0`.
- `oos`: net(순손익) `-133.51`, gross profit/loss(총이익/총손실) `818.96`/`-952.47`, PF(수익 팩터) `0.86`, DD(손실폭) `29.27%`, trades/day(일 거래 수) `9.235897435897435`, win rate(승률) `30.87%`, avg win/loss(평균 이익/손실) `1.4729496402877698`/`-0.7650361445783133`, payoff ratio(손익비) `1.9253333985934185`, expectancy(기대값) `-0.07`, recovery factor(회복 계수) `-0.88`, long/short(롱/숏) `1801`/`0`.

Unavailable fields(미확보 항목): time under water(회복 전 체류 시간), max consecutive loss(최대 연속 손실)는 현재 normalized runtime receipt(정규화 런타임 영수증)에 없다.

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
