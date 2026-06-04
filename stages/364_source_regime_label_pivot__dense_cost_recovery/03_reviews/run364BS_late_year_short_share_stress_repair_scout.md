# run364BS late-year short-share stress repair scout(364BS 연말 숏비중 압박 수리 탐색)

## Current Truth(현재 진실)

- selected candidate(선택 후보): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`
- repair type(수리 유형): `parent_session_suppression(부모 세션 억제)`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1063.14` / `1.4220035161` / `3.0720720721` / `0.1221896383`
- month_bad_count(월 나쁨 수): `0`
- min month net/PF(최저 월 순수익/수익 팩터): `8.44` / `1.0908354181`
- parent suppressed trades(억제된 부모 거래): `5` trades, net `-15.29`
- package-like proxy rows(패키지 유사 프록시 행): `37`. This is not package authority(패키지 권위가 아님).

## Action And Effect(행동과 효과)

Action(행동): BR failure memory(BR 실패 기억)를 month-of-year/session repair(월중/세션 수리) surface(표면)로 바꾸고, BQ selected proxy(BQ 선택 프록시)를 기준으로 synthetic addition(합성 숏 추가)과 parent session suppression(부모 세션 억제)을 비교했다.

Effect(효과): selected proxy(선택 프록시)는 month stress(월 압박)를 해소했지만, new MT5 execution(새 MT5 실행)이 없어서 `run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1` review(검토)로 넘긴다.

## Top Surface(상위 표면)

| candidate_id | candidate_status | repair_type | net_profit | profit_factor | trade_density_per_business_day | short_share | parent_suppressed_trade_count | month_bad_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bs02_late_year_parent_session_suppress__moy12__h21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1063.14 | 1.4220035161 | 3.0720720721 | 0.1221896383 | 5 | 0 | 351.568099272 |
| bs02_late_year_parent_session_suppress__moy12__h21__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1063.14 | 1.4220035161 | 3.0720720721 | 0.1221896383 | 5 | 0 | 351.568099272 |
| bs02_late_year_parent_session_suppress__moy12__h19_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1069.6 | 1.4285654756 | 3.0510510511 | 0.1230314961 | 12 | 0 | 339.44843126 |
| bs02_late_year_parent_session_suppress__moy12__h19_21__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1069.6 | 1.4285654756 | 3.0510510511 | 0.1230314961 | 12 | 0 | 339.44843126 |
| bs02_late_year_parent_session_suppress__moy12__h19__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1054.31 | 1.4194241877 | 3.0660660661 | 0.1224289912 | 7 | 0 | 337.747624506 |
| bs02_late_year_parent_session_suppress__moy12__h19__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1054.31 | 1.4194241877 | 3.0660660661 | 0.1224289912 | 7 | 0 | 337.747624506 |
| bs02_late_year_parent_session_suppress__moy12__h20_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1057.91 | 1.4207776639 | 3.0540540541 | 0.1229105211 | 11 | 0 | 335.38183584 |
| bs02_late_year_parent_session_suppress__moy12__h20_21__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1057.91 | 1.4207776639 | 3.0540540541 | 0.1229105211 | 11 | 0 | 335.38183584 |
| bs02_late_year_parent_session_suppress__moy12__h18_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1062.27 | 1.4260245179 | 3.036036036 | 0.1236399604 | 17 | 0 | 330.530338324 |
| bs02_late_year_parent_session_suppress__moy12__h19_20_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1064.37 | 1.4273414674 | 3.033033033 | 0.1237623762 | 18 | 0 | 329.825135912 |
| bs02_late_year_parent_session_suppress__moy12__h19_20_21__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1064.37 | 1.4273414674 | 3.033033033 | 0.1237623762 | 18 | 0 | 329.825135912 |
| bs02_late_year_parent_session_suppress__moy12__h18_21__side_both | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1058.75 | 1.4246128142 | 3.033033033 | 0.1227722772 | 19 | 0 | 326.897979532 |
| bs02_late_year_parent_session_suppress__moy12__h17_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1071.78 | 1.4348560112 | 3.015015015 | 0.124501992 | 25 | 0 | 323.47982226 |
| bs02_late_year_parent_session_suppress__moy12__h18_19_21__side_long | package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요) | parent_session_suppression(부모 세션 억제) | 1068.73 | 1.4326933315 | 3.015015015 | 0.124501992 | 24 | 0 | 323.43728632 |

