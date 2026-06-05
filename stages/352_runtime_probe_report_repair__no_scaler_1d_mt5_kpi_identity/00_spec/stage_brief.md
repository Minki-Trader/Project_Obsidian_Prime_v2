# Stage352 Runtime Probe Report Repair(352단계 런타임 탐침 보고서 수리)

- canonical_stage_id(정식 단계 ID): `352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity`
- subtitle(부제): `no_scaler_1d_mt5_kpi_identity`
- current_run_id(현재 실행 ID): `run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run352A_branch_stage351_to_report_identity_repair_without_db_v1`
- source_stage(원천 단계): `351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract`

## Question(질문)

Stage351C(351C 실행)의 MT5 runtime probe(MT5 런타임 탐침)는 telemetry parity(원격측정 동등성)를 냈지만, strategy report identity(전략 보고서 정체성) 수집이 막혔다. 기존 MT5 output(출력)을 재사용해서 report KPI(보고서 핵심 성과 지표)를 회수하고 proxy-vs-MT5 diff(프록시-MT5 차이)를 판정할 수 있는가?

## Source Truth(원천 진실)

- run351C(351C 실행): runtime_completed_rows(런타임 완료 행) `2`, proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행) `2`.
- run351C(351C 실행): matched_rows(일치 행) `17428/17428`, max_abs_probability_diff(최대 절대 확률 차이) `3.57600999978e-07`.
- run351C(351C 실행): order_fill_count(주문 체결 수) `2029`, long_count(롱 수) `4746`, short_count(숏 수) `3567`.
- blocker(차단 사유): report_available_rows(보고서 사용 가능 행) `0`. collector report name(수집기 보고서 이름)이 tester report name(테스터 보고서 이름)과 달랐다.

## Scope(범위)

Stage352(352단계)는 새 MT5 heavy rerun(무거운 MT5 재실행) 없이, Stage351C(351C 실행)의 이미 생성된 tester output(테스터 출력)을 재사용해 report identity repair(보고서 정체성 수리), KPI extraction(KPI 추출), proxy-MT5 attribution(프록시-MT5 귀속)을 좁게 수행한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
