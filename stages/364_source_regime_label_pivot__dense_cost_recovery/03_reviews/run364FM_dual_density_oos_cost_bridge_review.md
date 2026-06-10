# run364FM Dual Density OOS Cost Bridge Review(양쪽 밀도 표본외 비용 연결 검토)

Created(생성): 2026-06-07T04:34:42Z

Action(행동): FL dual density OOS cost bridge(FL 양쪽 밀도 표본외 비용 연결)를 package decision(패키지 결정), failure memory(실패 기억), FN queue(FN 대기열)로 분리했습니다.

Effect(효과): density3(밀도3) 회복은 보존 단서로 남기고 OOS PF/cost(표본외 수익 팩터/비용) 재손실 때문에 운영 주장(operating claim, 운영 주장)을 막습니다.

- judgment(판정): `negative_dual_density_oos_cost_bridge_review_oos_pf_cost_reloss_no_package_no_authority`
- selected model(선택 모델): `fl_sym_h2_m1p75__fl_oos_cost_session_macro__rf8_l24_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `102.566` / `1.0778107449` / `3.0218579235`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `43.189` / `1.0477871778` / `3.0763358779`
- OOS cost0.9(표본외 비용0.9): `-198.611`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `3.0445859873` / `-427.845` / `0.6809623431`
- validation_positive_density3_count(검증 양수 밀도3 수): `40`
- validation_positive_density3_oos_pf125_count(검증 양수 밀도3과 표본외 PF125 동시 수): `0`
- density_pf105_count(밀도3 표본외 PF105 수): `0`
- next_run_id(다음 실행 ID): `run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | oos_density | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fm_selected(선택 후보) | fl_sym_h2_m1p75__fl_oos_cost_session_macro__rf8_l24_n160 | 102.566 | 3.0218579235 | 1.0477871778 | -198.611 | 3.0763358779 | 3.0445859873 | -427.845 | 0.6809623431 | FL selected candidate(FL 선택 후보)는 density3(밀도3)를 회복했지만 OOS PF/cost(표본외 수익 팩터/비용)가 약합니다. |
| fm_best_density(밀도 후보) | fl_sym_h2_m1p75__fl_oos_cost_session_macro__rf8_l24_n160 | 102.566 | 3.0218579235 | 1.0477871778 | -198.611 | 3.0763358779 | 3.0445859873 | -427.845 | 0.6809623431 | density3(밀도3) 후보는 OOS PF/cost(표본외 수익 팩터/비용)를 통과하지 못했습니다. |
| fm_best_oos_cost(표본외 비용 후보) | fl_sym_h2_m1p5__fl_dense_behavior_macro__et7_l14_n160 | -263.5 | 2.5628415301 | 1.3432466506 | 42.381 | 2.7099236641 | 2.6242038217 | -502.519 | 0.640776699 | OOS PF/cost(표본외 수익 팩터/비용) 후보는 density3(밀도3)에 못 미칩니다. |
| fm_density_pf105(밀도 PF105) |  |  |  |  |  |  |  |  |  | density3(밀도3)와 OOS PF 1.05(표본외 수익 팩터 1.05)도 동시에 나오지 않았습니다. |
| fm_strict_like(엄격 유사) |  |  |  |  |  |  |  |  |  | strict-like(엄격 유사) 후보는 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fm01_density_salvage | selected_density=3.0218579235/3.0763358779/3.0445859873; validation_positive_density3_count=40 | FL score(FL 점수)가 hard density floor(강제 밀도 바닥)를 회복했습니다. | salvage(회수) | FN에서는 이 밀도 단서를 보존하되 OOS PF/cost(표본외 수익 팩터/비용) 없는 package(패키지)는 열지 않습니다. |
| fm02_oos_pf_cost_reloss | selected_oos_pf=1.0477871778; selected_oos_cost09=-198.611; combined_cost09=-427.845 | density3(밀도3)를 강제하자 OOS PF/cost(표본외 수익 팩터/비용)가 다시 무너졌습니다. | high(높음) | runtime package(런타임 패키지)를 열지 않고 density/cost objective(밀도/비용 목적)를 분리한 다음 탐색으로 넘깁니다. |
| fm03_no_overlap_even_pf105 | density_pf105_count=0; strict_like_count=0 | density3(밀도3) 행은 OOS PF 1.05(표본외 수익 팩터 1.05)도 넘지 못했습니다. | structural(구조) | FN은 같은 점수 안에서 가중치만 흔들지 말고 density leg(밀도 다리)와 cost leg(비용 다리)를 decoupled bridge(분리 연결)로 다룹니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | strict_candidate_count=0; density3_recovered_but_oos_pf_below_1p25_and_cost09_negative | not_opened | not_run | density(밀도) 회복을 MT5 운영 의미로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fm01_density_salvage_oos_cost_reloss | density3 with OOS PF125/cost09(밀도3과 표본외 PF125/비용0.9 동시 충족) | validation_positive_density3_count=40; validation_positive_density3_oos_pf125_count=0; selected_oos_pf=1.0477871778; selected_oos_cost09=-198.611 | density=3.0218579235/3.0763358779/3.0445859873; validation_net=102.566; short_share=0.6809623431 | density3 retained while OOS PF>=1.25 and OOS cost0.9>=0(밀도3 보존과 표본외 PF/비용 동시 충족) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fn01_density_cost_decoupled_bridge | density leg(밀도 다리)와 OOS cost leg(표본외 비용 다리)를 같은 scalar score(단일 점수)가 아니라 decoupled bridge(분리 연결)로 조합하면 왕복 실패를 줄일 수 있습니다. | validation_density>=3, oos_density>=3, combined_density>=3, validation_net>0(검증/표본외/합산 밀도와 검증 수익 보존) | OOS PF>=1.25, OOS cost0.9>=0, combined cost0.9 not deeply negative(표본외 수익 팩터/비용 회복) | FN은 밀도 후보와 비용 후보를 분리해 찾은 뒤 겹치는 조건을 좁혀 봅니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/input_manifest.csv | FL 입력 계보가 FM 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/required_gate_coverage_audit.csv | FL gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/fm_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_tradeoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/fm_surface_diagnostic.csv | density/OOS cost(밀도/표본외 비용) tradeoff(절충 관계)를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/fm_failure_attribution.csv | 표본외 PF/비용 재손실을 귀속했습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/fm_failure_memory.csv | 실패 기억과 재개 조건을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/fm_fn_queue.csv | FN density cost decoupled bridge(FN 밀도 비용 분리 연결) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FM/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
