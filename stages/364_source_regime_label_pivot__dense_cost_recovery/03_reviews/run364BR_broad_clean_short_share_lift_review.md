# run364BR broad clean short-share lift review(364BR 넓은 클린 숏비중 상승 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1047.85` / `1.4129932946` / `3.0870870871` / `0.1215953307`
- month_bad_count(월 나쁨 수): `1`
- min month net/PF(최저 월 순수익/수익 팩터): `-2.4` / `0.9849854547`
- package decision(패키지 결정): `rejected_package_ineligible_late_year_month_stress_no_mt5(패키지 부적격 거절, 연말 월 압박 및 MT5 없음)`
- next repair focus(다음 수리 초점): `late_year_short_share_density_stress_repair(연말 숏비중/밀도 압박 수리)`

## Action And Effect(행동과 효과)

Action(행동): BQ selected proxy(BQ 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), next repair queue(다음 수리 대기열)로 분리했다.

Effect(효과): BQ proxy(프록시)는 좋은 offensive seed(공격 씨앗)이지만, 2025-12 stress(2025-12 압박)와 new MT5 execution(새 MT5 실행) 없음 때문에 package(패키지)는 거절하고 BS repair(BS 수리)를 연다.

## Package Gate(패키지 게이트)

| gate_id | subject | gate_status | evidence | effect |
| --- | --- | --- | --- | --- |
| headline_kpi_gate | selected proxy KPI(선택 프록시 핵심 성과) | passed_for_proxy(프록시 통과) | net=1047.85;pf=1.4129932946;density=3.0870870871;short_share=0.1215953307 | proxy clue remains useful(프록시 단서는 유용하게 남김) |
| month_stress_gate | monthly stability(月 안정성) | failed_for_package(패키지 실패) | month_bad_count=1;min_month_net=-2.4;min_month_pf=0.9849854547 | late-year stress must become repair constraint(연말 압박을 수리 제약으로 바꿈) |
| mt5_runtime_gate | new MT5 execution(새 MT5 실행) | failed_for_package(패키지 실패) | new_mt5_execution=not_run | proxy cannot replace MT5 KPI(프록시는 MT5 핵심 성과를 대체하지 않음) |
| package_candidate_row_gate | package candidate rows(패키지 후보 행) | failed_for_package(패키지 실패) | package_candidate_rows=0 | package not opened before stress and runtime evidence(압박/런타임 근거 전 패키지 열지 않음) |

## Stress Failure Attribution(압박 실패 귀속)

| failure_id | failure_type | segment | net_profit | profit_factor | trade_count | density | short_share | repair_use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entry_month(진입월)__2025-12 | late_year_month_stress(연말 월 압박) | 2025-12 | -2.4 | 0.9849854547 | 61 | 2.7727272727 | 0.0819672131 | BS should test month-of-year/late-year stress repair without exact 2025-12 memorization(BS는 정확한 2025-12 암기 없이 월중/연말 압박 수리를 시험) |

## Positive Clues(긍정 단서)

| clue_id | clue_type | net_profit | profit_factor | density | short_share | synthetic_short_profit_factor | month_bad_count | usable_as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap | selected_bq_proxy_clue(선택 BQ 프록시 단서) | 1047.85 | 1.4129932946 | 3.0870870871 | 0.1215953307 | 1.2349834469 | 1 | BS offensive repair seed(BS 공격 수리 씨앗) |
| bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__chronological_no_overlap | family_top_bq04_h19_bridge_short_share_lift(계열 상위 단서) | 1047.85 | 1.4129932946 | 3.0870870871 | 0.1215953307 | 1.2349834469 | 1 | repair comparison seed(수리 비교 씨앗) |
| bq06_h16_h19_bridge_overlap_guard__h16_17_19_20__ps4425__m0800__chronological_no_overlap | family_top_bq06_h16_h19_bridge_overlap_guard(계열 상위 단서) | 1046.61 | 1.4082685494 | 3.0900900901 | 0.1214771623 | 1.2912058364 | 2 | repair comparison seed(수리 비교 씨앗) |
| bq05_extreme_multi_hour_overlap_guard__h16_17_18_20__ps4425__m0800__chronological_no_overlap | family_top_bq05_extreme_multi_hour_overlap_guard(계열 상위 단서) | 1032.58 | 1.4008634712 | 3.0960960961 | 0.1231813773 | 1.3484740023 | 2 | repair comparison seed(수리 비교 씨앗) |
| bq02_h16_extension_overlap_safe__h16_17_20__ps4350__m0800__chronological_no_overlap | family_top_bq02_h16_extension_overlap_safe(계열 상위 단서) | 1051.55 | 1.4107725602 | 3.0900900901 | 0.1214771623 | 1.432586778 | 3 | repair comparison seed(수리 비교 씨앗) |

## Proxy/MT5 Diff Review(프록시/MT5 차이 검토)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bq_proxy_vs_bk_mt5_runtime_probe(BQ 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1047.85 | 88.21 | 1.3820937835 | 1.4129932946 | usable_for_signal_sanity_and_BS_seed_not_runtime_authority(신호 점검 및 BS 씨앗에는 사용 가능, 런타임 권위 아님) |

## BS Queue(BS 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | bs01_late_year_short_share_density_repair | test late-year/month-of-year short-share and density repair(연말/월중 숏비중 및 밀도 수리 시험) | PF>=1.35, density>=3, short_share>=0.12, synthetic_short_pf>=1.15, month_bad_count=0, overlap=0(PF 1.35 이상, 밀도 3 이상, 숏비중 0.12 이상, 합성 숏 PF 1.15 이상, 월 나쁨 0, 겹침 0) |
| 2 | bs02_q4_session_bridge_control | compare h19 bridge with Q4/session controls(19시 브리지와 4분기/세션 대조 비교) | late-year repair survives without top_n or outcome-priority(연말 수리가 top_n/결과값 우선순위 없이 생존) |
| 3 | bs03_runtime_package_precheck_if_stress_clears | prepare MT5 package precheck only if stress clears(압박이 사라질 때만 MT5 패키지 사전점검 준비) | no package without stress_clear and proxy/MT5 diff review(압박 해소와 프록시/MT5 차이 검토 없이는 패키지 없음) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/positive_clue_register.csv | net/PF/expectancy/DD/recovery/trades/long-short를 분리 검토했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/package_gate_decision.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/stress_failure_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/proxy_mt5_diff_review.csv | 패키지, 압박, 프록시-MT5 차이를 서로 다른 행 단위로 분리했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BQ/final_decision.json | BQ 산출물만 사용하고 proxy(프록시)를 MT5 KPI(MT5 핵심 성과)로 대체하지 않았다. |
| package_reject_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/package_gate_decision.csv | 월 압박과 MT5 미실행 때문에 package(패키지)를 거절했다. |
| stress_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/stress_failure_attribution.csv | 2025-12 실패를 다음 수리 제약으로 전환했다. |
| next_offensive_seed_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/run364BS_late_year_short_share_stress_repair_queue.csv | BS 공격 탐색 대기열을 열었다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/required_gate_coverage_audit.csv | 필수 게이트와 closeout(종료 기록)을 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BR/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BR is review only(BR은 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
