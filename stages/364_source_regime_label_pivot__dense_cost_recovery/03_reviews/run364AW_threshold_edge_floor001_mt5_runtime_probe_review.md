# run364AW threshold edge floor001 MT5 runtime probe review(364AW 임계값 경계 하한 0.001 MT5 런타임 탐침 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AW_review_threshold_edge_floor001_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1`
- judgment(판정): `mixed_positive_runtime_probe_net_pf_recovery_clue_promotion_ineligible_trade_density_below_floor_long_skew_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## KPI Read(KPI 판독)

- MT5 net/PF/trades(메타트레이더5 순수익/수익 팩터/거래수): `878.55` / `1.36` / `971`
- expectancy/recovery/DD(기대값/회복 계수/낙폭): `0.9` / `6.75` / `17.51%`
- trade density(거래 밀도): `2.9159159159` per business day(영업일당), floor(하한) `3.0`
- long/short(롱/숏): `887` / `84`
- proxy diff(프록시 차이): net(순수익) `16.267`, trades(거래수) `-94`

## Judgment(판정)

Action(행동): AV runtime probe(런타임 탐침)를 KPI(핵심 성과 지표), density guardrail(밀도 가드레일), session/side/month attribution(세션/방향/월 귀속), runtime parity(런타임 동등성)로 검토했다.

Effect(효과): net/PF/RF(순수익/수익 팩터/회복 계수)는 강한 단서지만, 실제 trade density(거래 밀도) `2.9159159159`가 3/day(일 3회) 하한 아래라 promotion_candidate(승격 후보)도 아직 주장하지 않는다.

## Density Guardrail(거래 밀도 가드레일)

| guardrail_id | value | threshold | status | evidence | effect |
| --- | --- | --- | --- | --- | --- |
| actual_mt5_trade_density | 2.9159159159 | 3.0 | failed | 971 trades / 333 business_days | 실제 MT5 거래 밀도(actual MT5 trade density, 실제 MT5 거래 밀도)가 사용자 하한 3/day(일 3회)을 넘지 못했다. |
| proxy_density_survival | 3.1981981982 | 3.0 | proxy_pass_mt5_fail | proxy 1065 vs MT5 971; ratio 0.9117370892 | proxy(프록시)는 밀도를 통과했지만 MT5(메타트레이더5)에서는 거래수 94개가 줄어 다음 후보는 proxy density buffer(프록시 밀도 완충)가 필요하다. |
| actual_long_share | 0.9134912461 | 0.85 | warning_long_skew | long=887, short=84 | short(숏)이 수익은 냈지만 비중은 낮아 방향 균형(long/short balance, 롱/숏 균형)이 아직 약하다. |
| actual_period_density_crosscheck | 2.9159159159 | 3.0 | failed | 2025-01-02..2026-04-13, business_days=333 | 거래 리포트(report, 보고서)의 실제 첫/마지막 거래 기간 기준으로도 밀도 하한에 못 미친다. |

## Proxy vs MT5 Attribution(프록시 대 MT5 귀속)

| review_id | expected | actual | diff_actual_minus_expected | status | attribution | usability |
| --- | --- | --- | --- | --- | --- | --- |
| net_pf_proxy_useful | 862.283 | 878.55 | 16.267 | usable_directionally | MT5(메타트레이더5)가 proxy(프록시)보다 net/PF(순수익/수익 팩터)를 높게 냈으므로 신호 방향성은 유지된다. | proxy(프록시)는 후보 선별 보조로 유지하되 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. |
| density_proxy_not_sufficient | 1065 | 971 | -94 | requires_mt5_density_buffer | 확률/결정 parity(동등성)는 맞았으므로 거래수 차이는 확률 오류보다 MT5 position lifecycle(포지션 생명주기), fill/report semantics(체결/보고 의미), broker tester behavior(브로커 테스터 동작) 쪽에 가깝다. | 다음 proxy gate(프록시 게이트)는 3.35/day 이상을 요구해야 MT5 3/day 하한 생존 가능성이 커진다. observed_ratio=0.9117370892 |

## Side Attribution(방향 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| long | 887 | 775.81 | 1.35506991 | 0.874645 | 53.664036 | 1098 |
| short | 84 | 102.74 | 1.358653913 | 1.223095 | 45.238095 | 805 |

## Entry Hour Attribution(진입 시간 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | 84 | 207.14 | 1.643631731 | 2.465952 | 52.380952 | 1098 |
| 17 | 277 | 201.92 | 1.321943909 | 0.728953 | 53.429603 | 23 |
| 20 | 123 | 198.66 | 1.755447389 | 1.615122 | 53.658537 | 247 |
| 22 | 11 | 141.28 | 6.045714286 | 12.843636 | 63.636364 | 804 |
| 16 | 127 | 59.2 | 1.146480267 | 0.466142 | 55.905512 | 10 |
| 18 | 218 | 50.51 | 1.099380226 | 0.231697 | 50.0 | 25 |
| 19 | 131 | 19.84 | 1.062190458 | 0.15145 | 52.671756 | 19 |

## Monthly Attribution(월별 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-11 | 78 | 211.42 | 2.027957407 | 2.710513 | 58.974359 | 806 |
| 2025-04 | 119 | 207.56 | 1.429126695 | 1.744202 | 50.420168 | 804 |
| 2026-02 | 85 | 125.75 | 1.618544024 | 1.479412 | 60.0 | 808 |
| 2025-02 | 70 | 92.79 | 1.585610603 | 1.325571 | 55.714286 | 805 |
| 2025-05 | 72 | 63.82 | 1.480427582 | 0.886389 | 55.555556 | 804 |
| 2025-10 | 76 | 54.01 | 1.296839791 | 0.710658 | 57.894737 | 229 |
| 2025-06 | 66 | 52.4 | 1.463143009 | 0.793939 | 51.515152 | 228 |
| 2025-01 | 81 | 51.88 | 1.22029724 | 0.640494 | 53.08642 | 1098 |
| 2026-04 | 45 | 20.28 | 1.210504463 | 0.450667 | 57.777778 | 7 |
| 2026-01 | 79 | 16.68 | 1.085354621 | 0.211139 | 46.835443 | 229 |
| 2025-07 | 34 | 16.6 | 1.26370135 | 0.488235 | 55.882353 | 230 |
| 2025-03 | 7 | 10.42 | 1.918871252 | 1.488571 | 57.142857 | 6 |
| 2026-03 | 4 | 8.34 | 23.540540541 | 2.085 | 50.0 | 6 |
| 2025-08 | 44 | 1.84 | 1.018064009 | 0.041818 | 45.454545 | 247 |
| 2025-09 | 50 | -4.21 | 0.959070581 | -0.0842 | 38.0 | 230 |
| 2025-12 | 61 | -51.03 | 0.725261118 | -0.836557 | 49.180328 | 229 |

## Findings(발견)

| finding_id | severity | finding | effect |
| --- | --- | --- | --- |
| net_pf_recovery_positive | positive_clue | MT5 net/PF/RF(순수익/수익 팩터/회복 계수) = 878.55 / 1.36 / 6.75 | threshold-edge floor001(임계값 경계 하한 0.001)은 계속 수리할 가치가 있는 런타임 단서다. |
| runtime_parity_clean | positive_clue | matched_rows=17428, mismatch_rows=0, max_abs_probability_diff=5.965400001750609e-08 | 실패가 확률 변환 오류가 아니라 거래 형태/런타임 의미 쪽임을 좁힌다. |
| short_side_positive | positive_clue | short trades(숏 거래) 84개가 net(순수익) 102.74를 만들었다. | 롱 전용 문제를 줄이는 다음 공격 탐색 씨앗으로 쓸 수 있다. |
| density_below_user_floor | promotion_blocker | actual MT5 trade density(실제 MT5 거래 밀도) 2.9159159159 < 3/day | 사용자 목표의 trade per day(일별 거래수) 하한을 못 넘으므로 승격 후보가 아니다. |
| long_skew | promotion_blocker | long/short(롱/숏) = 887 / 84 | 방향 균형(long/short balance, 롱/숏 균형)이 아직 약해 운영 주장을 닫을 수 없다. |
| equity_drawdown_stress | stress | equity max drawdown(수익곡선 최대 낙폭) = 17.51% | 회복 계수는 좋지만 실거래 준비(live readiness, 실거래 준비)에는 drawdown stress(낙폭 압박) 추가 검토가 필요하다. |
| proxy_density_overstated | stress | proxy(프록시)는 1065 trades(거래)를 예상했지만 MT5(메타트레이더5)는 971 trades(거래)만 만들었다. | 다음 proxy gate(프록시 게이트)는 밀도 완충을 요구해야 한다. |

## Required Gates(필수 게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AV/threshold_edge_floor001_mt5_probe_summary.csv | MT5 report KPI(MT5 보고서 핵심 성과 지표)를 review(검토) 기준으로 고정한다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/closed_trade_attribution.csv | report trade count(보고서 거래수)와 parsed closed trades(파싱된 종료 거래)를 맞춘다. |
| source_authority_audit(진실 원천 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AV/strategy_tester_report_records.json | proxy(프록시)가 아니라 Strategy Tester(전략 테스터)를 KPI 권위로 둔다. |
| runtime_parity_evidence_gate(런타임 동등성 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/runtime_quality_review.csv | probability/decision parity(확률/결정 동등성)를 AW 판정에 연결한다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/monthly_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/entry_hour_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/side_attribution.csv | 월/시간/방향 성과를 분리해 다음 수리 방향을 만든다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/claim_boundary_receipt.json | positive clue(긍정 단서)를 runtime authority(런타임 권위)나 operating promotion(운영 승격)으로 올리지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AW/required_gate_coverage_audit.csv | kpi_evidence(KPI 근거) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Next Action(다음 행동)

`run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1`에서 density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 materialize(구체화)한다. trade splitting(거래 쪼개기)은 사용하지 않는다.

## Boundary(경계)

이 결과는 runtime_probe_review(런타임 탐침 검토)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
