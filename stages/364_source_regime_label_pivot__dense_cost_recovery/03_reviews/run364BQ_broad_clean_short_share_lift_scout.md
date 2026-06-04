# run364BQ broad clean short-share lift scout(364BQ 넓은 클린 숏비중 상승 정찰)

## Current Truth(현재 진실)

- selected candidate(선택 후보): `bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1047.85` / `1.4129932946` / `3.0870870871` / `0.1215953307`
- synthetic short PF(합성 숏 수익 팩터): `1.2349834469`
- month_bad_count(월 나쁨 수): `1`
- package candidate rows(패키지 후보 행): `0`

## Action And Effect(행동과 효과)

Action(행동): BP queue(BP 대기열)의 bo90/bo91/bo05 단서를 hour-set/p_short/margin/chronological no-overlap(시간묶음/p_short/마진/시간순 겹침방지) surface(표면)로 넓게 재생했다.

Effect(효과): short share(숏 비중)는 목표 `0.12` 이상으로 회복했지만, month stress(월 압박)와 new MT5 execution(새 MT5 실행) 부재 때문에 package(패키지)는 열지 않고 BR review(BR 검토)로 넘긴다.

## Top Surface(상위 표면)

| candidate_id | candidate_status | net_profit | profit_factor | trade_density_per_business_day | short_share | synthetic_short_profit_factor | synthetic_overlap_count | month_bad_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1047.85 | 1.4129932946 | 3.0870870871 | 0.1215953307 | 1.2349834469 | 0 | 1 | 221.2499394115 |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__raw | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1047.85 | 1.4129932946 | 3.0870870871 | 0.1215953307 | 1.2349834469 | 0 | 1 | 218.2499394115 |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4325__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1042.48 | 1.4087291319 | 3.0930930931 | 0.1233009709 | 1.1687195278 | 0 | 1 | 212.977142636 |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4350__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1042.48 | 1.4087291319 | 3.0930930931 | 0.1233009709 | 1.1687195278 | 0 | 1 | 212.977142636 |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4425__m0800__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1046.61 | 1.4082685494 | 3.0900900901 | 0.1214771623 | 1.2912058364 | 0 | 2 | 175.290641042 |
| bq05_extreme_multi_hour_overlap_guard__h16_17_18_20__ps4425__m0800__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1032.58 | 1.4008634712 | 3.0960960961 | 0.1231813773 | 1.3484740023 | 0 | 2 | 174.9822478445 |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4400__m0800__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1037.34 | 1.4014966232 | 3.1021021021 | 0.1248789932 | 1.1861142306 | 0 | 2 | 162.123748547 |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4425__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1035.27 | 1.3975129379 | 3.1111111111 | 0.1274131274 | 1.1721812909 | 0 | 2 | 160.0810939605 |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4450__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1028.63 | 1.3959968678 | 3.1021021021 | 0.1248789932 | 1.1923967089 | 0 | 2 | 159.0626304595 |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4350__m0850__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1030.61 | 1.4012069524 | 3.0930930931 | 0.1223300971 | 1.1500659798 | 0 | 2 | 152.891414283 |
| bq02_h16_extension_overlap_safe__h16_17_20__ps4350__m0800__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1051.55 | 1.4107725602 | 3.0900900901 | 0.1214771623 | 1.432586778 | 0 | 3 | 145.679592546 |
| bq02_h16_extension_overlap_safe__h16_17_20__ps4400__m0800__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1044.52 | 1.4070512358 | 3.0870870871 | 0.1206225681 | 1.4333200651 | 0 | 3 | 142.7110086925 |
| bq02_h16_extension_overlap_safe__h16_17_20__ps4450__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1038.64 | 1.4018681066 | 3.0930930931 | 0.1223300971 | 1.3682880565 | 0 | 3 | 134.2281308675 |
| bq02_h16_extension_overlap_safe__h16_17_20__ps4425__m0750__chronological_no_overlap | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1037.7 | 1.4013557214 | 3.0960960961 | 0.1231813773 | 1.3599398271 | 0 | 3 | 133.2770287385 |

