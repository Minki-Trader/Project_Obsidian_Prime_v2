# Run335M Branch-Specific Runtime Metric Extraction Design(335M 분기별 런타임 지표 추출 설계)

- run_id(실행 ID): `run335M_branch_specific_runtime_metric_extraction_design_v1`
- parent_run_id(부모 실행 ID): `run335L_independent_runtime_parity_and_proxy_usability_review_v1`
- status(상태): `completed_branch_specific_runtime_metric_extraction_design_no_forward_decision`
- decision(판정): `stage335M_branch_specific_metric_extraction_contract_ready_no_selection`
- branch_count(분기 수): `11`
- contract_rows(계약 행): `45`
- parser_report_count(파서 보고서 수): `6`
- queue_rows(대기열 행): `9`
- next_action(다음 행동): `run335N_materialize_branch_specific_runtime_metric_extractors_v1`

## Judgment(판정)

run335M(335M 실행)은 run335L(335L 실행)의 핵심 한계인 repeated aggregate proxy(반복 집계 프록시)를 분기별 런타임 지표(runtime metric, 실행 지표) 계약으로 바꿨다.

Effect(효과): 다음 run335N(335N 실행)은 MT5 HTML report(HTML 보고서), telemetry(기록), feature matrix(피처 행렬)를 구조화해서 trade ledger(거래 장부), cost stress(비용 압박), curve pocket(곡선 포켓), underwater stretch(수중 구간), long/short attribution(롱/숏 귀속), regime attribution(국면 귀속)을 실제 분기별 표로 만들 수 있다.

## Evidence(근거)

- metric_schema(지표 구조): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/branch_specific_metric_schema.csv`
- extraction_contract(추출 계약): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/branch_runtime_metric_extraction_contract.csv`
- source_audit(원천 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/metric_source_availability_audit.csv`
- parser_feasibility(파서 가능성): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/mt5_report_parser_feasibility_audit.csv`
- lookahead_rejection(미래정보 편향 거절): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/lookahead_bias_rejection_matrix.csv`
- run335N_queue(335N 대기열): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/run335N_metric_materialization_queue.csv`
- gate_audit(게이트 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/required_gate_coverage_audit.csv`
- result_judgment(결과 판정): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335M/result_judgment.csv`

## Boundary(경계)

이 실행은 설계와 계약이다. 모델(model, 모델), threshold(임계값), lot(로트), risk logic(위험 로직), feature order(피처 순서), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
