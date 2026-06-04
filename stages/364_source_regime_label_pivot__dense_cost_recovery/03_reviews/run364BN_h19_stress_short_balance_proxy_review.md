# run364BN h19 stress short-balance proxy review(364BN h19 압박 숏 균형 프록시 검토)

## Current Truth(현재 진실)

- BM selected(선택): `bm04_short_router_ps0440_h17_20_overlay_fixed6`
- BM combined proxy net/PF/density/short share(BM 합산 프록시 순수익/수익 팩터/밀도/숏비중): `967.76` / `1.3650661562` / `3.1471471471` / `0.1440839695`
- BM synthetic short net/PF(BM 합성 숏 순수익/수익 팩터): `-38.057` / `0.8733691583`
- package decision(패키지 결정): `rejected_package_ineligible(패키지 부적격 거절)`
- selected repair seed(선택 수리 씨앗): `bn02_h17_or_h20_margin_08_10_quality_repair`

## Action And Effect(행동과 효과)

Action(행동): BM combined proxy(합산 프록시)를 attribution(귀속), package gate(패키지 게이트), repair seed(수리 씨앗)으로 분리했다.

Effect(효과): BM 자체는 package candidate(패키지 후보)가 아니지만, `bn02_h17_or_h20_margin_08_10_quality_repair`가 synthetic short PF(합성 숏 수익 팩터)와 short share(숏 비중)를 동시에 살리는 공격 탐색 씨앗으로 남았다.

## Attribution(귀속)

| attribution_id | baseline_net | displaced_parent_net_profit | synthetic_short_net_profit | combined_net_profit | judgment |
| --- | --- | --- | --- | --- | --- |
| bm_selected_combined_proxy(BM 선택 합산 프록시) | 959.64 | -46.18 | -38.057 | 967.76 | combined_gain_from_removing_losing_parent_trades_not_positive_short_source(합산 개선은 양수 숏 원천이 아니라 손실 부모 거래 제거 영향) |
| selected_repair_seed(선택 수리 씨앗) |  | -33.54 | 43.99 | 1037.17 | repair_seed_positive_proxy_but_same_tape_review_only(수리 씨앗은 프록시 양수지만 동일 테이프 검토 전용) |

## Package Gate(패키지 게이트)

| gate_id | subject | status | reason | effect |
| --- | --- | --- | --- | --- |
| bm_selected_package_gate(BM 선택 패키지 게이트) | bm04_short_router_ps0440_h17_20_overlay_fixed6 | rejected_package_ineligible(거절, 패키지 부적격) | synthetic_short_pf=0.8733691583 < 1.15 | BM 합산 프록시 개선을 MT5 패키지 후보로 올리지 않는다. |
| repair_seed_package_gate(수리 씨앗 패키지 게이트) | bn02_h17_or_h20_margin_08_10_quality_repair | not_package_candidate_repair_scout_first(패키지 후보 아님, 수리 정찰 우선) | seed_short_pf=1.3816978038 passes proxy floor but same-tape and no MT5 reprobe(프록시 하한은 통과하지만 동일 테이프 및 MT5 재탐침 없음) | BO scout(BO 정찰)에서 forward/regime stress(전진/국면 압박)를 먼저 본다. |

## Repair Seed Surface(수리 씨앗 표면)

| seed_id | candidate_status | net_profit | profit_factor | trade_count | trade_density_per_business_day | short_share | synthetic_short_profit_factor | synthetic_short_net_profit | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bn05_h17_or_margin_08_10_all_watch | rejected_short_source_pf_below_1_15(거절, 숏 원천 PF 1.15 미만) | 1010.3 | 1.3939824555 | 1031 | 3.0960960961 | 0.1270611057 | 1.0472088022 | 7.57 | -89.258380606 |
| bn00_bm_selected_h17_20_ps0440_reference | rejected_short_source_pf_below_1_15(거절, 숏 원천 PF 1.15 미만) | 967.76 | 1.3650661562 | 1048 | 3.1471471471 | 0.1440839695 | 0.8733691583 | -38.06 | -129.047448988 |
| bn02_h17_or_h20_margin_08_10_quality_repair | repair_seed_review_candidate_no_authority(수리 씨앗 검토 후보, 권위 없음) | 1037.17 | 1.4101564709 | 1024 | 3.0750750751 | 0.1201171875 | 1.3816978038 | 43.99 | 61.807338718 |
| bn03_h17_or_h20_p0445_quality_repair | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1036.17 | 1.4101649494 | 1022 | 3.0690690691 | 0.1183953033 | 1.2538319111 | 31.53 | -43.908479776 |
| bn04_h17_or_p046_quality_watch | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1025.98 | 1.404606048 | 1022 | 3.0690690691 | 0.1183953033 | 1.3343368205 | 39.98 | -48.8149929 |
| bn01_h17_only_short_source_quality | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1019.86 | 1.4036183558 | 1019 | 3.0600600601 | 0.1157998037 | 1.2655745708 | 29.38 | -49.38624746 |

## Short Source Segments(숏 원천 조각)

