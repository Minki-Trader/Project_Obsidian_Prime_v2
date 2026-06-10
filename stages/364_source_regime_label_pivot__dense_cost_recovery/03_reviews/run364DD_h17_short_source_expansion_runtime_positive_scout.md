# run364DD h17 short-source expansion runtime-positive scout(17시 숏 원천 확장 런타임 긍정 단서 탐색)

Updated(갱신): 2026-06-06T05:23:02Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1`
- selected variant(선택 변형): `dd05_h17_21_short_source_m050_ex_aug`
- selected estimated MT5 net/PF/DD(선택 추정 MT5 순수익/수익 팩터/낙폭): `1019.7701` / `1.3743479483` / `130.9397`
- selected estimated density(선택 추정 밀도): `3.2961783439`
- selected short count/share(선택 숏 수/비중): `167` / `0.1604226705`
- package precheck(패키지 사전검토): `passed_proxy_precheck(프록시 사전검토 통과)`

## Action/Effect(행동/효과)

Action(행동): DB MT5 telemetry(DB MT5 텔레메트리)를 single-position replay(단일 포지션 재생)로 다시 돌리고, flat(관망)으로 막힌 short-source rows(숏 원천 행)를 11개 변형으로 열었습니다.

Effect(효과): pure exposure scaling(순수 노출 증폭) 반복이 아니라, 새 숏 진입 원천이 side balance(방향 균형)를 개선할 수 있는지 분리했습니다.

## Surface(표면)

| variant_id | override_rows | estimated_mt5_net_profit | estimated_mt5_profit_factor | estimated_mt5_density | sim_short_trade_count | package_precheck_status |
| --- | --- | --- | --- | --- | --- | --- |
| dd05_h17_21_short_source_m050_ex_aug | 166 | 1019.7701 | 1.3743479483 | 3.2961783439 | 167 | passed_proxy_precheck(프록시 사전검토 통과) |
| dd01_h16_premarket_short_m100 | 26 | 1027.0098 | 1.397447081 | 3.1464968153 | 119 | passed_proxy_precheck(프록시 사전검토 통과) |
| dd06_h17_19_high_conviction_m080 | 27 | 1019.9625 | 1.3992317584 | 3.1433121019 | 119 | passed_proxy_precheck(프록시 사전검토 통과) |
| dd09_bearish_impulse_h16_19_m030 | 476 | 822.7548 | 1.2470434558 | 3.601910828 | 257 | failed_proxy_precheck(프록시 사전검토 실패) |
| dd08_bearish_impulse_h17_21_m040 | 362 | 866.1935 | 1.2713218523 | 3.5541401274 | 245 | failed_proxy_precheck(프록시 사전검토 실패) |
| dd11_combo_no20_m050_bearish | 318 | 813.5655 | 1.2584148217 | 3.4872611465 | 224 | failed_proxy_precheck(프록시 사전검토 실패) |
| dd04_h18_21_short_source_m050_no20 | 101 | 983.5482 | 1.3693455381 | 3.2261146497 | 145 | failed_proxy_precheck(프록시 사전검토 실패) |
| dd10_combo_h16_high_h18_19_m060 | 103 | 971.556 | 1.353369853 | 3.2452229299 | 150 | failed_proxy_precheck(프록시 사전검토 실패) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/dd_short_source_expansion_surface.csv | all DD variants scored(모든 DD 변형 점수화) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/input_manifest.csv | inputs linked(입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/data_integrity_audit.csv | timestamp/no-overlap checks passed(시점/무겹침 점검 통과) |
| baseline_replay_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/baseline_replay_gap.csv | baseline replay gap declared(기준선 재생 차이 명시) |
| short_source_candidate_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/dd_short_source_expansion_surface.csv | selected variant changes short source(선택 변형이 숏 원천 변경) |
| kpi_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/package_precheck.csv | selected row preserves DD KPI contract(선택 행이 DD KPI 계약 유지) |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/data_integrity_audit.csv | single-position replay used(단일 포지션 재생 사용) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/run_evidence_receipt.json | required receipts exist(필수 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트를 종료 기록에 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DD/claim_boundary_receipt.json | no authority/promotion/goal claim(권위/승격/목표 주장 없음) |

## Boundary(경계)

This is proxy scout only(프록시 탐색 전용)입니다. new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
