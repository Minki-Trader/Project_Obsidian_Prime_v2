# Stage364W density side-balance runtime package(Stage364W 밀도 방향 균형 런타임 패키지)

## Current truth(현재 진실)

- run_id(실행 ID): `run364W_package_density_side_balance_repair_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364V_train_density_side_balance_repair_onnx_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `runtime_probe_package_ready_dual_side_density_balance_repair_mt5_execution_required_no_authority`
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_common_files_synced_compile_checked_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
- MT5 execution(MT5 실행): `not_run`

## Action/Effect(행동/효과)

Action(행동): `run364V` selected candidate(선택 후보) `dual_pshort_0_45__adx_block_40_0__maxhold_8`를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), expected tape(예상 기록)로 package(패키지)했다.

Effect(효과): short threshold(숏 임계값) `0.45`, ADX long block(ADX 롱 차단) `40.0`, max hold(최대 보유) `8` 조합을 MT5 Strategy Tester(MT5 전략 테스터)에서 바로 확인할 수 있게 했다.

## Expected proxy(예상 프록시)

| split | trade_count | trade_density_per_business_day | net_profit | profit_factor | expectancy | max_drawdown | recovery_factor | long_trade_count | short_trade_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation | 596 | 3.0721649485 | 270.552 | 1.1359021692 | 0.4539463087 | -155.007 | 1.7454179489 | 522 | 74 |
| oos | 485 | 3.4892086331 | 501.012 | 1.3368770697 | 1.033014433 | -90.53 | 5.5342096543 | 430 | 55 |
| combined | 1081 | 3.2462462462 | 771.564 | 1.2218406503 | 0.7137502313 | -155.007 | 4.9776074629 | 952 | 129 |

## Runtime handoff(런타임 인계)

- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/mt5/sets/OPv2_run364W.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/mt5/inis/OPv2_run364W.ini`
- runtime policy(런타임 정책): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/runtime_policy_config.json`
- Common Files sync(공용 파일 동기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/common_files_sync.csv`
- execution queue(실행 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/run364X_execution_queue.csv`
- compile status(컴파일 상태): `completed`
- portable EA sync(포터블 EA 동기화): `True`

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| runtime_package_scope_gate(런타임 패키지 범위 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/final_decision.json | scope(범위)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 닫는다. |
| common_files_handoff_gate(공용 파일 인계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/common_files_sync.csv | ONNX/feature/expected tape(온엑스/피처/예상 기록)를 Common Files(공용 파일)에 동기화한다. |
| metaeditor_compile_gate(메타에디터 컴파일 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/mt5_compile_result.json | EA source/binary(전문가 자문 소스/바이너리) 불일치를 MT5 실행 전에 드러낸다. |
| tester_identity_gate(테스터 정체성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/tester_identity_contract.csv | tester model/deposit/leverage(테스터 모델/예치금/레버리지)를 고정한다. |
| runtime_parity_contract_gate(런타임 동등성 계약 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/runtime_parity_contract.csv | Python expected tape(파이썬 예상 기록)와 MT5 execution(MT5 실행) 비교 계약을 만든다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/claim_boundary_receipt.json | package(패키지)를 운영 주장(operating claim, 운영 주장)으로 착각하지 않게 한다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364W/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

이 package(패키지)는 MT5 runtime probe(런타임 탐침) 준비물이다. tester report(테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next action(다음 행동)

`run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1`에서 Strategy Tester(전략 테스터)를 실행하고 probability parity(확률 동등성), trade KPI(거래 핵심 성과 지표), cost behavior(비용 현상)를 비교한다.
