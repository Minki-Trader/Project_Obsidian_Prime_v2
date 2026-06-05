# run364CL h17 bad month source balance repair inputs(364CL 17시 손실 월 원천 균형 수리 입력)

Updated(갱신): 2026-06-05T09:40:13Z

## Current Truth(현재 진실)

- status(상태): `completed_stage364CL_h17_bad_month_source_balance_repair_inputs_materialized_open_cm_no_authority`
- judgment(판정): `experiment_design_materialized_bad_month_source_balance_repair_inputs_no_authority`
- next run(다음 실행): `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1`
- queue rows(대기열 행): `16`
- reviewed seed(검토 씨앗): `cj09_cg07_native_short_cost_firewall_short_floor_rescue`
- reviewed KPI(검토 핵심 성과 지표): net `1034.32`, PF `1.4184722658`, density `3.1942675159`, shorts `100`
- blocker(차단 원인): bad months(손실 월) `2025-08;2025-12`

## Action And Effect(행동과 효과)

Action(행동): CK package rejection(CK 패키지 거절)을 bad month class guard(손실 월 클래스 가드), source balance(원천 균형), short restore quality(숏 복원 품질), package precheck boundary(패키지 사전점검 경계)로 materialize(구체화)했다.

Effect(효과): CM scout(CM 정찰)가 no-split(무분할), no top_n(no top_n), no exact-year date filter(정확 연도 날짜 필터 없음) 조건으로 바로 proxy replay(프록시 재생)할 수 있다.

## Failure Memory(실패 기억)

| memory_id | memory_type | source_segment | class_guard | net_profit | profit_factor | converted_constraint |
| --- | --- | --- | --- | --- | --- | --- |
| bad_month__2025-08 | bad_month_failure(손실 월 실패) | 2025-08 | month_of_year=08;quarter=Q3 | -1.43 | 0.98857093 | use reusable month/quarter class guard, not exact-year filter(재사용 월/분기 클래스 가드 사용, 정확 연도 필터 금지) |
| bad_month__2025-12 | bad_month_failure(손실 월 실패) | 2025-12 | month_of_year=12;quarter=Q4 | -0.62 | 0.9961409187 | use reusable month/quarter class guard, not exact-year filter(재사용 월/분기 클래스 가드 사용, 정확 연도 필터 금지) |
| month_stability_package_gate | package_gate_failure(패키지 게이트 실패) | monthly stability(월 안정성) | bad_month_count=2;bad_months=2025-08,2025-12 | 1034.32 | 1.4184722658 | 남은 손실 월을 다음 repair constraint(수리 제약)으로 바꾼다. |
| mt5_runtime_package_gate | package_gate_failure(패키지 게이트 실패) | new MT5 execution(새 MT5 실행) | new_mt5_execution=not_run(새 MT5 실행 미실행) | 1034.32 | 1.4184722658 | proxy(프록시)를 runtime authority(런타임 권위)로 올리지 않는다. |

## Repair Axes(수리 축)

| axis_id | axis_name | timestamp_safe_inputs | success_criteria | forbidden_shortcut |
| --- | --- | --- | --- | --- |
| cl_axis_01_bad_month_class | bad month class guard(손실 월 클래스 가드) | month_of_year and quarter known at entry(진입 시점에 알려진 월/분기) | bad_month_count decreases without exact-year filter(정확 연도 필터 없이 손실 월 수 감소) | top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터) |
| cl_axis_02_late_year_pressure | late-year pressure guard(연말 압박 가드) | month_of_year=12 and Q4 class(12월 및 4분기 클래스) | December-class weakness improves without deleting a calendar month(달력 월 삭제 없이 12월 계열 약점 개선) | top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터) |
| cl_axis_03_source_balance | native/synthetic short source balance(기본/합성 숏 원천 균형) | native short floor, synthetic overlay cap, source mix(기본 숏 하한, 합성 오버레이 상한, 원천 혼합) | short_count stays >=100 and edge is not one thin source(숏 100개 이상 유지 및 얇은 단일 원천 의존 회피) | top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터) |
| cl_axis_04_restore_quality | short-floor restore quality(숏 하한 복원 품질) | restored native shorts are quality-filtered by entry-known fields(복원 기본 숏을 진입 시점 필드로 품질 필터) | restored shorts preserve PF/net rather than masking collapse(복원 숏이 붕괴를 가리는 대신 PF/순수익 보존) | top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터) |
| cl_axis_05_package_precheck | package precheck boundary(패키지 사전점검 경계) | bad_month_count==0 and stress_delta>=0 before MT5 package(MT5 패키지 전 손실 월 0 및 압박 차이 0 이상) | proxy package only opens after all prechecks pass(모든 사전점검 통과 후에만 프록시 패키지 개방) | top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터) |

