# run364FQ Positive Density Floor Reseed Review(양수 밀도 바닥 재시드 검토)

Created(생성): 2026-06-07T05:32:29Z

Action(행동): FP positive density floor reseed(FP 양수 밀도 바닥 재시드)를 package decision(패키지 결정), failure memory(실패 기억), FR queue(FR 대기열)로 검토했습니다.

Effect(효과): validation positive density3(검증 양수 밀도3)이 없는 후보를 운영 후보로 올리지 않고, 다음 탐색을 regime/session/side split(국면/세션/방향 분할)로 보냅니다.

- judgment(판정): `negative_positive_density_floor_reseed_review_validation_positive_density3_absent_no_package_no_authority`
- selected model(선택 모델): `fp_sym_h2_m1p75__fp_validation_stability__rf8_l22_n176`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `22.075` / `1.0171796969` / `2.7704918033`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-61.734` / `0.9244281986` / `2.7633587786`
- OOS cost0.9(표본외 비용0.9): `-278.934`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `2.7675159236` / `-561.059` / `0.7583429229`
- validation_positive_density3_count(검증 양수 밀도3 수): `0`
- density3_all_splits_count(전 분할 밀도3 수): `35`
- density3_all_splits_valpos_oospos_count(전 분할 양수 밀도3 수): `0`
- density3_all_splits_oos_pf105_count(전 분할 밀도3과 표본외 PF105 동시 수): `0`
- oos_pf125_cost09_count(표본외 PF125와 비용0.9 수): `9835`
- oos_pf125_cost09_density3_count(표본외 PF125/비용0.9/밀도3 동시 수): `0`
- next_run_id(다음 실행 ID): `run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | oos_density | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fq_selected_candidate(선택 후보) | fp_sym_h2_m1p75__fp_validation_stability__rf8_l22_n176 | 22.075 | 2.7704918033 | 0.9244281986 | -278.934 | 2.7633587786 | 2.7675159236 | -561.059 | 0.7583429229 | 선택 후보는 validation(검증) 순수익은 양수였지만 density3(밀도3)와 OOS(표본외) 수익이 부족했습니다. |
| fq_best_validation_positive(검증 양수 상위) | fp_sym_h2_m1p75__fp_validation_stability__rf8_l22_n176 | 22.075 | 2.7704918033 | 0.9244281986 | -278.934 | 2.7633587786 | 2.7675159236 | -561.059 | 0.7583429229 | 검증 양수 후보는 존재하지만 density3(밀도3)에 닿지 못했습니다. |
| fq_density3_all_splits(전 분할 밀도3) | fp_sym_h1_m1p5__fp_all72__et7_l12_n176 | -62.952 | 3.0273224044 | 0.8347079073 | -369.549 | 3.0534351145 | 3.0382165605 | -764.901 | 0.7526205451 | 전 분할 density3(밀도3) 후보는 있었지만 validation/OOS(검증/표본외) 양수 수익과 겹치지 않았습니다. |
| fq_oos_pf125_cost09(표본외 PF125 비용0.9) | fp_sym_h2_m1p75__fp_all72__et7_l12_n176 | 69.498 | 2.2076502732 | 1.3171738095 | 20.11 | 2.1832061069 | 2.1974522293 | -152.792 | 0.6942028986 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 후보는 여전히 저밀도 쪽에 몰려 있습니다. |
| fq_density3_oos_pf105(밀도3 표본외 PF105) |  |  |  |  |  |  |  |  |  | density3(밀도3)와 OOS PF105(표본외 수익 팩터 1.05) 겹침은 없습니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fq01_positive_density_not_recovered | validation_positive_density3_count=0; selected_validation_density=2.7704918033; selected_validation_net=22.075 | FP score(FP 점수)가 검증 순수익을 양수로 만들었지만 density3(밀도3) 바닥까지 끌어올리지 못했습니다. | high(높음) | package(패키지)를 열지 않고 FR에서 regime/session split(국면/세션 분할)로 밀도3 행의 손익을 분리합니다. |
| fq02_dense_rows_negative | density3_all_splits_count=35; density3_all_splits_valpos_oospos_count=0 | density3(밀도3) 행은 생겼지만 검증/표본외 양수 수익과 겹치지 않았습니다. | structural(구조) | 다음 탐색은 threshold(임계값)만 낮추지 않고 regime split(국면 분할)과 side/session(방향/세션) 분리를 시도합니다. |
| fq03_cost_scout_still_low_density | oos_pf125_cost09_count=9835; oos_pf125_cost09_density3_count=0 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 후보는 계속 저밀도 영역에만 있습니다. | medium(중간) | 저밀도 비용 후보를 package(패키지)로 검토하지 않고 scout clue(탐색 단서)로만 유지합니다. |
| fq04_onnx_smoke_not_authority | onnx_smoke_pass_rows=36; new_mt5_execution=not_run | ONNX smoke(온엑스 스모크)는 변환 일치만 확인했고 MT5(메타트레이더5) 실행 근거는 아닙니다. | guardrail(가드레일) | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | validation_positive_density3_count=0; selected_oos_net_negative; strict_candidate_count=0 | not_opened | not_run | 양수 수익만 약하게 생긴 저밀도 후보를 MT5(메타트레이더5) 운영 후보로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fq01_positive_density_floor_not_recovered | validation positive density3 before OOS PF125(표본외 PF125 전 검증 양수 밀도3) | validation_positive_density3_count=0; density3_all_splits_valpos_oospos_count=0; selected_density=2.7704918033/2.7633587786/2.7675159236 | density3_all_splits_count=35; oos_pf125_cost09_count=9835; max_oos_pf=2.7551565712 | regime/session split finds validation_positive_density3_count>0 and density3_all_splits_valpos_oospos_count>0(국면/세션 분할이 검증 양수 밀도3과 전 분할 양수 밀도3을 찾을 때) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| fr01_density3_regime_split_repair | density3(밀도3) 행이 손실인 이유가 regime/session/side(국면/세션/방향) 혼합이면, 분할 학습과 분할 선택 점수가 양수 밀도 바닥을 되살릴 수 있습니다. | density3_all_splits_count>0 and OOS PF125/cost0.9 scout clue(전 분할 밀도3 수와 표본외 PF125/비용0.9 단서 보존) | validation_positive_density3_count>0, density3_all_splits_valpos_oospos_count>0, OOS PF>=1.05 before PF1.25(검증 양수 밀도3과 전 분할 양수 밀도3 우선 복구) | FR은 dense losing rows(고밀도 손실 행)를 국면/세션/방향으로 쪼개 수익 가능한 밀도 구간을 찾습니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/input_manifest.csv | FP 입력 계보가 FQ 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/required_gate_coverage_audit.csv | FP gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/fq_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_overlap_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/fq_surface_diagnostic.csv | positive density/PF/cost(양수 밀도/수익 팩터/비용) 겹침 부재를 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/fq_failure_attribution.csv | 실패 원인을 양수 밀도 바닥, 고밀도 손실 행, 저밀도 비용 후보, 권위 경계로 나눴습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/fq_failure_memory.csv | 다음 run(실행)이 반복하지 말아야 할 실패 기억을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/fq_fr_queue.csv | FR density3 regime split repair(FR 밀도3 국면 분할 수리) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| paired_tier_record_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv | Tier A/Tier B/Tier A+B 행을 장부에 남겼습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FQ/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
