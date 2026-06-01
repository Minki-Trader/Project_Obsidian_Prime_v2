# run362A Stage Branch(run362A 단계 분기)

- run_id(실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- source_stage_id(원천 단계 ID): `361_long_only_cost_buffer__validation_oos_positive_cost_failure`
- parent_run_id(부모 실행 ID): `run361A_design_long_only_cost_buffer_probe_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- status(상태): `completed_stage362A_user_requested_stage_split_long_only_margin_grid_opened_no_selection`
- judgment(판정): `stage_branch_completed_stage361_materialization_queue_split_to_stage362_margin_grid_no_operating_claim`
- decision(결정): `stage362A_open_run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- gates(게이트): `13/13`

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage361B(361B 실행)의 넓은 materialization(구체화)을 Stage362(362단계)의 q05 long-only margin grid(q05 롱 단독 마진 격자)로 나눴다.

Effect(효과): Stage361A(361A 실행)의 35-row margin grid(35행 마진 격자)는 보존되고, regime/label/short/density(국면/라벨/숏/밀도) 갈래는 후속 stage(단계) 후보로 분리된다.

Current Truth(현재 진실): Stage361A(361A 실행)는 validation net before cost(비용 전 검증 순수익) `45.97`, OOS net before cost(비용 전 표본외 순수익) `237.56`, validation +0.30 cost net(검증 +0.30 비용 순수익) `-146.63`, OOS +0.30 cost net(표본외 +0.30 비용 순수익) `95.96`를 기록했다.

Lineage(계보): source_inputs(원천 입력)는 Stage361A final decision(최종 결정), run361B materialization queue(구체화 대기열), margin grid plan(마진 격자 계획), source evidence snapshot(원천 근거 스냅샷), run361A report(보고서)다. producer(생산자)는 `stage_pipelines/stage362/branch_stage361_to_long_only_margin_grid_without_db.py`이고, consumer(소비자)는 `run362B_materialize_q05_long_only_margin_grid_without_db_v1`다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_long_only_margin_grid_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
