# run364HK Probability-Bin Veto MT5 Runtime Probe(확률 구간 거부 MT5 런타임 탐침)

Updated(갱신): 2026-06-08T12:54:56Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- parent_run_id(상위 실행 ID): `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`
- next_run_id(다음 실행 ID): `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mt5_runtime_probe_outputs_available_probability_bin_veto_proxy_diff_review_required_no_authority`
- mt5_execution(MT5 실행): `attempted`
- tester_first_status(첫 테스터 상태): `completed`
- tester_first_blocker(첫 테스터 차단): ``
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HJ package(HJ 패키지)의 GZ primary + HB fallback(GZ 우선 + HB 대체) ONNX(온엑스), probability-bin veto(확률 구간 거부), set/ini(설정/초기화 파일)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했습니다.

Effect(효과): proxy expected value(프록시 예상값)와 MT5 output(MT5 출력)을 분리해서 `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`에서 diff(차이), attribution(귀속), usability(활용 가능성)를 검토할 수 있습니다.

## Execution Summary(실행 요약)

| attempt_name | tester_status | runtime_status | report_status | net_profit | profit_factor | trade_count | long_trade_count | short_trade_count | blocker | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364HJ_probability_bin_veto_dual_source_runtime_probe | completed | completed | completed | 369.03 | 1.39 | 542 | 118 | 424 |  | runtime_or_report_available |

## Proxy vs MT5(프록시 대 MT5)

| attempt_name | expected_net_profit | actual_mt5_net_profit | net_profit_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | expected_profit_factor | actual_mt5_profit_factor | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364HJ_probability_bin_veto_dual_source_runtime_probe | 78.188 | 369.03 | 290.842 | 180.0 | 542.0 | 362.0 | 1.2173488818 | 1.39 | runtime_or_report_available |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| tester_execution_attempt_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/mt5_execution_result.json | MT5 Strategy Tester(MT5 전략 테스터) 실행 시도 또는 차단 사유를 기록합니다. |
| runtime_output_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/runtime_output_copy_manifest.csv | runtime telemetry(런타임 기록)와 summary(요약)를 확인합니다. |
| strategy_report_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/strategy_tester_report_records.json | Strategy Tester report(전략 테스터 보고서)에서 KPI(핵심 성과 지표)를 파싱합니다. |
| proxy_mt5_diff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다. |
| runtime_parity_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/runtime_parity_receipt.json | runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/runtime_parity_receipt.json | 필수 receipt(영수증)를 남깁니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HK/claim_boundary_receipt.json | Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 모두 막습니다. |

## Boundary(경계)

This run(이번 실행)은 runtime probe attempt(런타임 탐침 시도)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
