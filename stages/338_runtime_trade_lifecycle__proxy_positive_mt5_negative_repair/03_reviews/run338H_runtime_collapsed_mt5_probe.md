# run338H Runtime-Collapsed MT5 Probe(런타임 축약 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run338H_execute_runtime_collapsed_onnx_mt5_probe_without_db_v1`
- status(상태): `completed_stage338H_runtime_collapsed_onnx_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection`
- gates(게이트): `8/8`
- attempts(시도): `1`
- runtime_completed_rows(런타임 완료 행): `1`
- matched_rows(일치 행): `5827`
- mismatch_rows(불일치 행): `0`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run338I_review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db_v1`

## Action(행동)

run338G(338G 실행)의 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 실제 terminal64(터미널64)에 실행 시도했다.
Effect(효과): 성공이면 proxy-MT5 diff(프록시-MT5 차이)를 얻고, 실패면 정확한 blocker(차단 사유)를 남긴다.

## Evidence(근거)

- execution result(실행 결과): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338H/mt5_execution_result.json`
- runtime summary(런타임 요약): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338H/runtime_collapsed_mt5_probe_summary.csv`
- proxy-MT5 diff(프록시-MT5 차이): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338H/proxy_mt5_runtime_difference.csv`
- tester reports(테스터 보고서): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338H/strategy_tester_report_records.json`
- runtime identity(런타임 정체성): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338H/runtime_identity.csv`

## Boundary(경계)

run338H(338H 실행)는 runtime_probe attempt(런타임 탐침 시도)다. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
