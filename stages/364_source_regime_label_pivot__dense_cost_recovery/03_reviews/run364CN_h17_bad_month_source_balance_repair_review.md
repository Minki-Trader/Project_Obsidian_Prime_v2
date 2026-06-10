# run364CN h17 bad-month source-balance repair review(17시 손실 월/원천 균형 수리 검토)

Updated(갱신): 2026-06-06T01:14:34Z

## Current Truth(현재 진실)

Action(행동): CM selected candidate(CM 선택 후보) `cm04_cj09_month08_12_pair_guard`를 package gate(패키지 게이트), source/month/cost attribution(원천/월/비용 귀속), MT5 boundary(MT5 경계)로 검토했습니다.

Effect(효과): 후보를 `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1` MT5 runtime probe input materialization(MT5 런타임 탐침 입력 구체화)로 넘기지만, runtime authority(런타임 권위)나 operating promotion(운영 승격)은 주장하지 않습니다.

- net profit(순수익): `1036.46`
- profit factor(수익 팩터): `1.4281838362`
- expectancy(기대값): `1.0630358974`
- trade count(거래수): `975`
- density(밀도): `3.1050955414`
- long/short(롱/숏): `875` / `100`
- bad month count(손실 월 수): `0`
- weakest month(가장 약한 월): `2025-12` net `2.66`, PF `1.0269040154`
- stress delta(압박 차이): `2.14`

## Package Gate(패키지 게이트)

| gate_id | gate_status | evidence | effect |
| --- | --- | --- | --- |
| proxy_package_precheck_gate | passed_for_mt5_probe_input(통과, MT5 탐침 입력 인계) | status=passed_proxy_precheck(프록시 사전검사 통과);bad_months=0;stress_delta=2.14;source_balance=True | MT5 probe(MT5 탐침) 입력으로 넘기되 운영 주장(operating claim, 운영 주장)은 하지 않습니다. |
| headline_kpi_gate | passed_for_proxy_review(프록시 검토 통과) | net=1036.46;pf=1.4281838362;expectancy=1.0630358974;density=3.1050955414;trades=975 | 좋은 proxy(프록시) 숫자를 후보성(candidate quality, 후보성)으로만 보존합니다. |
| trade_density_and_no_split_gate | passed_no_split_density_ge_3(무분할 및 밀도 3 이상 통과) | density=3.1050955414;selected_trades=975;parent_trades=1003.0;removed=32.0;restored=4.0 | 거래수를 쪼개 수익을 나눈 결과인지 분리합니다. |
| month_stability_gate | passed_bad_month_zero(손실 월 0개 통과) | bad_month_count=0;weakest_month=2025-12 | CK/CL의 failure memory(실패 기억)가 해소됐는지 확인합니다. |
| source_balance_gate | passed_source_sum_and_short_floor(원천 합산 및 숏 하한 통과) | source_total=975;source_net=1036.46;long=875;short=100;short_share=0.1025641026 | long_threshold/native_short/synthetic_overlay(롱 임계값/기본 숏/합성 오버레이)가 끊기지 않았는지 확인합니다. |
| cost_stress_gate | passed_stress_delta_nonnegative(압박 차이 0 이상 통과) | stress_delta=2.14;swap_sum=-5.14;stress_judgment=passed_stress_delta_floor(압박 차이 하한 통과) | swap haircut(스왑 헤어컷) 뒤에도 후보성이 남는지 확인합니다. |
| new_mt5_execution_boundary_gate | not_run_boundary_preserved(미실행 경계 보존) | new_mt5_execution=not_run(새 MT5 실행 미실행) | proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표)로 대체하지 않습니다. |

## Source Balance(원천 균형)

| source_bucket | trade_count | net_profit | profit_factor | short_trade_count | source_judgment |
| --- | --- | --- | --- | --- | --- |
| long_threshold | 875 | 874.41 | 1.416145935 | 0 | main_long_profit_body(주 롱 수익 몸통) |
| native_short_threshold | 65 | 85.86 | 1.3593521115 | 65 | short_floor_support(숏 하한 지원) |
| synthetic_short_overlay | 35 | 76.19 | 1.8050507185 | 35 | high_pf_but_thin_watch(높은 PF지만 얇아서 관찰) |

## Weak Months(약한 월)

