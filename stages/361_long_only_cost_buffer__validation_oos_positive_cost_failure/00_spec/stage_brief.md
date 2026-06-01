# Stage361 Brief(361단계 개요): Long-Only Cost Buffer(롱 단독 비용 버퍼)

- stage_id(단계 ID): `361_long_only_cost_buffer__validation_oos_positive_cost_failure`
- opened_by_run_id(개설 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- source_stage_id(원천 단계 ID): `360_regime_stability_pivot__oos_long_cash_edge_validation_loss`
- latest_completed_run_id(최근 완료 실행 ID): `run361A_design_long_only_cost_buffer_probe_without_db_v1`
- handoff_run_id(인계 실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- next_stage_id(다음 단계 ID): `362_long_only_margin_grid__cost_buffer_first_branch`
- next_run_id(다음 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_long_only_margin_grid_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Can q05 long-only edge gain +0.30 cost buffer while preserving validation/OOS positivity and 3+ trades/day?(q05 롱 단독 우위가 검증/표본외 양수와 일 3거래 이상을 유지하면서 +0.30 비용 버퍼를 얻을 수 있는가?)

## Source Truth(원천 진실)

Action(행동): Stage360C(360C 실행)는 q05 long-only(롱 단독)를 Stage361(361단계)의 offensive seed(공격 씨앗)로 넘겼다.

Effect(효과): long/cash hard veto(롱/현금장 고정 제외)와 simple no-late veto(단순 후반 제외)에 묶이지 않고, margin/regime/label(마진/국면/라벨) 쪽으로 새 수익 원천을 탐색한다.

## run361A Design Closeout(361A 설계 종료)

Action(행동): long-only cost buffer(롱 단독 비용 버퍼)를 broad margin/regime/label design(넓은 마진/국면/라벨 설계)로 전환했다.

Effect(효과): Stage361(361단계)은 직접 구체화하지 않고 Stage362(362단계)의 margin grid(마진 격자)로 분기한다.

## Stage362A Branch Handoff(362A 분기 인계)

Action(행동): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`을 직접 실행하지 않고 `362_long_only_margin_grid__cost_buffer_first_branch`로 분기했다.

Effect(효과): Stage361(361단계)의 넓은 cost buffer design(비용 버퍼 설계)은 보존하고, Stage362(362단계)는 q05 long-only margin grid(q05 롱 단독 마진 격자) 하나만 구체화한다.
