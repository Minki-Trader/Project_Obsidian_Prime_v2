# run337JQ MT5 Runtime Probe(run337JQ MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `run337JQ_execute_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JP_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package_without_db_v1`
- status(상태): `completed_stage337JQ_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_executed_review_required_no_forward_decision`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection`
- gates(게이트): `9/9`
- attempts(시도): `3`
- runtime_completed_rows(런타임 완료 행): `3`
- matched_rows(일치 행): `17523`
- mismatch_rows(불일치 행): `0`
- net_profit(순수익): `-274.5`
- profit_factor(수익 팩터): `0.85`
- expectancy(기대값): `-0.52`
- recovery_factor(회복 계수): `-0.49`
- trade_count(거래수): `533`
- blocker(차단 사유): ``

## Action(행동)

JP package(JP 패키지)의 3개 ONNX(온엑스) 후보를 MT5 runtime probe(MT5 런타임 탐침)로 실행하거나 차단 사유를 기록했다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 output(MT5 출력) 또는 blocker(차단 사유)와 연결했다.

## Boundary(경계)

이번 실행은 runtime probe attempt(런타임 탐침 시도)만 의미한다. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

## Next(다음)

`run337JR_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db_v1`에서 runtime evidence(런타임 근거), proxy-MT5 diff(프록시-MT5 차이), repair need(수리 필요)를 판정한다.
