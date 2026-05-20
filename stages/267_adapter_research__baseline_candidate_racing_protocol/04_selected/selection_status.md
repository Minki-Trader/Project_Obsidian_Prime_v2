# Stage267 Selection Status(267단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_user_goal`
- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- selected_candidate(선택 후보): `none`
- candidate_pool(후보군): `s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor;s258_short_tight_control`
- source_boundary(원천 경계): `research_candidate_pool_only`
- next_action(다음 행동): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

Stage267(267단계)는 Baseline candidate pool(기준 후보군)을 racing start line(경주 출발선)으로 둘 뿐, operating baseline(운영 기준선)으로 선택하지 않는다.
Effect(효과): 후보군은 감정이나 과거 기록이 아니라 다음 연구에 실제로 도움이 되는지로 유지, 탈락, 갱신된다.