## Bad Month Classes(손실 월 클래스)

| source_bad_month | month_of_year_guard | quarter_guard | session_guard | exact_date_filter_status |
| --- | --- | --- | --- | --- |
| 2025-08 | month_of_year=08 | quarter=Q3 | open_hour=17 pressure class(17시 진입 압박 클래스) | forbidden(금지) |
| 2025-12 | month_of_year=12 | quarter=Q4 | open_hour=17 pressure class(17시 진입 압박 클래스) | forbidden(금지) |

## Source Balance(원천 균형)

| source_bucket | trade_count | net_profit | profit_factor | short_trade_count | short_share_of_shorts | cm_constraint |
| --- | --- | --- | --- | --- | --- | --- |
| long_threshold | 903 | 871.13 | 1.4046363376 | 0 | 0.0 | cap synthetic overlay and restore native short quality(합성 오버레이 상한 및 기본 숏 품질 복원) |
| native_short_threshold | 61 | 94.0 | 1.4475655431 | 61 | 0.61 | cap synthetic overlay and restore native short quality(합성 오버레이 상한 및 기본 숏 품질 복원) |
| synthetic_short_overlay | 39 | 69.19 | 1.6364054452 | 39 | 0.39 | cap synthetic overlay and restore native short quality(합성 오버레이 상한 및 기본 숏 품질 복원) |

## CM Queue(CM 대기열)

