# run364DM h17 short-source profit recovery MT5 runtime probe review(17시 숏 원천 수익 회복 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T08:13:05Z

## Judgment(판정)

- run_id(실행 ID): `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DL_execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`
- baseline_run_id(기준선 실행 ID): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`
- judgment(판정): `positive_runtime_probe_clue_profit_recovered_near_db_short_lift_preserved_pf_slightly_below_db_no_authority`
- next_run_id(다음 실행 ID): `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DL MT5 result(DL MT5 결과)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): short-source profit recovery(숏 원천 수익 회복)가 DG 대비 순수익은 회복했지만, DB 기준 순수익/수익 팩터 초과가 필요하다는 다음 탐색 조건(next exploration condition, 다음 탐색 조건)을 분리했습니다.

| dl_mt5_net | db_mt5_net | net_delta_vs_db | dg_source_mt5_net | net_delta_vs_dg_source | dl_profit_factor | db_profit_factor | profit_factor_delta_vs_db | dl_trade_count | db_trade_count | dl_short_trade_count | db_short_trade_count | short_count_delta_vs_db | short_count_delta_vs_dg_source | proxy_mt5_net_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1018.11 | 1018.78 | -0.67 | 987.88 | 30.23 | 1.4 | 1.41 | -0.01 | 1004.0 | 972.0 | 133.0 | 101.0 | 32.0 | -9.0 | -41.9637 |

## Result Boundary(결과 경계)

- positive clue(긍정 단서): DL은 DB보다 short count(숏 거래수)를 `32.0` 늘리고, DG source expansion(DG 원천 확장)보다 net profit(순수익)을 `30.23` 회복했습니다.
- unresolved guardrail(미해결 가드레일): DL net/PF/expectancy(순수익/수익 팩터/기대값)는 DB보다 각각 `-0.67` / `-0.01` / `-0.04` 후퇴했습니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없고, 운영 승격(operating promotion, 운영 승격)도 없습니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/required_gate_coverage_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/h17_short_source_profit_recovery_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/proxy_mt5_runtime_difference.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/strategy_tester_report_records.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/runtime_output_copy_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/runtime_identity.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DK/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DK/expected_kpi_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DK/runtime_policy_config.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DK/tester_set_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DG/h17_short_source_expansion_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/h17_short_quality_risk_scale_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/proxy_mt5_runtime_difference.csv | DL/DK/DB/DG evidence(DL/DK/DB/DG 근거)를 같은 비교 경계에 묶습니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/h17_short_source_profit_recovery_mt5_probe_summary.csv | MT5 runtime output(MT5 런타임 출력)이 review(검토) 가능한지 확인합니다. |
| baseline_trade_shape_comparison_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DM/dl_vs_db_dg_runtime_comparison.csv | DB baseline(DB 기준선) 대비 수익 구조와 trade shape(거래 형태)를 분리합니다. |
| proxy_mt5_gap_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DL/proxy_mt5_runtime_difference.csv | proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다. |
| result_judgment_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DM/result_judgment_receipt.json | positive clue(긍정 단서)를 operating promotion(운영 승격)으로 올리지 않습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DM/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DM/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 막습니다. |

## Next(다음)

`run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`는 margin_vs_flat(플랫 대비 마진), hour-pair veto(시간쌍 배제), short-source quality rank(숏 원천 품질 순위)를 탐색합니다. 효과(effect, 효과)는 숏 거래수 상승을 유지하면서 DB 기준 순수익/수익 팩터를 초과할 후보를 찾는 것입니다.
