# run337HR Proxy Negative Trade Shape Second-Order Repair Design(프록시 음수 거래 형태 2차 수리 설계)

- run_id(실행 ID): `run337HR_design_proxy_negative_trade_shape_second_order_repair_without_db_v1`
- status(상태): `completed_stage337HR_proxy_negative_trade_shape_second_order_repair_design_no_training_no_selection`
- judgment(판정): `all_proxy_negative_repair_memory_converted_to_second_order_density_calibration_regime_design`
- decision(결정): `stage337HR_open_run337HS_proxy_negative_trade_shape_second_order_repair_inputs`
- next_action(다음 행동): `run337HS_materialize_proxy_negative_trade_shape_second_order_repair_inputs_without_db_v1`

## Evidence(근거)

Action(행동): HQ all-negative proxy(HQ 전부 음수 프록시), HP train/holdout inversion(HP 학습/보류 역전), ONNX parity pass(온엑스 동등성 통과)를 함께 읽었다.
Effect(효과): 부정 결과를 버리지 않고 second-order repair(2차 수리) 조건으로 바꿨다.

- candidate_rows(후보 행): `5`
- positive_proxy_rows(양수 프록시 행): `0`
- best_model(최고 모델): `hp_hn_hm001_density_cost_selectivity_guard`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `-1.8709237180951277`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `0.8566430847055179`
- best_inner_holdout_expectancy(최고 내부 보류 기대값): `-0.0002828304940431032`
- best_inner_holdout_signal_density(최고 내부 보류 신호 밀도): `0.3772455089820359`
- train_holdout_inversion_rows(학습/보류 역전 행): `5/5`
- ONNX parity(온엑스 동등성): `5/5`

## Design(설계)

Action(행동): HR은 flat rescue calibration(무거래 구조 보정), cost-buffer sparse edge(비용 버퍼 희소 엣지), session/regime loss firewall(세션/국면 손실 방화벽), train/holdout inversion brake(학습/보류 역전 제동), multi-KPI release firewall(복수 KPI 릴리스 방화벽)을 만들었다.
Effect(효과): HS가 시점 안전 입력과 가중치를 만들 수 있게 했다.

## Boundary(경계)

No training(학습 없음), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음), no candidate selection(후보 선택 없음), no runtime package(런타임 패키지 없음), no MT5 execution(MT5 실행 없음).

Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `8/8`
- failed_gates(실패 게이트): `none`
