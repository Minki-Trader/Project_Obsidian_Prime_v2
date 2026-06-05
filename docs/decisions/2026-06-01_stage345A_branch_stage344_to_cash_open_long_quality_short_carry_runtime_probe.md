# 2026-06-01 Stage345A Branch Decision(345A 단계 분기 결정)

- decision(결정): `stage345A_open_run345B_execute_cash_open_long_quality_short_carry_mt5_probe`
- from(출발): `344_directional_long_quality__supply_surface_probe` / `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- to(도착): `345_cash_open_decomposition__long_quality_short_carry_runtime_probe` / `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- superseded_run(대체된 실행): `run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- reason(이유): Stage344(344단계)가 무거워졌고, 다음 질문은 cash-open MT5 runtime probe(현금장 MT5 런타임 탐침)라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage345(345단계)를 열고 run345B(345B 실행)를 runtime probe packet(런타임 탐침 묶음)으로 둔다.
Effect(효과): run344N package(344N 패키지)는 source truth(원천 진실)로 남고, 실행 근거는 Stage345(345단계)에서 수집한다.

claim_boundary(주장 경계): `state_sync_stage_branch_cash_open_long_quality_short_carry_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
