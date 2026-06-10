# run364DC h17 short-quality risk-scale MT5 runtime probe review(17시 숏 품질 위험비율 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T04:55:57Z

## Judgment(판정)

- run_id(실행 ID): `run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`
- judgment(판정): `positive_runtime_probe_clue_short_risk_scale_transfer_real_side_balance_unresolved_no_authority`
- next_run_id(다음 실행 ID): `run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed`

## Key Read(핵심 판독)

Action(행동): DB MT5 result(DB MT5 결과)를 CV runtime anchor(CV 런타임 기준점)와 비교했습니다.

Effect(효과): risk-scale overlay(위험비율 오버레이)가 MT5에서 실제 순수익 개선으로 전달됐는지와, long/short balance(롱/숏 균형)가 여전히 약한지를 분리했습니다.

| db_mt5_net | cv_mt5_net | mt5_net_delta_vs_cv | expected_risk_scale_net_delta | overlay_transfer_efficiency | db_profit_factor | db_trade_count | db_drawdown | db_long_trade_count | db_short_trade_count | short_share | proxy_mt5_net_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1018.78 | 1011.02 | 7.76 | 7.87 | 0.9860228717 | 1.41 | 972.0 | 130.11 | 871.0 | 101.0 | 0.103909465 | -56.29 |

## Result Boundary(결과 경계)

- positive clue(긍정 단서): MT5 net profit(MT5 순수익)은 CV 대비 `7.76` 개선됐고, 예상 risk-scale delta(위험비율 변화분) `7.87`와 거의 맞습니다.
- unresolved guardrail(미해결 가드레일): short_share(숏 비중)는 `0.103909465`이고 long/short balance(롱/숏 균형)는 아직 long-dominant(롱 우세)입니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없습니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/required_gate_coverage_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/h17_short_quality_risk_scale_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/proxy_mt5_runtime_difference.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/strategy_tester_report_records.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/runtime_output_copy_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/expected_kpi_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CV/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CV/h17_month12_secondary_guard_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CV/proxy_mt5_runtime_difference.csv | DB/CV/DA evidence(DB/CV/DA 근거)를 같은 비교 경계에 묶습니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DB/h17_short_quality_risk_scale_mt5_probe_summary.csv | MT5 output(MT5 출력)이 review(검토) 가능한지 확인합니다. |
| baseline_comparison_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DC/db_vs_cv_runtime_comparison.csv | DB를 CV runtime anchor(CV 런타임 기준점)와 비교합니다. |
| proxy_mt5_gap_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DC/db_vs_cv_runtime_comparison.csv | proxy/MT5 gap(프록시/MT5 차이)과 overlay delta(오버레이 변화분)를 분리합니다. |
| side_balance_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DC/db_vs_cv_runtime_comparison.csv | long/short balance(롱/숏 균형) 미해결을 다음 탐색 제약으로 기록합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DC/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DC/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않습니다. |

## Next(다음)

`run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1`는 pure exposure scaling(순수 노출 증폭) 반복이 아니라 short-source expansion(숏 원천 확장)을 탐색합니다.
