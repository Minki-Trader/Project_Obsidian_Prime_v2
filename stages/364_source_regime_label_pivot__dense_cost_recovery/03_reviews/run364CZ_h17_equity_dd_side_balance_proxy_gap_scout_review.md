# run364CZ h17 equity DD side balance proxy gap scout review(364CZ 17시 수익곡선 낙폭/방향 균형/프록시 차이 정찰 검토)

Updated(갱신): 2026-06-06T04:12:55Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`
- reviewed variant(검토 변형): `cx05_high_quality_short_boost110_h17_20`
- proxy net/PF/density(프록시 순수익/수익 팩터/밀도): `1075.07` / `1.4451946256` / `3.0796178344`
- risk-scaled short count(위험비율 조정 숏 수): `79`
- risk-scale net delta(위험비율 순수익 변화): `7.87`
- current MT5 anchor net/PF/density/equity DD(현재 MT5 기준 순수익/수익 팩터/밀도/수익곡선 낙폭): `1011.02` / `1.42` / `3.0955414013` / `130.11`
- package decision(패키지 결정): `runtime_representation_repair_required_before_mt5_probe`
- next run(다음 실행): `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`

## Action And Effect(행동과 효과)

Action(행동): `run364CY` selected proxy(선택 프록시) `cx05`를 EA support(EA 지원), runtime representation(런타임 표현), proxy/MT5 gap(프록시/MT5 차이), equity DD boundary(수익곡선 낙폭 경계)로 검토했습니다.

Effect(효과): `cx05`는 proxy(프록시) 기준으로 보존할 가치가 있지만, 현재 RuntimeProbeEA(런타임 탐침 EA)는 “17-20시 숏, `margin_vs_long >= 0.080`, risk_scale(위험비율) `1.10`”을 정확히 파라미터화하지 못합니다. 따라서 직접 MT5 package(MT5 패키지)는 막고 `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`에서 런타임 패키지 수리로 넘깁니다.

## Package Decision(패키지 결정)

| decision_id | decision_status | evidence | effect |
| --- | --- | --- | --- |
| proxy_kpi_review | passed_for_runtime_repair_queue(런타임 수리 대기열 통과) | net=1075.07;pf=1.4451946256;density=3.0796178344;shorts=100;risk_delta=7.87 | proxy quality justifies runtime package repair work(프록시 품질이 런타임 패키지 수리 작업을 정당화) |
| direct_mt5_package_decision | direct_package_blocked_runtime_repair_required(직접 패키지 차단, 런타임 수리 필요) | risk_overlay=False;model_risk=True;fixed_lot=True | avoids external MT5 probe with changed meaning(뜻이 바뀐 외부 MT5 탐침을 피함) |
| next_work_packet | open_run364DA_runtime_package_repair(run364DA 런타임 패키지 수리 개방) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/run364DA_short_quality_risk_scale_runtime_package_queue.csv | turns the gap into implementable EA/set requirements(간극을 구현 가능한 EA/설정 요구사항으로 바꿈) |

## Runtime Representation(런타임 표현)

| representation_id | representation_status | required_runtime_change | effect |
| --- | --- | --- | --- |
| cx05_exact_short_quality_risk_scale_overlay | repair_required_missing_parameterized_short_quality_risk_scale_overlay(파라미터화 숏 품질 위험비율 오버레이 누락으로 수리 필요) | add parameterized side/hour/margin risk-scale overlay before lot execution(랏 실행 전 방향/시간/마진 기반 위험비율 오버레이 추가) | prevents treating proxy lot scaling as MT5 behavior before EA support(EA 지원 전 프록시 랏 조정을 MT5 동작으로 취급하지 않음) |
| generic_model_risk_sizing_not_exact | available_but_not_semantically_equivalent(사용 가능하지만 의미 동일 아님) | do not substitute generic model risk for cx05 exact rule(cx05 정확 규칙을 일반 모델 위험으로 대체하지 않음) | keeps runtime parity boundary clear(런타임 동등성 경계를 명확히 유지) |
| current_cu_anchor_exact_for_cr04_not_cx05 | represented_anchor_but_not_selected_cx05(기준은 표현되지만 선택 cx05는 아님) | carry CU anchor forward and add risk-scale overlay(CU 기준을 이어가며 위험비율 오버레이 추가) | keeps previous MT5-positive anchor as the package base(이전 MT5 양수 기준을 패키지 기반으로 유지) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/selected_candidate_review.csv | selected CY candidate reviewed(선택 CY 후보 검토 완료) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/input_manifest.csv | CY/CW/CU inputs connected(CY/CW/CU 입력 연결) |
| proxy_kpi_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/package_decision.csv | proxy KPI supports repair queue, not authority(프록시 KPI는 수리 대기열만 지지하고 권위는 아님) |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/runtime_representation_audit.csv | exact support gap recorded(정확 지원 간극 기록) |
| package_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/run364DA_short_quality_risk_scale_runtime_package_queue.csv | direct MT5 package blocked until DA repair(DA 수리 전 직접 MT5 패키지 차단) |
| artifact_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/artifact_lineage_receipt.json | artifact lineage receipt written(산출물 계보 영수증 작성) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/required_gate_coverage_audit.csv | required gates linked to closeout(필수 게이트 종료 기록 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CZ/claim_boundary_receipt.json | no authority/promotion/goal claim(권위/승격/목표 주장 없음) |

## Boundary(경계)

This is review only(검토 전용)입니다. New MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
