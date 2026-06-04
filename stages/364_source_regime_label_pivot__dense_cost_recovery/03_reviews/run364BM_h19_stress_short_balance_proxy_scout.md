# run364BM h19 stress short-balance proxy scout(364BM h19 압박 숏 균형 프록시 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1`
- selected_variant(선택 변형): `bm04_short_router_ps0440_h17_20_overlay_fixed6`
- selected net/PF/expectancy/trades/density(선택 순수익/수익 팩터/기대값/거래수/밀도): `967.76` / `1.3650661562` / `0.9234379771` / `1048` / `3.1471471471`
- selected long/short/share(선택 롱/숏/비중): `897` / `151` / `0.1440839695`
- selected closed DD/recovery(선택 종료거래 낙폭/회복 계수): `74.067` / `13.0660483076`
- parent MT5 net/PF/trades/equity DD(부모 MT5 순수익/수익 팩터/거래수/평가손익 낙폭): `959.64` / `1.38` / `1006` / `18.24%`
- synthetic short PF/net(합성 숏 PF/순수익): `0.8733691583` / `-38.057`. This is no package candidate(패키지 후보 없음) until repaired.

## Action And Effect(행동과 효과)

Action(행동): BL queue(BL 대기열)를 closed trade + telemetry + US100 raw M5(종료거래 + 실행기록 + US100 원천 5분봉)로 proxy scout(프록시 정찰)했다.

Effect(효과): h17-20 short router(17~20시 숏 라우터)는 combined proxy(합산 프록시)를 개선했지만 standalone short source(숏 원천 단독)는 음수라서, BN review(BN 검토)에서 package reject(패키지 거절) 또는 short source repair(숏 원천 수리)로 분리한다.

## Top Surface(상위 표면)

| variant_id | candidate_status | net_profit | profit_factor | trade_count | trade_density_per_business_day | closed_drawdown_amount | short_share | synthetic_added_short_count | displaced_parent_trade_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bm04_short_router_ps0440_h17_20_overlay_fixed6 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) | 967.76 | 1.3650661562 | 1048 | 3.1471471471 | 74.067 | 0.1440839695 | 80 | 38 | 42.444884498 |
| bm04_short_router_ps0445_h17_20_overlay_fixed6 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) | 940.74 | 1.3589312545 | 1030 | 3.0930930931 | 68.32 | 0.1262135922 | 55 | 31 | 18.099433672 |
| bm04_short_router_ps0435_h17_20_overlay_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 928.72 | 1.340121946 | 1065 | 3.1981981982 | 109.692 | 0.1624413146 | 112 | 53 | -184.66244884 |
| bm03_short_router_ps0440_all_hours_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 811.27 | 1.2834881168 | 1072 | 3.2192192192 | 208.958 | 0.1641791045 | 106 | 40 | -283.990871042 |
| bm03_short_router_ps0445_all_hours_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 792.26 | 1.2817469406 | 1049 | 3.1501501502 | 213.242 | 0.1439466158 | 78 | 35 | -306.891683168 |
| bm00_current_h19_mt5_closed_trade_reference | watch_short_share_still_below_target(숏 비중 목표 미달 관찰) | 959.64 | 1.3820937835 | 1006 | 3.021021021 | 84.86 | 0.0984095427 | 0 | 0 | -107.18353982 |
| bm05_hold7to12_low_margin_guard_0005 | watch_short_share_still_below_target(숏 비중 목표 미달 관찰) | 954.52 | 1.3804566181 | 1003 | 3.012012012 | 88.0 | 0.0987038883 | 0 | 0 | -112.545927724 |
| bm02_december_h18_19_low_margin_soft_guard_0005 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) | 970.83 | 1.3976953391 | 981 | 2.9459459459 | 73.97 | 0.1009174312 | 0 | 0 | -1098.644154284 |

## Rejected Or Watch(거절 또는 관찰)

