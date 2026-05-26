# Run335N Branch-Specific Runtime Metric Materialization(335N 분기별 런타임 지표 물질화)

- run_id(실행 ID): `run335N_materialize_branch_specific_runtime_metric_extractors_v1`
- parent_run_id(부모 실행 ID): `run335M_branch_specific_runtime_metric_extraction_design_v1`
- status(상태): `completed_branch_specific_runtime_metric_materialization_no_forward_decision`
- decision(판정): `stage335N_structured_runtime_metric_materialized_no_selection`
- trade_rows(거래 행): `1347`
- branch_metric_rows(분기 지표 행): `270`
- cost_stress_rows(비용 압박 행): `330`
- regime_slice_rows(국면 조각 행): `4433`
- parser_mismatches(파서 불일치): `0`
- best_net_attempt(최고 순수익 시도): `m48_plain_rf`
- worst_pocket_attempt(최악 포켓 시도): `m48_bal_rf`
- next_action(다음 행동): `run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1`

## Judgment(판정)

run335N(335N 실행)은 run335K(335K 실행)의 MT5 Strategy Tester report(MT5 전략 테스터 보고서)를 trade ledger(거래 장부)로 구조화했다.

Effect(효과): run335L(335L 실행)에서 문제였던 repeated aggregate proxy(반복 집계 프록시) 대신, 실제 MT5 trade/deal list(거래/딜 목록)에서 net/PF/DD/trades per day/curve pocket/underwater/cost stress/regime slice(순수익/수익 팩터/손실/일 거래수/곡선 포켓/수중 구간/비용 압박/국면 조각)를 뽑았다.

## Evidence(근거)

- runtime_trade_ledger(런타임 거래 장부): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/runtime_trade_ledger.csv`
- parser_reconciliation(파서 대조): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/mt5_trade_parser_reconciliation.csv`
- trade_telemetry_join_audit(거래-기록 연결 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/trade_telemetry_join_audit.csv`
- branch_runtime_metric_matrix(분기 런타임 지표 행렬): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/branch_runtime_metric_matrix.csv`
- cost_stress_metric_matrix(비용 압박 지표 행렬): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/cost_stress_metric_matrix.csv`
- curve_pocket_underwater_matrix(곡선 포켓/수중 구간 행렬): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/curve_pocket_underwater_matrix.csv`
- regime_direction_slice_matrix(국면/방향 조각 행렬): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/regime_direction_slice_matrix.csv`
- proxy_difference(프록시 차이): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/protocol_specific_proxy_mt5_difference.csv`
- gate_audit(게이트 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/required_gate_coverage_audit.csv`

## Boundary(경계)

이 실행은 diagnostic runtime materialization(진단용 런타임 물질화)이다. 모델(model, 모델), threshold(임계값), lot(로트), risk logic(위험 로직), feature order(피처 순서), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
