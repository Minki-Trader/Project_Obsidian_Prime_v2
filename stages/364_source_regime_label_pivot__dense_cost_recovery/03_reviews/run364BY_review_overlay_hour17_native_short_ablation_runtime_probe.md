# run364BY review overlay hour17 native short ablation runtime probe(364BY 17시 오버레이 기본 숏 제거 비교 런타임 탐침 검토)

## Result(결과)

Action(행동): run364BX(364BX 실행)의 three-way MT5 runtime ablation(3방향 MT5 런타임 제거 비교)을 trade-level attribution(거래 단위 귀속), source bucket(원천 버킷), month/session stress(월/세션 압박), variant delta(변형 차이)로 검토했다.

Effect(효과): `bx03`의 개선이 “운영 승격”이 아니라 December h22 long guard(12월 22시 롱 가드)와 h17 overlay(17시 오버레이)의 runtime clue(런타임 단서)임을 분리했다.

- status(상태): `completed_stage364BY_reviewed_bx_runtime_ablation_attribution_open_bz_no_authority`
- judgment(판정): `runtime_ablation_review_positive_clue_bx03_december_late_session_guard_no_authority`
- best variant(최선 변형): `bx03_hour17_overlay_plus_weak_late_session_firewall`
- best MT5 net/PF/trades/density(최선 MT5 순수익/수익 팩터/거래수/밀도): `1008.18` / `1.4` / `1008` / `3.2101910828`
- BX3 vs BV net delta(BX3-BV 순수익 차이): `41.86`
- BX3 vs BX1 net delta(BX3-BX1 순수익 차이): `21.16`
- attribution confidence(귀속 신뢰도): `medium_runtime_trade_membership_exact_but_forward_unproven`

## Variant KPI(변형 KPI)

| variant_id | trade_count | net_profit | expectancy | profit_factor | win_rate_percent | avg_hold_minutes |
| --- | --- | --- | --- | --- | --- | --- |
| bx01_overlay_hour17_only_keep_native_short | 1008 | 987.02 | 0.979187 | 1.388571 | 53.075397 | 114.539319 |
| bx02_native_short_only_overlay_disabled | 1002 | 945.93 | 0.944042 | 1.374984 | 52.994012 | 115.060512 |
| bx03_hour17_overlay_plus_weak_late_session_firewall | 1008 | 1008.18 | 1.000179 | 1.400235 | 53.075397 | 113.428208 |

## Source Attribution(원천 귀속)

| source_bucket | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- |
| long_threshold | 903 | 883.52 | 0.978427 | 1.409384 | 53.820598 |
| native_short_threshold | 66 | 55.47 | 0.840455 | 1.220049 | 43.939394 |
| synthetic_short_overlay | 39 | 69.19 | 1.774103 | 1.636405 | 51.282051 |

## Worst BX3 Months(BX3 최악 월)

| close_month | trade_count | net_profit | expectancy | profit_factor |
| --- | --- | --- | --- | --- |
| 2025-08 | 47 | -1.01 | -0.021489 | 0.991177 |
| 2025-12 | 59 | -0.62 | -0.010508 | 0.996141 |
| 2025-07 | 35 | 5.13 | 0.146571 | 1.068565 |
| 2026-03 | 4 | 8.34 | 2.085 | 23.540541 |
| 2026-04 | 46 | 23.29 | 0.506304 | 1.231972 |
| 2026-01 | 82 | 30.85 | 0.37622 | 1.169851 |

## Pair Deltas(쌍 비교 차이)

| comparison_id | net_delta_left_minus_right | left_only_count | right_only_count | left_only_net | right_only_net | common_net_delta | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bx03_vs_bx01_late_firewall_increment | 21.16 | 1 | 1 | -16.94 | -38.1 | 0.0 | bx03 improvement is one December h22 long loss removed minus one h17 overlay short loss(bx03 개선은 12월 22시 롱 손실 차단에서 17시 오버레이 숏 손실을 뺀 효과). |
| bx01_vs_bx02_hour17_overlay_increment | 41.09 | 13 | 7 | 50.53 | 9.44 | 0.0 | hour17 overlay adds net positive but with several replacement trades(17시 오버레이는 순수익 양수이나 일부 대체 거래를 만든다). |
| bx03_vs_bx02_overlay_plus_late_firewall_increment | 62.25 | 14 | 8 | 33.59 | -28.66 | 0.0 | membership delta left_only=33.59; right_only=-28.66; common=0.00 |
| bx03_vs_bv_full_overlay_and_late_firewall_increment | 41.86 | 13 | 23 | -10.02 | -51.88 | 0.0 | restricting overlay to h17 plus late firewall improves net while reducing short count(오버레이를 17시로 제한하고 후반 방화벽을 더해 순수익은 개선, 숏 수는 감소). |

## Next Queue(다음 대기열)

| queue_id | action | evidence_seed | success_condition |
| --- | --- | --- | --- |
| bz01_december_h22_long_block_counterfactual | Materialize BX3 late-session guard input(BX3 후반 세션 가드 입력 구체화) | bx03 vs bx01: removed 2025-12-10 22:05 long loss -38.10 and added 2025-12-11 17:05 short loss -16.94, net +21.16. | confirm December h22 long block without exact-year memorization(정확한 연도 암기 없이 12월 22시 롱 차단 확인) |
| bz02_h17_overlay_loss_guard_quality_floor | Scout h17 overlay quality floor(17시 오버레이 품질 하한 탐색) | h17 overlay is positive versus native-only, but BX3 added one -16.94 h17 synthetic short loss. | keep h17 overlay net while reducing loss tail(17시 오버레이 순수익을 유지하면서 손실 꼬리 축소) |
| bz03_equity_dd_cluster_review | Materialize equity drawdown cluster inputs(평가손익 낙폭 클러스터 입력 구체화) | BX3 net/PF improved, but equity DD amount stayed 130.11. | identify drawdown cluster without reducing density below 3/day(밀도 3/day를 깨지 않고 낙폭 클러스터 식별) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/kpi_contract_audit.csv | scoreboard(점수표)와 deal table(딜 표) KPI를 대조한다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/row_grain_audit.csv | closed trade(종료 거래) 단위 귀속을 고정한다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/source_authority_audit.csv | MT5 report(보고서)와 telemetry(런타임 기록)의 권위를 분리한다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/performance_attribution_receipt.json | KPI 변화 원인과 대안을 기록한다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BY/claim_boundary_receipt.json | 운영 승격과 런타임 권위를 주장하지 않는다. |

## Boundary(경계)

runtime probe review(런타임 탐침 검토)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
