# run364CY h17 equity DD side-balance proxy-gap scout(17시 수익곡선 낙폭/방향 균형/프록시 차이 정찰)

Updated(갱신): 2026-06-06T03:56:09Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`
- selected variant(선택 변형): `cx05_high_quality_short_boost110_h17_20`
- selected net/PF/density(선택 순수익/수익 팩터/밀도): `1075.07` / `1.4451946256` / `3.0796178344`
- selected short count(선택 숏 수): `100`
- selected short net delta(선택 숏 순수익 변화): `7.87`
- month12 net/long(12월 순수익/롱): `34.6` / `21.36`
- package precheck(패키지 사전검사): `passed_proxy_precheck(프록시 사전검사 통과)`

## Action/Effect(행동/효과)

Action(행동): CX queue(CX 대기열) 12개를 selected CS trade tape(선택 CS 거래 테이프)에 risk-scale proxy replay(위험비율 프록시 재생)로 적용했습니다.

Effect(효과): `cx05_high_quality_short_boost110_h17_20`가 거래수(trade count, 거래수)를 바꾸지 않고 short contribution(숏 기여)을 높이는 positive proxy clue(긍정 프록시 단서)가 됐습니다. 다만 MT5 equity DD(MT5 수익곡선 낙폭)와 EA runtime representation(EA 런타임 표현)은 아직 검토가 필요합니다.

## Surface(표면)

| variant_id | net_profit | profit_factor | trade_density | short_trade_count | short_net_delta_vs_proxy_base | package_precheck_status |
| --- | --- | --- | --- | --- | --- | --- |
| cx05_high_quality_short_boost110_h17_20 | 1075.07 | 1.4451946256 | 3.0796178344 | 100 | 7.87 | passed_proxy_precheck(프록시 사전검사 통과) |
| cx00_cr04_secondary_guard_anchor | 1067.2 | 1.4466929377 | 3.0796178344 | 100 | 0.0 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx06_high_quality_short_boost120_h17_20 | 1056.58 | 1.4335220322 | 3.0796178344 | 100 | -10.62 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx02_weak_hour_long_risk_scale050_m010 | 971.01 | 1.457418593 | 3.0796178344 | 100 | 0.0 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx11_combo_short_boost110_plus_weak_long_scale075 | 1058.38 | 1.453363668 | 3.0796178344 | 100 | 7.87 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx01_weak_hour_long_risk_scale075_m005 | 1050.51 | 1.4550046873 | 3.0796178344 | 100 | 0.0 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx10_month12_preserve_plus_weak_hour_scale075 | 1050.51 | 1.4550046873 | 3.0796178344 | 100 | 0.0 | failed_proxy_precheck(프록시 사전검사 실패) |
| cx09_proxy_gap_margin_scale050_m006_all_sides | 764.38 | 1.3688099329 | 3.0796178344 | 100 | 0.0 | failed_proxy_precheck(프록시 사전검사 실패) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/cy_proxy_repair_surface.csv | 12 CY variants replayed(12개 CY 변형 재생 완료) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/input_manifest.csv | CX/CW/CS inputs connected(CX/CW/CS 입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/data_integrity_audit.csv | timestamp/no-split checks passed(시점/무분할 점검 통과) |
| kpi_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/package_precheck.csv | selected row keeps KPI guardrails(선택 행이 KPI 가드레일 유지) |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/variant_risk_scale_audit.csv | risk scale changes exposure, not entry count(위험비율은 노출만 바꾸고 진입수는 바꾸지 않음) |
| package_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/package_precheck.csv | package precheck is proxy-only(패키지 사전검사는 프록시 전용) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/run_evidence_receipt.json | required receipts exist(필수 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트 종료 기록 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CY/claim_boundary_receipt.json | no authority/promotion/goal claim(권위/승격/목표 주장 없음) |

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)입니다. new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
