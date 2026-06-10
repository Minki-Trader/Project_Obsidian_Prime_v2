# run364CR h17 month12 long equity drawdown repair inputs(17시 12월 롱/수익곡선 낙폭 수리 입력)

Updated(갱신): 2026-06-06T02:21:13Z

Action(행동): CQ review(CQ 검토)의 month12 loss(12월 손실), equity DD(수익곡선 낙폭), side balance(방향 균형) 단서를 CS scout queue(CS 정찰 대기열) `8`개로 materialize(구체화)했습니다.

Effect(효과): 다음 `run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`가 exact date filter(정확 날짜 필터), top_n(상위 N), trade splitting(거래 쪼개기) 없이 timestamp-safe(시점 안전) 수리 변형을 바로 시험할 수 있습니다.

## Baseline(기준선)

- MT5 net/PF/density(순수익/수익 팩터/밀도): `983.74` / `1.4` / `3.127388535`
- bad month count(손실 월 수): `1`
- equity DD(수익곡선 낙폭): `130.11`

## CS Queue(CS 대기열)

| variant_id | hypothesis | changed_variables | success_criteria |
| --- | --- | --- | --- |
| cr00_cm04_runtime_review_baseline | baseline replay preserves CQ MT5 read(CQ MT5 판독 기준선 유지) | none | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr01_month12_long_hours17_20_block | month12 long loss is concentrated in hours 17-20(12월 롱 손실은 17-20시에 집중) | block long entries when month_of_year=12 and open_hour in 17,18,19,20 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr02_month12_long_margin_floor_002 | raising month12 long margin floor reduces weak longs(12월 롱 마진 하한 상향이 약한 롱을 줄임) | month12 long signal-margin floor 0.02 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr03_month12_long_margin_floor_003 | stronger month12 long margin floor may remove bad month(더 강한 12월 롱 마진 하한이 손실 월 제거) | month12 long signal-margin floor 0.03 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr04_month12_long_hours17_20_floor002 | session and margin combined can repair month12 without broad damage(세션+마진 조합이 넓은 손상 없이 12월 수리) | month12 long open_hour 17-20 guard plus margin floor 0.02 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr05_equity_dd_long_hours18_19_floor002_all_months | long entries around hours 18-19 contribute open equity DD(18-19시 롱이 열린 수익곡선 낙폭에 기여) | all-month long open_hour 18-19 signal-margin floor 0.02 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr06_short_floor_preserve_month12_long_guard | month12 repair must keep short floor >=100(12월 수리는 숏 하한 100 이상을 유지해야 함) | cr01 guard plus native/synthetic short floor restore | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |
| cr07_equity_dd_and_bad_month_combo | small combined guard can repair both bad month and equity DD(작은 조합 가드가 손실 월과 낙폭을 같이 수리) | month12 long 17-20 block plus all-month long 18-19 floor 0.02 | proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/work_packet.json | CR 작업 묶음(work packet, 작업 묶음)의 가족/스킬/게이트를 고정합니다. |
| repair_scope_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/run364CS_h17_month12_long_equity_drawdown_repair_scout_queue.csv | CQ 수리 단서를 CS 실행 가능한 queue(대기열)로 바꿉니다. |
| timestamp_safety_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/timestamp_safety_audit.csv | 진입 시점에 알려진 입력만 쓰도록 제한합니다. |
| forbidden_action_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/forbidden_action_audit.csv | exact date/top_n/trade splitting(정확 날짜/상위 N/거래 쪼개기)을 금지합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CR/claim_boundary_receipt.json | materialization(구체화)을 운영 주장(operating claim, 운영 주장)으로 과장하지 않습니다. |

## Boundary(경계)

CR is materialization only(CR은 구체화 전용)입니다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`입니다.
