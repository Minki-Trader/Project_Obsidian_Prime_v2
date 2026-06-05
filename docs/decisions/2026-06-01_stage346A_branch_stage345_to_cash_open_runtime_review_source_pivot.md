# 2026-06-01 Stage346A Branch Decision(346A 단계 분기 결정)

- decision(결정): `stage346A_open_run346B_review_cash_open_runtime_probe_source_pivot`
- from(출발): `345_cash_open_decomposition__long_quality_short_carry_runtime_probe` / `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- to(도착): `346_cash_open_runtime_review__asymmetric_source_pivot` / `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- superseded_planned_run(대체된 예정 실행): `run345C_review_cash_open_long_quality_short_carry_mt5_probe_without_db_v1`
- reason(이유): Stage345(345단계)가 MT5 runtime probe(MT5 런타임 탐침) 실행, 결과, 검토 예정까지 안고 있어 무거워졌고, 다음 질문은 review/source pivot(검토/원천 전환)이라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage346(346단계)를 열고 run346B(346B 실행)를 review packet(검토 묶음)으로 둔다.
Effect(효과): run345B runtime evidence(345B 런타임 근거)는 source truth(원천 진실)로 남고, 검토는 새 stage(단계)에서 작게 시작한다.

claim_boundary(주장 경계): `state_sync_stage_branch_unreviewed_cash_open_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
