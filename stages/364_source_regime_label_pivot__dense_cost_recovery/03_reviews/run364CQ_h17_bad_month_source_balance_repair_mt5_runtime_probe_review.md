# run364CQ h17 bad-month source-balance MT5 runtime probe review(17시 손실 월/원천 균형 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T02:16:00Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mixed_positive_runtime_probe_net_pf_density_short_floor_clue_promotion_ineligible_month12_loss_equity_drawdown_long_skew_no_authority`
- MT5 net/PF/trades(순수익/수익 팩터/거래수): `983.74` / `1.4` / `982.0`
- density(밀도): `3.127388535` per feature day(피처 일 기준)
- short count(숏 수): `101.0`
- bad month count(손실 월 수): `1`
- equity DD(수익곡선 낙폭): `130.11`

## Action/Effect(행동/효과)

Action(행동): CP MT5 report(CP MT5 보고서)를 trade list(거래 목록), month/side/hour attribution(월/방향/시간 귀속), proxy/MT5 diff(프록시/MT5 차이)로 review(검토)했습니다.

Effect(효과): CM04 candidate(CM04 후보)는 positive runtime clue(긍정 런타임 단서)로 보존하지만, month12 loss(12월 손실), equity drawdown gap(수익곡선 낙폭 간극), long skew(롱 편중)를 다음 repair(수리) 입력으로 넘깁니다.

## Findings(발견)

| finding_id | severity | finding | effect |
| --- | --- | --- | --- |
| cq_kpi_positive_with_boundary | positive_clue | MT5 net/PF/density/short floor passed(MT5 순수익/수익 팩터/밀도/숏 하한 통과). | 후보를 폐기하지 않고 다음 수리 기준선으로 유지합니다. |
| cq_month12_loss | repair_required | MT5 month attribution(MT5 월 귀속)에서 2025-12가 음수입니다. | zero bad month(손실 월 0) 주장은 닫고 month12 long repair(12월 롱 수리)를 엽니다. |
| cq_equity_dd_gap | repair_required | Equity DD(수익곡선 낙폭)가 balance/proxy DD(잔고/프록시 낙폭)보다 큽니다. | operating promotion(운영 승격) 전에 risk shape(위험 형태)를 수리해야 합니다. |

## Month Attribution(월 귀속)

| month | trade_count | net_profit | average_net | win_rate |
| --- | --- | --- | --- | --- |
| 2025-12 | 37 | -3.9699999999999984 | -0.1072972972972972 | 0.4864864864864865 |
| 2025-07 | 35 | 4.030000000000003 | 0.1151428571428572 | 0.5142857142857142 |
| 2025-08 | 43 | 4.889999999999997 | 0.113720930232558 | 0.4418604651162791 |
| 2026-03 | 4 | 8.34 | 2.085 | 0.5 |
| 2026-04 | 46 | 23.29 | 0.5063043478260869 | 0.5652173913043478 |
| 2025-01 | 87 | 27.56000000000001 | 0.3167816091954024 | 0.5057471264367817 |
| 2026-01 | 82 | 30.3 | 0.3695121951219511 | 0.4756097560975609 |
| 2025-10 | 78 | 31.8 | 0.4076923076923076 | 0.5512820512820513 |

## Side Attribution(방향 귀속)

| direction | trade_count | net_profit | average_net | win_rate |
| --- | --- | --- | --- | --- |
| sell | 101 | 138.57999999999998 | 1.372079207920792 | 0.4752475247524752 |
| buy | 881 | 845.16 | 0.9593189557321226 | 0.5368898978433598 |

## Next Queue(다음 대기열)

| queue_id | candidate_seed | action | effect |
| --- | --- | --- | --- |
| cr01_month12_long_guard_sweep | month12 buy net negative; sell positive(12월 롱 음수, 숏 양수) | materialize month12 long guard variants(12월 롱 가드 변형 구체화) | MT5에서 남은 bad month(손실 월)를 줄이는지 시험합니다. |
| cr02_equity_dd_guard_sweep | equity DD exceeds balance DD(수익곡선 낙폭이 잔고 낙폭보다 큼) | materialize equity drawdown stress controls(수익곡선 낙폭 압박 대조 구체화) | closed-trade proxy(닫힌 거래 프록시)가 놓친 open-risk(열린 위험)를 줄이는지 본다. |
| cr03_side_balance_not_just_short_floor | short count floor passes but long share remains high(숏 하한은 통과하지만 롱 비중 높음) | materialize side-balance stress without killing density(밀도 보존 방향 균형 압박 구체화) | short floor(숏 하한)를 통과한 상태에서 수익을 나누지 않고 균형을 넓힙니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/mt5_kpi_review.csv | MT5 KPI(MT5 핵심 성과 지표)를 proxy(프록시)와 분리해 고정합니다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/trade_shape_review.csv | deal/trade row grain(체결/거래 행 단위)을 보고서 trade count(거래수)와 대조합니다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/proxy_mt5_attribution.csv | MT5 report(MT5 보고서)를 실제 KPI source of truth(진실 원천)로 둡니다. |
| backtest_forensics_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/tester_identity_review.csv | tester identity(테스터 정체성), report hash(보고서 해시), timeout boundary(시간 초과 경계)를 남깁니다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/month_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/side_attribution.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/drawdown_review.csv | 월/방향/낙폭 성과 귀속을 다음 repair(수리) 조건으로 만듭니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/required_gate_coverage_audit.csv | work packet(작업 묶음)의 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CQ/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 막습니다. |

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`입니다.