| variant_id | candidate_status | net_profit | profit_factor | trade_count | short_share | closed_drawdown_amount |
| --- | --- | --- | --- | --- | --- | --- |
| bm04_short_router_ps0440_h17_20_overlay_fixed6 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) | 967.76 | 1.3650661562 | 1048 | 0.1440839695 | 74.067 |
| bm04_short_router_ps0445_h17_20_overlay_fixed6 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) | 940.74 | 1.3589312545 | 1030 | 0.1262135922 | 68.32 |
| bm04_short_router_ps0435_h17_20_overlay_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 928.72 | 1.340121946 | 1065 | 0.1624413146 | 109.692 |
| bm03_short_router_ps0440_all_hours_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 811.27 | 1.2834881168 | 1072 | 0.1641791045 | 208.958 |
| bm03_short_router_ps0445_all_hours_fixed6 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) | 792.26 | 1.2817469406 | 1049 | 0.1439466158 | 213.242 |
| bm00_current_h19_mt5_closed_trade_reference | watch_short_share_still_below_target(숏 비중 목표 미달 관찰) | 959.64 | 1.3820937835 | 1006 | 0.0984095427 | 84.86 |
| bm05_hold7to12_low_margin_guard_0005 | watch_short_share_still_below_target(숏 비중 목표 미달 관찰) | 954.52 | 1.3804566181 | 1003 | 0.0987038883 | 88.0 |
| bm02_december_h18_19_low_margin_soft_guard_0005 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) | 970.83 | 1.3976953391 | 981 | 0.1009174312 | 73.97 |

## Forward/Regime Replay(전진/국면 재생)

| segment_type | segment_id | trade_count | net_profit | profit_factor | trade_density_per_business_day | short_share |
| --- | --- | --- | --- | --- | --- | --- |
| quarter | 2025Q1 | 186 | 135.3 | 1.2673187906 | 3.0 | 0.252688172 |
| quarter | 2025Q2 | 268 | 295.76 | 1.3796053738 | 4.1230769231 | 0.1044776119 |
| quarter | 2025Q3 | 134 | 56.93 | 1.2087385049 | 2.0303030303 | 0.0746268657 |
| quarter | 2025Q4 | 228 | 271.64 | 1.4736664063 | 3.5076923077 | 0.1359649123 |
| quarter | 2026Q1 | 186 | 200.04 | 1.4884567019 | 3.0 | 0.1827956989 |
| quarter | 2026Q2 | 46 | 8.09 | 1.0736056774 | 5.1111111111 | 0.0217391304 |
| month | 2025-01 | 90 | 67.11 | 1.2776488402 | 4.0909090909 | 0.1333333333 |
| month | 2025-02 | 75 | 93.65 | 1.5242552143 | 3.75 | 0.1866666667 |
| month | 2025-03 | 21 | -25.47 | 0.7031242714 | 1.05 | 1.0 |
| month | 2025-04 | 123 | 212.13 | 1.4320155921 | 5.5909090909 | 0.1544715447 |
| month | 2025-05 | 76 | 40.0 | 1.2486325211 | 3.4545454545 | 0.0789473684 |
| month | 2025-06 | 69 | 43.63 | 1.3429492218 | 3.2857142857 | 0.0434782609 |
| month | 2025-07 | 35 | 9.23 | 1.1305626653 | 1.5217391304 | 0.0571428571 |
| month | 2025-08 | 46 | 10.8 | 1.1045971224 | 2.1904761905 | 0.1086956522 |

## Short Source(숏 원천)

| audit_id | short_threshold | available_short_like_cycle_count | synthetic_added_short_count | displaced_parent_trade_count | synthetic_short_net_profit | profit_factor | short_share | candidate_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| short_like_cycle_coverage(숏 유사 사이클 커버리지) |  |  |  |  |  |  |  |  |
| bm04_short_router_ps0440_h17_20_overlay_fixed6 | 0.44 | 107 | 80 | 38 | -38.057 | 1.3650661562 | 0.1440839695 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) |
| bm04_short_router_ps0445_h17_20_overlay_fixed6 | 0.445 | 66 | 55 | 31 | -27.842 | 1.3589312545 | 0.1262135922 | watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수) |
| bm04_short_router_ps0435_h17_20_overlay_fixed6 | 0.435 | 155 | 112 | 53 | -47.909 | 1.340121946 | 0.1624413146 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) |
| bm03_short_router_ps0440_all_hours_fixed6 | 0.44 | 167 | 106 | 40 | -157.271 | 1.2834881168 | 0.1641791045 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) |
| bm03_short_router_ps0445_all_hours_fixed6 | 0.445 | 119 | 78 | 35 | -149.72 | 1.2817469406 | 0.1439466158 | watch_pf_below_keep_floor(PF 유지 하한 미달 관찰) |
| selected_short_balance(선택 숏 균형) |  |  |  |  |  |  |  |  |

