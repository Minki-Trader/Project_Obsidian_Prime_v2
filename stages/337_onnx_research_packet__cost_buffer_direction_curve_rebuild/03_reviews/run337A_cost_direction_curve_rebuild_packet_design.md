# run337A Cost Direction Curve Rebuild Packet Design(337A 비용/방향/곡선 재구성 설계)

- run_id(실행 ID): `run337A_design_cost_buffer_direction_curve_rebuild_packet_v1`
- status(상태): `completed_cost_direction_curve_rebuild_packet_design_no_selection`
- judgment(판정): `stage337A_predeclared_cost_direction_curve_proxy_mt5_packet_ready_no_selection`
- decision(결정): `stage337A_cost_direction_curve_rebuild_design_ready_no_selection`
- parent_run(부모 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- next_action(다음 행동): `run337B_materialize_cost_direction_curve_rebuild_inputs_v1`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Evidence Used(사용 근거)

- best_preserved_clue(보존 단서): `m48_plain_rf` score(점수) `12.0`, net(순익) `268.51`, PF(수익 팩터) `1.48140777395`
- cost_failure(비용 실패): cost+1.0 net(비용+1.0 순익) non-positive attempts(비양수 시도) `4/4`
- direction_failure(방향 실패): short-side non-positive(숏 방향 비양수) `3/4`
- curve_failure(곡선 실패): rolling20 worst <= -50(롤링20 최악 -50 이하) `4/4`
- proxy_mt5_boundary(프록시-MT5 경계): run336N(336N 실행) aligned parity evidence(정렬 동등성 근거) available(존재) `True`

## Materialized Design(물질화 설계)

- design constraints(설계 제약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/stage337_design_constraint_matrix.csv`
- branch matrix(분기 행렬): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/cost_direction_curve_branch_design_matrix.csv`
- gate contract(게이트 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/cost_direction_curve_gate_contract.csv`
- proxy-MT5 contract(프록시-MT5 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/proxy_expected_vs_mt5_runtime_contract.csv`
- negative controls(부정 대조): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/no_lookahead_negative_control_matrix.csv`
- run337B queue(337B 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/run337B_materialization_queue.csv`

Effect(효과): Stage337(337단계)은 수익이 좋아 보이는 조각을 바로 고르지 않고, cost buffer(비용 버퍼), direction symmetry(방향 대칭), curve pocket(곡선 포켓), proxy expected value(프록시 예상값), MT5 runtime probe(MT5 런타임 탐침), no-lookahead guard(미래참조 방어)를 다음 실행의 필수 물증으로 고정했다.