## Stress Slices(압박 조각)

| axis | segment_id | net_profit | profit_factor | trade_count | short_share | segment_status |
| --- | --- | --- | --- | --- | --- | --- |
| entry_month(진입월) | 2025-01 | 59.0 | 1.2440110845 | 90 | 0.1111111111 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-02 | 86.74 | 1.4674915927 | 75 | 0.1866666667 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-03 | 8.44 | 1.3178957682 | 16 | 1.0 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-04 | 224.04 | 1.4654438482 | 121 | 0.132231405 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-05 | 54.78 | 1.3726944299 | 75 | 0.0666666667 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-06 | 48.96 | 1.4016966395 | 68 | 0.0294117647 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-07 | 9.23 | 1.1305626653 | 35 | 0.0571428571 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-08 | 10.8 | 1.1045971224 | 46 | 0.1086956522 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-09 | 34.02 | 1.3446442137 | 52 | 0.0384615385 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-10 | 51.96 | 1.2581606797 | 79 | 0.1012658228 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-11 | 241.83 | 2.2092185992 | 84 | 0.1547619048 | passed_slice(통과 조각) |
| entry_month(진입월) | 2025-12 | -2.4 | 0.9849854547 | 61 | 0.0819672131 | bad_stress(불량 압박) |
| entry_month(진입월) | 2026-01 | 42.61 | 1.2465281796 | 81 | 0.0740740741 | passed_slice(통과 조각) |
| entry_month(진입월) | 2026-02 | 143.34 | 1.6423562098 | 91 | 0.1428571429 | passed_slice(통과 조각) |

## Short-Share Attribution(숏비중 귀속)

| comparison_id | source_candidate_id | net_diff | profit_factor_diff | short_share_diff | attribution |
| --- | --- | --- | --- | --- | --- |
| selected_vs_bo00_bn_seed_h17_or_h20_margin_08_10_reference | bo00_bn_seed_h17_or_h20_margin_08_10_reference | 10.68 | 0.0028368237 | 0.0014781432 | BQ changes hour/floor surface only with entry-known fields(BQ는 진입시점 필드로 시간/하한 표면만 바꿈) |
| selected_vs_bo05_h17_margin_075_105_or_h20_margin_08_10 | bo05_h17_margin_075_105_or_h20_margin_08_10 | 21.19 | 0.004157137 | 0.0104842196 | BQ changes hour/floor surface only with entry-known fields(BQ는 진입시점 필드로 시간/하한 표면만 바꿈) |
| selected_vs_bo90_broad_h17_20_ps0440_margin080_control | bo90_broad_h17_20_ps0440_margin080_control | 3.36 | -0.0028455657 | 0.0113591102 | BQ changes hour/floor surface only with entry-known fields(BQ는 진입시점 필드로 시간/하한 표면만 바꿈) |
| selected_vs_bo91_broad_h16_17_20_ps0445_margin080_control | bo91_broad_h16_17_20_ps0445_margin080_control | -19.51 | -0.0002216936 | -0.0024356771 | BQ changes hour/floor surface only with entry-known fields(BQ는 진입시점 필드로 시간/하한 표면만 바꿈) |
| family_top_bq04_h19_bridge_short_share_lift | bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap | 0.0 | 0.0 | 0.0 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |
| family_top_bq06_h16_h19_bridge_overlap_guard | bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4425__m0800__chronological_no_overlap | 1.24 | 0.0047247452 | 0.0001181684 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |
| family_top_bq05_extreme_multi_hour_overlap_guard | bq05_extreme_multi_hour_overlap_guard__h16_17_18_20__ps4425__m0800__chronological_no_overlap | 15.27 | 0.0121298234 | -0.0015860466 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |
| family_top_bq02_h16_extension_overlap_safe | bq02_h16_extension_overlap_safe__h16_17_20__ps4350__m0800__chronological_no_overlap | -3.7 | 0.0022207344 | 0.0001181684 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |
| family_top_bq01_broad_clean_h17_20 | bq01_broad_clean_h17_20__h17_20__ps4450__m0750__chronological_no_overlap | 3.17 | -0.0033525822 | 0.0122357248 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |
| family_top_bq03_high_short_pf_guardrail | bq03_high_short_pf_guardrail__h17_20__ps4450__m0750__chronological_no_overlap | 3.17 | -0.0033525822 | 0.0122357248 | family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교) |

