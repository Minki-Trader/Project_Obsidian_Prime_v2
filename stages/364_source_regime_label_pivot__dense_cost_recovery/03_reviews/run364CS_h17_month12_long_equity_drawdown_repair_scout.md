# run364CS h17 month12 long equity drawdown repair scout(364CS 17시 12월 롱/수익곡선 낙폭 수리 정찰)

Updated(갱신): 2026-06-06T02:37:31Z

## Current Truth(현재 진실)

- status(상태): `completed_stage364CS_h17_month12_long_equity_drawdown_proxy_scout_review_required_no_authority`
- judgment(판정): `positive_proxy_repair_candidate_month12_long_guard_review_required_no_authority`
- selected variant(선택 변형): `cr04_month12_long_hours17_20_floor002`
- selected KPI(선택 핵심 성과 지표): net(순수익) `1067.2`, PF(수익 팩터) `1.4466929377`, density(밀도) `3.0796178344`, shorts(숏) `100`
- month12 long net(12월 롱 순수익): `21.36`, delta(차이) `30.74`
- closed trade DD proxy(닫힌 거래 낙폭 프록시): `67.67`
- next run(다음 실행): `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`

## Action And Effect(행동과 효과)

Action(행동): CR queue(CR 대기열) `8`개를 CM selected tape(CM 선택 거래 테이프)에 proxy replay(프록시 재생)했습니다.

Effect(효과): `cr04_month12_long_hours17_20_floor002`가 density(밀도) `3` 이상과 short floor(숏 하한) `100` 이상을 유지하면서 month12 long net(12월 롱 순수익)을 `21.36`로 돌렸습니다. 다만 MT5 equity DD(MT5 수익곡선 낙폭)는 아직 재탐침 전입니다.

## Surface(표면)

| variant_id | candidate_status | net_profit | profit_factor | trade_density | short_trade_count | month12_long_net | closed_trade_drawdown_proxy | removed_trade_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cr04_month12_long_hours17_20_floor002 | proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음) | 1067.2 | 1.4466929377 | 3.0796178344 | 100 | 21.36 | 67.67 | 8 | 1381.38547211 |
| cr01_month12_long_hours17_20_block | proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음) | 1067.77 | 1.4548329525 | 3.0382165605 | 100 | 21.93 | 67.67 | 21 | 1376.99546085 |
| cr06_short_floor_preserve_month12_long_guard | proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음) | 1067.77 | 1.4548329525 | 3.0382165605 | 100 | 21.93 | 67.67 | 21 | 1376.99546085 |
| cr02_month12_long_margin_floor_002 | proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음) | 1057.5 | 1.4426523148 | 3.0732484076 | 100 | 11.66 | 67.67 | 10 | 1350.81771556 |
| cr03_month12_long_margin_floor_003 | proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음) | 1053.14 | 1.4434833989 | 3.0573248408 | 100 | 7.3 | 67.67 | 15 | 1335.1615883 |
| cr00_cm04_runtime_review_baseline | proxy_watch_no_authority(프록시 관찰, 권위 없음) | 1036.46 | 1.4281838362 | 3.1050955414 | 100 | -9.38 | 67.67 | 0 | 1210.32933903 |
| cr07_equity_dd_and_bad_month_combo | proxy_watch_no_authority(프록시 관찰, 권위 없음) | 1005.96 | 1.5461715057 | 2.3025477707 | 100 | 21.93 | 66.66 | 252 | 551.46262828 |
| cr05_equity_dd_long_hours18_19_floor002_all_months | proxy_watch_no_authority(프록시 관찰, 권위 없음) | 997.69 | 1.5272779852 | 2.3566878981 | 100 | 13.66 | 66.66 | 235 | 533.8046775 |

## Selected Filter Audit(선택 필터 감사)

| filter_step | filter_reason | removed_trade_count | removed_net_profit | short_count_before | short_count_after |
| --- | --- | --- | --- | --- | --- |
| 1 | month12_long_hours17_20_floor002(12월 롱 17-20시 마진 0.02 하한) | 8 | -30.74 | 100 | 100 |

## Selected Package Precheck(선택 패키지 사전검사)

| variant_id | package_precheck_status | net_positive | pf_ge_135 | density_ge_3 | short_floor_ge_100 | month12_long_nonnegative | closed_dd_not_worse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cr04_month12_long_hours17_20_floor002 | passed_proxy_precheck(프록시 사전검사 통과) | true | true | true | true | true | true |

## Proxy MT5 Diff Plan(프록시 MT5 차이 계획)

| comparison_id | proxy_net_profit | mt5_baseline_net_profit | proxy_month12_long_net | mt5_baseline_month12_net | proxy_closed_trade_dd | mt5_baseline_equity_dd |
| --- | --- | --- | --- | --- | --- | --- |
| selected_cs_proxy_vs_cq_mt5(선택 CS 프록시 대 CQ MT5) | 1067.2 | 983.74 | 21.36 | -3.97 | 67.67 | 130.11 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/cs_proxy_repair_surface.csv | 8 CS variants were replayed(8개 CS 변형 재생 완료) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/input_manifest.csv | CR/CQ/CM inputs are connected(CR/CQ/CM 입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/data_integrity_audit.csv | timestamp/no-split/no-top-n checks passed(시점/무분할/no top-n 검사 통과) |
| kpi_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/package_precheck.csv | selected row keeps net/PF/density/short/month12 guards(선택 행이 순수익/수익 팩터/밀도/숏/12월 가드 유지) |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/variant_filter_audit.csv | no candidate creates more entries than input(어떤 후보도 입력보다 많은 진입을 만들지 않음) |
| package_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/package_precheck.csv | package precheck is proxy-only(패키지 사전검사는 프록시 전용) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/run_evidence_receipt.json | skill receipts exist(스킬 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/required_gate_coverage_audit.csv | required gates are connected to closeout(필수 게이트가 종료 기록에 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CS/claim_boundary_receipt.json | runtime/operating claims remain blocked(런타임/운영 주장은 계속 차단) |

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)입니다. New ONNX model(새 ONNX 모델), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
