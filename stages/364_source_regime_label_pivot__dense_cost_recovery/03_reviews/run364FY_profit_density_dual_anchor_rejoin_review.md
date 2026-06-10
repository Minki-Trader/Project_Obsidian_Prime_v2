# run364FY Profit Density Dual Anchor Rejoin Review(수익 밀도 이중 앵커 재결합 검토)

Created(생성): 2026-06-07T07:57:23Z

Action(행동): FX proxy/ONNX smoke(FX 프록시/ONNX 간이 검증) 결과를 density recovery(밀도 회복), OOS profit failure(표본외 수익 실패), cost/short stress(비용/숏 압박), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 밀도 회복 단서를 보존하되, 표본외 수익 실패 때문에 운영 후보로 올리지 않고 FZ(364FZ) 밀도-수익 충돌 재혼합으로 넘깁니다.

- judgment(판정): `negative_profit_density_dual_anchor_rejoin_review_density_recovered_oos_profit_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `fx_sym_h1_m0p75__fx_profit_density_dual__et8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `0.474` / `1.0004002915` / `3.0601092896`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-77.441` / `0.8928911277` / `2.8396946565`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-300.641`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `-76.967` / `2.9681528662` / `-636.167` / `0.7693133047`
- density3_all_splits_count(전 분할 밀도3 수): `162`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `1176`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fy_selected_candidate(선택 후보) | true | fx_sym_h1_m0p75__fx_profit_density_dual__et8_l18_n132 | 0.474 | 3.0601092896 | -77.441 | 0.8928911277 | 2.8396946565 | -300.641 | -636.167 | 선택 후보는 density(밀도)를 일부 회복했지만 OOS profit(표본외 수익)이 다시 음수입니다. |
| fy_best_oos_positive(표본외 양수 상위) | true | fx_asym_h2_l0p75_s1p5__fx_profit_density_dual__rf8_l22_n132 | -41.871 | 2.7759562842 | 11.99 | 1.01581427 | 2.5648854962 | -189.61 | -536.281 | 표본외 양수 행은 아직 저밀도 수익 단서입니다. |
| fy_best_density3(밀도3 상위) | true | fx_sym_h1_m0p75__fx_all72__rf8_l22_n132 | -2.984 | 3.3278688525 | -114.676 | 0.8716285651 | 3.5267175573 | -391.876 | -760.26 | 전 분할 density3(밀도3)는 회복됐지만 수익이 깨졌습니다. |
| fy_oos_pf125_cost09(표본외 PF125 비용0.9) | true | fx_asym_h2_l0p75_s1p5__fx_profit_density_dual__et8_l18_n132 | 174.834 | 1.3333333333 | 178.188 | 1.469830723 | 1.2671755725 | 78.588 | 107.022 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)는 아직 저밀도 단서입니다. |
| fy_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fy01_density_recovered | density3_all_splits_count=162; selected_density=3.0601092896/2.8396946565/2.9681528662 | wide density hour sets(넓은 밀도 시간 집합)와 density target(밀도 목표)이 전 분할 density3(밀도3)를 일부 회복했습니다. | salvage_clue(회수 단서) | FZ(364FZ)는 이 밀도 앵커를 보존하되 수익 손실을 다시 줄여야 합니다. |
| fy02_oos_profit_failed | selected_oos_net=-77.441; selected_oos_pf=0.8928911277; density3_all_splits_valpos_oospos_count=0 | density3(밀도3)를 회복하는 쪽에서는 OOS net/PF(표본외 순수익/수익 팩터)가 다시 음수로 무너졌습니다. | high(높음) | package(패키지)를 거절하고 density-profit conflict reblend(밀도-수익 충돌 재혼합)로 넘깁니다. |
| fy03_cost_and_short_stress | selected_combined_cost09_net=-636.167; selected_short_share=0.7693133047 | 선택 후보는 비용 압박(cost stress, 비용 압박)과 숏 비중(short share, 숏 비중)이 남았습니다. | medium(중간) | 다음 실행에서 비용과 방향 균형을 보조 제약으로 둡니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | density3 rows recovered but validation_positive_density3_count=0, OOS net/PF failed, combined_cost09<0, strict_candidate_count=0 | not_opened | not_run | 밀도 회복을 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| fy01_density_recovered_oos_profit_failed | density3 plus OOS profit(밀도3과 표본외 수익 동시 충족) | selected_oos_net=-77.441; selected_oos_pf=0.8928911277; density3_all_splits_count=162; selected_density=3.0601092896/2.8396946565/2.9681528662 | density3_all_splits_count=162; max_oos_pf=1.5213167477; oos_pf125_cost09_count=1176 | validation/OOS/combined density stay >=3 while OOS net/PF turn positive(전 분할 밀도3 유지와 표본외 순수익/수익 팩터 양수 전환) | Do not recover density3 by accepting OOS-negative rows(표본외 음수 행으로 밀도3만 회복하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 | fz01_density_profit_conflict_reblend | density3 negative rows(밀도3 음수 행)와 low-density OOS-positive rows(저밀도 표본외 양수 행)를 conflict constraints(충돌 제약)로 재혼합하면 밀도와 수익의 동시 회복 가능성을 다시 열 수 있습니다. | OOS net>0, OOS PF>=1.05, validation_net>0(표본외/검증 수익 보존) | validation_density>=3, oos_density>=3, combined_density>=3, combined_cost09 improves(밀도3 및 비용 개선) | OOS-positive low-density rows and density-only OOS-negative rows(표본외 양수 저밀도 행과 밀도 전용 표본외 음수 행) | FZ는 밀도 행과 저밀도 수익 행의 충돌 조건을 다시 혼합합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/fy_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/fy_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/fy_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/fy_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/fy_fz_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FY/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
