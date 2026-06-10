# run364CX h17 equity DD side-balance proxy-gap repair inputs(17시 수익곡선 낙폭/방향 균형/프록시 차이 수리 입력)

Updated(갱신): 2026-06-06T03:48:32Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`
- judgment(판정): `repair_input_queue_ready_equity_dd_side_balance_proxy_runtime_gap_no_authority`
- baseline MT5 net/PF/density(기준 MT5 순수익/수익 팩터/밀도): `1011.02` / `1.42` / `3.0955414013`
- baseline equity DD(기준 수익곡선 낙폭): `130.11`
- baseline long share(기준 롱 비중): `0.896090535`
- baseline proxy net diff(기준 프록시 순수익 차이): `-56.18`
- queue rows(대기열 행): `12`

## Action/Effect(행동/효과)

Action(행동): `run364CW`의 open repair(열린 수리) 세 축인 equity DD(수익곡선 낙폭), side balance(방향 균형), proxy/runtime gap(프록시/런타임 차이)을 `run364CY` scout queue(정찰 대기열)로 구체화했습니다.

Effect(효과): 다음 실행은 12월 수리(month12 repair, 12월 수리), density floor(밀도 하한), short floor(숏 하한)을 보존한 채 weak-hour long margin(약한 시간 롱 마진), hold-shape guard(보유 형태 가드), short-quality guard(숏 품질 가드), micro-margin gap filter(미세 마진 차이 필터)를 비교할 수 있습니다.

## CY Queue(CY 대기열)

| queue_id | variant_id | variant_family | changed_variables | expected_effect |
| --- | --- | --- | --- | --- |
| run364CY_01 | cx00_cr04_secondary_guard_anchor | anchor(기준) | none |  |
| run364CY_02 | cx01_weak_hour_long_risk_scale075_m005 | equity_dd_open_risk_guard(수익곡선 낙폭 개방위험 가드) | long open_hour in 16,18,19 with direction_margin < 0.005 gets risk_scale 0.75 |  |
| run364CY_03 | cx02_weak_hour_long_risk_scale050_m010 | equity_dd_open_risk_guard(수익곡선 낙폭 개방위험 가드) | long open_hour in 16,18,19 with direction_margin < 0.010 gets risk_scale 0.50 |  |
| run364CY_04 | cx03_long_hold_tail_risk_scale050_120m | hold_shape_guard(보유 형태 가드) | long trades with hold proxy >120m get risk_scale 0.50 proxy stress |  |
| run364CY_05 | cx04_weak_hour_scale075_plus_hold050 | combo_open_risk_guard(조합 개방위험 가드) | cx01 risk_scale 0.75 plus long hold proxy >120m risk_scale 0.50 |  |
| run364CY_06 | cx05_high_quality_short_boost110_h17_20 | side_balance_short_quality(방향 균형 숏 품질) | short trades in hours 17,18,19,20 with margin_vs_long >= 0.080 get risk_scale 1.10 |  |
| run364CY_07 | cx06_high_quality_short_boost120_h17_20 | side_balance_short_quality(방향 균형 숏 품질) | short trades in hours 17,18,19,20 with margin_vs_long >= 0.090 get risk_scale 1.20 |  |
| run364CY_08 | cx07_long_share_soft_scale075_m005 | side_balance_long_skew_guard(방향 균형 롱 쏠림 가드) | all long trades with direction_margin < 0.005 get risk_scale 0.75, month12 existing guards preserved |  |
| run364CY_09 | cx08_proxy_gap_margin_scale075_m003_all_sides | proxy_runtime_gap(프록시/런타임 차이) | all entries with absolute direction_margin < 0.003 get risk_scale 0.75 |  |
| run364CY_10 | cx09_proxy_gap_margin_scale050_m006_all_sides | proxy_runtime_gap(프록시/런타임 차이) | all entries with absolute direction_margin < 0.006 get risk_scale 0.50 |  |
| run364CY_11 | cx10_month12_preserve_plus_weak_hour_scale075 | month12_preserve_dd_guard(12월 보존 낙폭 가드) | CR04 month12 guards preserved plus cx01 weak-hour long risk scale |  |
| run364CY_12 | cx11_combo_short_boost110_plus_weak_long_scale075 | combo_side_risk_guard(조합 방향/위험 가드) | cx01 weak long risk scale plus cx05 high-quality short boost |  |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/work_packet.json | CX work packet(작업 묶음)의 family/skills/gates(작업군/스킬/게이트)를 고정합니다. |
| repair_scope_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/run364CY_h17_equity_dd_side_balance_proxy_gap_scout_queue.csv | CW 열린 문제를 CY 실행 가능한 repair queue(수리 대기열)로 바꿉니다. |
| timestamp_safety_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/timestamp_safety_audit.csv | 미래 정보(future information, 미래 정보) 없는 entry-known(진입시점 기지) 입력만 허용합니다. |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/data_integrity_audit.csv | source tape(원천 테이프)의 time-axis(시간축)와 leakage boundary(누수 경계)를 적습니다. |
| forbidden_action_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/forbidden_action_audit.csv | exact date/top_n/trade splitting(정확 날짜/상위 N/거래 쪼개기)을 금지합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CX/claim_boundary_receipt.json | materialization(구체화)을 운영 주장(operating claim, 운영 주장)으로 과장하지 않습니다. |

## Boundary(경계)

This materialization(이번 구체화)은 next scout input(다음 정찰 입력)입니다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