## Equity DD Boundary(평가손익 낙폭 경계)

| diagnostic_id | value | percent | delta_vs_baseline | status | effect |
| --- | --- | --- | --- | --- | --- |
| parent_mt5_equity_dd(부모 MT5 평가손익 낙폭) | 18.24 |  |  | stress_required(압박 필요) | closed-trade proxy(종료거래 프록시)가 MT5 equity path(MT5 평가손익 경로)를 대체하지 못함을 기록한다. |
| baseline_closed_trade_dd(기준 종료거래 낙폭) | 84.86 | 14.4168390608 |  | proxy_reference(프록시 기준) | BM 후보의 낙폭 개선은 종료거래 기준으로만 비교한다. |
| selected_closed_trade_dd(선택 종료거래 낙폭) | 74.067 | 10.4672676456 | -10.793 | proxy_improved(프록시 개선) | BN review(BN 검토)에서 MT5 equity DD(MT5 평가손익 낙폭) 재탐침 필요 여부를 결정하게 한다. |

## BN Queue(BN 대기열)

| queue_rank | queue_id | review_question | success_criteria |
| --- | --- | --- | --- |
| 1 | bn01_review_combined_gain_vs_negative_short_source | Is the combined gain caused by displacing worse parent trades rather than positive short source?(합산 개선이 양수 숏 원천이 아니라 더 나쁜 부모 거래 대체에서 온 것인가?) | attribution separates synthetic short PF from displaced parent PnL(합성 숏 PF와 대체된 부모 손익을 분리) |
| 2 | bn02_repair_short_source_quality_or_reject_package | Can short source quality be repaired without long hard-delete or trade splitting?(롱 강제 삭제나 거래 쪼개기 없이 숏 원천 품질을 수리할 수 있는가?) | synthetic short PF>=1.15 and combined PF>=1.35 with density>=3/day(합성 숏 PF 1.15 이상, 합산 PF 1.35 이상, 밀도 3/day 이상) |
| 3 | bn03_package_gate_only_if_short_source_positive | Only if short source becomes positive, prepare narrow MT5 runtime probe handoff(숏 원천이 양수로 바뀔 때만 좁은 MT5 런타임 탐침 인계를 준비할 것인가?) | fixed parameters plus positive short source and proxy/MT5 diff plan(고정 파라미터 + 양수 숏 원천 + 프록시/MT5 차이 계획) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/proxy_scout_surface.csv | BL queue(BL 대기열)의 forward/regime, short source, equity DD 축을 BM surface(BM 표면)로 닫았다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/selected_proxy_candidate.json | net/PF/expectancy/DD/recovery/trades/long-short를 동시에 기록했다. |
| data_integrity_join_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/entry_probability_join_audit.csv | closed trade(종료거래)와 telemetry(실행 기록)를 1:1로 결합했다. |
| raw_bar_proxy_label_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/raw_bar_price_parity_audit.csv | US100 raw M5(원천 5분봉) 기반 synthetic short label(합성 숏 라벨)의 최소 가격 정합성을 확인했다. |
| short_balance_proxy_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/short_source_feasibility.csv | short share(숏 비중) 목표는 통과했지만 short source PF(숏 원천 PF)는 별도 실패 기억으로 낮췄다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/selected_proxy_trade_tape.csv | synthetic short(합성 숏)은 fixed hold(고정 보유) 단일 포지션 의미로만 추가했다. |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/run_evidence_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/data_integrity_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/experiment_design_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/model_validation_receipt.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/artifact_lineage_receipt.json | experiment_execution(실험 실행) 스킬 영수증을 산출물에 연결했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/run364BN_review_queue.csv | BN review(BN 검토) 이전에 필수 게이트와 다음 조건을 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BM/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 차단했다. |

## Claim Boundary(주장 경계)

This run(이번 실행)은 proxy scout(프록시 정찰)이다. New MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.
