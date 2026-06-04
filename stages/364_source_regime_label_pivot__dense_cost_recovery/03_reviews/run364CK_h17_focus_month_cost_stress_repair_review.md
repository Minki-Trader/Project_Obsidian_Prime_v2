# run364CK h17 focus repair review(17시 집중 수리 검토)

Updated(갱신): 2026-06-04T22:01:20Z

## Current truth(현재 진실)

- reviewed candidate(검토 후보): `cj09_cg07_native_short_cost_firewall_short_floor_rescue`
- KPI(핵심 성과 지표): net `1034.32`, PF `1.4184722658`, expectancy `1.031226321`, trades `1003`, density `3.1942675159`, drawdown proxy `67.67`, recovery proxy `15.2847642973`, long/short `903`/`100`
- cost stress(비용 압박): stress delta `31.69`
- bad months(손실 월): `2025-08;2025-12`
- package decision(패키지 결정): `rejected_open_cl_repair_inputs_no_authority(거절, CL 수리 입력 개방, 권위 없음)`
- next action(다음 행동): `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1`

## Package Gate(패키지 게이트)

| gate_id | gate_status | evidence | effect |
| --- | --- | --- | --- |
| headline_proxy_kpi_gate | passed_for_proxy(프록시 기준 통과) | net_delta=36.83;pf_delta=0.0207247521;density=3.1942675159;shorts=100 | positive clue(긍정 단서)는 보존하지만 package(패키지) 판단은 안정성 게이트까지 본다. |
| no_trade_splitting_gate | passed_no_split(무분할 통과) | selected_trades=1003;parent_trades=1008;restored_trades=14 | trade/day(일 거래수)가 수익 쪼개기로 올라간 결과인지 분리한다. |
| short_floor_source_balance_gate | passed_for_proxy_review(프록시 검토 기준 통과) | shorts=100;restored_shorts=14 | 숏 100개 하한은 지켰지만 source mix(원천 혼합)는 다음 수리에서 계속 본다. |
| cost_stress_package_gate | passed_for_proxy_package_precheck(프록시 패키지 사전점검 통과) | stress_delta=31.69;stress_judgment=stress_positive(압박 양호) | 비용 압박은 개선됐지만 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. |
| month_stability_package_gate | failed_for_package(패키지 기준 실패) | bad_month_count=2;bad_months=2025-08,2025-12 | 남은 손실 월을 다음 repair constraint(수리 제약)으로 바꾼다. |
| mt5_runtime_package_gate | failed_for_package(패키지 기준 실패) | new_mt5_execution=not_run(새 MT5 실행 미실행) | proxy(프록시)를 runtime authority(런타임 권위)로 올리지 않는다. |
| package_decision_gate | rejected_open_cl_repair_inputs(거절, CL 수리 입력 개방) | package_precheck=failed_proxy_precheck(프록시 사전점검 실패);bad_months=2;stress_delta=31.69;new_mt5_execution=not_run | CK를 운영 패키지가 아니라 CL materialization(CL 구체화)으로 넘긴다. |

## Month Failure(월 실패)

| failure_id | segment | net_profit | profit_factor | trade_count | short_trade_count | repair_use |
| --- | --- | --- | --- | --- | --- | --- |
| bad_month__2025-08 | 2025-08 | -1.43 | 0.98857093 | 47 | 4 | CL should test reusable month/quarter/session class guards without exact 2025 date memorization(CL은 정확한 2025년 날짜 암기 없이 재사용 월/분기/세션 클래스 가드를 시험) |
| bad_month__2025-12 | 2025-12 | -0.62 | 0.9961409187 | 59 | 6 | CL should test reusable month/quarter/session class guards without exact 2025 date memorization(CL은 정확한 2025년 날짜 암기 없이 재사용 월/분기/세션 클래스 가드를 시험) |

## Source Balance(원천 균형)

| source_bucket | trade_count | net_profit | profit_factor | short_trade_count | restored_short_count_total | source_judgment |
| --- | --- | --- | --- | --- | --- | --- |
| long_threshold | 903 | 871.13 | 1.4046363376 | 0 | 14 | source_contribution_usable(원천 기여 사용 가능) |
| native_short_threshold | 61 | 94.0 | 1.4475655431 | 61 | 14 | source_contribution_usable(원천 기여 사용 가능) |
| synthetic_short_overlay | 39 | 69.19 | 1.6364054452 | 39 | 14 | positive_but_thin_overlay_watch(긍정이나 얇은 오버레이 관찰) |

## Preserved Clues(보존 단서)

