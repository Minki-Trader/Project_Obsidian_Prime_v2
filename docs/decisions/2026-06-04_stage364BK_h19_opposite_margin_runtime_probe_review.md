# run364BK h19 opposite-margin runtime probe review(364BK 19시 반대마진 런타임 탐침 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BJ_implement_h19_opposite_margin_runtime_guard_without_db_v1`
- next_run_id(다음 실행 ID): `run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1`
- judgment(판정): `positive_runtime_probe_net_pf_density_pass_but_short_balance_equity_dd_forward_stress_required_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## KPI Read(KPI 판독)

- MT5 net/PF/expectancy/trades(MT5 순수익/수익 팩터/기대값/거래 수): `959.64` / `1.38` / `0.95` / `1006`
- RF/equity DD(회복 계수/평가손익 낙폭): `7.38` / `130.11` amount(금액), `18.24%`
- density(밀도): `3.021021021` per business day(영업일당), buffer(완충) `0.021021021`
- long/short(롱/숏): `907` / `99`, short share(숏 비중) `0.0984095427`
- proxy diff(프록시 차이): net(순수익) `21.05`, PF(수익 팩터) `0.0067720167`, trades(거래 수) `3`

## Judgment(판정)

Action(행동): BJ MT5 runtime probe(BJ MT5 런타임 탐침)를 KPI(핵심 성과 지표), equity curve quality(수익곡선 품질), proxy-vs-MT5 attribution(프록시-MT5 귀속), session/regime(세션/국면), long/short balance(롱/숏 균형)로 검토했다.

Effect(효과): h19 opposite-margin guard(19시 반대마진 가드)는 MT5에서 순수익/PF/밀도를 올린 긍정 단서지만, short share(숏 비중), equity DD(평가손익 낙폭), forward/cost stress(전진/비용 압박)가 남아 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.

## Density/Side(밀도/방향)

| review_id | value | threshold | status | evidence | effect |
| --- | --- | --- | --- | --- | --- |
| actual_mt5_trade_density | 3.021021021 | 3.0 | passed_thin_buffer | 1006 trades / 333 business_days | MT5 actual density(MT5 실제 밀도)가 3/day(일 3회) 하한을 넘는지 확인한다. |
| density_buffer | 0.021021021 | >= 0.05 preferred buffer(선호 완충) | thin_buffer_review_required | actual_density=3.021021021, floor=3.0 | 밀도는 통과했지만 작은 완충이면 다음 수리에서 거래 수 붕괴를 경계한다. |
| short_share_balance | 0.0984095427 | 0.12 | failed_short_share_below_target | long=907, short=99, total=1006 | long/short balance(롱/숏 균형)가 운영 후보 품질을 막는지 판단한다. |
| proxy_trade_count_parity | 3 | small absolute diff(작은 절대 차이) | proxy_mt5_close | proxy=1003, mt5=1006 | proxy EV(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않고 선별 보조로 쓸 수 있는지 본다. |

## Equity Curve(수익곡선)

| review_id | net_profit | profit_factor | expectancy | recovery_factor | equity_dd_percent | status | effect |
| --- | --- | --- | --- | --- | --- | --- | --- |
| headline_profit_risk | 959.64 | 1.38 | 0.95 | 7.38 |  | positive_profit_structure | net/PF/expectancy/RF(순수익/수익 팩터/기대값/회복 계수)는 런타임 긍정 단서다. |
| equity_drawdown_stress |  |  |  |  | 18.24 | equity_dd_stress_remains | 수익 구조가 좋아도 equity DD(평가손익 낙폭)가 운영 주장을 막는지 분리한다. |
| closed_vs_equity_dd_gap |  |  |  |  |  | open_equity_drawdown_harsher_than_closed_proxy | closed-trade proxy(종료 거래 프록시)보다 tick equity path(틱 평가손익 경로)가 더 거칠 수 있음을 기록한다. |

## Proxy vs MT5(프록시 대 MT5)

| review_id | expected | actual | diff_actual_minus_expected | status | attribution | usability |
| --- | --- | --- | --- | --- | --- | --- |
| proxy_vs_mt5_net_pf | net=938.59;pf=1.3732279833 | net=959.64;pf=1.38 | net=21.05;pf=0.0067720167 | proxy_direction_confirmed_by_mt5 | exact h19 guard(정확 19시 가드)가 런타임에서 작동했고, 남은 차이는 Strategy Tester(전략 테스터)의 체결/보유 경로 차이로 본다. | proxy EV(프록시 예상값)는 선별 보조로 유지하되 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. |
| proxy_vs_mt5_trade_count | 1003 | 1006 | 3 | trade_count_close_density_survived | MT5 position lifecycle(MT5 포지션 생명주기) 때문에 proxy(프록시)보다 3개 많지만 밀도 하한은 유지됐다. | 다음 후보도 proxy density buffer(프록시 밀도 완충)를 작게라도 남겨야 한다. |
| runtime_guard_observed | h19 opposite-margin guard enabled(19시 반대마진 가드 켜짐) | 54 | observed_runtime_blocks(런타임 차단 관측) | runtime_semantic_observed | decision_reason(결정 사유)에 time_margin_guard(시간-마진 가드)가 기록됐다. | 런타임 의미(runtime semantics, 런타임 의미)는 검토 가능하나 권위(authority, 권위)는 아직 아니다. |

## Side Attribution(방향 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| long | 907 | 876.07 | 1.40404101 | 0.965899 | 53.803749 | 1098 |
| short | 99 | 83.57 | 1.243459768 | 0.844141 | 45.454545 | 805 |

## Entry Hour Attribution(진입 시간 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | 88 | 293.88 | 2.191969175 | 3.339545 | 51.136364 | 1098 |
| 22 | 12 | 191.91 | 9.271982759 | 15.9925 | 75.0 | 804 |
| 17 | 293 | 179.44 | 1.260042896 | 0.612423 | 53.242321 | 23 |
| 20 | 125 | 173.53 | 1.639907073 | 1.38824 | 51.2 | 247 |
| 18 | 224 | 53.6 | 1.10175412 | 0.239286 | 51.785714 | 25 |
| 19 | 135 | 37.41 | 1.116129633 | 0.277111 | 54.074074 | 23 |
| 16 | 129 | 29.87 | 1.06919798 | 0.23155 | 54.263566 | 10 |

## Monthly Attribution(월별 귀속)

| group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | expectancy_after_cost | win_rate_after_cost_percent | max_hold_m5_calendar |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-11 | 83 | 244.44 | 2.239113905 | 2.94506 | 60.240964 | 806 |
| 2025-04 | 120 | 220.1 | 1.460585515 | 1.834167 | 50.833333 | 804 |
| 2026-02 | 90 | 140.86 | 1.641818927 | 1.565111 | 61.111111 | 230 |
| 2025-02 | 73 | 70.18 | 1.39263735 | 0.96137 | 53.424658 | 805 |
| 2025-06 | 67 | 58.72 | 1.523677874 | 0.876418 | 53.731343 | 228 |
| 2025-05 | 75 | 46.19 | 1.298597194 | 0.615867 | 54.666667 | 804 |
| 2025-01 | 88 | 42.49 | 1.17685744 | 0.482841 | 50.0 | 1098 |
| 2026-01 | 81 | 38.41 | 1.220658356 | 0.474198 | 48.148148 | 228 |
| 2025-09 | 51 | 34.97 | 1.357639599 | 0.685686 | 45.098039 | 230 |
| 2025-10 | 78 | 32.35 | 1.158601755 | 0.414744 | 55.128205 | 229 |
| 2026-04 | 46 | 23.29 | 1.231972112 | 0.506304 | 56.521739 | 7 |
| 2025-07 | 34 | 12.09 | 1.17816092 | 0.355588 | 52.941176 | 230 |
| 2025-03 | 8 | 8.71 | 1.66743295 | 1.08875 | 50.0 | 6 |
| 2026-03 | 4 | 8.34 | 23.540540541 | 2.085 | 50.0 | 6 |
| 2025-08 | 46 | 7.49 | 1.072824502 | 0.162826 | 43.478261 | 247 |
| 2025-12 | 62 | -28.99 | 0.830229562 | -0.467581 | 51.612903 | 229 |

## Findings(발견)

| finding_id | severity | finding | effect |
| --- | --- | --- | --- |
| F01_mt5_profit_structure_positive | positive_clue | MT5 net/PF/expectancy/RF = 959.64 / 1.38 / 0.95 / 7.38 | h19 guard(19시 가드)는 계속 밀어볼 가치가 있다. |
| F02_density_floor_survived | positive_clue | actual density(실제 밀도) 3.021021021 >= 3/day | 거래 쪼개기 없이 최소 운용 밀도를 넘겼다. |
| F03_runtime_guard_observed | positive_clue | time_margin_guard blocks(시간-마진 가드 차단) = 54 | EA 입력과 실제 의사결정 의미가 연결됐다. |
| R01_short_balance_unresolved | stress_required | short_share(숏 비중) 0.0984095427 < 0.12 | long/short balance(롱/숏 균형)가 아직 운영 후보를 막는다. |
| R02_equity_dd_stress_remains | stress_required | equity DD(평가손익 낙폭) 18.24% | 수익 곡선 품질(equity curve quality, 수익곡선 품질)을 추가 압박해야 한다. |
| R03_forward_cost_stress_missing | stress_required | no forward pass(전진 통과 없음), no extra cost stress(추가 비용 압박 없음) | 운영 주장 전에 BL에서 검토 입력을 만든다. |

## Required Gates(필수 게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BJ/strategy_tester_report_records.json | MT5 report KPI(MT5 보고서 핵심 성과 지표)를 권위로 고정했다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/closed_trade_attribution.csv | parsed closed trades(파싱한 종료 거래)가 보고서 trade count(거래 수)와 일치한다. |
| source_authority_audit(진실 원천 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BJ/tester_identity_contract.csv | proxy(프록시)가 아니라 Strategy Tester(전략 테스터)를 KPI 원천으로 쓴다. |
| backtest_forensics_gate(백테스트 포렌식 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BJ/tester_identity_contract.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BJ/strategy_tester_report_records.json | 터미널/심볼/모델/예치금/레버리지와 보고서 경로를 확인했다. |
| runtime_parity_evidence_gate(런타임 동등성 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BJ/runtime_policy_config.json; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/runtime_telemetry_session_regime_review.csv | h19 guard(19시 가드)가 런타임 의사결정에 나타났는지 확인했다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/monthly_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/entry_hour_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/side_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/baseline_comparison.csv | 성과를 기간/시간/방향/기준선으로 분해했다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/claim_boundary_receipt.json | positive runtime probe(긍정 런타임 탐침)를 operating promotion(운영 승격)으로 올리지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BK/required_gate_coverage_audit.csv | kpi_evidence(KPI 근거) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |

## Next Action(다음 행동)

`run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1`에서 forward/regime replay(전진/국면 재생), short source restore(숏 원천 복원), equity DD/cost guardrails(평가손익 낙폭/비용 가드레일)을 물질화한다. trade splitting(거래 쪼개기)은 계속 쓰지 않는다.

## Boundary(경계)

이 결과는 reviewed runtime probe(검토된 런타임 탐침)다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
