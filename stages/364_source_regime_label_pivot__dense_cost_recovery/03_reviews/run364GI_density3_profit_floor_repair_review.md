# run364GI Density3 Profit-Floor Repair Review(밀도3 수익 바닥 수리 검토)

Created(생성): 2026-06-07T10:51:28Z

Action(행동): GH proxy/ONNX smoke(GH 프록시/ONNX 온엑스 간이 검증) 결과를 density lift(밀도 상승), cost-floor failure(비용 바닥 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 밀도 공급 단서는 보존하되 운영 후보로 올리지 않고 GJ density-cost floor rejoin(GJ 밀도-비용 바닥 재결합)으로 넘깁니다.

- judgment(판정): `negative_density3_profit_floor_repair_review_density_lift_cost_floor_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gh_sym_h1_m0p35__gh_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `0.439` / `1.0005209817` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `82.117` / `1.1481991485` / `2.6870229008`
- selected OOS cost0.6/cost0.9 net(선택 표본외 비용0.6/비용0.9 순수익): `-23.483` / `-129.083`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `82.556` / `2.7006369427` / `-426.244` / `0.6827830189`
- density275_all_splits_count(전 분할 밀도2.75 수): `30`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gi_selected_candidate(선택 후보) | true | gh_sym_h1_m0p35__gh_all72__rf8_l18_n132 | 2.977 | 2.7158469945 | 82.117 | 1.1481991485 | 2.6870229008 | -129.083 | -424.306 | 선택 후보는 density(밀도)를 크게 올렸지만 validation/cost floor(검증/비용 바닥)가 약해졌습니다. |
| gi_best_density275(밀도2.75 상위) | true | gh_sym_h1_m0p35__gh_cost_session_regime__rf8_l18_n132 | -121.274 | 2.7759562842 | -203.506 | 0.7325885454 | 2.9083969466 | -432.106 | -858.18 | 전 분할 density2.75(밀도2.75) 이상 후보가 수익을 보존하는지 확인합니다. |
| gi_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | 전 분할 density3(밀도3) 후보가 있는지 확인합니다. |
| gi_oos_pf125_cost09(표본외 PF125 비용0.9) | true | gh_sym_h2_m0p35__gh_density_profit_blend__et8_l14_n132 | 52.306 | 1.1092896175 | 84.919 | 1.3036161206 | 0.9389312977 | 11.119 | -58.375 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다. |
| gi_cost_floor_rejoin(비용 바닥 재결합) | true | gh_sym_h2_m0p35__gh_density_profit_blend__et8_l14_n132 | 37.936 | 1.825136612 | 62.674 | 1.1382921447 | 1.4809160305 | -53.726 | -216.19 | 수익 바닥을 보존한 후보의 밀도 상한을 확인합니다. |
| gi_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행이 있는지 확인합니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| gi01_density_lift_salvage | selected_density=2.7103825137/2.6870229008/2.7006369427; density275_count=30 | lower threshold and wider hours(낮은 임계값과 넓은 시간)이 density supply(밀도 공급)를 실제로 늘렸습니다. | salvage_clue(회수 단서) | GJ(364GJ)는 이 밀도 공급을 유지하면서 cost floor(비용 바닥)를 다시 붙여야 합니다. |
| gi02_cost_floor_failed | selected_oos_cost06_net=-23.483; selected_combined_cost09_net=-426.244; selected_validation_net=0.439 | density lift(밀도 상승)가 cost0.6/cost0.9(비용0.6/비용0.9)와 validation net(검증 순수익)을 약화했습니다. | high(높음) | package(패키지)를 거절하고 density-cost floor rejoin(밀도-비용 바닥 재결합)으로 넘깁니다. |
| gi03_no_density3_yet | density3_all_splits_count=0; max_combined_density=2.8312101911 | density3(밀도3)에는 아직 도달하지 못했습니다. | medium(중간) | 다음 실행에서 밀도 공급은 유지하되 손실 구간을 잘라야 합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | GH lifted density but validation net is near flat, OOS cost0.6<0, combined cost0.9<0, strict_candidate_count=0(GH 밀도 상승, 검증 순수익 거의 평탄, 표본외 비용0.6 음수, 합산 비용0.9 음수, 엄격 후보 0) | not_opened | not_run | 밀도 개선 단서를 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| gi01_density_lift_cost_floor_failed | density lift plus validation/OOS/cost floor(밀도 상승과 검증/표본외/비용 바닥 동시 충족) | selected_density=2.7103825137/2.6870229008/2.7006369427; selected_validation_net=0.439; selected_oos_cost06=-23.483; selected_combined_cost09=-426.244 | density275_all_splits_count=30; selected_oos_net=82.117; selected_oos_pf=1.1481991485; max_combined_density=2.8312101911 | preserve combined density near 2.7 while restoring validation net and OOS cost0.6(합산 밀도 2.7 근처를 보존하며 검증 순수익과 표본외 비용0.6 복구) | Do not chase density by accepting cost-floor collapse(비용 바닥 붕괴를 받아들이며 밀도만 추적하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 | gj01_density_cost_floor_rejoin | GH density lift(GH 밀도 상승)를 유지하면서 cost guard(비용 가드)와 validation floor(검증 바닥)를 다시 붙이면 density-cost balance(밀도-비용 균형)가 개선될 수 있습니다. | combined density near 2.6+, OOS net>0, OOS PF>=1.05(합산 밀도 2.6 이상 근처, 표본외 순수익 양수, 표본외 수익 팩터 1.05 이상) | validation net lift, OOS cost0.6>=0, combined_cost09 improves(검증 순수익 상승, 표본외 비용0.6 0 이상, 합산 비용0.9 개선) | density-only cost collapse(밀도 전용 비용 붕괴) | GJ는 GH의 밀도 공급을 잃지 않으면서 비용과 검증 바닥을 다시 붙입니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/gi_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/gi_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/gi_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/gi_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/gi_gj_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GI/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
