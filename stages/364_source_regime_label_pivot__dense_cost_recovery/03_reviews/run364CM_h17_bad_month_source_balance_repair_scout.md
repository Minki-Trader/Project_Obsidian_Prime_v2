# run364CM h17 bad month source balance repair scout(364CM 17시 손실 월 원천 균형 수리 정찰)

Updated(갱신): 2026-06-06T01:02:42Z

## Current Truth(현재 진실)

- status(상태): `completed_stage364CM_h17_bad_month_source_balance_proxy_scout_review_required_no_authority`
- judgment(판정): `exploratory_proxy_repair_scout_bad_months_zero_review_required_no_authority`
- selected candidate(선택 후보): `cm04_cj09_month08_12_pair_guard`
- selected KPI(선택 핵심 성과 지표): net `1036.46`, PF `1.4281838362`, density `3.1050955414`, shorts `100`
- bad month count(손실 월 수): `0`
- stress delta(압박 차이): `2.14`
- next run(다음 실행): `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1`

## Action And Effect(행동과 효과)

Action(행동): CL queue(CL 대기열) `16`개 후보를 entry-known month/source/probability rules(진입시점 월/원천/확률 규칙)로 proxy replay(프록시 재생)했다.

Effect(효과): `cm04_cj09_month08_12_pair_guard`가 bad month count(손실 월 수) `0`, density(밀도) `3.1050955414`, shorts(숏) `100`를 만들었지만, MT5(메타트레이더5) 실행은 없으므로 review-required(검토 필요) 상태로만 넘긴다.

## Surface Top Rows(표면 상위 행)

| candidate_id | candidate_status | package_precheck_status | net_profit | profit_factor | trade_count | trade_density | short_trade_count | stress_adjusted_net_delta_vs_parent | bad_month_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cm04_cj09_month08_12_pair_guard | proxy_package_review_candidate_no_authority(프록시 패키지 검토 후보, 권위 없음) | passed_proxy_precheck(프록시 사전검사 통과) | 1036.46 | 1.4281838362 | 975 | 3.1050955414 | 100 | 2.14 | 0 | 1330.70036133 |
| cm08_cj09_native_short_floor110_pressure | proxy_package_review_candidate_no_authority(프록시 패키지 검토 후보, 권위 없음) | passed_proxy_precheck(프록시 사전검사 통과) | 1035.46 | 1.412551787 | 1013 | 3.2261146497 | 110 | 1.14 | 0 | 1313.53075195 |
| cm05_cj11_month12_salvage_guard | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1014.48 | 1.4180483805 | 975 | 3.1050955414 | 100 | -19.84 | 0 | 1163.74681576 |
| cm11_cj09_late_year_h17_pressure | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1051.48 | 1.4307741231 | 994 | 3.1656050955 | 100 | 17.16 | 1 | 1076.32193779 |
| cm02_cj09_month12_class_soft_guard | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1037.6 | 1.4305018269 | 975 | 3.1050955414 | 100 | 3.28 | 1 | 1034.3521604 |
| cm15_cj07_december_guard_anchor | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1037.6 | 1.4305018269 | 975 | 3.1050955414 | 100 | 3.28 | 1 | 1034.3521604 |
| cm01_cj09_month08_class_soft_guard | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1033.18 | 1.4162620921 | 1003 | 3.1942675159 | 100 | -1.14 | 1 | 1020.11404679 |
| cm12_cj09_august_h17_pressure | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1033.18 | 1.4162620921 | 1003 | 3.1942675159 | 100 | -1.14 | 1 | 1020.11404679 |
| cm14_cj05_august_guard_anchor | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1033.18 | 1.4162620921 | 1003 | 3.1942675159 | 100 | -1.14 | 1 | 1020.11404679 |
| cm07_cj09_native_short_floor105_quality | proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음) | failed_proxy_precheck(프록시 사전검사 실패) | 1030.14 | 1.4127137259 | 1008 | 3.2101910828 | 105 | -4.18 | 1 | 996.718828 |

## Selected Source Attribution(선택 원천 귀속)

| source_bucket | trade_count | net_profit | profit_factor | short_trade_count |
| --- | --- | --- | --- | --- |
| long_threshold | 875 | 874.41 | 1.416145935 | 0 |
| native_short_threshold | 65 | 85.86 | 1.3593521115 | 65 |
| synthetic_short_overlay | 35 | 76.19 | 1.8050507185 | 35 |

## Selected Month Stability(선택 월 안정성)