## Overfit Guardrail(과적합 가드레일)

| audit_id | status | evidence | effect |
| --- | --- | --- | --- |
| timestamp_safe_feature_boundary(시점 안전 피처 경계) | passed | entry_hour, p_short, short_margin_vs_long only; no exact month and no realized pnl selector(진입시/확률/마진만 사용, 정확 월 및 실현손익 선택 없음) | look-ahead bias(미래참조 편향) 재발을 차단했다. |
| chronological_no_overlap_guard(시간순 겹침 방지 가드) | passed | selected_overlap=0; selection_mode=chronological_no_overlap | 합성 숏이 서로 겹치는 후보를 운영 단서로 과장하지 않는다. |
| broad_before_micro_search(미세탐색 전 넓은 탐색) | passed | surface_rows=366; families=6 | 한 후보만 미세조정하지 않고 계열/시간/하한을 넓게 비교했다. |
| package_boundary_guard(패키지 경계 가드) | passed | package_like_proxy_rows=0; new_mt5_execution=not_run | proxy(프록시)만으로 package(패키지)나 runtime authority(런타임 권위)를 주장하지 않는다. |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bq_proxy_vs_bk_mt5_runtime_probe(BQ 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1047.85 | 88.21 | 1.3820937835 | 1.4129932946 | usable_for_signal_sanity_and_BR_review_not_runtime_authority(신호 점검 및 BR 검토에는 사용 가능, 런타임 권위 아님) |

## BR Queue(BR 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | br01_review_bq_selected_stress_and_package_gate | review selected BQ stress slices and package gate(BQ 선택 압박 조각과 패키지 게이트 검토) | month_bad_count reaches 0 or remains explicit blocker(월 나쁨 수 0 도달 또는 명시 차단) |
| 2 | br02_compare_proxy_to_mt5_runtime_probe | compare BQ proxy with source MT5 probe(BQ 프록시와 원천 MT5 탐침 비교) | diff attribution remains usable but not authority(차이 귀속은 사용 가능하되 권위 아님) |
| 3 | br03_choose_runtime_package_or_repair_seed | decide package block or next repair seed(패키지 차단 또는 다음 수리 씨앗 결정) | no authority without MT5 reprobe(MT5 재탐침 없이 권위 없음) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/bq_rule_surface.csv | BP queue(BP 대기열)를 BQ rule surface(BQ 규칙 표면)로 실행했다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/selected_bq_candidate.json | net/PF/expectancy/DD/recovery/trades/short share를 같이 점검했다. |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/run_evidence_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/data_integrity_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/experiment_design_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/model_validation_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/performance_attribution_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/result_judgment_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/artifact_lineage_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/claim_boundary_receipt.json | experiment/data/model/lineage/judgment receipt(영수증)를 closeout(종료 기록)에 연결했다. |
| no_lookahead_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/overfit_guardrail_audit.csv | 정확 월, 결과값 우선순위, top_n(상위 N개)을 사용하지 않았다. |
| synthetic_overlap_guard | passed | synthetic_overlap_count=0 | bo91 계열의 겹침 문제를 runtime-safe(런타임 안전) 제약으로 바꿨다. |
| short_share_lift_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/short_share_lift_attribution.csv | 숏 비중 목표 0.12 이상을 회복했다. |
| package_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/proxy_mt5_diff_plan.csv | 새 MT5 실행 전 package(패키지) 주장을 차단했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/required_gate_coverage_audit.csv | 필수 게이트와 산출물을 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BQ is proxy scout only(BQ는 프록시 정찰 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
