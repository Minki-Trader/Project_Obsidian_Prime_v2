# run364BE density restore stress candidate MT5 runtime probe(364BE 밀도 복원 압박 후보 MT5 런타임 탐침)

## Current truth(현재 진실)

- run_id(실행 ID): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- status(상태): `completed_stage364BE_density_restore_stress_candidate_mt5_runtime_probe_executed_review_required_no_authority`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority`
- gates(게이트): `8/8`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`

## Action/Effect(행동/효과)

Action(행동): run364BD package(364BD 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry/report(런타임 기록/보고서)를 수집했다.

Effect(효과): density restore stress candidate(밀도 복원 압박 후보)의 proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표) diff(차이)를 review(검토) 가능한 산출물로 만들었다.

## Execution summary(실행 요약)

| attempt_name | tester_status | runtime_status | report_status | net_profit | profit_factor | trade_count | long_trade_count | short_trade_count | ready_model_rows | matched_rows | mismatch_rows | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364BD_density_restore_ba02_pshort045_floor00025_hold6 | completed | completed | completed | 900.36 | 1.35 | 1016 | 917 | 99 | 17428 | 17428 |  | completed_full_proxy_mt5_parity_reached_feature_last |

## Proxy vs MT5(프록시 대 MT5)

| attempt_name | expected_net_profit | actual_mt5_net_profit | net_profit_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | expected_profit_factor | actual_mt5_profit_factor | report_status | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364BD_density_restore_ba02_pshort045_floor00025_hold6 | 919.75 | 900.36 | -19.39 | 1112 | 1016 | -96.0 | 1.3178004168 | 1.35 | completed | completed_full_proxy_mt5_parity_reached_feature_last |

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| tester_execution_attempt_gate(테스터 실행 시도 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/mt5_execution_result.json | MT5 Strategy Tester(MT5 전략 테스터) 실행 시도를 기록한다. |
| runtime_evidence_gate(런타임 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/runtime_output_copy_manifest.csv | runtime telemetry/summary(런타임 기록/요약) 존재를 확인한다. |
| strategy_report_gate(전략 테스터 보고서 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/strategy_tester_report_records.json | tester KPI(테스터 핵심 성과 지표) 출처를 고정한다. |
| proxy_mt5_diff_gate(프록시 MT5 차이 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리한다. |
| runtime_parity_audit(런타임 동등성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/probability_runtime_difference.csv | probability/decision parity(확률/결정 동등성)를 측정한다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/expected_kpi_summary.csv | expected KPI(예상 핵심 성과 지표)를 비교 기준으로 보존한다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/required_gate_coverage_audit.csv | runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

이 run(실행)은 runtime_probe(런타임 탐침)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
