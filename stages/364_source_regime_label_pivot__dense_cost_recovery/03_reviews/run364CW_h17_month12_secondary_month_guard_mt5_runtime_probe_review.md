# run364CW h17 month12 secondary month guard MT5 runtime probe review(17시 12월 보조 월 가드 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T03:34:17Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mixed_positive_runtime_probe_month12_repaired_net_pf_density_short_floor_positive_equity_dd_long_skew_proxy_gap_repair_required_no_authority`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `1011.02` / `1.42` / `972.0`
- density(밀도): `3.0955414013` per feature day(피처일 기준)
- month12 net/long/short(12월 순수익/롱/숏): `23.31` / `8.79` / `14.52`
- equity DD(수익곡선 낙폭): `130.11` / `17.64%`
- long/short share(롱/숏 비중): `0.896090535` / `0.103909465`

## Action/Effect(행동/효과)

Action(행동): run364CV MT5 report(MT5 보고서)를 KPI(핵심 성과 지표), month/side/hour attribution(월/방향/시간 귀속), proxy/MT5 diff(프록시/MT5 차이), drawdown review(낙폭 검토)로 검토했습니다.

Effect(효과): `cr04`는 month12 repair(12월 수리)와 net/PF/RF lift(순수익/수익 팩터/회복 계수 개선) 단서로 보존하지만, equity DD(수익곡선 낙폭), long skew(롱 쏠림), proxy gap(프록시 차이)을 `run364CX` 수리 입력(repair inputs, 수리 입력)으로 넘깁니다.

## Findings(발견)

| finding_id | severity | finding | effect |
| --- | --- | --- | --- |
| cw_month12_repaired | positive_clue | 2025-12 and 2025-12 long side(12월 및 12월 롱 방향)가 MT5에서 양수입니다. | 12월 방어 규칙(month guard, 월 가드)을 보존 조건으로 둡니다. |
| cw_kpi_lift_vs_cp | positive_clue | CP 대비 net/PF/RF(순수익/PF/회복 계수)가 개선됐습니다. | cr04는 버리지 않고 다음 risk/side repair(위험/방향 수리)의 기준 후보로 씁니다. |
| cw_equity_dd_gap | repair_required | equity DD(수익곡선 낙폭)가 130.11로 balance DD(잔고 낙폭)보다 큽니다. | 운영 주장(operating claim, 운영 주장) 전에 open-risk path(개방 위험 경로)를 줄여야 합니다. |
| cw_long_skew | repair_required | long share(롱 비중)가 약 89.6%로 높습니다. | 숏 수량(short count, 숏 수량)이 아니라 숏 품질(short quality, 숏 품질)을 같이 봅니다. |

## Month Attribution(월 귀속)

| month | trade_count | net_profit | average_net | win_rate |
| --- | --- | --- | --- | --- |
| 2025-07 | 35 | 4.030000000000003 | 0.1151428571428572 | 0.5142857142857142 |
| 2025-08 | 43 | 4.889999999999997 | 0.113720930232558 | 0.4418604651162791 |
| 2026-03 | 4 | 8.34 | 2.085 | 0.5 |
| 2026-04 | 46 | 23.29 | 0.5063043478260869 | 0.5652173913043478 |
| 2025-12 | 27 | 23.31 | 0.8633333333333333 | 0.5555555555555556 |
| 2025-01 | 87 | 27.56000000000001 | 0.3167816091954024 | 0.5057471264367817 |
| 2026-01 | 82 | 30.3 | 0.3695121951219511 | 0.4756097560975609 |
| 2025-10 | 78 | 31.8 | 0.4076923076923076 | 0.5512820512820513 |

## Side Attribution(방향 귀속)

| direction | trade_count | net_profit | average_net | win_rate |
| --- | --- | --- | --- | --- |
| sell | 101 | 138.57999999999998 | 1.372079207920792 | 0.4752475247524752 |
| buy | 871 | 872.44 | 1.0016532721010334 | 0.539609644087256 |

## Next Queue(다음 대기열)

| queue_id | candidate_seed | action | effect |
| --- | --- | --- | --- |
| cx01_equity_dd_open_risk_guard | equity DD remains 130.11 while balance DD remains 67.67(수익곡선 낙폭 130.11, 잔고 낙폭 67.67) | materialize open-risk and hold-shape guards(개방 위험/보유 형태 가드 구체화) | 잔고 프록시가 숨긴 평가손익 경로(equity path, 수익곡선 경로)를 줄이는지 봅니다. |
| cx02_short_quality_side_balance | short floor passes but long share remains high(숏 하한 통과, 롱 비중 높음) | materialize side-balance variants preserving short net(숏 순수익 보존 방향 균형 변형 구체화) | 숏을 억지로 늘리지 않고 수익 기여(short quality, 숏 품질)를 유지하는지 봅니다. |
| cx03_proxy_runtime_gap_attribution | MT5 net is 56.18 below proxy and trades are 5 above proxy(MT5 순수익은 프록시보다 56.18 낮고 거래는 5개 많음) | materialize proxy/runtime gap checks using telemetry and deal pairs(텔레메트리/거래쌍 기반 프록시-런타임 차이 점검 구체화) | 프록시를 후보 선별 보조로 유지할 수 있는지와 어떤 차이를 보정해야 하는지 분리합니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/mt5_kpi_review.csv | MT5 KPI(MT5 핵심 성과 지표)를 proxy(프록시)와 분리해 고정합니다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/trade_shape_review.csv | deal/trade row grain(체결/거래 행 단위)이 보고서 trade count(거래 수)와 맞는지 확인합니다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/proxy_mt5_attribution.csv | MT5 report(MT5 보고서)를 실제 KPI source of truth(진실 원천)로 둡니다. |
| backtest_forensics_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/tester_identity_review.csv | tester identity(테스터 정체성), report hash(보고서 해시), set/ini(설정/INI)를 연결합니다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/month_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/side_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/drawdown_review.csv | 월/방향/낙폭 귀속(month/side/drawdown attribution, 월/방향/낙폭 귀속)을 다음 수리 조건으로 연결합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/required_gate_coverage_audit.csv | work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CW/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 막습니다. |

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