| clue_id | clue_type | net_profit | profit_factor | trade_count | short_trade_count | stress_delta | bad_month_count | usable_as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cj09_cg07_native_short_cost_firewall_short_floor_rescue | selected_repair_proxy_clue(선택 수리 프록시 단서) | 1034.32 | 1.4184722658 | 1003 | 100 | 31.69 | 2 | CL primary repair seed(CL 주 수리 씨앗) |
| cj09_cg07_native_short_cost_firewall_short_floor_rescue__long_threshold | source_attribution_clue(원천 귀속 단서) | 871.13 | 1.4046363376 | 903 | 0 |  |  | CL source balance diagnostic(CL 원천 균형 진단) |
| cj09_cg07_native_short_cost_firewall_short_floor_rescue__native_short_threshold | source_attribution_clue(원천 귀속 단서) | 94.0 | 1.4475655431 | 61 | 61 |  |  | CL source balance diagnostic(CL 원천 균형 진단) |
| cj09_cg07_native_short_cost_firewall_short_floor_rescue__synthetic_short_overlay | source_attribution_clue(원천 귀속 단서) | 69.19 | 1.6364054452 | 39 | 39 |  |  | CL source balance diagnostic(CL 원천 균형 진단) |
| cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue | lower_bad_month_salvage_seed(손실 월 감소 회수 씨앗) | 1011.2 | 1.4064075752 | 1003 | 100 | 8.57 | 1 | CL comparison seed with fewer bad months(CL 손실 월이 적은 비교 씨앗) |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | parent_mt5_net | proxy_net | net_diff_proxy_minus_parent | parent_mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| selected_cj_proxy_vs_parent_mt5(선택 CJ 프록시 대 부모 MT5) | 997.49 | 1034.32 | 36.83 | 1.4 | 1.4184722658 | usable_for_CL_selection_only_not_runtime_authority(CL 선별 전용 사용 가능, 런타임 권위 아님) |

## CL Queue(CL 대기열)

| queue_rank | queue_id | seed_candidate_id | repair_policy | success_criteria | expected_effect |
| --- | --- | --- | --- | --- | --- |
| 1 | cl01_selected_cj09_bad_month_class_guard | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year_and_quarter_class_guard | bad_month_count decreases;stress_delta>=0;shorts>=100 | turn cj09 into reusable month class repair(CJ09를 재사용 월 클래스 수리로 전환) |
| 2 | cl02_cj11_one_bad_month_salvage_guard | cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue | one_bad_month_salvage_guard | bad_month_count<=1;net_delta>0;shorts>=100 | use cj11 as lower bad-month comparison seed(CJ11을 손실 월 감소 비교 씨앗으로 사용) |
| 3 | cl03_month08_open_hour17_overlay_pressure_guard | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=08_open_hour17_pressure | no exact 2025 date;bad_month_count decreases | test August class without memorizing 2025-08(2025-08 암기 없이 8월 클래스를 시험) |
| 4 | cl04_month12_late_year_overlay_pressure_guard | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=12_late_year_pressure | no exact 2025 date;bad_month_count decreases | test December class without memorizing 2025-12(2025-12 암기 없이 12월 클래스를 시험) |
| 5 | cl05_q3_q4_weak_overlay_class_guard | cj09_cg07_native_short_cost_firewall_short_floor_rescue | q3_q4_weak_overlay_class | bad_month_count decreases without killing stress | generalize bad month memory to quarter class(손실 월 기억을 분기 클래스로 일반화) |
| 6 | cl06_source_mix_native_overlay_balance_guard | cj09_cg07_native_short_cost_firewall_short_floor_rescue | native_overlay_balance_guard | source bucket not one tiny edge;shorts>=100 | keep synthetic overlay clue but reduce thin-source risk(합성 오버레이 단서를 보존하되 얇은 원천 위험 감소) |
| 7 | cl07_short_floor_restore_quality_control | cj09_cg07_native_short_cost_firewall_short_floor_rescue | short_floor_restore_quality_control | restored shorts do not erase net/PF edge | audit restored 14 shorts as quality not collapse mask(복원 숏 14개가 붕괴 가림막인지 감사) |
| 8 | cl08_mt5_precheck_boundary_after_month_zero | cj09_cg07_native_short_cost_firewall_short_floor_rescue | package_precheck_boundary | MT5 package only if bad_month_count==0 and stress_delta>=0 | prevent weak proxy from becoming runtime claim(약한 프록시가 런타임 주장으로 바뀌는 것을 방지) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/package_gate_decision.csv | CK review outputs package/month/source rows(CK 검토가 패키지/월/원천 행을 산출) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/input_manifest.csv | CJ input artifacts are connected(CJ 입력 산출물이 연결) |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/package_gate_decision.csv | package was rejected before MT5 handoff(MT5 인계 전 패키지를 거절) |
| proxy_mt5_diff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/proxy_mt5_diff_review.csv | proxy/MT5 diff remains explicit(프록시/MT5 차이를 명시 유지) |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/run364CL_h17_bad_month_source_balance_repair_queue.csv | CL repair queue has 8 rows(CL 수리 대기열 8행 생성) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/kpi_evidence_receipt.json | KPI/data/attribution/judgment/claim receipts exist(KPI/데이터/귀속/판정/주장 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CK/required_gate_coverage_audit.csv | required gates are connected to closeout(필수 게이트가 종료 기록에 연결) |

## Boundary(경계)

This is review only(검토 전용)입니다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없습니다.
