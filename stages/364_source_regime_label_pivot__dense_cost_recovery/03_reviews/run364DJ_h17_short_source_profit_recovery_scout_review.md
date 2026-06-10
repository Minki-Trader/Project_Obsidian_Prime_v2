# run364DJ h17 short-source profit recovery scout review(17시 숏 원천 수익 회복 스카우트 검토)

Updated(갱신): 2026-06-06T06:28:35Z

## Judgment(판정)

- run_id(실행 ID): `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`
- selected_variant_id(선택 변형 ID): `di02_h17_18_20_21_no19_m050`
- judgment(판정): `positive_proxy_runtime_ready_short_source_profit_recovery_candidate_package_required_no_authority`
- next_run_id(다음 실행 ID): `run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Selected Candidate(선택 후보)

| selected_variant_id | estimated_mt5_net_profit | estimated_mt5_profit_factor | estimated_mt5_trade_count | estimated_mt5_short_trade_count | estimated_net_delta_vs_db | estimated_net_delta_vs_dg | review_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| di02_h17_18_20_21_no19_m050 | 1060.0737 | 1.4035432158 | 1020.0 | 149.0 | 41.2937 | 72.1937 | package_ready_proxy_candidate(패키지 준비 프록시 후보) |

## Runtime Path(런타임 경로)

| selected_variant_id | runtime_representation_status | ea_change_required | set_parameter_changes | runtime_decision |
| --- | --- | --- | --- | --- |
| di02_h17_18_20_21_no19_m050 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | false | InpSyntheticShortSourceHours=17\|18\|20\|21;InpSyntheticShortSourcePShortMin=0.4375;InpSyntheticShortSourceMarginVsLongMin=0.05;InpSyntheticShortSourceMarginVsFlatMin=0.0 | parameter_only_package_allowed(파라미터 전용 패키지 허용) |

## Month Stress Boundary(月 스트레스 경계)

| variant_id | estimated_mt5_net_profit | estimated_mt5_profit_factor | runtime_representation_status | review_status |
| --- | --- | --- | --- | --- |
| di09_no19_month_stress_6_7_8_12 | 1096.531 | 1.4246081415 | repair_required_multi_month_block(다중 월 차단 보정 필요) | regime_clue_only_not_package(국면 단서 전용, 패키지 아님) |
| di07_exclude_months_6_7_8_12 | 1072.0412 | 1.4033452927 | repair_required_multi_month_block(다중 월 차단 보정 필요) | regime_clue_only_not_package(국면 단서 전용, 패키지 아님) |
| di08_exclude_months_3_6_7_8_12 | 1090.5992 | 1.4254593567 | repair_required_multi_month_block(다중 월 차단 보정 필요) | regime_clue_only_not_package(국면 단서 전용, 패키지 아님) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/input_manifest.csv | DI inputs(DI 입력) linked(연결됨) |
| selected_candidate_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/selected_candidate_review.csv | selected candidate reviewed(선택 후보 검토됨) |
| runtime_representability_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/runtime_representation_review.csv | runtime parameter path confirmed(런타임 파라미터 경로 확인됨) |
| month_stress_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/month_stress_boundary_review.csv | month stress kept as clue(月 스트레스 단서로만 유지) |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/package_decision.csv | runtime package next action recorded(런타임 패키지 다음 행동 기록됨) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/result_judgment_receipt.json | receipts exist(영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트 종료 기록 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DJ/claim_boundary_receipt.json | authority/promotion/goal claims blocked(권위/승격/목표 주장 차단) |

## Boundary(경계)

This run(이번 실행)은 proxy review(프록시 검토)입니다. MT5 runtime execution(MT5 런타임 실행), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
