# run364CH cost-stable h17 source guard review(364CH 비용 안정 17시 원천 가드 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `cg09_best_open_hour_overlay_focus`
- reviewed KPI(검토 핵심 성과 지표): net/PF/expectancy/density/trades(순수익/수익 팩터/기대값/밀도/거래수) `1001.5` / `1.3999745705` / `0.9945382324` / `3.2070063694` / `1007`
- long/short balance(롱/숏 균형): `903` / `104`
- month bad count(나쁜 월 수): `2` with `['2025-08', '2025-12']`
- cost stress(비용 압박): `stress_watch(압박 관찰)`, stress delta(압박 차이) `-1.13`
- package decision(패키지 결정): `rejected_package_open_ci_repair_inputs_no_authority(패키지 거절, CI 수리 입력 개방, 권위 없음)`
- next action(다음 행동): `run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1`

## Action And Effect(행동과 효과)

Action(행동): CG selected proxy(CG 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), CI queue(CI 대기열)로 분리했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`의 작은 positive clue(긍정 단서)는 보존하지만, bad months(나쁜 월), cost stress watch(비용 압박 관찰), new MT5 execution(새 MT5 실행) 없음 때문에 package(패키지)는 거절하고 CI repair(CI 수리)를 연다.

## Package Gate(패키지 게이트)

| gate_id | subject | gate_status | evidence | effect |
| --- | --- | --- | --- | --- |
| headline_proxy_kpi_gate | selected proxy KPI(선택 프록시 핵심 성과) | passed_for_proxy(프록시 기준 통과) | net_delta=4.01;pf_delta=0.0022270568;density=3.2070063694;shorts=104 | 작은 positive clue(긍정 단서)는 보존하지만 package(패키지) 판단은 뒤 게이트에 맡긴다. |
| no_trade_splitting_gate | trade splitting boundary(거래 쪼개기 경계) | passed_no_split(무분할 통과) | candidate_status=proxy_review_candidate_no_split(프록시 검토 후보, 무분할);trade_delta=-1 | 거래수를 쪼개 수익을 나눈 결과가 아님을 분리 기록한다. |
| month_stability_package_gate | monthly stability(월별 안정성) | failed_for_package(패키지 기준 실패) | bad_month_count=2;bad_months=2025-08,2025-12 | 나쁜 월을 다음 repair constraint(수리 제약)로 바꾼다. |
| cost_stress_package_gate | cost stress(비용 압박) | failed_for_package(패키지 기준 실패) | stress_delta=-1.13;stress_judgment=stress_watch(압박 관찰) | 스왑 haircut(헤어컷) 진단이 MT5 KPI(MT5 핵심 성과)를 대체하지 못하게 막는다. |
| mt5_runtime_package_gate | new MT5 execution(새 MT5 실행) | failed_for_package(패키지 기준 실패) | new_mt5_execution=not_run(새 MT5 실행 미실행) | proxy(프록시)를 runtime authority(런타임 권위)로 승격하지 않는다. |
| package_decision_gate | package decision(패키지 결정) | rejected_open_repair_inputs(거절, 수리 입력 개방) | bad_months=2;stress_delta=-1.13;new_mt5_execution=not_run | CH를 운영 패키지가 아니라 CI materialization(CI 구체화)로 넘긴다. |

## Stress Failure Attribution(압박 실패 귀속)

| failure_id | failure_type | axis | segment | net_profit | profit_factor | trade_count | short_trade_count | repair_use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bad_month__2025-08 | month_stability_failure(월 안정성 실패) | open_month(진입 월) | 2025-08 | -1.43 | 0.98857093 | 47 | 4 | CI should test month-of-year/quarter guard without exact 2025 month memorization(CI는 정확한 2025년 월 암기 없이 월중/분기 가드를 시험) |
| bad_month__2025-12 | month_stability_failure(월 안정성 실패) | open_month(진입 월) | 2025-12 | -0.62 | 0.9961409187 | 59 | 6 | CI should test month-of-year/quarter guard without exact 2025 month memorization(CI는 정확한 2025년 월 암기 없이 월중/분기 가드를 시험) |
| cost_haircut_selected_delta | cost_stress_watch(비용 압박 관찰) | swap_haircut(스왑 헤어컷) | selected_candidate(선택 후보) | 1001.5 | 1.3999745705 | 1007 | 104 | CI should keep h17 clue only if stress-adjusted delta clears(CI는 압박 조정 차이가 해소될 때만 17시 단서를 유지) |
| sparse_synthetic_overlay_positive_but_thin | thin_positive_source(얇은 긍정 원천) | source_bucket(원천 버킷) | synthetic_short_overlay | 73.2 | 1.6990736319 | 38 | 38 | CI should preserve clue but add short-floor and stress controls(CI는 단서를 보존하되 숏 하한과 압박 대조를 붙임) |

## Positive Clues(긍정 단서)

| clue_id | clue_type | net_profit | profit_factor | trade_count | short_trade_count | net_delta_vs_parent | usable_as |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cg09_best_open_hour_overlay_focus | selected_h17_focus_proxy_clue(선택 17시 집중 프록시 단서) | 1001.5 | 1.3999745705 | 1007 | 104 | 4.01 | CI primary repair seed(CI 주 수리 씨앗) |
| cg09_best_open_hour_overlay_focus__long_threshold | source_attribution_clue(원천 귀속 단서) | 871.13 | 1.4046363376 | 903 | 0 |  | source balance diagnostic(원천 균형 진단) |
| cg09_best_open_hour_overlay_focus__native_short_threshold | source_attribution_clue(원천 귀속 단서) | 57.17 | 1.2346763567 | 66 | 66 |  | source balance diagnostic(원천 균형 진단) |
| cg09_best_open_hour_overlay_focus__synthetic_short_overlay | source_attribution_clue(원천 귀속 단서) | 73.2 | 1.6990736319 | 38 | 38 |  | source balance diagnostic(원천 균형 진단) |
| cg07_native_short_cost_firewall | higher_net_salvage_seed(더 높은 순수익 회수 씨앗) | 1071.27 | 1.4472258461 | 989 | 86 | 73.78 | CI secondary comparison seed; repair short floor if below 100(CI 보조 비교 씨앗, 100 미만이면 숏 하한 수리) |
| cg12_trade_shape_quality_no_split | higher_net_salvage_seed(더 높은 순수익 회수 씨앗) | 1033.47 | 1.4226630855 | 993 | 90 | 35.98 | CI secondary comparison seed; repair short floor if below 100(CI 보조 비교 씨앗, 100 미만이면 숏 하한 수리) |
| cg08_bad_overlay_month_guard_scout | higher_net_salvage_seed(더 높은 순수익 회수 씨앗) | 1031.29 | 1.4210169271 | 992 | 89 | 33.8 | CI secondary comparison seed; repair short floor if below 100(CI 보조 비교 씨앗, 100 미만이면 숏 하한 수리) |

## Proxy/MT5 Diff Review(프록시/MT5 차이 검토)

| comparison_id | parent_mt5_net | proxy_net | net_diff_proxy_minus_parent | parent_mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| selected_proxy_vs_parent_mt5(선택 프록시 대 상위 MT5) | 997.49 | 1001.5 | 4.01 | 1.4 | 1.3999745705 | usable_for_CI_seed_and_signal_sanity_not_runtime_authority(CI 씨앗과 신호 점검에는 사용 가능, 런타임 권위는 아님) |

## CI Queue(CI 대기열)

| queue_rank | queue_id | action | success_criteria | effect |
| --- | --- | --- | --- | --- |
| 1 | ci01_h17_focus_cost_stress_guard | materialize h17 focus with cost stress guard(17시 집중에 비용 압박 가드를 붙여 구체화) | stress_adjusted_net_delta>=0, PF>=parent, density>=3, short_count>=100(압박 조정 순수익 차이 0 이상, PF 상위 이상, 밀도 3 이상, 숏 100개 이상) | CG의 작은 h17 lift(17시 우위)를 비용에 버티는 수리 입력으로 바꾼다. |
| 2 | ci02_bad_month_micro_guard_no_exact_date | test month-of-year/quarter guard without exact 2025 date memorization(정확한 2025년 날짜 암기 없이 월중/분기 가드 시험) | bad_month_count decreases without deleting one known month(알려진 특정 월 삭제 없이 나쁜 월 수 감소) | 2025-08/2025-12 실패를 과적합 필터가 아니라 timestamp-safe(시점 안전) 국면 제약으로 바꾼다. |
| 3 | ci03_short_floor_rescue_from_cg07_cg12 | rescue net lift from cg07/cg12 while restoring short floor(cg07/cg12 순수익 우위를 회수하되 숏 하한 복원) | net lift remains positive and short_count>=100(순수익 우위 양수 유지, 숏 100개 이상) | 더 큰 net lift(순수익 우위)를 버리지 않고 long/short balance(롱/숏 균형) 제약과 결합한다. |
| 4 | ci04_mt5_reprobe_precheck_only_if_stress_clears | prepare MT5 precheck only after stress clears(압박이 해소된 뒤에만 MT5 사전 점검 준비) | no MT5 package unless CI clears stress and source balance(CI가 압박과 원천 균형을 통과하기 전 MT5 패키지 없음) | external verification(외부 검증)을 미루지 않되, 약한 proxy(프록시)를 곧장 runtime claim(런타임 주장)으로 올리지 않는다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/positive_clue_register.csv | net/PF/expectancy/DD/recovery/trades/long-short를 분리 검토했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/package_gate_decision.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/stress_failure_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/proxy_mt5_diff_review.csv | package(패키지), stress(압박), proxy/MT5 diff(프록시/MT5 차이)를 다른 행 단위로 분리했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CG/final_decision.json | CG 산출물만 사용하고 proxy(프록시)를 MT5 KPI(MT5 핵심 성과)로 대체하지 않았다. |
| package_reject_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/package_gate_decision.csv | 월/비용 압박과 MT5 미실행 때문에 package(패키지)를 거절했다. |
| stress_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/stress_failure_attribution.csv | 나쁜 월과 비용 압박을 CI repair constraint(CI 수리 제약)로 전환했다. |
| next_offensive_seed_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/run364CI_h17_focus_month_cost_stress_repair_queue.csv | same Stage364(같은 364단계) 안에서 다음 공격 수리 대기열을 열었다. |
| proxy_mt5_diff_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/proxy_mt5_diff_review.csv | proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)를 구분했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CH/work_packet.json | work packet(작업 묶음)의 필수 gate(게이트)가 closeout(종료 기록)에 연결됐다. |

## Boundary(경계)

CH is review only(CH는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