## Stress Slices(압박 조각)

| axis | segment_id | net_profit | profit_factor | trade_count | short_share | segment_status |
| --- | --- | --- | --- | --- | --- | --- |
| entry_month(진입 월) | 2025-01 | 59.0 | 1.2440110845 | 90 | 0.1111111111 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-02 | 86.74 | 1.4674915927 | 75 | 0.1866666667 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-03 | 8.44 | 1.3178957682 | 16 | 1.0 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-04 | 224.04 | 1.4654438482 | 121 | 0.132231405 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-05 | 54.78 | 1.3726944299 | 75 | 0.0666666667 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-06 | 48.96 | 1.4016966395 | 68 | 0.0294117647 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-07 | 9.23 | 1.1305626653 | 35 | 0.0571428571 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-08 | 10.8 | 1.1045971224 | 46 | 0.1086956522 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-09 | 34.02 | 1.3446442137 | 52 | 0.0384615385 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-10 | 51.96 | 1.2581606797 | 79 | 0.1012658228 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-11 | 241.83 | 2.2092185992 | 84 | 0.1547619048 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2025-12 | 12.89 | 1.0908354181 | 56 | 0.0892857143 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2026-01 | 42.61 | 1.2465281796 | 81 | 0.0740740741 | passed_slice(통과 조각) |
| entry_month(진입 월) | 2026-02 | 143.34 | 1.6423562098 | 91 | 0.1428571429 | passed_slice(통과 조각) |

## Attribution(귀속)

| comparison_id | source_candidate_id | net_diff | profit_factor_diff | month_bad_count_before | month_bad_count_after | parent_suppressed_trade_count | attribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| selected_vs_bq_reference(선택 후보 대 BQ 기준) | bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap | 15.29 | 0.0090102215 | 1 | 0 | 5 | late-year entry-known session suppression cleared the bad month in proxy(연말 진입시점 세션 억제가 프록시 불량 월을 해소) |
| suppressed_parent_trade_shape(억제된 부모 거래 형태) | run364BR_review_broad_clean_short_share_lift_scout_without_db_v1 |  |  | 1 | 0 | 5 | suppression uses month_of_year/hour/side only and does not rank by realized PnL(억제는 월중/시간/방향만 쓰며 실현손익 순위를 쓰지 않음) |
| family_top_bs02_late_year_parent_session_suppress | bs02_late_year_parent_session_suppress__moy12__h21__side_long | 0.0 | 0.0 | 0 | 0 | 5 | family top comparison for repair surface(수리 표면 계열별 최상위 비교) |
| family_top_bs01_late_year_synthetic_density_add | bs01_late_year_synthetic_density_add__moy11_12__h16__ps4300__m0800 | -3.9 | 0.0015777156 | 1 | 0 | 0 | family top comparison for repair surface(수리 표면 계열별 최상위 비교) |
| family_top_bs00_bq_reference | bs00_bq_reference__h17_19_20__ps4375__m0750__chronological_no_overlap | 15.29 | 0.0090102215 | 1 | 0 | 0 | family top comparison for repair surface(수리 표면 계열별 최상위 비교) |

## Overfit Guardrail(과적합 가드레일)

