# run364BW BV runtime probe review(364BW BV 런타임 탐침 검토)

## Result(결과)

Action(행동): `run364BV` MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) report(보고서), deal table(딜 표), runtime telemetry(런타임 원격측정), proxy diff(프록시 차이)를 분해했다.

Effect(효과): synthetic short source overlay(합성 숏 원천 덧씌움)가 전체 수익을 만든 것이 아니라, native short threshold(기본 숏 임계값)과 long source(롱 원천)가 더 큰 수익 동인임을 분리했다.

- status(상태): `completed_stage364BW_reviewed_bv_runtime_probe_attribution_open_bx_no_authority`
- judgment(판정): `runtime_probe_review_positive_clue_weak_overlay_increment_native_short_and_hour17_edge_no_authority`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `966.32` / `1.38` / `1018`
- MT5 expectancy/recovery/DD(기대값/회복 계수/낙폭): `0.95` / `7.43` / `130.11`
- proxy net/PF/trades(프록시 순수익/수익 팩터/거래수): `1063.14` / `1.4220035161` / `1023`
- operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).

## Source Attribution(원천 귀속)

| source_bucket | direction | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- | --- |
| long_threshold | long | 904 | 818.6 | 0.905531 | 1.37301 | 53.650442 |
| native_short_threshold | short | 41 | 128.7 | 3.139024 | 2.079789 | 51.219512 |
| synthetic_short_overlay | short | 73 | 19.02 | 0.260548 | 1.075858 | 45.205479 |

Read(판독): synthetic overlay(합성 덧씌움)는 `73` trades(거래)에서 약한 `+19.02` net(순수익)만 만들었다. Native short(기본 숏)는 `41` trades(거래)에서 `+128.70`이고, long(롱)은 `+818.60`이다.

## Direction Attribution(방향 귀속)

| direction | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- |
| long | 904 | 818.6 | 0.905531 | 1.37301 | 53.650442 |
| short | 114 | 147.72 | 1.295789 | 1.39933 | 47.368421 |

## Time And Regime(시간 및 국면)

Worst months(취약 월):

| close_month | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- |
| 2025-12 | 59 | -21.78 | -0.369153 | 0.880211 | 52.542373 |
| 2025-08 | 47 | -1.01 | -0.021489 | 0.991177 | 42.553191 |
| 2025-07 | 35 | 7.07 | 0.202 | 1.097009 | 51.428571 |
| 2026-03 | 4 | 8.34 | 2.085 | 23.540541 | 50.0 |
| 2025-06 | 69 | 18.33 | 0.265652 | 1.147811 | 50.724638 |
| 2026-04 | 46 | 23.29 | 0.506304 | 1.231972 | 56.521739 |

Best months(강한 월):

| close_month | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- |
| 2025-11 | 85 | 231.62 | 2.724941 | 2.10248 | 58.823529 |
| 2025-04 | 120 | 182.83 | 1.523583 | 1.382594 | 50.833333 |
| 2026-02 | 92 | 145.29 | 1.579239 | 1.636623 | 59.782609 |
| 2025-05 | 75 | 113.63 | 1.515067 | 1.821976 | 58.666667 |
| 2025-02 | 75 | 70.98 | 0.9464 | 1.380141 | 53.333333 |
| 2025-10 | 79 | 51.96 | 0.657722 | 1.258161 | 56.962025 |

Close-hour attribution(청산 시간 귀속):

| close_hour | trade_count | net_profit | expectancy | profit_factor | win_rate_percent |
| --- | --- | --- | --- | --- | --- |
| 16 | 32 | 332.26 | 10.383125 | 5.679718 | 65.625 |
| 17 | 302 | 419.11 | 1.387781 | 1.506839 | 55.629139 |
| 18 | 250 | 7.67 | 0.03068 | 1.012045 | 52.0 |
| 19 | 183 | 125.93 | 0.688142 | 1.315875 | 51.36612 |
| 20 | 123 | 88.09 | 0.716179 | 1.27302 | 49.593496 |
| 21 | 112 | 13.21 | 0.117946 | 1.049293 | 50.892857 |
| 22 | 16 | -19.95 | -1.246875 | 0.507407 | 50.0 |