| open_month | trade_count | net_profit | profit_factor | short_trade_count | month_status |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 87 | 68.31 | 1.3022967651 | 7 | positive_or_neutral(양수 또는 중립) |
| 2025-02 | 74 | 68.2 | 1.3695475481 | 13 | positive_or_neutral(양수 또는 중립) |
| 2025-03 | 8 | 14.81 | 2.1829073482 | 8 | positive_or_neutral(양수 또는 중립) |
| 2025-04 | 121 | 203.25 | 1.4117122774 | 16 | positive_or_neutral(양수 또는 중립) |
| 2025-05 | 75 | 51.45 | 1.3336143172 | 5 | positive_or_neutral(양수 또는 중립) |
| 2025-06 | 67 | 58.3 | 1.5199322215 | 1 | positive_or_neutral(양수 또는 중립) |
| 2025-07 | 35 | 4.71 | 1.0629510826 | 2 | positive_or_neutral(양수 또는 중립) |
| 2025-08 | 43 | 5.57 | 1.0553677932 | 0 | positive_or_neutral(양수 또는 중립) |
| 2025-09 | 51 | 34.34 | 1.3511965637 | 1 | positive_or_neutral(양수 또는 중립) |
| 2025-10 | 77 | 43.04 | 1.222924328 | 6 | positive_or_neutral(양수 또는 중립) |
| 2025-11 | 83 | 241.92 | 2.2211397708 | 12 | positive_or_neutral(양수 또는 중립) |
| 2025-12 | 31 | 2.66 | 1.0269040154 | 6 | positive_or_neutral(양수 또는 중립) |
| 2026-01 | 82 | 30.64 | 1.1686945989 | 6 | positive_or_neutral(양수 또는 중립) |
| 2026-02 | 91 | 177.63 | 1.8619886446 | 13 | positive_or_neutral(양수 또는 중립) |
| 2026-03 | 4 | 8.34 | 23.5405405405 | 4 | positive_or_neutral(양수 또는 중립) |
| 2026-04 | 46 | 23.29 | 1.2319721116 | 0 | positive_or_neutral(양수 또는 중립) |

## Selected Cost Stress(선택 비용 압박)

| candidate_id | net_profit | swap_sum | stress_adjusted_net_delta_vs_parent | stress_judgment |
| --- | --- | --- | --- | --- |
| cm04_cj09_month08_12_pair_guard | 1036.46 | -5.14 | 2.14 | passed_stress_delta_floor(압박 차이 하한 통과) |

## Selected Package Precheck(선택 패키지 사전검사)

| candidate_id | package_precheck_status | net_delta_nonnegative | pf_delta_nonnegative | density_ge_3 | short_floor_ge_100 | stress_delta_nonnegative | bad_month_count_zero |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cm04_cj09_month08_12_pair_guard | passed_proxy_precheck(프록시 사전검사 통과) | True | True | True | True | True | True |

## Selected Filter Audit(선택 필터 감사)

| filter_step | filter_reason | removed_trade_count | removed_net_profit | restored_trade_count | restored_net_profit |
| --- | --- | --- | --- | --- | --- |
| 1 | month08_synthetic_short_overlay_class_guard(8월 합성 숏 오버레이 클래스 가드) | 4 | -7.0 | 0 | 0.0 |
| 2 | month12_low_margin_long_guard(12월 낮은 마진 롱 가드) | 28 | -3.28 | 0 | 0.0 |
| 3 | restore_native_short_until_floor_100_entry_known_native_restore(restore_native_short_until_floor_100 진입시점 기본 숏 복원) | 0 | 0.0 | 4 | -8.14 |

## Review Queue(검토 대기열)

| next_run_id | selected_candidate_id | selected_package_precheck_status | review_task | mt5_execution_status |
| --- | --- | --- | --- | --- |
| run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1 | cm04_cj09_month08_12_pair_guard | passed_proxy_precheck(프록시 사전검사 통과) | package_gate_source_month_cost_attribution_and_mt5_boundary(패키지 게이트/원천/월/비용 귀속 및 MT5 경계) | not_run_in_CM(CM에서는 미실행) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/cm_proxy_repair_surface.csv | CM proxy surface exists(CM 프록시 표면 존재) |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/data_integrity_audit.csv | density/short/bad-month guards checked(밀도/숏/손실 월 가드 확인) |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/run_evidence_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/experiment_design_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/data_integrity_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/model_validation_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/artifact_lineage_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/result_judgment_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/claim_boundary_receipt.json | required skill receipts exist(필수 스킬 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트가 종료 기록에 연결) |

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)이다. New ONNX model(새 ONNX 모델), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없다.
