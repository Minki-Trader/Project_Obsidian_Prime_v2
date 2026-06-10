# run364CO h17 bad-month source-balance MT5 runtime probe inputs(17시 손실 월/원천 균형 MT5 런타임 탐침 입력)

Updated(갱신): 2026-06-06T01:27:12Z

Action(행동): CN candidate(CN 후보) `cm04_cj09_month08_12_pair_guard`를 RuntimeProbeEA(런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), compile check(컴파일 확인)로 materialize(구체화)했습니다.

Effect(효과): 다음 실행 `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`가 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 기록할 수 있습니다.

- compile status(컴파일 상태): `completed`
- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/mt5/sets/OPv2_run364CO_cm04.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/mt5/inis/OPv2_run364CO_cm04.ini`
- expected proxy KPI(예상 프록시 핵심 성과 지표): net `1036.46`, PF `1.4281838362`, trades `975`, density `3.1050955414`, shorts `100`
- MT5 execution(MT5 실행): `not_run`

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/work_packet.json | CO 작업 묶음(work packet, 작업 묶음)의 주 스킬과 게이트를 고정합니다. |
| runtime_representation_gate | passed | compile_status=completed;module_hashes=7 | CM 규칙이 EA 입력 표면에서 표현되고 컴파일되는지 확인합니다. |
| runtime_handoff_package_gate | passed | set=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/mt5/sets/OPv2_run364CO_cm04.set;ini=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/mt5/inis/OPv2_run364CO_cm04.ini;attempt=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CO/runtime_probe_attempt_package.csv | CP가 바로 실행할 파일 묶음을 만듭니다. |
| required_gate_coverage_audit | passed | receipts_written=True | required gate(필수 게이트)와 receipt(영수증)를 종료에 연결합니다. |
| final_claim_guard | passed | mt5_execution=not_run;runtime_authority=not_claimed;operating_promotion=not_claimed | 패키지를 운영 권위로 과장하지 않습니다. |

## Boundary(경계)

CO is package only(CO는 패키지 전용)입니다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
