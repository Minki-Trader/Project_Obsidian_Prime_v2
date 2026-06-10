# run364FW Density3 OOS Profit Bridge Review(밀도3 표본외 수익 연결 검토)

Created(생성): 2026-06-07T07:16:28Z

Action(행동): FV proxy/ONNX smoke(FV 프록시/ONNX 스모크) 결과를 OOS profit recovery(표본외 수익 회복), density loss(밀도 손실), cost/short stress(비용/숏 압박), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 표본외 수익 단서를 보존하되, 밀도3 손실 때문에 운영 후보로 올리지 않고 FX(364FX) 이중 앵커 재결합으로 넘깁니다.

- judgment(판정): `negative_density3_oos_profit_bridge_review_oos_profit_recovered_density_lost_no_package_no_authority`
- selected_model_id(선택 모델 ID): `fv_sym_h1_m0p75__fv_all72__rf8_l24_n144`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `31.787` / `1.0383962641` / `2.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `34.163` / `1.0632477145` / `2.2671755725`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-144.037`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `65.95` / `2.3184713376` / `-370.85` / `0.8104395604`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `1395`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fw_selected_candidate(선택 후보) | true | fv_sym_h1_m0p75__fv_all72__rf8_l24_n144 | 31.787 | 2.3551912568 | 34.163 | 1.0632477145 | 2.2671755725 | -144.037 | -370.85 | 선택 후보는 OOS profit(표본외 수익)을 회복했지만 density(밀도)가 3/day(일 3회) 아래입니다. |
| fw_best_oos_positive(표본외 양수 상위) | true | fv_sym_h1_m0p75__fv_all72__rf8_l24_n144 | 31.787 | 2.3551912568 | 34.163 | 1.0632477145 | 2.2671755725 | -144.037 | -370.85 | 표본외 양수 행은 생겼지만 밀도3 앵커가 약합니다. |
| fw_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | FV 표면에는 전 분할 density3(밀도3) 행이 없습니다. |
| fw_oos_pf125_cost09(표본외 PF125 비용0.9) | true | fv_sym_h2_m1p0__fv_all72__et7_l12_n144 | 180.611 | 1.4098360656 | 198.599 | 1.581503073 | 1.2061068702 | 103.799 | 129.61 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)는 아직 저밀도 단서입니다. |
| fw_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fw01_oos_profit_recovered | selected_oos_net=34.163; selected_oos_pf=1.0632477145; max_oos_pf=1.581503073 | OOS profit bridge score(표본외 수익 연결 점수)가 OOS net/PF(표본외 순수익/수익 팩터)를 회복했습니다. | salvage_clue(회수 단서) | FX(364FX)는 이 표본외 수익 앵커를 보존해야 합니다. |
| fw02_density_lost | density3_all_splits_count=0; selected_density=2.3551912568/2.2671755725/2.3184713376 | OOS profit(표본외 수익)을 보상하면서 density3(밀도3) 바닥이 사라졌습니다. | high(높음) | package(패키지)를 거절하고 profit-density dual anchor(수익-밀도 이중 앵커) 재결합으로 넘깁니다. |
| fw03_cost_and_short_stress | selected_combined_cost09_net=-370.85; selected_short_share=0.8104395604 | 선택 후보는 비용 압박(cost stress, 비용 압박)과 숏 비중(short share, 숏 비중)이 남았습니다. | medium(중간) | 다음 실행에서 비용과 방향 균형을 보조 제약으로 둡니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | OOS profit recovered but density3_all_splits_count=0, selected_density<3, combined_cost09<0, strict_candidate_count=0 | not_opened | not_run | 표본외 수익 회복을 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| fw01_oos_profit_recovered_density_lost | OOS profit plus density3(표본외 수익과 밀도3 동시 충족) | selected_oos_net=34.163; selected_oos_pf=1.0632477145; density3_all_splits_count=0; selected_density=2.3551912568/2.2671755725/2.3184713376 | selected_oos_net=34.163; selected_oos_pf=1.0632477145; max_oos_pf=1.581503073; oos_pf125_cost09_count=1395 | OOS net/PF stay positive while validation/OOS/combined density return >=3(표본외 순수익/수익 팩터 양수 유지와 전 분할 밀도3 회복) | Do not recover OOS profit by dropping below density3(밀도3 아래로 내려가서 표본외 수익만 회복하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 | fx01_profit_density_dual_anchor_rejoin | FT density anchor(FT 밀도 앵커)와 FV OOS profit anchor(FV 표본외 수익 앵커)를 같은 score(점수) 안에서 이중 앵커로 묶으면 density3와 OOS profit을 동시에 되살릴 수 있습니다. | OOS net>0, OOS PF>=1.05, validation_net>0(표본외/검증 수익 보존) | validation_density>=3, oos_density>=3, combined_density>=3, combined_cost09 improves(밀도3 및 비용 개선) | OOS-positive low-density rows and density-only OOS-negative rows(표본외 양수 저밀도 행과 밀도 전용 표본외 음수 행) | FX는 두 회차의 반쪽 단서를 한 표면에서 다시 결합합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/fw_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/fw_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/fw_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/fw_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/fw_fx_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FW/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
