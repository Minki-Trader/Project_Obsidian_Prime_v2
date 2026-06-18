# F88C Runtime Substrate Repair Result(F88C 런타임 바탕 수리 결과)

Updated(갱신): 2026-06-18T23:12:47Z

Conclusion(결론): F88C produced a bounded MT5 Strategy Tester runtime probe observation(F88C는 경계 있는 MT5 전략 테스터 런타임 탐침 관찰을 만들었다).

Action(행동): The tester ToDate(테스터 종료일)를 feature span(피처 범위)에 맞춰 `2025.01.09`로 좁히고, embedded report trades(보고서 내장 거래)를 separate trade-list CSV(분리 거래목록 CSV)로 추출했다.

Effect(효과): timestamp coverage gap(타임스탬프 커버리지 간극)과 trade-list identity gap(거래목록 정체성 간극)을 실제 runtime evidence(런타임 근거)로 관찰했다.

KPI(핵심 성과 지표): net_profit(순수익) `-36.2`, PF(수익 팩터) `0.67`, DD(손실폭) `17.16%`, trades(거래 수) `23`, trades_per_calendar_day(달력일당 거래 수) `3.2857`.

Closeout KPI(마감 핵심 성과 지표): gross_profit/loss(총이익/총손실) `74.77/-110.97`, win_rate(승률) `56.52`, avg_win/loss(평균 이익/손실) `5.7515/-11.097`, payoff_ratio(손익비) `0.5183`, expectancy(기대값) `-1.57`, recovery_factor(회복 계수) `-0.39`, max_consecutive_loss(최대 연속 손실) `3`.

Coverage(커버리지): parent skip(부모 스킵) `1250`, current skip(현재 스킵) `1063`, skip_reduced(스킵 감소) `True`.

Trade list(거래목록): `stages/stage_frontier_88__runtime_substrate_first_materialization_probe/02_runs/frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1/trade_lists/f88c_tier_a_validation_is_trades.csv`.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Next action(다음 행동): `frontier89_pending_frontier_extra_due_and_topic_rotation_check_v1` requires frontier_extra_due_check(전선 추가 도래 점검) and frontier_topic_rotation_check(전선 주제 회전 점검) before any formal F89 open(정식 F89 개방).
