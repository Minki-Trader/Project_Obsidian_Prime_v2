# run364FU Regime Profit Density Reexpand Review(국면 수익 밀도 재확장 검토)

Created(생성): 2026-06-07T06:46:49Z

Action(행동): FT proxy/ONNX smoke(FT 프록시/ONNX 스모크) 결과를 density recovery(밀도 회복), OOS profit failure(표본외 수익 실패), cost stress(비용 압박), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 밀도 회복 단서를 보존하되, 운영 후보나 runtime authority(런타임 권위)로 올리지 않고 FV(364FV) 수리 조건으로 넘깁니다.

- judgment(판정): `negative_regime_profit_density_reexpand_review_density_recovered_profit_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `ft_sym_h1_m0p75__ft_session_regime_broad__rf8_l24_n176`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `100.978` / `1.0922701014` / `3.3715846995`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-79.583` / `0.8976134726` / `3.106870229`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-323.783`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `21.395` / `3.2611464968` / `-593.005` / `0.7490234375`
- density3_all_splits_count(전 분할 밀도3 수): `246`
- validation_positive_density3_count(검증 양수 밀도3 수): `54`
- density3_all_splits_valpos_oospos_count(전 분할 밀도3 검증/표본외 양수 수): `0`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `2652`
- oos_pf125_cost09_density3_count(표본외 PF125 비용0.9 밀도3 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fu_selected_candidate(선택 후보) | true | ft_sym_h1_m0p75__ft_session_regime_broad__rf8_l24_n176 | 100.978 | 3.3715846995 | -79.583 | 0.8976134726 | 3.106870229 | -323.783 | -593.005 | 선택 후보는 density3(밀도3)를 회복했지만 OOS(표본외) 손익과 비용이 약합니다. |
| fu_best_density3_by_oos_net(밀도3 중 표본외 순수익 상위) | true | ft_sym_h1_m0p75__ft_all72__rf8_l24_n176 | -149.906 | 3.1092896175 | -28.485 | 0.9633165874 | 3.2061068702 | -280.485 | -771.791 | 전 분할 density3(밀도3)는 회복됐지만 최고 OOS(표본외) 손익도 양수가 아닙니다. |
| fu_validation_positive_density3(검증 양수 밀도3) | true | ft_sym_h1_m0p75__ft_session_regime_broad__rf8_l24_n176 | 100.978 | 3.3715846995 | -79.583 | 0.8976134726 | 3.106870229 | -323.783 | -593.005 | 검증 양수 밀도3 행은 다음 FV(364FV)의 보존 단서입니다. |
| fu_oos_pf125_cost09_low_density(표본외 PF125 비용0.9 저밀도) | true | ft_sym_h2_m1p0__ft_profit_density_broad__et8_l18_n176 | 41.301 | 1.3715846995 | 201.908 | 1.5656018982 | 1.2671755725 | 102.308 | -6.991 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)는 아직 저밀도 단서입니다. |
| fu_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fu01_density_recovered | density3_all_splits_count=246; validation_positive_density3_count=54; selected_density=3.3715846995/3.106870229/3.2611464968 | broad hour/filter(넓은 시간/필터)와 lower label barrier(낮은 라벨 장벽)가 거래수를 회복했습니다. | salvage_clue(회수 단서) | FV(364FV)는 density3(밀도3)를 버리지 않고 OOS profit(표본외 수익)을 고쳐야 합니다. |
| fu02_oos_profit_failed | selected_oos_net=-79.583; selected_oos_pf=0.8976134726; density3_all_splits_valpos_oospos_count=0 | density reexpand(밀도 재확장)이 OOS edge(표본외 엣지)를 희석했습니다. | high(높음) | package(패키지)를 거절하고 density3+OOS profit bridge(밀도3+표본외 수익 연결)를 다음 작업으로 엽니다. |
| fu03_cost_stress_worsened | selected_oos_cost09_net=-323.783; selected_combined_cost09_net=-593.005; max_oos_cost09_net=102.308 | high-density trades(고밀도 거래)가 비용 압박(cost stress, 비용 압박)을 키웠습니다. | high(높음) | 비용 양수 단서는 저밀도라서 운영 후보로 올리지 않습니다. |
| fu04_onnx_smoke_not_authority | onnx_smoke_pass_rows=36; new_mt5_execution=not_run | ONNX smoke(ONNX 스모크)는 변환 일치만 확인하고 MT5(메타트레이더5) 실행 근거가 아닙니다. | guardrail(가드레일) | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | density recovered but selected_oos_net<0, selected_oos_pf<1, combined_cost09<0, strict_candidate_count=0 | not_opened | not_run | 밀도 회복을 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| fu01_density_recovered_profit_failed | density3 plus OOS profit(밀도3과 표본외 수익 동시 충족) | density3_all_splits_count=246; density3_all_splits_valpos_oospos_count=0; selected_oos_net=-79.583; selected_combined_cost09_net=-593.005 | validation_positive_density3_count=54; selected_validation_net=100.978; selected_combined_density=3.2611464968; max_oos_pf=1.5656018982 | density3_all_splits_valpos_oospos_count>0 and OOS PF>=1.05 while validation/combined density stay >=3(밀도3 양수 교차와 표본외 PF 1.05 이상) | Do not solve density by accepting OOS negative and cost-stressed rows(표본외 음수와 비용 압박 행으로 밀도만 해결하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 | fv01_density3_oos_profit_bridge | FT의 density3(밀도3) 회복 단서를 고정하고 OOS profit/PF(표본외 수익/수익 팩터)를 직접 보상하면 전 분할 양수 행을 만들 수 있습니다. | validation_density>=3, oos_density>=3, combined_density>=3, validation_net>0(밀도3과 검증 수익 보존) | oos_net>0, oos_pf>=1.05, combined_cost09 improves, density3_all_splits_valpos_oospos_count>0(표본외 수익과 비용 개선) | density-only negative OOS rows and low-density cost-only rows(밀도 전용 표본외 음수와 저밀도 비용 전용 행) | FV는 밀도 회복을 유지한 채 표본외 수익을 다시 연결합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/fu_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/fu_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/fu_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/fu_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/fu_fv_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FU/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
