# run337HM Proxy Negative Trade Shape Repair Design(run337HM 프록시 음수 거래 형태 수리 설계)

Action(행동): HL/HK training review(HL/HK 학습 검토)의 all-negative proxy memory(전부 음수 프록시 기억)를 HN materialization(HN 물질화) 설계로 바꿨다. Effect(효과): high-density churn(고밀도 과회전), train/holdout gap(학습/보류 간극), side weakness(방향 약점)를 다음 입력 조건으로 연결했다.

## Judgment(판정)

- status(상태): `completed_stage337HM_proxy_negative_trade_shape_repair_design_no_training_no_selection`
- judgment(판정): `all_proxy_negative_generalization_gap_converted_to_density_cost_trade_shape_repair_design`
- decision(결정): `stage337HM_open_run337HN_proxy_negative_trade_shape_repair_inputs`
- next_action(다음 행동): `run337HN_materialize_post_runtime_probe_proxy_negative_trade_shape_repair_inputs_without_db_v1`
- claim_boundary(주장 경계): `research_development_only_stage337HM_proxy_negative_trade_shape_repair_design_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Evidence(근거)

- best_model(최고 모델): `hk_hi_hh003_probability_precision_margin`
- best_holdout_net(최고 보류 순수익): `-1.0452519969367131`
- best_holdout_pf(최고 보류 수익 팩터): `0.9496067213895452`
- best_holdout_density(최고 보류 밀도): `0.8133447390932421`
- train_positive/holdout_positive(학습 양수/보류 양수): `5/5` / `0/5`
- avg_holdout_density(평균 보류 밀도): `0.8190248075278015`
- ONNX parity(ONNX 동등성): `5/5`

## Experiment Design(실험 설계)

- hypothesis(가설): HK failure(HK 실패)는 단순 ONNX parity(온엑스 동등성) 문제가 아니라 high-density weak-edge churn(고밀도 약한 엣지 과회전)과 train/holdout generalization gap(학습/보류 일반화 간극)이다.
- decision_use(결정 용도): HN input materialization(HN 입력 물질화)만 가능하다.
- comparison_baseline(비교 기준): HL all-negative proxy review(HL 전부 음수 프록시 검토).
- controls(대조): threshold tuning(임계값 조정), lot optimization(랏 최적화), runtime package(런타임 패키지), candidate selection(후보 선택)은 없다.
- invalid_conditions(무효 조건): look-ahead bias(미래참조 편향), MT5 KPI leak(MT5 지표 누수), holdout row leak(보류 행 누수), proxy-only promotion(프록시 단독 승격).

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `14/14`
- failed_gates(실패 게이트): `none`

Action(행동): 이 run(실행)은 training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지)를 하지 않았다. Effect(효과): 운영 가능 모델이라는 주장을 만들지 않고 다음 입력 설계만 닫았다.
