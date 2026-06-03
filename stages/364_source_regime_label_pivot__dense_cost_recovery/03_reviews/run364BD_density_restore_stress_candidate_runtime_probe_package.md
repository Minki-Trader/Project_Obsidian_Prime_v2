# run364BD density restore stress candidate runtime probe package(364BD 밀도 복원 압박 후보 런타임 탐침 패키지)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- selected_candidate(선택 후보): `run364BB_ba02_between_ax03_ax08_floor025_ps450`
- expected net/PF/density/DD/trades(예상 순수익/수익 팩터/밀도/낙폭/거래수): `919.75` / `1.3178004168` / `3.045045045` / `-127.733` / `1112`
- compile_status(컴파일 상태): `completed`
- MT5 execution(MT5 실행): `not_run`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): `run364BC` selected primary(선택 주 후보)를 RuntimeProbeEA(런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), runtime policy(런타임 정책), execution queue(실행 대기열)로 package(패키지)했다.

Effect(효과): short threshold(숏 임계값) `0.45`, entry margin floor(진입 마진 하한) `0.00025`, max hold(최대 보유) `6` 조합을 `run364BE` MT5 Strategy Tester(MT5 전략 테스터)에서 바로 실행할 수 있다.

## Expected KPI(예상 KPI)

| split | net_profit | profit_factor | trade_count | trade_per_business_day | estimated_mt5_trade_per_business_day | max_drawdown | long_trade_count | short_trade_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation | 420.422 | 1.2739082195 | 568 | 2.9278350515 |  | -77.504 | 514 | 54 |
| oos | 499.328 | 1.3673660675 | 544 | 3.9136690647 |  | -127.733 | 495 | 49 |
| combined | 919.75 | 1.3178004168 | 1112 | 3.3393393393 | 3.045045045 | -127.733 | 1009 | 103 |

## Runtime Handoff(런타임 인계)

- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/mt5/sets/OPv2_run364BD.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/mt5/inis/OPv2_run364BD.ini`
- runtime policy(런타임 정책): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/runtime_policy_config.json`
- Common Files sync(공용 파일 동기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/common_files_sync.csv`
- execution queue(실행 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/run364BE_execution_queue.csv`
- portable EA sync(포터블 EA 동기화): `True`

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| runtime_evidence_gate(런타임 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/common_files_sync.csv | Common Files(공용 파일) 인계를 완료했다. |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/runtime_probe_attempt_package.csv | package scope(패키지 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 둔다. |
| runtime_filter_support_gate(런타임 필터 지원 게이트) | passed | foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5 | proxy policy(프록시 정책)를 EA input(EA 입력)으로 표현한다. |
| metaeditor_compile_gate(메타에디터 컴파일 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/mt5_compile_result.json | EA(전문가 자문)를 컴파일하고 portable tester(포터블 테스터)에 복사했다. |
| tester_identity_gate(테스터 정체성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/tester_set_manifest.csv | US100 M5, real ticks, deposit 500, leverage 100(US100 M5, 실제 틱, 예치금 500, 레버리지 100)을 고정했다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/expected_kpi_summary.csv | proxy KPI(프록시 핵심 성과 지표)와 추정 MT5 밀도 조건을 남겼다. |
| artifact_lineage_gate(산출물 계보 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/model_handoff_manifest.csv | model/handoff/parity(모델/인계/동등성) 경로를 연결했다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/required_gate_coverage_audit.csv | runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BD/final_decision.json | runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다. |

## Boundary(경계)

This is a runtime probe package(런타임 탐침 패키지) only. MT5 tester report(MT5 테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next Action(다음 행동)

`run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)의 차이(diff, 차이), 원인(attribution, 귀속), 활용 가능성(usability, 활용 가능성)을 기록한다.
