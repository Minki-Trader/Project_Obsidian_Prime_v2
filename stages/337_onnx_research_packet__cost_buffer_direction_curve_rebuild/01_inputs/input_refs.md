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
