# run364BF density restore stress candidate MT5 runtime probe review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1`
- judgment(판정): `positive_runtime_probe_density_survived_pf_lift_clean_parity_forward_regime_stress_required_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## KPI Read(KPI 판독)

- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `900.36` / `1.35` / `1016`
- expectancy/recovery/DD(기대값/회복 계수/낙폭): `0.89` / `6.92` / `18.3%`
- trade density(거래 밀도): `3.0510510511` per business day(영업일당), floor(하한) `3.0`
- long/short(롱/숏): `917` / `99`
- proxy diff(프록시 차이): net(순수익) `-19.39`, PF(수익 팩터) `0.0321995832`, trades(거래수) `-96`

## Judgment(판정)

Action(행동): BE runtime probe(BE 런타임 탐침)를 KPI(핵심 성과 지표), density guardrail(밀도 가드레일), session/side/month attribution(세션/방향/월 귀속), runtime parity(런타임 동등성)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서지만, forward pass(전진 통과)와 live-like replay(실거래 유사 재생)가 없어 operating promotion(운영 승격)과 runtime authority(런타임 권위)는 주장하지 않는다.

## Density Guardrail(거래 밀도 가드레일)

| guardrail_id | value | threshold | status | evidence | effect |
| --- | --- | --- | --- | --- | --- |
| actual_mt5_trade_density | 3.0510510511 | 3.0 | passed | 1016 trades / 333 business_days | actual MT5 trade density(실제 MT5 거래 밀도)가 사용자 하한 3/day(일 3회)를 통과했는지 확인한다. |
| actual_period_density_crosscheck | 3.0510510511 | 3.0 | passed | 2025-01-02..2026-04-13, business_days=333 | trade report period(거래 보고서 기간) 기준으로도 밀도 하한을 대조한다. |
| proxy_trade_count_survival | 0.9136690647 | mt5/proxy >= 0.90 | passed | proxy=1112, mt5=1016, proxy_density=3.3393393393 | proxy(프록시)의 거래수 예상이 MT5(메타트레이더5)에서 얼마나 살아남았는지 기록한다. |
| long_share_warning | 0.9025590551 | 0.85 | warning_long_skew | long=917, short=99 | long/short balance(롱/숏 균형)가 운영 전 추가 검토가 필요한지 표시한다. |

## Proxy vs MT5 Attribution(프록시 대 MT5 귀속)

| review_id | expected | actual | diff_actual_minus_expected | status | attribution | usability |
| --- | --- | --- | --- | --- | --- | --- |
| net_pf_proxy_direction_useful | 919.75 | 900.36 | -19.39 | usable_directionally | MT5(메타트레이더5)는 proxy(프록시)보다 net(순수익)은 약간 낮지만 PF(수익 팩터)는 높아 신호 방향성은 유지된다. | proxy(프록시)는 후보 선별 보조로 유지하되 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. |
| trade_count_proxy_buffer_small_but_survived | 1112 | 1016 | -96 | density_survived_review_required | probability/decision parity(확률/결정 동등성)가 맞았으므로 거래수 차이는 MT5 position lifecycle(포지션 생명주기)와 broker tester semantics(브로커 테스터 의미) 차이로 본다. | 다음 후보는 실제 MT5 3/day(일 3회) 생존을 확인하기 위해 proxy density buffer(프록시 밀도 완충)를 계속 기록한다. |
| profit_factor_runtime_lift | 1.3178004168 | 1.35 | 0.0321995832 | runtime_pf_lift_positive | MT5 report(메타트레이더5 보고서)의 PF(수익 팩터)가 proxy(프록시)보다 높아 비용 포함 trade shape(거래 형태)가 예상보다 버텼다. | forward/regime stress(전진/국면 압박) 후보로 보존하되 운영 승격은 금지한다. |

## Side Attribution(방향 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| long | 917 | 812.07 | 1.365055675 | 0.885573 | 53.544166 | 1098 |
| short | 99 | 88.29 | 1.258990906 | 0.891818 | 45.454545 | 805 |

## Entry Hour Attribution(진입 시간 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | 88 | 271.53 | 2.063322368 | 3.085568 | 51.136364 | 1098 |
| 22 | 12 | 183.66 | 8.026013772 | 15.305 | 75.0 | 804 |
| 17 | 293 | 179.44 | 1.260042896 | 0.612423 | 53.242321 | 23 |
| 20 | 127 | 175.52 | 1.636934354 | 1.382047 | 51.181102 | 247 |
| 18 | 224 | 53.6 | 1.10175412 | 0.239286 | 51.785714 | 25 |
| 16 | 129 | 29.87 | 1.06919798 | 0.23155 | 54.263566 | 10 |
| 19 | 143 | 6.74 | 1.018728465 | 0.047133 | 52.447552 | 23 |

## Monthly Attribution(월별 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-11 | 84 | 224.51 | 2.056517647 | 2.672738 | 59.52381 | 806 |
| 2025-04 | 121 | 211.95 | 1.438756288 | 1.751653 | 50.413223 | 804 |
| 2026-02 | 91 | 135.91 | 1.610419942 | 1.493516 | 60.43956 | 230 |
| 2025-02 | 74 | 73.97 | 1.411928496 | 0.999595 | 54.054054 | 805 |
| 2025-06 | 67 | 57.54 | 1.513154374 | 0.858806 | 53.731343 | 228 |
| 2025-05 | 76 | 42.33 | 1.265575005 | 0.556974 | 55.263158 | 804 |
| 2025-01 | 88 | 40.14 | 1.165457543 | 0.456136 | 50.0 | 1098 |
| 2025-09 | 52 | 36.86 | 1.376891616 | 0.708846 | 44.230769 | 230 |
| 2025-10 | 78 | 31.76 | 1.155709173 | 0.407179 | 55.128205 | 229 |
| 2026-01 | 82 | 27.43 | 1.148704326 | 0.334512 | 47.560976 | 228 |
| 2026-04 | 46 | 23.29 | 1.231972112 | 0.506304 | 56.521739 | 7 |
| 2025-07 | 35 | 11.69 | 1.172266431 | 0.334 | 54.285714 | 230 |
| 2025-03 | 8 | 8.71 | 1.66743295 | 1.08875 | 50.0 | 6 |
| 2026-03 | 4 | 8.34 | 23.540540541 | 2.085 | 50.0 | 6 |
| 2025-08 | 47 | -0.37 | 0.996640029 | -0.007872 | 42.553191 | 247 |
| 2025-12 | 63 | -33.7 | 0.807944378 | -0.534921 | 50.793651 | 229 |

## Findings(발견)

| finding_id | severity | finding | effect |
| --- | --- | --- | --- |
| F01_mt5_profit_structure_positive | positive_clue | MT5 net/PF/RF(순수익/수익 팩터/회복 계수) = 900.36 / 1.35 / 6.92 | density restore stress candidate(밀도 복원 압박 후보)는 다음 forward/regime stress(전진/국면 압박)로 보존할 가치가 있다. |
| F02_trade_density_survived | positive_clue | actual MT5 density(실제 MT5 밀도) 3.0510510511 >= 3/day | 사용자 trade-per-day(일별 거래수) 하한을 거래 쪼개기 없이 통과했다. |
| F03_runtime_parity_clean | positive_clue | matched_rows=17428, mismatch_rows=None, max_abs_probability_diff=5.965400001750609e-08 | runtime parity(런타임 동등성)가 깨지지 않아 MT5 KPI(MT5 핵심 성과 지표)를 검토 근거로 쓸 수 있다. |
| R01_long_skew_remains | stress_required | long/short(롱/숏) = 917/99; long_share=0.9025590551 | 방향 균형(long/short balance, 롱/숏 균형)이 아직 약해 운영 승격은 닫지 않는다. |
| R02_forward_regime_missing | stress_required | no forward pass(전진 통과 없음), no live-like replay(실거래 유사 재생 없음) | runtime_probe(런타임 탐침)를 runtime authority(런타임 권위)로 올리지 않는다. |
| R03_side_quality_needs_review | stress_required | short net(숏 순수익)=88.29, short trades(숏 거래수)=99 | short(숏) 단서는 양수 여부와 무관하게 적은 표본이라 다음 국면별 검토가 필요하다. |

## Required Gates(필수 게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/density_restore_stress_candidate_mt5_probe_summary.csv | MT5 report KPI(MT5 보고서 핵심 성과 지표)를 검토 기준으로 고정한다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/closed_trade_attribution.csv | report trade count(보고서 거래수)와 parsed closed trades(파싱된 종료 거래)를 맞춘다. |
| source_authority_audit(진실 원천 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/strategy_tester_report_records.json | proxy(프록시)가 아니라 Strategy Tester(전략 테스터)를 KPI 권위로 둔다. |
| runtime_parity_evidence_gate(런타임 동등성 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/runtime_quality_review.csv | probability/decision parity(확률/결정 동등성)를 BF 판정에 연결한다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/monthly_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/entry_hour_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/side_attribution.csv | 월/시간/방향 성과를 분리해 다음 검증 방향을 만든다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/claim_boundary_receipt.json | positive runtime clue(긍정 런타임 단서)를 runtime authority(런타임 권위)나 operating promotion(운영 승격)으로 올리지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/required_gate_coverage_audit.csv | kpi_evidence(KPI 근거) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Next Action(다음 행동)

`run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1`에서 forward/regime stress input(전진/국면 압박 입력), session-side guardrail(세션-방향 가드레일), short quality restore(숏 품질 복원)를 materialize(구체화)한다. trade splitting(거래 쪼개기)은 사용하지 않는다.

## Boundary(경계)

이 결과는 runtime_probe_review(런타임 탐침 검토)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
