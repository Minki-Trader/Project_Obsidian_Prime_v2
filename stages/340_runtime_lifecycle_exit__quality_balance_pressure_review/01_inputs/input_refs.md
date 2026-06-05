# Stage340 Input Refs(340단계 입력 참조)

## Source Inputs(원천 입력)

- run339G final decision(339G 최종 결정): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339G/final_decision.json`
- run339G gate audit(339G 게이트 감사): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339G/required_gate_coverage_audit.csv`
- run339G MT5 summary(339G MT5 요약): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339G/quality_balance_blend_mt5_probe_summary.csv`
- run339G proxy-MT5 diff(339G 프록시-MT5 차이): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339G/proxy_mt5_runtime_difference.csv`
- run339F variant preview(339F 변형 미리보기): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339F/variant_preview.csv`

## Stage340 Handoff Files(340단계 인계 파일)

- handoff manifest(인계 목록): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340A/stage339_to_stage340_handoff_manifest.csv`
- runtime preview(런타임 미리보기): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340A/quality_balance_runtime_preview.csv`
- runtime output inventory(런타임 출력 목록): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340A/quality_balance_runtime_output_inventory.csv`
- next queue(다음 대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340A/run340B_queue.csv`

Effect(효과): run340B(340B 실행)가 같은 파일을 다시 찾느라 시간을 쓰지 않게 한다.
