# run364CT h17 month12 long equity drawdown repair review(364CT 17시 12월 롱/수익곡선 낙폭 수리 검토)

Updated(갱신): 2026-06-06T02:46:53Z

## Current Truth(현재 진실)

- status(상태): `completed_stage364CT_h17_month12_long_equity_dd_review_runtime_representation_repair_required_no_authority`
- judgment(판정): `positive_proxy_candidate_cr04_runtime_representation_gap_open_cu_secondary_month_guard_no_authority`
- reviewed variant(검토 변형): `cr04_month12_long_hours17_20_floor002`
- proxy KPI(프록시 핵심 성과 지표): net(순수익) `1067.2`, PF(수익 팩터) `1.4466929377`, density(밀도) `3.0796178344`, trades(거래수) `967`, shorts(숏) `100`
- month12 long net(12월 롱 순수익): `21.36`
- package decision(패키지 결정): `runtime_representation_repair_required_before_mt5_probe`
- next run(다음 실행): `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`

## Action And Effect(행동과 효과)

Action(행동): CS selected proxy(CS 선택 프록시) `cr04`를 KPI(핵심 성과 지표), proxy/MT5 gap(프록시/MT5 차이), EA representation(EA 표현 가능성)으로 검토했습니다.

Effect(효과): `cr04`는 보존하지만, 현재 EA에는 두 번째 month margin guard(월 마진 가드)가 없어 바로 MT5 package(MT5 패키지)로 넘기지 않고 `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`에서 런타임 표현을 먼저 수리합니다.

## Package Gate(패키지 게이트)

| gate_id | gate_status | evidence | effect |
| --- | --- | --- | --- |
| proxy_kpi_package_gate | passed_for_runtime_repair_queue(런타임 수리 대기열 통과) | net=1067.2;pf=1.4466929377;density=3.0796178344;shorts=100;month12_long=21.36 | proxy quality is enough to justify repairing runtime representation(프록시 품질은 런타임 표현 수리를 정당화) |
| runtime_exact_representation_gate | repair_required_before_mt5_probe(MT5 탐침 전 수리 필요) | month_guard=True;time_guard=True;calendar_block=True;second_month_guard=False | blocks premature MT5 package if cr04 cannot be represented exactly(cr04를 정확히 표현할 수 없으면 성급한 MT5 패키지를 막음) |
| package_decision | open_cu_runtime_repair_not_mt5_execution(CU 런타임 수리 개방, MT5 실행 아님) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/run364CU_runtime_package_queue.csv | next action fixes handoff tooling before external verification(다음 행동은 외부 검증 전 인계 도구를 고침) |

## Runtime Representation(런타임 표현)

| variant_id | representation_id | representation_status | required_runtime_change | effect |
| --- | --- | --- | --- | --- |
| cr04_month12_long_hours17_20_floor002 | cr04_exact_piecewise_month12_margin_guard | gap_requires_secondary_month_margin_guard(간극 있음, 두 번째 월 마진 가드 필요) | add InpMonthMarginGuard2* inputs or equivalent month-specific secondary guard(InpMonthMarginGuard2 계열 입력 또는 동등한 월별 보조 가드 추가) | prevents replacing a precise proxy rule with broader runtime behavior(정확한 프록시 규칙을 더 넓은 런타임 동작으로 바꾸지 않음) |
| cr02_month12_long_margin_floor_002 | representable_fallback_all_month12_floor002 | represented_but_not_selected_proxy_best(표현 가능하지만 선택 프록시 최상위 아님) | none for cr02(CR02에는 없음) | keeps a fallback if CU cannot patch runtime(CU에서 런타임 보강 실패 시 대체 후보 유지) |
| cr01_month12_long_hours17_20_block | representable_fallback_calendar_block | represented_but_more_destructive_than_cr04(표현 가능하지만 cr04보다 제거 폭 큼) | none for cr01(CR01에는 없음) | keeps conservative fallback without pretending it is cr04(cr04인 척하지 않는 보수 대체 후보 유지) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/selected_variant_review.csv | proxy KPI is reviewed without MT5 authority(프록시 KPI를 MT5 권위 없이 검토) |
| row_grain_audit | passed | Tier A separate / Tier B missing_required / Tier A+B out_of_scope rows written(티어 행 작성) | Tier B gap is named(티어 B 간극을 이름 붙임) |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/input_manifest.csv | CT judgment is tied to CS/CQ/EA artifacts(CT 판정이 CS/CQ/EA 산출물에 연결) |
| runtime_representation_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/runtime_representation_review.csv | runtime representation gap is recorded before MT5 probing(MT5 탐침 전 런타임 표현 간극 기록) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/required_gate_coverage_audit.csv | required gates connect to closeout(필수 게이트가 종료 기록에 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CT/claim_boundary_receipt.json | runtime authority and operating promotion remain not claimed(런타임 권위와 운영 승격을 주장하지 않음) |

## Boundary(경계)

This is review only(검토 전용)입니다. New MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
