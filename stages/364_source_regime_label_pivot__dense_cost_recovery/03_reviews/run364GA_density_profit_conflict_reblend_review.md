# run364GA Density Profit Conflict Reblend Review(밀도 수익 충돌 재혼합 검토)

Created(생성): 2026-06-07T08:30:58Z

Action(행동): FZ proxy/ONNX smoke(FZ 프록시/ONNX 간이 검증) 결과를 profit-density failure(수익-밀도 실패), cost/short stress(비용/숏 압박), session-side loss(세션/방향 손실), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 충돌 재혼합 결과를 운영 후보로 올리지 않고 GB(364GB) session/side loss veto rescue(세션/방향 손실 차단 회수)로 넘깁니다.

- judgment(판정): `negative_density_profit_conflict_reblend_review_profit_and_density_worse_no_package_no_authority`
- selected_model_id(선택 모델 ID): `fz_sym_h1_m0p65__fz_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `-95.425` / `0.9025867965` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-107.009` / `0.8470401907` / `2.786259542`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-326.009`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `-202.434` / `2.7420382166` / `-719.034` / `0.7944250871`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `2430`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`

## Diagnostics(진단)

| diagnostic_id | row_found | model_id | validation_net | validation_density | oos_net | oos_profit_factor | oos_density | oos_cost09_net | combined_cost09_net | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ga_selected_candidate(선택 후보) | true | fz_sym_h1_m0p65__fz_all72__rf8_l18_n132 | -95.362 | 2.7158469945 | -107.009 | 0.8470401907 | 2.786259542 | -326.009 | -719.571 | 선택 후보는 validation/OOS profit(검증/표본외 수익)과 density(밀도)가 모두 악화됐습니다. |
| ga_best_oos_positive(표본외 양수 상위) | true | fz_asym_h2_l0p65_s1p35__fz_conflict_blend__et7_l10_n132 | 136.281 | 2.0710382514 | 111.798 | 1.1859967558 | 1.8167938931 | -31.002 | -122.121 | 표본외 양수 행은 아직 저밀도 수익 단서입니다. |
| ga_best_density3(밀도3 상위) | false |  |  |  |  |  |  |  |  | 전 분할 density3(밀도3) 후보가 남아 있는지 확인합니다. |
| ga_oos_pf125_cost09(표본외 PF125 비용0.9) | true | fz_asym_h2_l0p65_s1p35__fz_conflict_blend__rf8_l18_n132 | -79.149 | 1.1147540984 | 205.511 | 1.7040627901 | 1.1679389313 | 113.711 | -87.838 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)가 남아 있는지 확인합니다. |
| ga_strict_like(엄격 유사) | false |  |  |  |  |  |  |  |  | 엄격 유사 행은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| ga01_profit_and_density_worse | density3_all_splits_count=0; selected_density=2.7103825137/2.786259542/2.7420382166 | conflict reblend(충돌 재혼합)가 밀도 바닥과 표본외 수익을 동시에 살리지 못했습니다. | high(높음) | GB(364GB)는 전역 재혼합보다 session/side loss veto(세션/방향 손실 차단)를 먼저 적용해야 합니다. |
| ga02_oos_profit_failed | selected_oos_net=-107.009; selected_oos_pf=0.8470401907; density3_all_splits_valpos_oospos_count=0 | 선택 후보는 OOS net/PF(표본외 순수익/수익 팩터)가 FX보다 더 나빠졌습니다. | high(높음) | package(패키지)를 거절하고 session/side loss veto rescue(세션/방향 손실 차단 회수)로 넘깁니다. |
| ga03_session_side_loss | selected_combined_cost09_net=-719.034; selected_short_share=0.7944250871 | 선택 후보는 비용 압박(cost stress, 비용 압박)과 방향/세션 손실(side/session loss, 방향/세션 손실)이 남았습니다. | medium(중간) | 다음 실행에서 16-17시 롱 손실과 20시 숏 손실을 보조 제약으로 둡니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | FZ selected validation/OOS net are both negative, density is below 3, combined_cost09<0, strict_candidate_count=0(FZ 선택 검증/표본외 순수익 모두 음수, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0) | not_opened | not_run | 충돌 재혼합 결과를 운영 가능한 후보로 과장하지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition | do_not_repeat |
| --- | --- | --- | --- | --- | --- |
| ga01_conflict_reblend_profit_and_density_worse | density3 plus OOS profit(밀도3과 표본외 수익 동시 충족) | selected_oos_net=-107.009; selected_oos_pf=0.8470401907; density3_all_splits_count=0; selected_density=2.7103825137/2.786259542/2.7420382166 | max_oos_pf=1.7136822919; max_oos_cost09_net=113.711; positive months/sessions need veto review(양수 월/세션은 차단 검토 필요) | session/side veto removes worst loss clusters while preserving OOS net>0 and density near or above 3(세션/방향 차단이 최악 손실 군집을 제거하면서 표본외 순수익 양수와 밀도 3 근접/이상을 보존) | Do not use global conflict reblend without session/side loss constraints(세션/방향 손실 제약 없는 전역 충돌 재혼합을 반복하지 말 것). |

## Next Queue(다음 대기열)

| next_run_id | queue_id | hypothesis | required_preserve | required_repair | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 | gb01_session_side_loss_veto_rescue | FZ loss clusters(FZ 손실 군집), especially 16-17 long loss(16-17시 롱 손실) and 20 short loss(20시 숏 손실), can be vetoed while preserving surviving short 18/session profit(18시 숏/세션 수익)을 보존하면 표본외 수익과 밀도 균형을 다시 열 수 있습니다. | OOS net>0, OOS PF>=1.05, validation_net>0, trade density near 3(표본외/검증 수익과 밀도 3 근접 보존) | lossy long 16-17 and short 20 clusters vetoed, combined_cost09 improves(손실 롱 16-17과 숏 20 군집 차단 및 합산 비용 개선) | global reblend without session/side constraints(세션/방향 제약 없는 전역 재혼합) | GB는 FZ 손실 군집을 차단해 수익과 밀도를 다시 분리하지 않도록 시험합니다. |

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/required_gate_coverage_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/ga_review_summary.csv
- surface_overlap_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/ga_surface_diagnostic.csv
- failure_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/ga_failure_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/ga_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/ga_gb_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/result_judgment_receipt.json
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GA/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