| open_month | trade_count | net_profit | profit_factor | short_trade_count | watch_role |
| --- | --- | --- | --- | --- | --- |
| 2025-12 | 31 | 2.66 | 1.0269040154 | 6 | weak_positive_month_watch(약한 양수 월 관찰) |
| 2025-07 | 35 | 4.71 | 1.0629510826 | 2 | weak_positive_month_watch(약한 양수 월 관찰) |
| 2025-08 | 43 | 5.57 | 1.0553677932 | 0 | weak_positive_month_watch(약한 양수 월 관찰) |
| 2026-03 | 4 | 8.34 | 23.5405405405 | 4 | weak_positive_month_watch(약한 양수 월 관찰) |
| 2025-03 | 8 | 14.81 | 2.1829073482 | 8 | positive_month(양수 월) |
| 2026-04 | 46 | 23.29 | 1.2319721116 | 0 | positive_month(양수 월) |
| 2026-01 | 82 | 30.64 | 1.1686945989 | 6 | positive_month(양수 월) |
| 2025-09 | 51 | 34.34 | 1.3511965637 | 1 | positive_month(양수 월) |

## Cost Stress(비용 압박)

| net_profit | swap_sum | stress_adjusted_net_delta_vs_parent | stress_judgment | review_judgment |
| --- | --- | --- | --- | --- |
| 1036.46 | -5.14 | 2.14 | passed_stress_delta_floor(압박 차이 하한 통과) | passed_for_proxy_probe_handoff(프록시 탐침 인계 통과) |

## Filter Boundary(필터 경계)

| filter_step | filter_reason | removed_trade_count | restored_trade_count | restored_net_profit | review_judgment |
| --- | --- | --- | --- | --- | --- |
| 1 | month08_synthetic_short_overlay_class_guard(8월 합성 숏 오버레이 클래스 가드) | 4 | 0 | 0.0 | entry_known_rule_kept(진입시점 규칙 유지) |
| 2 | month12_low_margin_long_guard(12월 낮은 마진 롱 가드) | 28 | 0 | 0.0 | entry_known_rule_kept(진입시점 규칙 유지) |
| 3 | restore_native_short_until_floor_100_entry_known_native_restore(restore_native_short_until_floor_100 진입시점 기본 숏 복원) | 0 | 4 | -8.14 | entry_known_rule_kept(진입시점 규칙 유지) |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | proxy_net | proxy_profit_factor | usability | effect |
| --- | --- | --- | --- | --- |
| cm_proxy_vs_next_mt5_probe | 1036.46 | 1.4281838362 | must_compare_in_CO_or_later(CO 이후 반드시 비교) | proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)와 혼동하지 않게 합니다. |

## MT5 Probe Handoff(MT5 탐침 인계)

| candidate_id | queue_status | expected_proxy_net | expected_proxy_profit_factor | expected_proxy_density | expected_proxy_short_count |
| --- | --- | --- | --- | --- | --- |
| cm04_cj09_month08_12_pair_guard | ready_for_runtime_input_materialization(런타임 입력 구체화 준비) | 1036.46 | 1.4281838362 | 3.1050955414 | 100 |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | net=1036.46;pf=1.4281838362;density=3.1050955414;drawdown=67.67 | KPI(핵심 성과 지표)를 같은 grain(입도)에서 비교합니다. |
| row_grain_audit | passed | Tier A separate / Tier B missing_required / Tier A+B out_of_scope rows will be written(티어 행 기록 예정) | Tier B(티어 B) 누락을 숨기지 않습니다. |
| source_authority_audit | passed | parent_final=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/final_decision.json;parent_manifest=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CM/run_manifest.json;input_count=14 | CN 판정이 CM 산출물 계보에서 끊기지 않습니다. |
| required_gate_coverage_audit | passed | required=kpi_contract_audit;row_grain_audit;source_authority_audit;required_gate_coverage_audit;final_claim_guard;receipts_written=True | 필수 gate(게이트)와 receipt(영수증)가 closeout(종료)에 묶입니다. |
| final_claim_guard | passed | no runtime authority / no operating promotion / no goal claim(권위/승격/목표 달성 주장 없음) | MT5 미실행 후보를 운영 후보로 과장하지 않습니다. |

## Boundary(경계)

CN is review only(CN은 검토 전용)입니다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없습니다.
