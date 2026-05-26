# Run335K Independent Proxy/MT5 Runtime Probe(독립 프록시/MT5 런타임 탐침)

- run_id(실행 ID): `run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1`
- parent_run_id(부모 실행 ID): `run335J_materialize_proxy_expected_values_and_mt5_runtime_probe_attempts_or_block_v1`
- status(상태): `completed_independent_proxy_signal_and_mt5_runtime_probe_materialized_no_forward_decision`
- decision(결정): `stage335K_independent_proxy_signal_mt5_runtime_probe_diagnostic_usable_not_forward_usable_no_selection`
- fresh_runtime_completed(신규 런타임 완료): `6/6`
- signal_parity_matched(신호 동등성 일치): `30/30`
- diagnostic_usability(진단 활용 가능성): `usable_for_runtime_signal_parity_and_repair_prioritization`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- next_action(다음 행동): `run335L_independent_runtime_parity_and_proxy_usability_review_v1`

## What Changed(무엇이 바뀌었나)

run335K(335K 실행)는 run330E(330E 실행)의 frozen ONNX/feature/threshold/risk(고정 온엑스/피처/임계값/위험)을 바꾸지 않고 새 Common Files(공통 파일) 경로, 새 `.set/.ini`, 새 telemetry/report(기록/보고서) identity(정체성)를 만들었다.

효과(effect, 효과)는 run335J(335J 실행)의 existing MT5 evidence(기존 MT5 근거) 재사용 문제를 줄이고, Python ONNX proxy expected signal(파이썬 온엑스 프록시 예상 신호)과 fresh MT5 telemetry(신규 MT5 기록)를 직접 비교할 수 있게 한 것이다.

## Boundary(경계)

이 결과는 runtime parity diagnostic(런타임 동등성 진단)에는 활용 가능하지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다. numeric proxy(숫자 프록시)는 아직 branch-specific fresh P/L proxy(분기별 신규 손익 프록시)가 아니기 때문이다.

## Evidence(근거)

- handoff attempts(인계 시도): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335K/independent_handoff_attempt_manifest.csv`
- proxy expected signal values(프록시 예상 신호값): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335K/proxy_signal_expected_values.csv`
- fresh MT5 runtime summary(신규 MT5 런타임 요약): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335K/mt5_fresh_runtime_probe_summary.csv`
- signal difference(신호 차이): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335K/proxy_signal_vs_mt5_runtime_difference.csv`
- numeric proxy/fresh MT5 difference(숫자 프록시/신규 MT5 차이): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335K/proxy_numeric_vs_fresh_mt5_difference.csv`
