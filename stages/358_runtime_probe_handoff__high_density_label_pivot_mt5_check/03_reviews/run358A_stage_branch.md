# run358A Stage Branch(run358A 단계 분기)

- run_id(실행 ID): `run358A_branch_stage357_to_runtime_probe_handoff_without_db_v1`
- source_stage_id(원천 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- parent_run_id(부모 실행 ID): `run357B_design_high_density_label_pivot_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run357C_package_high_density_label_pivot_mt5_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- status(상태): `completed_stage358A_user_requested_stage_split_runtime_probe_handoff_opened_no_selection`
- judgment(판정): `stage_branch_completed_stage357_proxy_queue_split_to_stage358_runtime_probe_handoff_no_operating_claim`
- decision(결정): `stage358A_open_run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- gates(게이트): `7/7`

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage357(357단계)의 MT5 package/probe(MT5 패키지/탐침) 다음 질문을 Stage358(358단계)로 넘겼다.

Effect(효과): Stage357(357단계)은 high-density label pivot proxy scout(고밀도 라벨 전환 프록시 탐색)와 MT5 probe queue(MT5 탐침 대기열)까지만 보존하고, runtime verification(런타임 검증)은 Stage358B(358B 실행)에서 가볍게 시작한다.

Current Truth(현재 진실): Stage357B(357B 실행)는 trained_models(학습 모델) `12`, ONNX parity(온엑스 동등성) `12/12`, threshold_sweep_rows(임계값 스윕 행) `6912`, mt5_probe_queue_rows(MT5 탐침 대기열 행) `8`을 남겼다.

Best Proxy Clue(최선 프록시 단서): best_model_id(최선 모델 ID)는 `run357B_d04_h12_q45_55_high_density_band__extratrees_cls_depth5_leaf100_seed11`이고, validation trade/day(검증 일별 거래수)는 `3.191256830601093`, validation PF(검증 수익 팩터)는 `1.0468369083281632`, OOS trade/day(표본외 일별 거래수)는 `3.4427480916030535`, OOS PF(표본외 수익 팩터)는 `1.0837603236717956`이다.

Lineage(계보): source_inputs(원천 입력)는 Stage357B final decision(최종 결정), MT5 probe candidate queue(MT5 탐침 후보 대기열), ONNX parity matrix(온엑스 동등성 행렬), Stage357B report(보고서)다. producer(생산자)는 Codex stage split(코덱스 단계 분기) 작업이고, consumer(소비자)는 `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`이다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_runtime_probe_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
