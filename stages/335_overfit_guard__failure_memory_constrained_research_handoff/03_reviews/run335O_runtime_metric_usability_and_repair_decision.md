# Run335O Runtime Metric Usability and Repair Decision(335O 런타임 지표 활용성 및 수리 결정)

- run_id(실행 ID): `run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1`
- parent_run_id(부모 실행 ID): `run335N_materialize_branch_specific_runtime_metric_extractors_v1`
- status(상태): `completed_runtime_metric_usability_and_repair_decision_no_forward_decision`
- judgment(판정): `structured_runtime_metrics_usable_with_boundary_proxy_not_selection_usable`
- decision(결정): `stage335O_proxy_context_only_runtime_metrics_usable_with_boundary_repair_defense_offense_queue`
- best_research_clue(최상 연구 단서): `m48_plain_rf`
- proxy_decision(프록시 결정): `context_only_not_selection_usable`
- high_fragility_findings(높은 취약성 발견): `4`
- next_action(다음 행동): `run335P_materialize_balanced_repair_defense_offense_research_inputs_v1`

## Judgment(판정)

run335O(335O 실행)는 run335N(335N 실행)의 structured MT5 runtime metrics(구조화 MT5 런타임 지표)를 활용성 관점에서 판정했다.

Effect(효과): proxy expected numeric value(프록시 예상 숫자값)는 branch ranking(분기 순위)이나 Forward Passed/Failed(전진 통과/실패)에 쓸 수 없다. 다만 MT5 trade ledger(거래 장부), cost stress(비용 압박), curve pocket(곡선 포켓), regime slice(국면 조각)는 다음 연구 제약(research constraint, 연구 제약)으로 쓸 수 있다.

## Key Findings(핵심 발견)

- proxy(프록시): repeated aggregate context(반복 집계 문맥)라서 selection(선택) 근거가 아니다.
- cost(비용): extra cost 0.5(추가 비용 0.5)에서 여러 attempt(시도)가 무너진다.
- direction(방향): short side(숏 방향) 손익이 대부분 약하다.
- curve(곡선): underwater stretch(수중 구간)가 길고 rolling pocket(롤링 포켓)이 깊다.
- parity/data(동등성/데이터): 9개 trade-level exact join gap(거래 수준 정확 조인 공백)과 18개 open-feature cell gap(개별 셀 공백)은 repair queue(수리 대기열)로 넘겼다.

## Evidence(근거)

- attempt_scorecard(시도 점수표): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/attempt_runtime_usability_scorecard.csv`
- proxy_usability(프록시 활용성): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/proxy_mt5_usability_decision.csv`
- branch_decision(분기 결정): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/branch_metric_usability_decision.csv`
- fragility_findings(취약성 발견): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/runtime_fragility_findings.csv`
- repair_queue(수리 대기열): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/repair_research_queue.csv`
- defense_queue(방어 대기열): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/defensive_guard_queue.csv`
- offense_queue(공격 대기열): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/offensive_research_queue.csv`
- gate_audit(게이트 감사): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335O/required_gate_coverage_audit.csv`

## Boundary(경계)

이 실행은 diagnostic decision(진단 결정)이다. model(모델), threshold(임계값), lot(로트), risk logic(위험 로직), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
