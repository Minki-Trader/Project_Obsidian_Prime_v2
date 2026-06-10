# run364CU h17 month12 secondary month guard runtime package(17시 12월 보조 월 가드 런타임 패키지)

Updated(갱신): 2026-06-06T03:00:35Z

Action(행동): `cr04_month12_long_hours17_20_floor002`를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) set/ini(설정/INI)로 materialize(구체화)했습니다.

Effect(효과): primary month guard(주 월 가드) `0.01`과 secondary month guard(보조 월 가드) `0.02`가 모두 들어간 상태로 `run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행할 수 있습니다.

- compile status(컴파일 상태): `completed`
- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/mt5/sets/OPv2_run364CU_cr04_secondary_month_guard.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/mt5/inis/OPv2_run364CU_cr04_secondary_month_guard.ini`
- expected proxy KPI(예상 프록시 핵심 성과 지표): net(순수익) `1067.2`, PF(수익 팩터) `1.4466929377`, density(밀도) `3.0796178344`, trades(거래수) `967`
- MT5 execution(MT5 실행): `not_run`

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/work_packet.json | work packet(작업 묶음)이 CU 목적과 필수 게이트를 고정합니다. |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/input_manifest.csv | 입력 산출물(input artifacts, 입력 산출물)의 해시(hash, 해시)를 연결합니다. |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/tester_set_manifest.csv | primary/secondary month guard(주/보조 월 가드)가 set(설정)에 모두 있는지 확인합니다. |
| compile_gate | passed | compile_status=completed;log=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/mt5/compile/ObsidianPrimeV2_RuntimeProbeEA_compile.log | MetaEditor compile(메타에디터 컴파일)로 EA 문법과 EX5 생성 가능성을 확인합니다. |
| runtime_handoff_package_gate | passed | set=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/mt5/sets/OPv2_run364CU_cr04_secondary_month_guard.set;ini=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/mt5/inis/OPv2_run364CU_cr04_secondary_month_guard.ini;attempt=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CU/runtime_probe_attempt_package.csv | CV가 실행할 handoff package(인계 패키지)를 만듭니다. |
| required_gate_coverage_audit | passed | receipts_written=True | required gates(필수 게이트)를 receipt(영수증)와 연결합니다. |
| final_claim_guard | passed | mt5_execution=not_run;runtime_authority=not_claimed;operating_promotion=not_claimed;goal_achieve=not_claimed | 패키지를 운영 권위(operating authority, 운영 권위)로 과장하지 않습니다. |

## Boundary(경계)

CU is package only(CU는 패키지 전용)입니다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
