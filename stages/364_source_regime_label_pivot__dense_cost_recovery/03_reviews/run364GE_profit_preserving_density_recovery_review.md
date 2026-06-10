# run364GE Profit Preserving Density Recovery Review(수익 보존 밀도 회복 검토)

Created(생성): 2026-06-07T09:32:51Z

Action(행동): GD proxy/ONNX smoke(GD 프록시/ONNX 간이 검증) 결과를 OOS profit improvement(표본외 수익 개선), validation weakness(검증 약화), density failure(밀도 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 표본외 수익/비용 단서를 보존하되 운영 후보로 올리지 않고 GF(364GF) profit-floor density lift(수익 바닥 밀도 상승)로 넘깁니다.

- judgment(판정): `negative_profit_preserving_density_recovery_review_oos_profit_improved_density_validation_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gd_sym_h1_m0p65__gd_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `16.965` / `1.0259839517` / `2.0546448087`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `83.737` / `1.184927453` / `2.0458015267`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-77.063`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `100.702` / `2.050955414` / `-285.698` / `0.7329192547`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `750`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ge_selected_candidate(선택 후보) | true | gd_sym_h1_m0p65__gd_all72__rf8_l18_n132 | 16.965 | 2.0546448087 | 83.737 | 1.184927453 | 2.0458015267 | -77.063 | -285.698 | 선택 후보는 OOS profit/cost(표본외 수익/비용)를 개선했지만 validation/density(검증/밀도)가 실패했습니다. |
| ge_best_oos_positive(표본외 양수 상위) | true | gd_sym_h1_m0p65__gd_all72__rf8_l18_n132 | 16.965 | 2.0546448087 | 83.737 | 1.184927453 | 2.0458015267 | -77.063 | -285.698 | 표본외 양수 행의 밀도와 비용 상태를 확인합니다. |
| ge_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | 전 분할 density3(밀도3) 후보가 수익을 보존하는지 확인합니다. |
| ge_oos_pf125_cost09(표본외 PF125 비용0.9) | true | gd_asym_h1_l0p55_s1p10__gd_profit_density_blend__et7_l10_n132 | -6.875 | 0.3442622951 | 56.972 | 1.9633412242 | 0.2519083969 | 37.172 | -7.503 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다. |
| ge_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| ge01_oos_profit_cost_improved | density3_all_splits_count=0; selected_density=2.0546448087/2.0458015267/2.050955414 | profit-preserving density recovery(수익 보존 밀도 회복)가 OOS net/PF(표본외 순수익/수익 팩터)와 OOS cost0.6(표본외 비용0.6)을 개선했습니다. | salvage_clue(회수 단서) | GF(364GF)는 OOS profit floor(표본외 수익 바닥)를 유지하면서 density(밀도)를 끌어올려야 합니다. |
| ge02_validation_density_failed | selected_oos_net=83.737; selected_oos_pf=1.184927453; density3_all_splits_valpos_oospos_count=0 | 선택 후보는 validation net(검증 순수익)이 약하고 density(밀도)가 3 미만입니다. | high(높음) | package(패키지)를 거절하고 profit-floor density lift(수익 바닥 밀도 상승)로 넘깁니다. |
| ge03_cost_and_short_improved_but_not_enough | selected_combined_cost09_net=-285.698; selected_short_share=0.7329192547 | 선택 후보는 short share(숏 비중)는 개선됐지만 combined cost0.9(합산 비용0.9)는 아직 음수입니다. | medium(중간) | 다음 실행에서 cost0.9(비용0.9) 개선을 보조 제약으로 유지합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | GD improved OOS profit and OOS cost0.6 but validation is weak, density is below 3, combined_cost09<0, strict_candidate_count=0(GD 표본외 수익/비용0.6 개선, 약한 검증, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0) | not_opened | not_run | 표본외 개선 단서를 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| ge01_oos_profit_improved_validation_density_failed | OOS profit plus validation plus density plus cost(표본외 수익과 검증과 밀도와 비용 동시 충족) | selected_oos_net=83.737; selected_oos_pf=1.184927453; density3_all_splits_count=0; selected_density=2.0546448087/2.0458015267/2.050955414 | selected_oos_net=83.737; selected_oos_pf=1.184927453; selected_oos_cost09_net=-77.063; max_combined_cost09_net=183.344 | preserve OOS net/PF and OOS cost0.6 while lifting density and validation net(표본외 순수익/수익 팩터와 표본외 비용0.6 보존, 밀도와 검증 순수익 상승) | Do not improve OOS by starving density or weakening validation(밀도를 굶기거나 검증을 약화하며 표본외만 개선하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 | gf01_profit_floor_density_lift | GD OOS profit floor(GD 표본외 수익 바닥)를 고정하고 threshold/density target(임계값/밀도 목표)을 다시 조정하면 validation/density(검증/밀도)를 끌어올릴 수 있습니다. | OOS net>0, OOS PF>=1.10, OOS cost0.6>=0(표본외 순수익/수익 팩터/비용0.6 보존) | validation_net and density lift toward 3, combined_cost09 improves(검증 순수익과 밀도 3 접근, 합산 비용0.9 개선) | low-density OOS-only optimization(저밀도 표본외 전용 최적화) | GF는 GD의 표본외 수익 바닥을 보존하면서 검증과 밀도를 다시 끌어올립니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/ge_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/ge_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/ge_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/ge_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/ge_gf_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GE/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
