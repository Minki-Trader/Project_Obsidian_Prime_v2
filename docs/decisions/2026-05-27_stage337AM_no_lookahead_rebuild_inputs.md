# Decision(결정): Stage337 run337AM No-Lookahead Rebuild Inputs(337AM 미래참조 없는 재구성 입력)

- run_id(실행 ID): `run337AM_no_lookahead_cost_direction_curve_rebuild_input_materialization_v1`
- parent_run_id(부모 실행 ID): `run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait_v1`
- status(상태): `completed_stage337AM_no_lookahead_rebuild_inputs_materialized_no_training_no_selection`
- decision(결정): `stage337AM_open_run337AN_broker_rollover_reprobe_and_run337AO_asof_instrumentation_no_selection`
- next_action(다음 행동): `run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1`
- secondary_next_action(보조 다음 행동): `run337AO_asof_regime_and_db_source_materialization_v1`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

run337AM(337AM 실행)은 failure memory(실패 기억)를 selector(선택자)가 아니라 predeclared input(사전 선언 입력)으로 바꿨다.

Effect(효과): cost/direction/curve(비용/방향/곡선) 재구성은 계속 진행하지만, look-ahead bias(미래참조 편향), proxy-only KPI(프록시 단독 KPI), completed-day side filter(완성일 방향 필터)를 금지한다.
