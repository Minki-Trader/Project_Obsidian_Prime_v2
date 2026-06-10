# run364FK OOS Density Preserve Review(표본외 밀도 보존 검토)

Created(생성): 2026-06-07T04:14:58Z

Action(행동): FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리)를 package decision(패키지 결정), failure memory(실패 기억), FL queue(FL 대기열)로 분리했습니다.

Effect(효과): OOS PF/cost(표본외 수익 팩터/비용) 회복은 보존 단서로 남기고, density3(밀도3) 부재 때문에 운영 주장(operating claim, 운영 주장)을 막습니다.

- judgment(판정): `negative_oos_density_preserve_review_density_reloss_no_package_no_authority`
- selected model(선택 모델): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `116.181` / `1.1134556811` / `2.131147541`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `333.32` / `1.4709758917` / `2.5496183206`
- OOS cost0.9(표본외 비용0.9): `132.92`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `2.3057324841` / `15.101` / `0.5483425414`
- validation_positive_density3_count(검증 양수 밀도3 수): `0`
- oos_pf125_cost09_short077_count(표본외 PF125 비용0.9 숏 균형 수): `5675`
- floor21_bridge_count(밀도2.1 연결 수): `15`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | oos_density | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fk_selected(선택 후보) | fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160 | 116.181 | 2.131147541 | 1.4709758917 | 132.92 | 2.5496183206 | 2.3057324841 | 15.101 | 0.5483425414 | FJ selected candidate(FJ 선택 후보)는 OOS PF/cost(표본외 수익 팩터/비용)를 회복했지만 density(밀도)가 낮습니다. |
| fk_best_oos_cost_short(표본외 비용 숏) | fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160 | 116.181 | 2.131147541 | 1.4709758917 | 132.92 | 2.5496183206 | 2.3057324841 | 15.101 | 0.5483425414 | OOS PF/cost/short(표본외 수익 팩터/비용/숏) 조건은 많지만 density3(밀도3)가 없습니다. |
| fk_floor21_bridge(밀도 2.1 연결) | fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160 | 116.181 | 2.131147541 | 1.4709758917 | 132.92 | 2.5496183206 | 2.3057324841 | 15.101 | 0.5483425414 | floor 2.1(밀도 2.1)에서는 연결 후보가 있지만 3/day(일 3회)에는 못 미칩니다. |
| fk_best_dense(밀도 후보) | fj_sym_h2_m1p75__fj_behavior_density_cost__rf8_l28_n160 | -62.089 | 3.1202185792 | 0.7883256933 | -451.857 | 3.0687022901 | 3.0987261146 | -856.546 | 0.6618705036 | density3(밀도3) 후보 자체는 선택 가능한 수익 구조를 만들지 못했습니다. |
| fk_best_strict_like(엄격 유사) |  |  |  |  |  |  |  |  |  | strict-like(엄격 유사) 후보는 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fk01_oos_pf_cost_salvage | selected_oos_pf=1.4709758917; selected_oos_cost09=132.92; combined_cost09=15.101 | FJ score(FJ 점수)가 OOS PF/cost(표본외 수익 팩터/비용)를 강하게 회복했습니다. | salvage(회수) | FL에서는 이 단서를 보존하되 density3(밀도3) 없이는 package(패키지) 근거로 쓰지 않습니다. |
| fk02_density_reloss | selected_validation_density=2.131147541; selected_oos_density=2.5496183206; selected_combined_density=2.3057324841; validation_positive_density3_count=0 | OOS PF/cost(표본외 수익 팩터/비용)를 살리자 validation/combined density(검증/합산 밀도)가 다시 무너졌습니다. | high(높음) | runtime package(런타임 패키지)를 열지 않고 dual density hard floor(양쪽 밀도 강제 바닥)를 다음 조건으로 둡니다. |
| fk03_bridge_exists_below_three | floor21_bridge_count=15; oos_pf125_cost09_short077_count=5675 | 2.1/day(일 2.1회) 부근에는 표본외 PF/비용/숏 연결 후보가 있습니다. | salvage(회수) | FL은 2.1/day 연결을 3/day(일 3회)로 올리는 hard floor search(강제 바닥 탐색)를 시도합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | strict_candidate_count=0; validation_positive_density3_count=0; selected_density_below_3_even_with_oos_pf_cost_recovered | not_opened | not_run | OOS PF/cost(표본외 수익 팩터/비용) 회복을 MT5 운영 의미로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fk01_oos_salvage_density_reloss | OOS PF125/cost09 with validation and combined density3(표본외 PF125/비용0.9와 검증/합산 밀도3 동시 충족) | validation_positive_density3_count=0; oos_pf125_cost09_density3_count=0; selected_density=2.131147541/2.5496183206/2.3057324841 | OOS PF/cost0.9/combined cost0.9/short share=1.4709758917/132.92/15.101/0.5483425414; floor21_bridge_count=15 | validation_density>=3, oos_density>=3, combined_density>=3, OOS PF>=1.25, OOS cost0.9>=0, validation_net>0(검증/표본외/합산 밀도와 표본외 PF/비용 동시 충족) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fl01_dual_density_oos_cost_bridge | FJ에서 OOS PF/cost(표본외 수익 팩터/비용)는 충분히 회복됐으므로 FL은 density3(밀도3)를 hard floor(강제 바닥)로 두고 OOS cost/PF를 다시 보존하는지 시험합니다. | OOS PF>=1.25, OOS cost0.9>=0, combined cost0.9>=0, short_share<=0.77(표본외 PF/비용과 숏 균형 보존) | validation_density>=3, oos_density>=3, combined_density>=3, validation_net>0(검증/표본외/합산 밀도와 검증 수익 회복) | FL은 수익 팩터와 거래 빈도 조건을 같은 필터 안에서 동시에 요구합니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/input_manifest.csv | FJ 입력 계보가 FK 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/required_gate_coverage_audit.csv | FJ gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/fk_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_tradeoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/fk_surface_diagnostic.csv | OOS PF/cost/density(표본외 PF/비용/밀도) tradeoff(절충 관계)를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/fk_failure_attribution.csv | 밀도 재손실을 귀속했습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/fk_failure_memory.csv | 실패 기억과 재개 조건을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/fk_fl_queue.csv | FL dual density OOS cost bridge(FL 양쪽 밀도 표본외 비용 연결) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FK/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