| audit_id | status | evidence | effect |
| --- | --- | --- | --- |
| timestamp_safe_feature_boundary(시점 안전 피처 경계) | passed | month_of_year, entry_hour, side, p_short, short_margin are entry-known; exact year_month is absent(월중/시간/방향/p_short/마진은 진입시점 정보이며 정확 연월은 없음) | look-ahead bias(미래참조 편향) 재발을 막는다. |
| no_outcome_priority_or_top_n(결과 우선순위와 top_n 없음) | passed | surface enumerates rule families; it never sorts trades by realized PnL for selection(규칙 계열을 열거하며 거래별 실현손익으로 정렬하지 않음) | repair(수리)가 결과 암기로 바뀌는 것을 줄인다. |
| month_of_year_overfit_watch(월중 과적합 관찰) | watch | selected_months=12; package_like_proxy_rows=37 | stress clear(압박 해소)가 바로 runtime authority(런타임 권위)가 되지 않게 한다. |
| chronological_no_overlap_guard(시간상 겹침 방지 가드) | passed | selected_overlap=0; selection_mode=chronological_no_overlap | one-position runtime meaning(단일 포지션 런타임 의미)을 보존한다. |
| package_boundary_guard(패키지 경계 가드) | watch | package_like_proxy_rows=37; new_mt5_execution=not_run | proxy(프록시)만으로 package(패키지)나 runtime authority(런타임 권위)를 주장하지 않는다. |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bs_proxy_vs_bk_mt5_runtime_probe(BS 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1063.14 | 103.5 | 1.3820937835 | 1.4220035161 | usable_for_signal_sanity_and_BT_review_not_runtime_authority(신호 점검과 BT 검토에는 사용 가능, 런타임 권위 아님) |

## BT Queue(BT 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | bt01_review_bs_selected_stress_and_overfit | review BS selected stress clear and month-of-year overfit(BS 선택 압박 해소와 월중 과적합 검토) | stress clear survives attribution without exact 2025-12 claim(정확 2025-12 주장 없이 압박 해소 귀속 유지) |
| 2 | bt02_compare_proxy_to_mt5_runtime_probe | compare BS proxy against BK MT5 runtime probe(BS 프록시와 BK MT5 런타임 탐침 비교) | diff attribution is explicit and usable only as handoff(차이 귀속이 명시되고 인계로만 사용) |
| 3 | bt03_package_precheck_only_if_review_accepts | prepare MT5 package precheck only if BT review accepts(BT 검토가 수락할 때만 MT5 패키지 사전검사 준비) | no package without BT review and MT5 reprobe(BT 검토와 MT5 재탐침 없이는 패키지 없음) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/bs_rule_surface.csv | BR repair queue(BR 수리 대기열)를 BS rule surface(BS 규칙 표면)로 실행했다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/selected_bs_candidate.json | net/PF/expectancy/DD/recovery/trades/short share를 함께 확인했다. |
| late_year_stress_repair_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/stress_slice_review.csv | BR의 2025-12 bad month(불량 월)을 month-of-year repair(월중 수리) 조건으로 변환했다. |
| no_lookahead_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/overfit_guardrail_audit.csv | 정확 연월, 실현손익 우선순위, top_n(상위 N개)을 배제했다. |
| synthetic_overlap_guard | passed | synthetic_overlap_count=0 | trade splitting(거래 쪼개기) 없이 단일 포지션 의미를 보존했다. |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/run_evidence_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/data_integrity_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/experiment_design_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/model_validation_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/performance_attribution_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/result_judgment_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/artifact_lineage_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/claim_boundary_receipt.json | experiment/data/model/lineage/judgment receipt(영수증)를 closeout(종료 기록)에 연결했다. |
| proxy_mt5_diff_recorded | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/proxy_mt5_diff_plan.csv | proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 분리해 기록했다. |
| package_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/proxy_mt5_diff_plan.csv | stress clear(압박 해소)가 있어도 새 MT5 실행 전에는 package(패키지)와 authority(권위)를 주장하지 않는다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/required_gate_coverage_audit.csv | 필수 gate(게이트)와 산출물 연결을 확인했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BS is proxy scout only(BS는 프록시 탐색 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
