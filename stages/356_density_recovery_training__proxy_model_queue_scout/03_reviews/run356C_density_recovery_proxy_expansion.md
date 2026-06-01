# run356C Density Recovery Proxy Expansion(run356C 밀도 회복 프록시 확장)

- run_id(실행 ID): `run356C_expand_density_recovery_proxy_training_search_without_db_v1`
- parent_run_id(부모 실행 ID): `run356B_train_density_recovery_proxy_models_without_db_v1`
- status(상태): `completed_stage356C_density_recovery_expansion_no_trade_density_edge_no_selection`
- judgment(판정): `negative_proxy_expansion_scout_density_edge_not_recovered_no_operating_claim`
- decision(결정): `stage356C_open_run356D_design_high_density_label_pivot_without_db_v1`
- next_run_id(다음 실행 ID): `run356D_design_high_density_label_pivot_without_db_v1`
- trained_regression_models(학습 회귀 모델): `12`
- onnx_parity_rows(온엑스 동등성 행): `12`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `0`

Action(행동): Stage356B(356B 실행)의 낮은 trade density(거래 밀도) 실패 기억을 바탕으로 raw return regression head(원시 수익률 회귀 헤드), score quantile(점수 분위수), ADX/session filter(ADX/세션 필터), union non-overlap(합집합 비중첩)을 탐색했다.

Effect(효과): trade/day(일별 거래수) 3~10 조건을 trade splitting(거래 쪼개기) 없이 회복할 수 있는지 확인했고, proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.

## Best Expansion Row(최선 확장 행)

- source_type(원천 유형): `union_regression_heads(회귀 헤드 합집합)`
- model_id(모델 ID): `run356C_d02_tb12_path_quality__extratrees_reg_depth5_leaf120+run356C_d01_h6_cost_buffer__extratrees_reg_depth5_leaf120`
- validation_stress_net(검증 압박 순수익): `0.009857477825702315`
- validation_trade_per_day(검증 일별 거래수): `2.4451219512195124`
- oos_stress_net(표본외 압박 순수익): `0.031124279379026655`
- oos_trade_per_day(표본외 일별 거래수): `2.6814159292035398`
- candidate_gate(후보 게이트): `failed_proxy_scout_queue(프록시 탐색 대기열 실패)`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
