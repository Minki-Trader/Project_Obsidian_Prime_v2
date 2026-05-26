# Stage337 Input References(337단계 입력 참조)

- source_stage(원천 단계): `336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild`
- source_closeout_report(원천 종료 보고서): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/03_reviews/run336P_forward_decision_failure_memory_handoff.md`
- forward_decision_matrix(전진 판정 행렬): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336P/stage336_forward_decision_matrix.csv`
- failure_memory_handoff(실패 기억 인계): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336P/stage336_failure_memory_handoff.csv`
- opening_contract(개방 계약): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336P/stage337_opening_contract.csv`
- design_queue(설계 대기열): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336P/run337A_design_queue.csv`
- run336O_scorecard(336O 점수표): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336O/forward_robustness_scorecard.csv`
- run336O_trade_summary(336O 거래 요약): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336O/attempt_forward_attribution_summary.csv`
- run336N_parity_decision(336N 동등성 결정): `stages/336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild/02_runs/run336N/final_timestamp_aligned_parity_decision.json`

Effect(효과): Stage337(337단계)은 run336O(336O 실행)의 나쁜 조각을 직접 필터로 쓰지 않고, 사전 선언된 design constraint(설계 제약)와 negative control(부정 대조)로 바꿔 시작한다.

## run337A Outputs(337A 산출물)

## run337A Outputs(337A 산출물)

- design_constraints(설계 제약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/stage337_design_constraint_matrix.csv`
- branch_design(분기 설계): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/cost_direction_curve_branch_design_matrix.csv`
- gate_contract(게이트 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/cost_direction_curve_gate_contract.csv`
- proxy_mt5_contract(프록시-MT5 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/proxy_expected_vs_mt5_runtime_contract.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337A/run337B_materialization_queue.csv`

Effect(효과): 다음 실행은 proxy(프록시)만 보지 않고 MT5 runtime probe(런타임 탐침)까지 같이 만들어 difference(차이)와 usability(활용성)를 판정한다.

## run337B Outputs(337B 산출물)

## run337B Outputs(337B 산출물)

- source_lineage(원천 계보): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/source_lineage_index.csv`
- proxy_expected(프록시 예상값): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/proxy_expected_signal_values.csv`
- mt5_observed(MT5 관측값): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/mt5_runtime_probe_observed_values.csv`
- difference_report(차이 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/proxy_mt5_difference_report.csv`
- usability_decision(활용성 결정): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/proxy_mt5_usability_decision.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/run337C_review_queue.csv`

Effect(효과): proxy(프록시)는 signal sanity check(신호 점검)로만 쓰고, KPI(핵심 성과 지표) 판정은 MT5 runtime probe(런타임 탐침)와 비용/곡선/방향 게이트에 묶는다.

## run337C Outputs(337C 산출물)

## run337C Outputs(337C 산출물)

- source_lineage_review(원천 계보 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/source_lineage_review.csv`
- data_integrity_review(데이터 무결성 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/data_integrity_review.csv`
- proxy_mt5_review(프록시-MT5 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/proxy_mt5_usability_review.csv`
- branch_acceptance(분기 승인): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/branch_gate_acceptance_matrix.csv`
- rejected_claim_memory(거절 주장 기억): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/rejected_claim_memory.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337C/run337D_research_execution_protocol_queue.csv`

Effect(효과): 다음 실행은 모델 학습 전 no-lookahead(미래참조 방어), proxy-MT5 fresh probe(신규 프록시-MT5 탐침), core56 repair(핵심56 수리), cost/direction/curve gate(비용/방향/곡선 게이트) 계약을 먼저 만든다.

## run337D Outputs(337D 산출물)

## run337D Outputs(337D 산출물)

- no_lookahead_execution_protocol(미래참조 방어 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/no_lookahead_execution_protocol.csv`
- proxy_mt5_fresh_probe_protocol(프록시-MT5 신규 탐침 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/proxy_mt5_fresh_probe_protocol.csv`
- core56_refresh_repair_protocol(핵심56 갱신 수리 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/core56_refresh_repair_protocol.csv`
- cost_direction_curve_gate_protocol(비용/방향/곡선 게이트 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/cost_direction_curve_gate_execution_protocol.csv`
- offense_rebuild_protocol(공격형 재구성 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/offense_rebuild_execution_protocol.csv`
- economic_regime_asof_protocol(경제 국면 시점 기준 절차): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/economic_regime_asof_protocol.csv`
- runtime_probe_requirements(런타임 탐침 요구사항): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/runtime_probe_package_requirements.csv`
- run337E_queue(337E 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337D/run337E_review_execution_protocols_queue.csv`

Effect(효과): 다음 실행은 학습이나 후보 선택이 아니라, 이 절차들이 실제로 과적합 방어와 MT5 근거 요구를 충분히 고정했는지 검토한다.

## run337E Outputs(337E 산출물)

## run337E Outputs(337E 산출물)

- protocol_input_lineage_review(절차 입력 계보 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337E/protocol_input_lineage_review.csv`
- accepted_protocols_for_blueprint_queue(청사진용 승인 절차 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337E/accepted_protocols_for_blueprint_queue.csv`
- repair_protocol_gap_queue(수리 절차 공백 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337E/repair_protocol_gap_queue.csv`
- run337F_blueprint_queue(337F 청사진 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337E/run337F_blueprint_materialization_queue.csv`
- gate_audit(게이트 감사): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337E/required_gate_coverage_audit.csv`

Effect(효과): 다음 실행은 모델 학습이 아니라, 검토 통과한 절차를 실제 실행 청사진과 schema(스키마)로 바꾼다.

## run337F Outputs(337F 산출물)

- blueprint_source_lineage_review(청사진 원천 계보 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/blueprint_source_lineage_review.csv`
- no_lookahead_harness_blueprint(미래참조 방어 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/no_lookahead_harness_blueprint.csv`
- proxy_expected_schema_blueprint(프록시 예상값 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/proxy_expected_schema_blueprint.csv`
- mt5_runtime_probe_package_blueprint(MT5 런타임 탐침 패키지 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/mt5_runtime_probe_package_blueprint.csv`
- core56_repair_blueprint(핵심56 수리 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/core56_repair_blueprint.csv`
- cost_direction_curve_extraction_blueprint(비용/방향/곡선 추출 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/cost_direction_curve_extraction_blueprint.csv`
- offense_branch_blueprint(공격 분기 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/offense_branch_blueprint.csv`
- economic_regime_asof_source_blueprint(경제 국면 시점 기준 원천 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/economic_regime_asof_source_blueprint.csv`
- runtime_probe_package_blueprint(런타임 탐침 패키지 청사진): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/runtime_probe_package_blueprint.csv`
- run337G_queue(337G 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337F/run337G_blueprint_review_queue.csv`

Effect(효과): 다음 실행은 이 청사진들이 실제 materialization package(물질화 패키지)로 넘어가도 되는지 검토한다.

## run337G Outputs(337G 산출물)

- blueprint_review_source_lineage(청사진 검토 원천 계보): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/blueprint_review_source_lineage.csv`
- no_lookahead_harness_blueprint_review(미래참조 방어 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/no_lookahead_harness_blueprint_review.csv`
- proxy_mt5_blueprint_review(프록시-MT5 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/proxy_mt5_blueprint_review.csv`
- core56_repair_blueprint_review(핵심56 수리 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/core56_repair_blueprint_review.csv`
- cost_direction_curve_extraction_blueprint_review(비용/방향/곡선 추출 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/cost_direction_curve_extraction_blueprint_review.csv`
- offense_branch_blueprint_review(공격 분기 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/offense_branch_blueprint_review.csv`
- economic_regime_asof_blueprint_review(경제 국면 시점 기준 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/economic_regime_asof_blueprint_review.csv`
- runtime_probe_package_blueprint_review(런타임 탐침 패키지 청사진 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/runtime_probe_package_blueprint_review.csv`
- accepted_blueprints_for_package_queue(패키지용 승인 청사진 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/accepted_blueprints_for_package_queue.csv`
- run337H_queue(337H 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337G/run337H_package_materialization_queue.csv`

Effect(효과): 다음 실행은 이 검토 결과를 근거로 실제 package spec(패키지 명세)을 만들되, 학습과 MT5 실행은 계속 닫아둔다.

## run337H Outputs(337H 산출물)

- package_source_lineage_review(패키지 원천 계보 검토): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/package_source_lineage_review.csv`
- no_lookahead_canary_harness_package_spec(미래참조 방어 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/no_lookahead_canary_harness_package_spec.csv`
- proxy_mt5_fresh_probe_package_spec(프록시-MT5 신규 탐침 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/proxy_mt5_fresh_probe_package_spec.csv`
- core56_asof_repair_package_spec(핵심56 시점 기준 수리 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/core56_asof_repair_package_spec.csv`
- cost_direction_curve_extraction_package_spec(비용/방향/곡선 추출 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/cost_direction_curve_extraction_package_spec.csv`
- offense_branch_thesis_package_spec(공격 분기 논제 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/offense_branch_thesis_package_spec.csv`
- economic_regime_asof_join_package_spec(경제 국면 시점 기준 조인 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/economic_regime_asof_join_package_spec.csv`
- runtime_probe_package_spec(런타임 탐침 패키지 명세): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/runtime_probe_package_spec.csv`
- package_blocker_matrix(패키지 차단 행렬): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/package_blocker_matrix.csv`
- package_manifest_index(패키지 색인): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/package_manifest_index.csv`
- run337I_queue(337I 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337H/run337I_package_review_queue.csv`

Effect(효과): 다음 실행은 이 패키지 명세들이 실제 runner scaffold(러너 뼈대)로 넘어가도 되는지 검토한다.
