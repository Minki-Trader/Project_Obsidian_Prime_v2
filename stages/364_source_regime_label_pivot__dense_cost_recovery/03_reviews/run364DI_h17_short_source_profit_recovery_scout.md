# run364DI h17 short-source profit recovery scout(17시 숏 원천 수익 회복 스카우트)

Updated(갱신): 2026-06-06T06:23:05Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`
- selected_variant_id(선택 변형 ID): `di02_h17_18_20_21_no19_m050`
- judgment(판정): `proxy_short_source_profit_recovery_scout_found_runtime_ready_candidate_review_required_no_authority`
- next_run_id(다음 실행 ID): `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): DH failure memory(DH 실패 기억)를 기반으로 hour veto(시간 배제), margin filter(마진 필터), month stress(月 스트레스)를 proxy scout(프록시 스카우트)로 실행했습니다.

Effect(효과): DG가 늘린 short count(숏 거래수)를 유지하면서 DB net/PF(DB 순수익/수익 팩터)를 회복할 수 있는 runtime-ready(런타임 준비) 후보를 분리했습니다.

## Selected Candidate(선택 후보)

| variant_id | estimated_mt5_net_profit | estimated_mt5_profit_factor | estimated_mt5_trade_count | estimated_mt5_short_trade_count | estimated_net_delta_vs_db | estimated_net_delta_vs_dg | runtime_representation_status | package_precheck_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| di02_h17_18_20_21_no19_m050 | 1060.0737 | 1.4035432158 | 1020.0 | 149.0 | 41.2937 | 72.1937 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | passed_proxy_precheck(프록시 사전검토 통과) |

## Surface Top Rows(표면 상위 행)

| variant_id | estimated_mt5_net_profit | estimated_mt5_profit_factor | estimated_mt5_trade_count | estimated_mt5_short_trade_count | estimated_net_delta_vs_db | estimated_net_delta_vs_dg | runtime_representation_status | package_precheck_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| di02_h17_18_20_21_no19_m050 | 1060.0737 | 1.4035432158 | 1020.0 | 149.0 | 41.2937 | 72.1937 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | passed_proxy_precheck(프록시 사전검토 통과) | 1835.862587168 |
| di05_margin_vs_flat_026_m050 | 1048.1813 | 1.4008238997 | 1003.0 | 132.0 | 29.4013 | 60.3013 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | passed_proxy_precheck(프록시 사전검토 통과) | 1729.574843712 |
| di03_h17_18_20_no19_no21_m050 | 1055.0057 | 1.3999641208 | 1017.0 | 146.0 | 36.2257 | 67.1257 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | failed_proxy_precheck(프록시 사전검토 실패) | 1585.222655968 |
| di09_no19_month_stress_6_7_8_12 | 1096.531 | 1.4246081415 | 1016.0 | 145.0 | 77.751 | 108.651 | repair_required_multi_month_block(다중 월 차단 보정 필요) | passed_proxy_precheck(프록시 사전검토 통과) | 1537.77030264 |
| di01_dd05_broad_anchor | 1019.7701 | 1.3743479483 | 1035.0 | 164.0 | 0.9901 | 31.8901 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | failed_proxy_precheck(프록시 사전검토 실패) | 1525.887205368 |
| di07_exclude_months_6_7_8_12 | 1072.0412 | 1.4033452927 | 1029.0 | 158.0 | 53.2612 | 84.1612 | repair_required_multi_month_block(다중 월 차단 보정 필요) | passed_proxy_precheck(프록시 사전검토 통과) | 1506.537955992 |
| di08_exclude_months_3_6_7_8_12 | 1090.5992 | 1.4254593567 | 1007.0 | 136.0 | 71.8192 | 102.7192 | repair_required_multi_month_block(다중 월 차단 보정 필요) | passed_proxy_precheck(프록시 사전검토 통과) | 1483.073972072 |
| di06_high_margin_m090 | 1039.5987 | 1.4106116273 | 988.0 | 117.0 | 20.8187 | 51.7187 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | failed_proxy_precheck(프록시 사전검토 실패) | 1432.733960368 |
| di04_h17_18_21_no19_no20_m050 | 1005.9654 | 1.3783488396 | 1013.0 | 142.0 | -12.8146 | 18.0854 | runtime_ready_existing_params(기존 파라미터로 런타임 가능) | failed_proxy_precheck(프록시 사전검토 실패) | 1350.092686016 |
| di00_db_policy_anchor | 1018.78 | 1.41 | 972.0 | 101.0 | 0.0 | 30.9 | anchor_not_package(기준, 패키지 아님) | failed_proxy_precheck(프록시 사전검토 실패) | 1306.18 |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/di_short_source_profit_recovery_surface.csv | all DI variants scored(모든 DI 변형 점수화) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/input_manifest.csv | inputs linked(입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/data_integrity_audit.csv | timestamp/no-overlap checks passed(시점/무겹침 점검 통과) |
| candidate_surface_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/di_short_source_profit_recovery_surface.csv | selected variant changes short source(선택 변형이 숏 원천 변경) |
| runtime_representability_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/runtime_representation_audit.csv | selected variant is parameter-ready(선택 변형이 파라미터 준비됨) |
| kpi_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/package_precheck.csv | selected row preserves DI KPI contract(선택 행이 DI KPI 계약 유지) |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/data_integrity_audit.csv | single-position replay used(단일 포지션 재생 사용) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/run_evidence_receipt.json | required receipts exist(필수 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트를 종료 기록에 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DI/claim_boundary_receipt.json | no authority/promotion/goal claim(권위/승격/목표 주장 없음) |

## Boundary(경계)

This run(이번 실행)은 proxy scout(프록시 스카우트)입니다. MT5 runtime execution(MT5 런타임 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
