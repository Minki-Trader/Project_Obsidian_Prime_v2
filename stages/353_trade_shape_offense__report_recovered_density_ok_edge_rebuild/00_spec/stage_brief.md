# Stage353 Trade Shape Offense(353단계 거래 형태 공격 탐색)

- canonical_stage_id(정식 단계 ID): `353_trade_shape_offense__report_recovered_density_ok_edge_rebuild`
- subtitle(부제): `report_recovered_density_ok_edge_rebuild`
- current_run_id(현재 실행 ID): `run353A_branch_stage352_to_trade_shape_offensive_rebuild_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1`
- source_stage(원천 단계): `352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity`

## Question(질문)

Stage352B(352B 실행)에서 report KPI(보고서 핵심 성과 지표)는 회수됐고 trade density(거래 밀도)는 `3~10` 구간을 충족했다. 그러나 OOS loss(표본외 손실)와 high drawdown(높은 낙폭)이 남았다. density(밀도)와 ONNX runtime parity(온엑스 런타임 동등성)는 유지하면서 label(라벨), rule stack(규칙 묶음), trade shape(거래 형태)를 공격적으로 바꿔 수익 원천을 다시 만들 수 있는가?

## Source Truth(원천 진실)

- Stage352B combined net_profit(합산 순수익): `41.48`
- Stage352B combined PF(합산 수익 팩터): `1.0079426019`
- Stage352B trade_density(거래 밀도): `4.1815286624`
- Stage352B OOS net_profit(표본외 순수익): `-200.11`
- Stage352B max_drawdown_percent(최대 낙폭률): `65.34`

## Scope(범위)

Stage353(353단계)는 report repair(보고서 수리)가 아니라 offensive exploration(공격 탐색)이다. 새 label(라벨), threshold surface(임계값 표면), exit shape(청산 형태), session/regime filter(세션/국면 필터)를 열어 탐색한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
