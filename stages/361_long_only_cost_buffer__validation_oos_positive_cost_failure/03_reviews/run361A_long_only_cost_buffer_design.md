# run361A Long-Only Cost Buffer Design(361A 롱 단독 비용 버퍼 설계)

- run_id(실행 ID): `run361A_design_long_only_cost_buffer_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`
- status(상태): `completed_stage361A_long_only_cost_buffer_design_ready_materialization_required_no_selection_no_mt5`
- judgment(판정): `long_only_cost_buffer_design_ready_materialization_required_no_operating_claim`
- gate_result(게이트 결과): `12/12`
- claim_boundary(주장 경계): `research_development_design_only_long_only_cost_buffer_no_model_training_no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Current Truth(현재 진실)

Action(행동): q05 long-only(롱 단독) seed(씨앗)를 margin/regime/label(마진/국면/라벨) 설계로 확장했다.

Effect(효과): 비용 전 validation(검증) `+45.97` 및 OOS(표본외) `+237.56` 단서를, +0.30 cost buffer(+0.30 비용 버퍼) 회복 문제로 바꿨다.

## Design Output(설계 산출물)

- margin_grid_rows(마진 격자 행): `35`
- broad_sweep_rows(넓은 탐색 행): `5`
- materialization_queue_rows(구체화 대기열 행): `5`
- wfo_plan_rows(WFO 계획 행): `4`

## Guardrails(가드레일)

- density(밀도): `trade_per_day_min_3_to_10_plus_no_trade_splitting`
- side policy(방향 정책): long-only primary(롱 단독 주 경로), short only negative control(숏은 부정 대조 전용)
- cost stress(비용 압박): +0.30 per trade(+0.30/거래)가 primary gate(주 게이트)다.
- claim boundary(주장 경계): design only(설계 전용)이며 proxy/MT5/candidate selection(프록시/MT5/후보 선택)은 없다.

## Next Action(다음 행동)

Action(행동): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`에서 runtime telemetry(런타임 텔레메트리)를 써서 q05 long-only margin grid(q05 롱 단독 마진 격자), regime joins(국면 결합), label inputs(라벨 입력)을 구체화한다.

Effect(효과): 이후 proxy(프록시)를 만들 수 있는지 판단하고, proxy(프록시)가 생기면 MT5 runtime probe(MT5 런타임 탐침)와 비교할 수 있다.
