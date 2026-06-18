# F89B Deal-Path Teacher Proxy Scout(F89B 딜 경로 교사 프록시 탐색)

Updated(갱신): 2026-06-18T23:41:47Z

Conclusion(결론): F89B is inconclusive/negative for materialization(F89B는 물질화 후보 관점에서 불충분/부정이다).

Action(행동): F88C deals(F88C 딜)을 episode table(에피소드 표)로 묶고 entry feature join(진입 피처 조인)을 수행한 뒤 adverse-selection proxy(역선택 프록시)를 학습/점수화했다.

Effect(효과): runtime deal output(런타임 딜 출력)을 teacher signal(교사 신호)로 바꾸는 경로는 기록됐지만, sample size(표본 수)와 Tier B fallback absence(Tier B 대체 부재) 때문에 MT5 materialization candidate(MT5 물질화 후보)로 올리지 않는다.

Proxy KPI(프록시 핵심 성과 지표): episodes(에피소드) `23`, joined_rows(조인 행) `23`, readout_top20_net_delta(리드아웃 상위20 순변화) `5.450000000000001`, readout_top20_adverse_lift(리드아웃 상위20 역선택 리프트) `0.05555555555555558`.

Runtime KPI(런타임 핵심 성과 지표): not_applicable(해당 없음). No Strategy Tester run(전략 테스터 실행 없음) in F89B because no meaningful materialization candidate(의미 있는 물질화 후보 없음).

Closeout KPI(마감 핵심 성과 지표): gross_profit/loss(총이익/총손실) `74.77000000000001/-110.97`, net_profit(순수익) `-36.20000000000001`, PF(수익 팩터) `0.6737857078489683`, trades(거래 수) `23`, trades_per_day(일 거래 수) `3.2857142857142856`, win_rate(승률) `0.5652173913043478`, avg_win/loss(평균 이익/손실) `5.751538461538463/-11.097`, expectancy(기대값) `-1.5739130434782613`, max_consecutive_loss(최대 연속 손실) `3`, long/short(롱/숏) `14/9`.

Tier records(티어 기록): Tier A used(Tier A 사용) `23` episodes, Tier B fallback used(Tier B 대체 사용) `missing_required`, actual routed total(실제 라우팅 전체) `23` episodes.

Gap cause(간극 원인): `joined deal episode count below predeclared runtime-candidate minimum and no Tier B fallback deal surface`.

Next action(다음 행동): `frontier89C_deal_path_teacher_repair_or_rotation_decision_v1` decides repair or rotation(수리 또는 회전 결정).

Gate status(게이트 상태): work_packet_schema_lint=pass, skill_receipt_schema_lint=pass, state_sync_audit=pass, required_gate_coverage_audit=pass.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Claim boundary(주장 경계): `proxy_scout_only_no_strategy_tester_runtime_economics_no_selected_baseline_no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.
