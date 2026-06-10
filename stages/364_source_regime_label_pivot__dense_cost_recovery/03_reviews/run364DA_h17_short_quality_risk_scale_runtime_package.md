# run364DA h17 short-quality risk-scale runtime package(364DA 17시 숏 품질 위험비율 런타임 패키지)

Updated(갱신): 2026-06-06T04:23:24Z

Action(행동): `cx05_high_quality_short_boost110_h17_20`를 RuntimeProbeEA(런타임 탐침 EA) risk-scale overlay(위험비율 오버레이)와 set/ini(설정/INI)로 materialize(구체화)했습니다.

Effect(효과): `run364DB`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

- compile status(컴파일 상태): `completed`
- compile zero errors(컴파일 오류 0개): `True`
- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/mt5/sets/OPv2_run364DA_cx05_short_quality_risk_scale.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/mt5/inis/OPv2_run364DA_cx05_short_quality_risk_scale.ini`
- expected proxy KPI(예상 프록시 핵심 성과 지표): net(순수익) `1075.07`, PF(수익 팩터) `1.4451946256`, density(밀도) `3.0796178344`, trades(거래수) `967`, risk scaled shorts(위험비율 조정 숏) `79`
- MT5 execution(MT5 실행): `not_run`

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/work_packet.json | DA work packet recorded(DA 작업 묶음 기록) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/input_manifest.csv | CZ/CY/CU inputs connected(CZ/CY/CU 입력 연결) |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/runtime_representation_audit.csv | cx05 rule represented in set/EA contract(cx05 규칙이 설정/EA 계약에 표현) |
| compile_gate | passed | compile_status=completed;zero_errors=True;log=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/mt5/compile/ObsidianPrimeV2_RuntimeProbeEA_compile.log | EA compile checked and portable binary synced(EA 컴파일 점검 및 포터블 바이너리 동기화) |
| runtime_handoff_package_gate | passed | set=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/mt5/sets/OPv2_run364DA_cx05_short_quality_risk_scale.set;ini=stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DA/mt5/inis/OPv2_run364DA_cx05_short_quality_risk_scale.ini | DB handoff package prepared(DB 인계 패키지 준비) |
| required_gate_coverage_audit | passed | receipts_written=True | required gates linked to receipts(필수 게이트와 영수증 연결) |
| final_claim_guard | passed | mt5_execution=not_run;authority=not_claimed | package is not overstated as authority(패키지를 권위로 과장하지 않음) |

## Boundary(경계)

DA is package only(DA는 패키지 전용)입니다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