| queue_rank | candidate_id | axis_id | seed_candidate_id | month_guard_policy | source_mix_policy | short_floor_policy | expected_effect |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | cm01_cj09_month08_class_soft_guard | cl_axis_01_bad_month_class | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=08 | native_overlay_balance_keep | restore_native_short_until_floor_100 | turn August class into reusable guard(8월 클래스를 재사용 가드로 전환) |
| 2 | cm02_cj09_month12_class_soft_guard | cl_axis_02_late_year_pressure | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=12 | native_overlay_balance_keep | restore_native_short_until_floor_100 | turn December class into reusable guard(12월 클래스를 재사용 가드로 전환) |
| 3 | cm03_cj09_q3_q4_combo_guard | cl_axis_01_bad_month_class | cj09_cg07_native_short_cost_firewall_short_floor_rescue | quarter=Q3_or_Q4 | native_overlay_balance_keep | restore_native_short_until_floor_100 | generalize weak months to quarter class(약한 월을 분기 클래스로 일반화) |
| 4 | cm04_cj09_month08_12_pair_guard | cl_axis_01_bad_month_class | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=08_or_12 | native_overlay_balance_keep | restore_native_short_until_floor_100 | test paired month class without exact-year filter(정확 연도 필터 없이 쌍 월 클래스 시험) |
| 5 | cm05_cj11_month12_salvage_guard | cl_axis_02_late_year_pressure | cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue | month_of_year=12 | native_overlay_balance_keep | restore_native_short_until_floor_100 | use lower bad-month seed as package bridge(손실 월 감소 씨앗을 패키지 다리로 사용) |
| 6 | cm06_cj11_q4_late_year_balance | cl_axis_02_late_year_pressure | cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue | quarter=Q4 | native_overlay_balance_keep | restore_native_short_until_floor_100 | test late-year class on cj11 seed(cj11 씨앗에서 연말 클래스 시험) |
| 7 | cm07_cj09_native_short_floor105_quality | cl_axis_04_restore_quality | cj09_cg07_native_short_cost_firewall_short_floor_rescue | none | native_short_first_quality | restore_native_short_until_floor_105 | raise native short quality floor(기본 숏 품질 하한 상향) |
| 8 | cm08_cj09_native_short_floor110_pressure | cl_axis_03_source_balance | cj09_cg07_native_short_cost_firewall_short_floor_rescue | none | native_short_first_quality | restore_native_short_until_floor_110 | test whether extra native shorts improve balance(추가 기본 숏이 균형을 개선하는지 시험) |
| 9 | cm09_cj09_synthetic_overlay_cap | cl_axis_03_source_balance | cj09_cg07_native_short_cost_firewall_short_floor_rescue | none | synthetic_overlay_cap_30_percent | restore_native_short_until_floor_100 | reduce thin synthetic source risk(얇은 합성 원천 위험 감소) |
| 10 | cm10_cj09_native_synthetic_even_mix | cl_axis_03_source_balance | cj09_cg07_native_short_cost_firewall_short_floor_rescue | none | native_synthetic_even_short_mix | restore_native_short_until_floor_100 | test balanced short source mix(균형 숏 원천 혼합 시험) |
| 11 | cm11_cj09_late_year_h17_pressure | cl_axis_02_late_year_pressure | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=12;open_hour=17 | native_overlay_balance_keep | restore_native_short_until_floor_100 | separate late-year and h17 pressure(연말과 17시 압박 분리) |
| 12 | cm12_cj09_august_h17_pressure | cl_axis_01_bad_month_class | cj09_cg07_native_short_cost_firewall_short_floor_rescue | month_of_year=08;open_hour=17 | native_overlay_balance_keep | restore_native_short_until_floor_100 | separate August and h17 pressure(8월과 17시 압박 분리) |
| 13 | cm13_cj10_trade_shape_quality_bridge | cl_axis_04_restore_quality | cj10_cg12_trade_shape_quality_no_split_short_floor_rescue | none | trade_shape_quality_bridge | restore_native_short_until_floor_100 | reuse trade-shape quality without splitting(거래 쪼개기 없이 거래 형태 품질 재사용) |
| 14 | cm14_cj05_august_guard_anchor | cl_axis_01_bad_month_class | cj05_month_of_year_08_overlay_soft_guard | month_of_year=08 | overlay_month_pressure_sensitive | preserve_short_floor_100 | anchor August guard to prior CJ row(8월 가드를 기존 CJ 행에 고정) |
| 15 | cm15_cj07_december_guard_anchor | cl_axis_02_late_year_pressure | cj07_month_of_year_12_overlay_soft_guard | month_of_year=12 | overlay_month_pressure_sensitive | preserve_short_floor_100 | anchor December guard to prior CJ row(12월 가드를 기존 CJ 행에 고정) |
| 16 | cm16_package_precheck_control | cl_axis_05_package_precheck | cj09_cg07_native_short_cost_firewall_short_floor_rescue | bad_month_count_zero_required | precheck_flags_only | precheck_flags_only | keep MT5 package boundary explicit(MT5 패키지 경계 명시 유지) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/run364CM_h17_bad_month_source_balance_repair_scout_queue.csv | CM queue has materialized rows(CM 대기열 행 구체화) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/input_manifest.csv | CL inputs are connected(CL 입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/data_integrity_audit.csv | timestamp/top_n/split guards passed(시점/top_n/쪼개기 가드 통과) |
| repair_axis_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/repair_axis_map.csv | repair axes and seed matrix exist(수리 축과 씨앗 행렬 존재) |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/run364CM_h17_bad_month_source_balance_repair_scout_queue.csv | next scout queue has 16 rows(다음 정찰 대기열 16행) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/experiment_design_receipt.json | required receipts exist(필수 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/required_gate_coverage_audit.csv | required gates are connected to closeout(필수 게이트가 종료 기록에 연결) |

## Boundary(경계)

CL is materialization only(CL은 구체화 전용)이다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없다.