## Proxy MT5 Diff(프록시 MT5 차이)

| comparison | proxy_net_profit | mt5_net_profit | net_diff_proxy_minus_mt5 | proxy_trade_count | mt5_trade_count | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| proxy_total_vs_bv_mt5_total | 1063.14 | 966.32 | 96.82 | 1023 | 1018 | proxy remains useful for signal sanity, but MT5 report is KPI authority(프록시는 신호 점검용, MT5 보고서가 KPI 권위). |
| proxy_synthetic_short_vs_runtime_overlay_trade_source | 33.15 | 19.02 | 14.13 | 47 | 73 | runtime overlay fired more trades with lower expectancy(런타임 덧씌움은 거래가 늘고 기대값이 낮아짐). |
| runtime_native_short_vs_runtime_overlay |  | 128.7 | 109.68 |  | 41 | native short threshold carried stronger short edge than synthetic overlay(기본 숏 임계값이 합성 덧씌움보다 강함). |
| runtime_long_source_share |  | 818.6 |  |  | 904 | most MT5 profit remains long source driven(대부분의 MT5 수익은 롱 원천에서 나옴). |

Attribution confidence(귀속 신뢰도): medium(중간). Deal-level PnL(딜 단위 손익)과 runtime source(런타임 원천)는 매칭됐지만, overlay/calendar(덧씌움/달력 차단)의 true counterfactual(진짜 반사실)은 아직 별도 MT5 ablation(절제 실행)이 필요하다.

## Next Probe(다음 탐침)

| variant_id | action | evidence_seed | success_condition |
| --- | --- | --- | --- |
| bx01_overlay_hour17_only_keep_native_short | MT5 runtime ablation(MT5 런타임 절제): keep native short threshold(기본 숏 임계값 유지), restrict synthetic overlay(합성 덧씌움 제한) to hour 17 only. | BV overlay open-hour attribution: hour17 net +90.14, non-17 overlay net -71.12. | net improves over BV without PF/recovery/trade-density collapse(BV보다 순수익 개선, PF/회복/밀도 붕괴 없음). |
| bx02_native_short_only_overlay_disabled | MT5 runtime control(MT5 런타임 대조): disable synthetic overlay(합성 덧씌움 비활성) while keeping calendar block(달력 차단 유지). | Synthetic overlay source net was only +19.02; native short source net was +128.70. | isolates whether overlay adds real net or only churn(덧씌움이 실제 수익인지 회전인지 분리). |
| bx03_hour17_overlay_plus_weak_late_session_firewall | MT5 runtime probe(MT5 런타임 탐침): hour17 overlay(17시 덧씌움) plus weak close-hour 22/late-session risk firewall(22시/후반 세션 위험 방화벽). | Close hour 22 net -19.95 and 18/21 near-flat; month 12 remained negative. | improves December and weak-session risk without deleting trade density(12월/약세 세션 위험 개선, 거래 밀도 유지). |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/kpi_contract_audit.csv | MT5 KPI와 파싱 거래가 일치한다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/row_grain_audit.csv | 거래/신호 행 단위가 분리된다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/source_authority_audit.csv | MT5와 proxy 권위 경계를 분리한다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/performance_attribution_receipt.json | 성과 귀속 산출물이 생성된다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/claim_boundary_receipt.json | 운영 승격/런타임 권위를 주장하지 않는다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BW/required_gate_coverage_audit.csv | 필수 gate를 종료 기록에 연결한다. |

## Boundary(경계)

This review(이 검토)는 runtime probe review(런타임 탐침 검토)만 주장한다. Forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
