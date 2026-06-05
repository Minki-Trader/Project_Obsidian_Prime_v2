# Stage339 Input References(339단계 입력 참조)

## Source Inputs(원천 입력)

- run338M final decision(338M 최종 결정): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338M/final_decision.json`
- run338M attempt package(338M 시도 패키지): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338M/runtime_probe_attempt_package.csv`
- run338M expected tape(338M 기대 테이프): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338M/expected/expected_tape.csv`
- run338N partial summary(338N 부분 요약): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338N/lifecycle_exit_mt5_probe_summary.csv`
- run338N execution result(338N 실행 결과): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338N/mt5_execution_result.json`
- run338N report records(338N 보고 기록): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338N/strategy_tester_report_records.json`

## Stage339 Handoff Files(339단계 인계 파일)

- handoff manifest(인계 목록): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339A/stage338_to_stage339_handoff_manifest.csv`
- runtime output inventory(런타임 출력 목록): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339A/recovered_runtime_output_inventory.csv`
- runtime preview(런타임 미리보기): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339A/recovered_runtime_preview.csv`
- next queue(다음 대기열): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339A/run339B_queue.csv`

Effect(효과): run339B(339B 실행)가 같은 파일을 다시 찾느라 시간을 쓰지 않게 한다.
