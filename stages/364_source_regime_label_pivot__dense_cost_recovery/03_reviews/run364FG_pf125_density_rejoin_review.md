# run364FG PF125 Density Rejoin Review(PF125 밀도 재결합 검토)

Created(생성): 2026-06-07T03:31:44Z

Action(행동): FF PF125 density rejoin cost09 short guard(FF PF125 밀도 재결합 비용0.9 숏 가드)를 package decision(패키지 결정), failure memory(실패 기억), FH queue(FH 대기열)로 분리했습니다.

Effect(효과): OOS PF/cost/short(표본외 PF/비용/숏) 회복은 보존 단서로 남기고, validation/combined density(검증/합산 밀도) 실패를 다음 탐색 제약으로 고정합니다.

- judgment(판정): `negative_pf125_density_rejoin_review_density_profit_failure_no_package_no_authority`
- selected model(선택 모델): `ff_sym_h2_m2p25__ff_all72__et8_l24_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `208.962` / `1.1922187829` / `2.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `215.966` / `1.3184287197` / `2.358778626`
- OOS cost0.9(표본외 비용0.9): `30.566`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `2.3566878981` / `-19.072` / `0.672972973`
- strict_candidate_count(엄격 후보 수): `0`
- validation_positive_density3_count(검증 양수 밀도3 수): `0`
- next_run_id(다음 실행 ID): `run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | combined_density | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fg_selected(선택 후보) | ff_sym_h2_m2p25__ff_all72__et8_l24_n128 | 208.187 | 2.3606557377 | 1.3184287197 | 30.566 | 2.3598726115 | 0.673414305 | FF 선택 후보는 OOS PF/cost/short(표본외 PF/비용/숏)를 회복했지만 density(밀도)가 낮습니다. |
| fg_best_near_gap(근접 간격) | ff_sym_h2_m2p25__ff_all72__et8_l24_n128 | 208.187 | 2.3606557377 | 1.3184287197 | 30.566 | 2.3598726115 | 0.673414305 | 근접 후보도 validation/combined density(검증/합산 밀도)가 3/day(일 3회)에 못 미칩니다. |
| fg_best_dense(밀도 후보) | ff_sym_h2_m2p25__ff_session_macro_rejoin__et8_l24_n128 | -202.08 | 3.0 | 1.301062717 | 13.967 | 3.0445859873 | 0.6412133891 | 밀도 3/day(일 3회) 후보는 validation net(검증 순수익)이 음수입니다. |
| fg_best_oos_cost_short(표본외 비용 숏) | ff_sym_h2_m2p25__ff_all72__et8_l24_n128 | 208.187 | 2.3606557377 | 1.3184287197 | 30.566 | 2.3598726115 | 0.673414305 | 표본외 비용/숏 조건은 많지만 밀도와 검증 수익을 동시에 통과하지 못합니다. |
| fg_best_strict_like(엄격 유사) |  |  |  |  |  |  |  | 모든 핵심 조건을 동시에 만족한 후보는 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fg01_oos_pf_cost_short_salvage | oos_pf=1.3184287197; oos_cost09=30.566; combined_short_share=0.672972973 | FF score(FF 점수)가 표본외 PF/비용과 숏 비중을 살렸습니다. | salvage(회수) | FH에서는 이 단서를 보존 조건으로만 쓰고 패키지 근거로 쓰지 않습니다. |
| fg02_density_rejoin_failed | validation_density=2.3551912568; oos_density=2.358778626; combined_density=2.3566878981 | 선택 후보가 3/day(일 3회) 밀도 조건을 만족하지 못했습니다. | high(높음) | 패키지를 열지 않고 validation density profit repair(검증 밀도 수익 수리)로 넘깁니다. |
| fg03_dense_validation_profit_collapse | validation_positive_density3_count=0; oos_pf125_cost09_density3_count=5 | 밀도 3/day(일 3회)를 맞추는 표면은 검증 순수익이 무너졌습니다. | structural(구조) | 다음 탐색은 threshold(임계값) 반복보다 validation density profit(검증 밀도 수익)을 목적 함수에 직접 넣습니다. |
| fg04_validation_cost09_weak | validation_cost09=-49.638; oos_cost09=30.566; combined_cost09=-19.072 | 표본외 비용0.9는 양수지만 검증 비용0.9와 합산 비용0.9가 약합니다. | high(높음) | 운영 주장(operating claim, 운영 주장)을 막고 비용 압박을 FH guard(가드)로 남깁니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | strict_candidate_count=0; validation_positive_density3_count=0; selected_density_below_3 | not_opened | not_run | 프록시 단서를 MT5 운영 의미로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fg01_validation_density_profit_gap | PF125 OOS cost/short with validation-positive 3/day density(PF125 표본외 비용/숏과 검증 양수 일 3회 밀도) | selected_density=2.3551912568/2.358778626/2.3566878981; validation_positive_density3_count=0; strict_like_count=0 | OOS PF/cost0.9/short share=1.3184287197/30.566/0.672972973; validation PF=1.1922187829 | validation_density>=3 and validation_net>0 while OOS PF>=1.25 and OOS cost0.9>=0(검증 밀도/순수익과 표본외 PF/비용 동시 충족) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fh01_validation_density_profit_repair | Validation density profit score(검증 밀도 수익 점수)를 직접 넣으면 OOS PF/cost(표본외 PF/비용) 단서를 버리지 않고 3/day(일 3회)를 회복할 수 있습니다. | OOS PF>=1.25, OOS cost0.9>=0, combined_short_share<=0.77(표본외 PF/비용0.9/숏 비중 보존) | validation_density>=3, combined_density>=3, validation_net>0(검증/합산 밀도와 검증 순수익 회복) | FH는 밀도 회복이 수익 붕괴를 만들지 않는지 직접 공격합니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/input_manifest.csv | FF 입력 계보가 FG 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/required_gate_coverage_audit.csv | FF 게이트 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/fg_review_summary.csv | KPI(핵심 성과 지표)와 패키지 결정을 분리했습니다. |
| surface_tradeoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/fg_surface_diagnostic.csv | PF/비용/숏/밀도 tradeoff(절충 관계)를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/fg_failure_attribution.csv | 밀도 수익 실패를 귀속했습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/package_decision.csv | 런타임 패키지 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/fg_failure_memory.csv | 실패 기억과 재개 조건을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/fg_fh_queue.csv | FH validation density profit repair(FH 검증 밀도 수익 수리) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FG/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
