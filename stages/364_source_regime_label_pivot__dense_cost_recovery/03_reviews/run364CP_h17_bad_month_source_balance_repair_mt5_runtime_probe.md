# run364CP h17 bad-month source-balance MT5 runtime probe(17시 손실 월/원천 균형 MT5 런타임 탐침)

Updated(갱신): 2026-06-06T02:04:09Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority`
- mt5_execution(MT5 실행): `attempted`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): CO package(CO 패키지) `cm04_cj09_month08_12_pair_guard`를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도하고 telemetry/report(런타임 기록/보고서)를 수집했습니다.

Effect(효과): proxy expected value(프록시 예상값)와 실제 MT5 output(MT5 출력)을 분리해 CQ review(CQ 검토)에서 차이(diff, 차이), 원인(attribution, 귀속), usability(활용 가능성)를 판단할 수 있게 했습니다.

## Execution Summary(실행 요약)

| attempt_name | tester_status | runtime_status | report_status | net_profit | profit_factor | trade_count | long_trade_count | short_trade_count | blocker | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364CO_cm04_month08_12_source_balance_guard | completed_with_terminal_timeout_after_outputs_available | completed | completed | 983.74 | 1.4 | 982 | 881 | 101 | terminal_timeout_after_outputs_available | runtime_or_report_available |

## Proxy vs MT5(프록시 대 MT5)

| attempt_name | expected_net_profit | actual_mt5_net_profit | net_profit_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | expected_profit_factor | actual_mt5_profit_factor | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364CO_cm04_month08_12_source_balance_guard | 1036.46 | 983.74 | -52.72 | 975.0 | 982.0 | 7.0 | 1.4281838362 | 1.4 | runtime_or_report_available |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| tester_execution_attempt_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/mt5_execution_result.json | MT5 Strategy Tester(MT5 전략 테스터) 실행 시도 또는 차단 사유를 기록합니다. |
| runtime_output_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/runtime_output_copy_manifest.csv | runtime telemetry/summary(런타임 기록/요약) 존재를 확인합니다. |
| strategy_report_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/strategy_tester_report_records.json | tester KPI(테스터 핵심 성과 지표) 추출 여부를 고정합니다. |
| proxy_mt5_diff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다. |
| runtime_parity_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/runtime_parity_receipt.json | runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않게 합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CP/claim_boundary_receipt.json | Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 모두 막습니다. |

## Boundary(경계)

This run(이번 실행)은 runtime probe attempt(런타임 탐침 시도)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`입니다.
