# run364GG Profit-Floor Density Lift Review(수익 바닥 밀도 상승 검토)

Created(생성): 2026-06-07T10:15:13Z

Action(행동): GF proxy/ONNX smoke(GF 프록시/ONNX 온엑스 간이 검증) 결과를 validation lift(검증 상승), OOS floor preserve(표본외 바닥 보존), density3 failure(밀도3 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 개선된 검증/표본외 단서를 보존하되 운영 후보로 올리지 않고 GH density3 profit-floor repair(GH 밀도3 수익 바닥 수리)로 넘깁니다.

- judgment(판정): `negative_profit_floor_density_lift_review_validation_improved_density_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gf_sym_h1_m0p50__gf_profit_density_blend__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `78.008` / `1.101326856` / `2.2568306011`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `83.438` / `1.2040677568` / `1.9694656489`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-71.362`
- OOS cost0.6 net(표본외 비용0.6 순수익): `6.038`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `161.446` / `2.1369426752` / `-241.154` / `0.7615499255`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- max_combined_cost09_net(최대 합산 비용0.9 순수익): `39.212`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gg_selected_candidate(선택 후보) | true | gf_sym_h1_m0p50__gf_profit_density_blend__rf8_l18_n132 | 78.008 | 2.2568306011 | 83.438 | 1.2040677568 | 1.9694656489 | -71.362 | -241.154 | 선택 후보는 validation net(검증 순수익)을 개선하고 OOS floor(표본외 바닥)를 보존했지만 density3(밀도3)은 실패했습니다. |
| gg_best_oos_positive(표본외 양수 상위) | true | gf_sym_h1_m0p50__gf_profit_density_blend__rf8_l18_n132 | 78.008 | 2.2568306011 | 83.438 | 1.2040677568 | 1.9694656489 | -71.362 | -241.154 | 표본외 양수 후보의 밀도와 비용 상태를 확인합니다. |
| gg_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | 전 분할 density3(밀도3) 후보가 수익을 보존하는지 확인합니다. |
| gg_oos_pf125_cost09(표본외 PF125 비용0.9) | true | gf_sym_h2_m0p50__gf_cost_session_regime__rf8_l18_n132 | 66.797 | 0.7868852459 | 121.215 | 1.6967780875 | 0.7938931298 | 58.815 | 39.212 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다. |
| gg_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행이 있는지 확인합니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| gg01_validation_profit_improved_oos_floor_preserved | validation_net=78.008; oos_pf=1.2040677568; oos_cost06=6.038 | profit-floor density lift(수익 바닥 밀도 상승)가 validation net(검증 순수익)을 개선하고 OOS PF/cost0.6(표본외 수익 팩터/비용0.6)을 보존했습니다. | salvage_clue(회수 단서) | GH(364GH)는 이 수익 바닥을 유지하면서 density3(밀도3)을 다시 공격해야 합니다. |
| gg02_density3_failed | density3_all_splits_count=0; selected_density=2.2568306011/1.9694656489/2.1369426752 | 선택 후보는 validation net(검증 순수익)이 좋아졌지만 density(밀도)가 3 미만입니다. | high(높음) | package(패키지)를 거절하고 density3 profit-floor repair(밀도3 수익 바닥 수리)로 넘깁니다. |
| gg03_cost09_still_negative | selected_combined_cost09_net=-241.154; max_combined_cost09_net=39.212 | combined cost0.9(합산 비용0.9)는 아직 음수입니다. | medium(중간) | 다음 실행에서 cost0.9(비용0.9) 개선을 보조 제약으로 유지합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | GF improved validation and preserved OOS floor but density is below 3, combined_cost09<0, strict_candidate_count=0(GF 검증 개선, 표본외 바닥 보존, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0) | not_opened | not_run | 좋아진 프록시 단서를 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| gg01_validation_improved_density3_failed | validation plus OOS floor plus density plus cost(검증과 표본외 바닥과 밀도와 비용 동시 충족) | selected_validation_net=78.008; selected_oos_pf=1.2040677568; density3_all_splits_count=0; selected_density=2.2568306011/1.9694656489/2.1369426752 | selected_validation_net=78.008; selected_oos_net=83.438; selected_oos_pf=1.2040677568; selected_oos_cost06=6.038 | preserve validation net, OOS net/PF, and OOS cost0.6 while lifting density toward 3(검증 순수익, 표본외 순수익/수익 팩터, 표본외 비용0.6을 보존하며 밀도3으로 상승) | Do not improve validation by starving density or losing OOS cost0.6(밀도를 굶기거나 표본외 비용0.6을 잃으며 검증만 개선하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 | gh01_density3_profit_floor_repair | GF validation lift(GF 검증 상승)와 OOS profit floor(표본외 수익 바닥)를 고정하고 density target(밀도 목표)을 더 공격하면 density3(밀도3)에 접근할 수 있습니다. | validation net>0, OOS net>0, OOS PF>=1.10, OOS cost0.6>=0(검증/표본외 수익 바닥 보존) | density lift toward 3 and combined_cost09 improves(밀도 3 접근과 합산 비용0.9 개선) | low-density validation-only optimization(저밀도 검증 전용 최적화) | GH는 GF의 검증 개선을 보존하면서 부족한 거래 밀도를 다시 공격합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/gg_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/gg_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/gg_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/gg_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/gg_gh_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GG/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
