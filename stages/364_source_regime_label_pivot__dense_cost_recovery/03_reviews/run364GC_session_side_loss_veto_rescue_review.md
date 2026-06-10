# run364GC Session Side Loss Veto Rescue Review(세션 방향 손실 차단 회수 검토)

Created(생성): 2026-06-07T09:02:36Z

Action(행동): GB proxy/ONNX smoke(GB 프록시/ONNX 간이 검증) 결과를 profit recovery(수익 회복), density failure(밀도 실패), cost/short stress(비용/숏 압박), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 수익 회복 단서를 보존하되 운영 후보로 올리지 않고 GD(364GD) profit-preserving density recovery(수익 보존 밀도 회복)로 넘깁니다.

- judgment(판정): `negative_session_side_loss_veto_rescue_review_profit_recovered_density_cost_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gb_sym_h1_m0p60__gb_oos_profit_regime__rf8_l20_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `49.565` / `1.0554349516` / `2.5464480874`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `60.74` / `1.1268140527` / `2.106870229`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-104.86`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `110.305` / `2.3630573248` / `-334.895` / `0.8477088949`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `1548`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gc_selected_candidate(선택 후보) | true | gb_sym_h1_m0p60__gb_oos_profit_regime__rf8_l20_n132 | 49.565 | 2.5464480874 | 60.74 | 1.1268140527 | 2.106870229 | -104.86 | -334.895 | 선택 후보는 validation/OOS profit(검증/표본외 수익)을 회복했지만 density/cost(밀도/비용)가 실패했습니다. |
| gc_best_oos_positive(표본외 양수 상위) | true | gb_sym_h1_m0p60__gb_oos_profit_regime__rf8_l20_n132 | 49.565 | 2.5464480874 | 60.74 | 1.1268140527 | 2.106870229 | -104.86 | -334.895 | 표본외 양수 행의 밀도와 비용 상태를 확인합니다. |
| gc_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | 전 분할 density3(밀도3) 후보가 수익을 보존하는지 확인합니다. |
| gc_oos_pf125_cost09(표본외 PF125 비용0.9) | true | gb_sym_h2_m0p60__gb_session_side_blend__et8_l16_n132 | -101.72 | 1.1639344262 | 136.394 | 1.6404165708 | 0.786259542 | 74.594 | -154.926 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다. |
| gc_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| gc01_profit_recovered | density3_all_splits_count=0; selected_density=2.5464480874/2.106870229/2.3630573248 | session/side veto(세션/방향 차단)가 validation/OOS profit(검증/표본외 수익)을 양수로 돌렸습니다. | salvage_clue(회수 단서) | GD(364GD)는 이 수익 회복을 보존하면서 밀도와 비용을 수리해야 합니다. |
| gc02_density_cost_failed | selected_oos_net=60.74; selected_oos_pf=1.1268140527; density3_all_splits_valpos_oospos_count=0 | 선택 후보는 density(밀도)가 3 미만이고 cost0.9(비용0.9)가 음수입니다. | high(높음) | package(패키지)를 거절하고 profit-preserving density recovery(수익 보존 밀도 회복)로 넘깁니다. |
| gc03_short_skew_remaining | selected_combined_cost09_net=-334.895; selected_short_share=0.8477088949 | 선택 후보는 short share(숏 비중)가 높고 비용 압박(cost stress, 비용 압박)이 남았습니다. | medium(중간) | 다음 실행에서 숏 비중과 비용을 보조 제약으로 둡니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | GB recovered validation/OOS profit but density is below 3, combined_cost09<0, strict_candidate_count=0(GB 검증/표본외 수익 회복, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0) | not_opened | not_run | 수익 회복 단서를 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| gc01_profit_recovered_density_cost_failed | profit plus density plus cost(수익과 밀도와 비용 동시 충족) | selected_oos_net=60.74; selected_oos_pf=1.1268140527; density3_all_splits_count=0; selected_density=2.5464480874/2.106870229/2.3630573248 | selected_validation_net=49.565; selected_oos_net=60.74; max_oos_pf=1.7916754608; max_combined_cost09_net=129.923 | preserve validation/OOS profit while raising density toward 3 and improving cost0.9(검증/표본외 수익 보존, 밀도 3 근접/이상, 비용0.9 개선) | Do not raise density by giving back OOS profit(표본외 수익을 반납하면서 밀도만 올리지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 | gd01_profit_preserving_density_recovery | GB profit recovery(GB 수익 회복)를 보존하면서 density target(밀도 목표)과 cost repair(비용 수리)를 다시 올리면 운영 후보 전 단계의 균형을 회복할 수 있습니다. | validation_net>0, OOS net>0, OOS PF>=1.05(검증/표본외 수익 보존) | validation_density/oos_density/combined_density move toward 3 and combined_cost09 improves(전 분할 밀도 3 접근과 합산 비용0.9 개선) | density-only negative recovery(수익 반납형 밀도 회복) | GD는 GB 수익 회복을 바닥 조건으로 고정하고 밀도와 비용을 다시 수리합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/gc_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/gc_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/gc_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/gc_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/gc_gd_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GC/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