| axis | segment_id | synthetic_short_trade_count | synthetic_short_net_profit | synthetic_short_profit_factor | segment_status |
| --- | --- | --- | --- | --- | --- |
| entry_hour(진입시) | 17 | 36 | 29.38 | 1.2655745708 | positive_clue(긍정 단서) |
| entry_hour(진입시) | 18 | 18 | -24.81 | 0.6969260092 | watch_or_negative(관찰 또는 음수) |
| entry_hour(진입시) | 19 | 17 | -38.57 | 0.5384900738 | watch_or_negative(관찰 또는 음수) |
| entry_hour(진입시) | 20 | 9 | -4.06 | 0.8343330477 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-01 | 8 | 12.3 | 1.5760101128 | positive_clue(긍정 단서) |
| entry_month(진입월) | 2025-02 | 6 | 19.04 | 2.3362335111 | positive_clue(긍정 단서) |
| entry_month(진입월) | 2025-03 | 17 | -23.38 | 0.7048484848 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-04 | 6 | 9.72 | 1.3406246714 | positive_clue(긍정 단서) |
| entry_month(진입월) | 2025-05 | 3 | -15.51 | 0.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-06 | 2 | -15.09 | 0.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-07 | 1 | -2.86 | 0.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-08 | 4 | -7.67 | 0.5012360135 | watch_or_negative(관찰 또는 음수) |

## Forward/Regime Stress(전진/국면 압박)

| axis | segment_id | trade_count | net_profit | profit_factor | short_share | segment_status |
| --- | --- | --- | --- | --- | --- | --- |
| quarter(분기) | 2025Q1 | 177 | 161.91 | 1.3653943366 | 0.2033898305 | positive(양수) |
| quarter(분기) | 2025Q2 | 263 | 307.37 | 1.4041045463 | 0.0874524715 | positive(양수) |
| quarter(분기) | 2025Q3 | 134 | 56.93 | 1.2087385049 | 0.0746268657 | positive(양수) |
| quarter(분기) | 2025Q4 | 223 | 276.45 | 1.4978703479 | 0.1121076233 | positive(양수) |
| quarter(분기) | 2026Q1 | 181 | 211.22 | 1.5325903326 | 0.1602209945 | positive(양수) |
| quarter(분기) | 2026Q2 | 46 | 23.29 | 1.2319721116 | 0.0 | positive(양수) |
| month(월) | 2025-01 | 89 | 76.45 | 1.3382189642 | 0.1011235955 | positive(양수) |
| month(월) | 2025-02 | 74 | 94.73 | 1.5334572281 | 0.1756756757 | positive(양수) |
| month(월) | 2025-03 | 14 | -9.26 | 0.7656451654 | 1.0 | stress_watch(압박 관찰) |
| month(월) | 2025-04 | 121 | 205.24 | 1.4179957109 | 0.1404958678 | positive(양수) |
| month(월) | 2025-05 | 75 | 43.41 | 1.2756472538 | 0.0666666667 | positive(양수) |
| month(월) | 2025-06 | 67 | 58.72 | 1.5236778739 | 0.0149253731 | positive(양수) |

## BO Queue(BO 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | bo01_train_h17_h20_margin_short_source_quality_repair_scout | train/replay selected repair seed as proxy scout(선택 수리 씨앗을 프록시 정찰로 학습/재생) | synthetic short PF>=1.15, combined PF>=1.35, density>=3/day, short_share>=0.12 across stress slices(합성 숏 PF 1.15 이상, 합산 PF 1.35 이상, 밀도 3/day 이상, 숏비중 0.12 이상) |
| 2 | bo02_reject_exact_month_shortcut_and_test_entry_known_rules | forbid exact month rescue and test entry-known hour/margin/probability rules(정확 월 구조 금지 및 진입시점 시간/마진/확률 규칙 시험) | no exact future losing month dependency and no top_n(미래 손실 월 의존 없음, top_n 없음) |
| 3 | bo03_mt5_package_only_after_proxy_and_stress_survive | prepare MT5 package only after BO proxy and stress pass(BO 프록시와 압박 통과 뒤에만 MT5 패키지 준비) | BO review keeps proxy/MT5 diff plan and runtime parity handoff(BO 검토가 프록시/MT5 차이 계획과 런타임 동등성 인계를 유지) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/repair_seed_surface.csv | net/PF/expectancy/DD/recovery/trades/short share를 함께 검토했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/attribution_decomposition.csv | BM selected row(선택 행), synthetic short row(합성 숏 행), displaced parent row(대체 부모 행)를 분리했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/package_gate_decision.csv | MT5 KPI(MT5 핵심 성과 지표)는 BK/BM 근거로 제한하고 BN은 리뷰 권위만 가진다. |
| package_reject_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/package_gate_decision.csv | BM 선택 후보를 패키지 후보에서 제외했다. |
| repair_seed_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/selected_repair_seed.json | BO로 넘길 공격 수리 씨앗을 찾았다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/selected_repair_trade_tape.csv | 새 거래 쪼개기 없이 one-position proxy(단일 포지션 프록시)만 유지했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/run364BO_short_source_quality_repair_queue.csv | 다음 BO 작업과 필수 리뷰 게이트를 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BN/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 차단했다. |

## Boundary(경계)

BN is review only(BN은 검토 전용). No new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
