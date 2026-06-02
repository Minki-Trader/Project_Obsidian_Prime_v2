# Stage364X density side-balance MT5 runtime probe(Stage364X 밀도 방향 균형 MT5 런타임 탐침)

## Current truth(현재 진실)

- run_id(실행 ID): `run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364W_package_density_side_balance_repair_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_attempt_only_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): `run364W` package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry/report(런타임 기록/보고서)를 수집했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)의 probability/decision/KPI(확률/판정/핵심 성과 지표) 차이를 review(검토) 가능한 산출물로 만들었다.

## Execution summary(실행 요약)

| attempt_name | tester_status | runtime_status | report_status | net_profit | profit_factor | trade_count | long_trade_count | short_trade_count | ready_model_rows | matched_rows | mismatch_rows | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364W_dual_pshort045_adx40_maxhold8 | completed | completed | completed | 989.22 | 1.3 | 1081 | 952 | 129 | 17428 | 17428 |  | completed_full_proxy_mt5_parity_reached_feature_last |

## Proxy vs MT5(프록시 대 MT5)

| attempt_name | expected_net_profit | actual_mt5_net_profit | net_profit_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | expected_profit_factor | actual_mt5_profit_factor | report_status | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run364W_dual_pshort045_adx40_maxhold8 | 771.564 | 989.22 | 217.656 | 1081 | 1081 | 0.0 | 1.2218406503 | 1.3 | completed | completed_full_proxy_mt5_parity_reached_feature_last |

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| tester_execution_attempt_gate(테스터 실행 시도 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/mt5_execution_result.json | MT5 Strategy Tester(MT5 전략 테스터) 실행 시도를 기록한다. |
| runtime_output_gate(런타임 출력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/runtime_output_copy_manifest.csv | runtime telemetry/summary(런타임 기록/요약) 존재를 확인한다. |
| strategy_report_gate(전략 테스터 보고서 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/strategy_tester_report_records.json | tester KPI(테스터 핵심 성과 지표)의 출처를 고정한다. |
| proxy_mt5_diff_gate(프록시-MT5 차이 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리한다. |
| runtime_parity_audit(런타임 동등성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/probability_runtime_difference.csv | probability/decision parity(확률/판정 동등성) 차이를 측정한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/claim_boundary_receipt.json | runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364X/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

이 run(실행)은 runtime probe(런타임 탐침)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
