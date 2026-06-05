# Stage351 ONNX Trade Surface Rebuild(351단계 온엑스 거래 표면 재구축)

- canonical_stage_id(정식 단계 ID): `351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract`
- subtitle(부제): `no_scaler_or_1d_scaler_runtime_contract`
- current_run_id(현재 실행 ID): `run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1`
- source_stage(원천 단계): `350_onnx_runtime_interop__softmax_output_shape_repair_probe`

## Question(질문)

Stage350E(350E 실행)에서 MT5 runtime parity(MT5 런타임 동등성)를 통과한 no-scaler ONNX(스케일러 없음 온엑스) 또는 1D scaler ONNX(1차원 스케일러 온엑스) 계약으로, 거래 가능한 trade surface(거래 표면)를 다시 만들 수 있는가?

## Source Truth(원천 진실)

- run350E(350E 실행): runtime_completed_rows(런타임 완료 행) `5`, probability_parity_pass_rows(확률 동등성 통과 행) `5`.
- run350E(350E 실행): no_scaler_passed(스케일러 없음 통과) `True`, one_d_scaler_passed(1차원 스케일러 통과) `True`, table_runtime_passed(표 런타임 통과) `True`.
- proxy/MT5 runtime max_abs_diff(프록시/MT5 런타임 최대 절대 차이): `e00_array_no_scaler_linear=5e-11, e01_matrix_no_scaler_linear=5e-11, e02_matrix_sub_only_linear=5e-11, e03_matrix_1d_scaler_linear=2.98e-08, e04_table_feature0_sign_surface=1.42e-08`.

## Scope(범위)

Stage351(351단계)은 Stage350(350단계)의 runtime interop repair(런타임 상호운용 수리)를 닫고, no-scaler/1D-scaler ONNX(스케일러 없음/1차원 스케일러 온엑스) trade surface(거래 표면) 재구축을 새 질문으로 다룬다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.

## run351B No-Scaler/1D-Scaler ONNX Trade Surface(351B 실행 스케일러 없음/1차원 스케일러 온엑스 거래 표면)

- latest_completed_run_id(최근 완료 실행 ID): `run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1`
- current_run_id(현재 실행 ID): `run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`
- judgment(판정): `exploratory_proxy_weak_runtime_handoff_ready_mt5_probe_required_before_interpretation`
- selected_surfaces(선택 표면): `1`
- runtime_attempt_rows(런타임 시도 행): `2`

## run351C No-Scaler/1D-Scaler ONNX MT5 Probe(351C 실행 스케일러 없음/1차원 스케일러 온엑스 MT5 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`
- current_run_id(현재 실행 ID): `run351D_review_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`
- judgment(판정): `blocked_runtime_probe_outputs_missing_or_terminal_failed`
- attempts(시도): `2`
- runtime_completed_rows(런타임 완료 행): `2`
- best_attempt(최상위 시도): `p01_b01_1d_logreg_balanced_c100_none_validation`
