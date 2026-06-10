# run364FO Density Cost Decoupled Bridge Review(밀도 비용 분리 연결 검토)

Created(생성): 2026-06-07T04:59:15Z

Action(행동): FN density cost decoupled bridge(FN 밀도 비용 분리 연결)를 package decision(패키지 결정), failure memory(실패 기억), FP queue(FP 대기열)로 검토했습니다.

Effect(효과): strict candidate(엄격 후보)가 없는 proxy(프록시) 결과를 운영 후보로 올리지 않고, 다음 탐색을 positive density floor(양수 밀도 바닥) 복구로 좁힙니다.

- judgment(판정): `negative_density_cost_decoupled_bridge_review_density_pf_overlap_absent_no_package_no_authority`
- selected model(선택 모델): `fn_sym_h2_m1p25__fn_cost_leg__rf9_l18_n192`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `136.115` / `1.1130419978` / `2.8743169399`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-40.679` / `0.9500226673` / `2.7938931298`
- OOS cost0.9(표본외 비용0.9): `-260.279`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `2.8407643312` / `-439.764` / `0.730941704`
- validation_positive_density3_count(검증 양수 밀도3 수): `0`
- density3_all_splits_count(전 분할 밀도3 수): `5`
- density3_all_splits_oos_pf105_count(전 분할 밀도3과 표본외 PF105 동시 수): `0`
- oos_pf125_cost09_count(표본외 PF125와 비용0.9 수): `9510`
- oos_pf125_cost09_density3_count(표본외 PF125/비용0.9/밀도3 동시 수): `0`
- next_run_id(다음 실행 ID): `run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | oos_density | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fo_selected_candidate(선택 후보) | fn_sym_h2_m1p25__fn_cost_leg__rf9_l18_n192 | 136.115 | 2.8743169399 | 0.9500226673 | -260.279 | 2.7938931298 | 2.8407643312 | -439.764 | 0.730941704 | 선택 후보는 validation(검증) 수익은 있었지만 OOS(표본외) 수익과 비용에서 무너졌습니다. |
| fo_oos_pf125_cost09(표본외 PF125 비용0.9) | fn_sym_h2_m1p5__fn_density_leg__et9_l14_n192 | 168.464 | 1.8087431694 | 1.2994442551 | 18.8 | 1.6946564885 | 1.7611464968 | -11.336 | 0.6473779385 | OOS PF125(표본외 수익 팩터 1.25)와 cost0.9(비용0.9)는 낮은 밀도 영역에만 남았습니다. |
| fo_density3_all_splits(전 분할 밀도3) | fn_sym_h1_m1p0__fn_all72__rf9_l18_n192 | -230.27 | 3.0765027322 | 0.8245892271 | -375.63 | 3.0763358779 | 3.076433121 | -943.7 | 0.7732919255 | 전 분할 density3(밀도3) 행은 있었지만 validation/OOS(검증/표본외) 양수 수익과 겹치지 않았습니다. |
| fo_density3_oos_pf105(밀도3 표본외 PF105) |  |  |  |  |  |  |  |  |  | density3(밀도3)와 OOS PF105(표본외 수익 팩터 1.05)도 동시에 나오지 않았습니다. |
| fo_combined_cost09_nonneg(합산 비용0.9 비음수) | fn_sym_h2_m1p25__fn_all72__et9_l14_n192 | 191.375 | 1.606557377 | 1.2496982395 | -6.493 | 1.6564885496 | 1.627388535 | 8.482 | 0.6966731898 | combined cost0.9(합산 비용0.9) 비음수 후보는 density3(밀도3) 안정성과 겹치지 않았습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fo01_selected_oos_reloss | selected_validation_net=136.115; selected_oos_net=-40.679; selected_oos_pf=0.9500226673; selected_oos_cost09=-260.279 | selection score(선택 점수)가 density leg(밀도 다리)와 cost leg(비용 다리)를 분리했지만, 선택 후보는 OOS(표본외)에서 손실로 전환됐습니다. | high(높음) | package(패키지)를 열지 않고 다음 run(실행)에서 positive density floor(양수 밀도 바닥)를 먼저 다시 세웁니다. |
| fo02_density_pf_overlap_absent | density3_all_splits_count=5; density3_oos_pf105_count=0; strict_like_count=0 | density3(밀도3) 안정성과 OOS PF(표본외 수익 팩터)가 같은 후보에서 겹치지 않았습니다. | structural(구조) | FP는 비용 후보를 좇기 전에 validation positive density3(검증 양수 밀도3)를 다시 확보합니다. |
| fo03_cost_candidates_too_sparse | oos_pf125_cost09_count=9510; oos_pf125_cost09_density3_count=0 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 후보는 존재하지만 trade density(거래 밀도)가 낮습니다. | medium(중간) | trade per day(일 거래수) 목표를 만족하지 못한 저밀도 후보를 운영 후보로 올리지 않습니다. |
| fo04_onnx_smoke_not_authority | onnx_smoke_pass_rows=36; new_mt5_execution=not_run | ONNX smoke(온엑스 스모크)는 변환 일치만 확인했고 MT5(메타트레이더5) 실행 의미는 만들지 않았습니다. | guardrail(가드레일) | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 차단합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | strict_candidate_count=0; selected_oos_net_negative; density3_pf_overlap_absent | not_opened | not_run | proxy(프록시)에서 무너진 후보가 MT5(메타트레이더5) 운영 주장으로 승격되지 않게 합니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fo01_decoupled_bridge_no_density_pf_overlap | density3 with OOS PF125/cost09(밀도3과 표본외 PF125/비용0.9 동시 충족) | validation_positive_density3_count=0; density3_all_splits_oos_pf105_count=0; oos_pf125_cost09_density3_count=0 | oos_pf125_cost09_count=9510; max_oos_pf=2.6041482355; max_oos_cost09=99.171 | validation positive density3 returns and at least OOS PF105 appears before PF125/cost09 chase(검증 양수 밀도3 회복 뒤 표본외 PF105 이상이 먼저 나타날 때) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fp01_positive_density_floor_reseed | positive density floor(양수 밀도 바닥)을 먼저 복구한 뒤 OOS PF/cost(표본외 수익 팩터/비용)를 다시 연결하면 FN의 저밀도 비용 후보 문제를 줄일 수 있습니다. | OOS PF125/cost0.9 candidates exist as scout clue(표본외 PF125/비용0.9 후보가 탐색 단서로 존재) | validation_positive_density3_count>0, density3_all_splits_valpos_oospos_count>0, then OOS PF>=1.05 before PF1.25(검증 양수 밀도3과 전 분할 양수 밀도3 우선 복구) | FP는 trade per day(일 거래수) 목표를 살린 뒤 수익성을 붙이는 순서로 탐색을 다시 엽니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/input_manifest.csv | FN 입력 계보가 FO 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/required_gate_coverage_audit.csv | FN gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/fo_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_overlap_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/fo_surface_diagnostic.csv | density/PF/cost(밀도/수익 팩터/비용) 겹침 부재를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/fo_failure_attribution.csv | 실패 원인을 선택 후보, 표면 겹침, 비용 후보, 권위 경계로 나눴습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/fo_failure_memory.csv | 다음 run(실행)이 반복하지 말아야 할 실패 기억을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/fo_fp_queue.csv | FP positive density floor reseed(FP 양수 밀도 바닥 재시드) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| paired_tier_record_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv | Tier A/Tier B/Tier A+B 행을 장부에 남겼습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FO/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
