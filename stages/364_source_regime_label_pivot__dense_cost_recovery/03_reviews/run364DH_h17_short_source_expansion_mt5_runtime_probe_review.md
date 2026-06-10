# run364DH h17 short-source expansion MT5 runtime probe review(17시 숏 원천 확장 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T06:07:33Z

## Judgment(판정)

- run_id(실행 ID): `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`
- baseline_run_id(기준선 실행 ID): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`
- judgment(판정): `positive_runtime_probe_clue_short_source_added_density_but_profit_retreated_side_balance_unresolved_no_authority`
- next_run_id(다음 실행 ID): `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DG MT5 result(DG MT5 결과)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): short-source expansion(숏 원천 확장)이 trade shape(거래 형태)는 개선했지만, DB 기준 순수익/수익 팩터 회복이 필요하다는 다음 탐색 조건(next exploration condition, 다음 탐색 조건)을 분리했습니다.

| dg_mt5_net | db_mt5_net | net_delta_vs_db | dg_profit_factor | db_profit_factor | profit_factor_delta_vs_db | dg_trade_count | db_trade_count | dg_short_trade_count | db_short_trade_count | short_count_delta_vs_db | dg_short_share | db_short_share | proxy_mt5_net_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 987.88 | 1018.78 | -30.9 | 1.38 | 1.41 | -0.03 | 1014.0 | 972.0 | 142.0 | 101.0 | 41.0 | 0.1400394477 | 0.103909465 | -31.8901 |

## Result Boundary(결과 경계)

- positive clue(긍정 단서): DG는 DB보다 short count(숏 거래수)를 `41.0` 늘리고 trade density(거래 밀도)를 `3.2292993631`까지 올렸습니다.
- unresolved guardrail(미해결 가드레일): DG net/PF/expectancy(순수익/수익 팩터/기대값)는 DB보다 각각 `-30.9` / `-0.03` / `-0.08` 후퇴했습니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없고, 운영 승격(operating promotion, 운영 승격)도 없습니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/required_gate_coverage_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/h17_short_source_expansion_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/proxy_mt5_runtime_difference.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/strategy_tester_report_records.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/runtime_output_copy_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/runtime_identity.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DF/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DF/expected_kpi_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DF/runtime_policy_config.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DF/tester_set_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/h17_short_quality_risk_scale_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/proxy_mt5_runtime_difference.csv | DG/DF/DB evidence(DG/DF/DB 근거)를 같은 비교 경계에 묶습니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/h17_short_source_expansion_mt5_probe_summary.csv | MT5 runtime output(MT5 런타임 출력)이 review(검토) 가능한지 확인합니다. |
| baseline_trade_shape_comparison_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DH/dg_vs_db_runtime_comparison.csv | DB baseline(DB 기준선) 대비 수익 구조와 trade shape(거래 형태)를 분리합니다. |
| proxy_mt5_gap_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다. |
| result_judgment_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DH/result_judgment_receipt.json | positive clue(긍정 단서)를 operating promotion(운영 승격)으로 올리지 않습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DH/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DH/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 막습니다. |

## Next(다음)

`run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`는 margin_vs_flat(플랫 대비 마진), hour veto(시간 배제), short-source quality filter(숏 원천 품질 필터)를 탐색합니다. 효과(effect, 효과)는 숏 거래수 상승을 유지하면서 DB 기준 순수익/수익 팩터를 회복할 후보를 찾는 것입니다.
