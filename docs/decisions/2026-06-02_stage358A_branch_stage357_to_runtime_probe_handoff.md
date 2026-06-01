# Decision(결정): Stage358A Branch(358A 단계 분기)

- date(날짜): `2026-06-02`
- source_stage(원천 단계): `357_high_density_label_pivot__trade_frequency_recovery`
- new_stage(새 단계): `358_runtime_probe_handoff__high_density_label_pivot_mt5_check`
- branch_run(분기 실행): `run358A_branch_stage357_to_runtime_probe_handoff_without_db_v1`
- next_run(다음 실행): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`

Action(행동): Stage357(357단계)이 무거워졌다는 사용자 요청에 따라, high-density label pivot proxy scout(고밀도 라벨 전환 프록시 탐색)는 Stage357(357단계)에 남기고 MT5 package/runtime probe(MT5 패키지/런타임 탐침)는 Stage358(358단계)로 분리했다.

Effect(효과): 다음 작업은 Stage358B(358B 실행)에서 MT5 handoff package(MT5 인계 패키지), runtime parity check(런타임 동등성 점검), proxy-to-MT5 diff attribution(프록시 대 MT5 차이 귀속)에 집중한다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_runtime_probe_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
