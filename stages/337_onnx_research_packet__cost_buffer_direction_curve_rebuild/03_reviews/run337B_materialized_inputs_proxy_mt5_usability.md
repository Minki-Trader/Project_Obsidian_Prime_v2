# run337B Materialized Inputs and Proxy-MT5 Usability(337B 입력 물질화 및 프록시-MT5 활용성)

- run_id(실행 ID): `run337B_materialize_cost_direction_curve_rebuild_inputs_v1`
- status(상태): `completed_cost_direction_curve_rebuild_inputs_materialized_no_selection`
- judgment(판정): `stage337B_proxy_mt5_signal_usability_context_only_inputs_ready_no_selection`
- decision(결정): `stage337B_materialized_inputs_ready_proxy_mt5_context_only_no_selection`
- parent_run(부모 실행): `run337A_design_cost_buffer_direction_curve_rebuild_packet_v1`
- next_action(다음 행동): `run337C_review_materialized_inputs_and_proxy_mt5_usability_v1`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Proxy-MT5 Read(프록시-MT5 판독)

- proxy_expected_rows(프록시 예상 행): `20`
- mt5_observed_rows(MT5 관측 행): `20`
- compared_subjects(비교 대상): `4`
- matched_signal_subjects(신호 일치 대상): `4`
- usability(활용성): repaired subset(수리 부분집합) `4`개는 signal sanity only(신호 점검 전용), core56(핵심56)은 refresh and MT5 probe required(갱신 및 MT5 탐침 필요)

## Materialized Inputs(물질화 입력)

- source_lineage(원천 계보): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/source_lineage_index.csv`
- data_integrity_contract(데이터 무결성 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/data_integrity_contract.csv`
- branch_payloads(분기 패키지): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/branch_payload_index.csv`
- gate_schema(게이트 스키마): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/gate_schema_per_branch.csv`
- proxy_mt5_difference(프록시-MT5 차이): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/proxy_mt5_difference_report.csv`
- usability_decision(활용성 결정): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/proxy_mt5_usability_decision.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337B/run337C_review_queue.csv`

Effect(효과): proxy expected value(프록시 예상값)는 MT5 runtime value(MT5 런타임 값)와 timestamp-aligned(타임스탬프 정렬)로 맞는지 확인한 뒤에만 signal sanity check(신호 점검)로 쓴다. 수익/PF/DD(순익/수익 팩터/낙폭) 권한은 MT5 report/telemetry(보고서/실행 기록)와 cost/direction/curve gate(비용/방향/곡선 게이트)에 남긴다.
