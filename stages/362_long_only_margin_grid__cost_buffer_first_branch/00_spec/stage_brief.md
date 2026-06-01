# Stage362 Brief(362단계 개요): Long-Only Margin Grid(롱 단독 마진 격자)

- canonical_stage_id(정식 단계 ID): `362_long_only_margin_grid__cost_buffer_first_branch`
- current_run_id(현재 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- source_stage_id(원천 단계 ID): `361_long_only_cost_buffer__validation_oos_positive_cost_failure`
- source_run_id(원천 실행 ID): `run361A_design_long_only_cost_buffer_probe_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_long_only_margin_grid_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Can the q05 long-only probability margin grid(q05 롱 단독 확률 마진 격자) find a cost-buffer surface before adding regime/label complexity(국면/라벨 복잡도 추가 전 비용 버퍼 표면을 찾을 수 있는가)?

## Source Truth(원천 진실)

- validation_net_before_cost(비용 전 검증 순수익): `45.97`
- oos_net_before_cost(비용 전 표본외 순수익): `237.56`
- validation_cost_0_30_net(+0.30 비용 검증 순수익): `-146.63`
- oos_cost_0_30_net(+0.30 비용 표본외 순수익): `95.96`
- source_margin_grid_rows(원천 마진 격자 행): `35`
- source_materialization_queue_rows(원천 구체화 대기열 행): `5`

## Scope(범위)

Action(행동): Stage362(362단계)는 Stage361A(361A 실행)의 `s361B_r01_q05_long_only_margin_grid`만 먼저 구체화한다.

Effect(효과): regime router(국면 라우터), long quality label(롱 품질 라벨), short firewall(숏 방화벽), density control(밀도 대조)을 한 stage(단계)에 몰아넣지 않는다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST362-Q05-LONG-ONLY-MARGIN-GRID`
- hypothesis(가설): q05 long-only(롱 단독)의 probability margin(확률 마진)을 넓게 스코어링하면 +0.30 cost buffer(+0.30 비용 버퍼)를 얻을 수 있는 후보 표면을 먼저 찾을 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): q05 margin gap(마진 차이), p_long floor(p_long 하한), p_flat veto(p_flat 제외), trade density(거래 밀도)
- extreme_sweep(극단 탐색): sparse high-margin(희소 고마진), dense low-margin(고밀도 저마진), no-veto control(무제외 대조)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): margin surface(마진 표면)가 비용 후 양수면 다음 stage(단계)에서 WFO(walk-forward optimization, 워크포워드 최적화)로 재검증한다.
- failure_memory(실패 기억): Stage361A(361A 실행)는 q05 long-only(롱 단독)가 비용 전 양수지만 validation +0.30 cost(검증 +0.30 비용)에서 실패한다고 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## Deferred Branches(보류 갈래)

- `s361B_r02_long_regime_router_inputs`: Stage362B(362B 실행) 뒤 필요할 때 별도 stage(단계)로 분기
- `s361B_r03_long_quality_label_inputs`: margin grid(마진 격자) 단서가 비용 후 양수일 때 label stage(라벨 단계)로 분기
- `s361B_r04_short_firewall_negative_control`: short control(숏 대조)은 negative control(부정 대조) stage(단계)로 분리
- `s361B_r05_density_no_trade_controls`: density/no-trade controls(밀도/무거래 대조)는 score surface(점수 표면) 뒤 검증 stage(단계)로 분리

## run362B Materialization Closeout(362B 구체화 종료)

Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자)를 report-derived open-time probability filter(보고서 파생 진입 시점 확률 필터)로 구체화했다.

Effect(효과): 35개 격자 중 validation/OOS +0.30 cost and density gate(검증/표본외 +0.30 비용 및 밀도 게이트)를 동시에 통과한 행은 `0`개이며, 다음 작업은 `run362C_review_q05_long_only_margin_grid_without_db_v1` 검토다.
