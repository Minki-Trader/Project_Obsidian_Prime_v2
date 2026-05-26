# Run335L Independent Runtime Parity/Proxy Usability Review(독립 런타임 동등성/프록시 활용성 검토)

- run_id(실행 ID): `run335L_independent_runtime_parity_and_proxy_usability_review_v1`
- parent_run_id(부모 실행 ID): `run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1`
- status(상태): `completed_independent_runtime_parity_and_proxy_usability_review_no_forward_decision`
- decision(결정): `stage335L_runtime_parity_usable_proxy_numeric_not_branch_specific_no_selection`
- row_level_overlap_rows(행 단위 겹친 행): `30404`
- decision_mismatch_rows(결정 불일치 행): `0`
- feature_only_terminal_flat_rows(피처 전용 말단 관망 행): `2`
- max_probability_abs_diff(최대 확률 절대 차이): `1.4903921813358423e-07`
- diagnostic_usability(진단 활용 가능성): `usable_for_runtime_signal_parity_and_repair_prioritization`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- next_action(다음 행동): `run335M_branch_specific_runtime_metric_extraction_design_v1`

## Judgment(판정)

run335L(335L 실행)는 run335K(335K 실행)의 Python ONNX proxy(파이썬 온엑스 프록시)와 fresh MT5 telemetry(신규 MT5 기록)를 bar_time_server(서버 바 시간) 기준으로 다시 맞췄다.

효과(effect, 효과)는 신호/확률 동등성(signal/probability parity, 신호/확률 동등성)은 진단에 쓸 수 있다는 점과, numeric proxy(숫자 프록시)는 branch-specific(분기별) 판정력이 부족하다는 점을 분리한 것이다.

## Evidence(근거)

- row_level_runtime_parity_summary(행 단위 런타임 동등성 요약): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/row_level_runtime_parity_summary.csv`
- row_level_runtime_parity_gap_rows(행 단위 공백 행): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/row_level_runtime_parity_gap_rows.csv`
- runtime_probability_diff_extremes(런타임 확률 차이 최대치): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/runtime_probability_diff_extremes.csv`
- proxy_numeric_protocol_specificity_audit(프록시 숫자 계약 특이성 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/proxy_numeric_protocol_specificity_audit.csv`
- proxy_usability_scope_matrix(프록시 활용 범위 행렬): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/proxy_usability_scope_matrix.csv`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/required_gate_coverage_audit.csv`
- result_judgment(결과 판정): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335L/result_judgment.csv`

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
