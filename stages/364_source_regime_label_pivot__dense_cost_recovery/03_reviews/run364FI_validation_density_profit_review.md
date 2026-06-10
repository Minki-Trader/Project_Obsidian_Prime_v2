# run364FI Validation Density Profit Review(검증 밀도 수익 검토)

Created(생성): 2026-06-07T03:54:29Z

Action(행동): FH validation density profit repair(FH 검증 밀도 수익 수리)를 package decision(패키지 결정), failure memory(실패 기억), FJ queue(FJ 대기열)로 분리했습니다.

Effect(효과): validation-positive density3(검증 양수 밀도3) 단서는 다음 seed(씨앗)로 남기고, OOS PF/cost(표본외 수익 팩터/비용) 재손실 때문에 운영 주장(operating claim, 운영 주장)을 막습니다.

- judgment(판정): `negative_validation_density_profit_repair_review_oos_pf_cost_reloss_no_package_no_authority`
- selected model(선택 모델): `fh_sym_h2_m1p75__fh_session_macro_profit__et7_l18_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `76.781` / `1.0531729164` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `152.487` / `1.1853206259` / `2.7175572519`
- OOS cost0.9(표본외 비용0.9): `-61.113`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `2.7133757962` / `-281.932` / `0.691314554`
- validation_positive_density3_count(검증 양수 밀도3 수): `50`
- validation_positive_density3_oos_pf125_count(검증 양수 밀도3과 표본외 PF125 동시 수): `0`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fi_selected(선택 후보) | fh_sym_h2_m1p75__fh_session_macro_profit__et7_l18_n128 | 76.781 | 2.7103825137 | 1.1853206259 | -61.113 | 2.7133757962 | -281.932 | 0.691314554 | FH selected candidate(FH 선택 후보)는 validation net(검증 순수익)을 양수로 살렸지만 density(밀도), OOS PF(표본외 수익 팩터), cost0.9(비용0.9)가 부족합니다. |
| fi_best_validation_dense_profit(검증 밀도 수익) | fh_sym_h2_m1p75__fh_validation_profit_stack__rf7_l30_n128 | 99.35 | 3.4426229508 | 0.8338977746 | -475.793 | 3.5063694267 | -754.443 | 0.6848319709 | validation-positive density3(검증 양수 밀도3) 후보는 생겼지만 OOS PF(표본외 수익 팩터) 1.25와 결합되지 않았습니다. |
| fi_best_near_repair(근접 수리) | fh_asym_h2_l1p75_s2p75__fh_all72__rf7_l30_n128 | 10.726 | 3.2459016393 | 1.1247321454 | -132.824 | 3.152866242 | -478.498 | 0.8272727273 | near repair(근접 수리)는 OOS PF(표본외 수익 팩터) 1.10대에서 멈추고 cost0.9(비용0.9)를 통과하지 못합니다. |
| fi_best_oos_pf_cost_short(표본외 비용 숏) | fh_sym_h2_m1p75__fh_validation_profit_stack__et8_l22_n128 | 185.318 | 2.0491803279 | 1.2846889574 | 11.591 | 1.9936305733 | -28.091 | 0.6581469649 | OOS PF/cost/short(표본외 수익 팩터/비용/숏) 후보는 많지만 density3(밀도3)와 검증 양수 수익을 같이 통과하지 못합니다. |
| fi_best_strict_like(엄격 유사) |  |  |  |  |  |  |  |  | strict-like(엄격 유사) 후보는 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fi01_validation_dense_profit_partial_success | validation_positive_density3_count=50; near_repair_count=5 | FH score(FH 점수)가 validation net(검증 순수익)과 density(밀도)를 일부 복구했습니다. | salvage(회수) | FJ에서는 이 단서를 seed(씨앗)로 쓰되 package(패키지) 근거로 쓰지 않습니다. |
| fi02_oos_pf125_not_preserved | selected_oos_pf=1.1853206259; validation_positive_density3_oos_pf125_count=0 | validation density repair(검증 밀도 수리)를 강화하자 OOS PF(표본외 수익 팩터) 1.25 보존이 무너졌습니다. | high(높음) | runtime package(런타임 패키지)를 열지 않고 OOS preserve(표본외 보존)를 다음 필수 조건으로 둡니다. |
| fi03_cost_stress_failed | validation_cost09=-220.819; oos_cost09=-61.113; combined_cost09=-281.932 | cost0.9(비용0.9) 압박에서 validation(검증), OOS(표본외), combined(합산)이 모두 약합니다. | high(높음) | 운영 주장(operating claim, 운영 주장)을 차단하고 비용 압박을 FJ score(FJ 점수)의 패널티로 남깁니다. |
| fi04_short_balance_salvage | combined_short_share=0.691314554 | short share(숏 비중)는 0.77보다 낮아 쏠림 위험이 줄었습니다. | salvage(회수) | FJ에서는 short balance(숏 균형)를 보존 조건으로 유지하고 PF/cost/density(PF/비용/밀도)를 다시 올립니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | strict_candidate_count=0; operational_proxy_stack_pass_count=0; selected_oos_pf_below_1p25; selected_density_below_3; cost09_negative | not_opened | not_run | FH proxy(프록시)를 MT5 runtime authority(MT5 런타임 권위)로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fi01_validation_density_repair_oos_reloss | validation-positive density3 with OOS PF125 and cost09(검증 양수 밀도3과 표본외 PF125/비용0.9 동시 충족) | validation_positive_density3_count=50; validation_positive_density3_oos_pf125_count=0; oos_pf125_cost09_density3_count=0 | validation_net/PF=76.781/1.0531729164; short_share=0.691314554; near_repair_count=5 | validation_density>=3, combined_density>=3, validation_net>0, OOS PF>=1.25, OOS cost0.9>=0, combined_short_share<=0.77(검증/합산 밀도와 표본외 PF/비용/숏 균형 동시 충족) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fj01_oos_density_preserve_repair | FH에서 validation-positive density3(검증 양수 밀도3)는 생겼으므로 FJ는 그 조건을 보존하면서 OOS PF/cost(표본외 수익 팩터/비용)를 다시 회복할 수 있는지 공격합니다. | validation_net>0, validation_density>=3, combined_density>=3, combined_short_share<=0.77(검증 수익/밀도/합산 밀도/숏 균형 보존) | OOS PF>=1.25, OOS cost0.9>=0, validation cost0.9 not deeply negative(표본외 수익 팩터/비용 회복과 검증 비용 방어) | FJ는 FH가 만든 검증 밀도 단서를 버리지 않고 표본외 보존을 되살리는지 확인합니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/input_manifest.csv | FH 입력 계보가 FI 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/required_gate_coverage_audit.csv | FH gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/fi_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_tradeoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/fi_surface_diagnostic.csv | validation density/OOS PF/cost(검증 밀도/표본외 PF/비용) tradeoff(절충 관계)를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/fi_failure_attribution.csv | 표본외 PF/비용 재손실을 귀속했습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/fi_failure_memory.csv | 실패 기억과 재개 조건을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/fi_fj_queue.csv | FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FI/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
