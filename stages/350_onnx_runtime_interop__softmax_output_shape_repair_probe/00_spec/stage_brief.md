# Stage350 ONNX Runtime Interop Repair(350단계 온엑스 런타임 상호운용 수리)

- canonical_stage_id(정식 단계 ID): `350_onnx_runtime_interop__softmax_output_shape_repair_probe`
- subtitle(부제): `softmax_output_shape_repair_probe`
- current_run_id(현재 실행 ID): `run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1`
- source_stage(원천 단계): `349_onnx_short_carry_runtime__execute_mt5_probe`
- handoff_stage(인계 단계): `351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract`

## Question(질문)

MT5 ONNX runtime(MT5 온엑스 런타임)이 probability output(확률 출력)을 Python(파이썬)과 같은 의미로 읽게 만들 수 있는가?

## Source Truth(원천 진실)

- run349D(349D 실행): input_hash(입력 해시)는 `5827`행 일치했지만 probability_match(확률 일치)는 `0`행이었다.
- run349D(349D 실행): MT5 KPI(MT5 핵심 성과 지표)는 net_profit(순수익) `-197.95`, profit_factor(수익 팩터) `0.89`, trade_count(거래 수) `451`였다.
- run349E(349E 실행): pure tensor MLP(순수 텐서 다층 퍼셉트론) 후보 `2`개를 실행했지만 parity_pass_rows(동등성 통과 행)는 `0`이었다.
- run349E(349E 실행): best_attempt(최고 시도)는 `e01_mlp_teacher_balanced`, net_profit(순수익) `0.0`, profit_factor(수익 팩터) `0.0`, trade_count(거래 수) `0`였다.

## Scope(범위)

Stage350(350단계)은 ONNX operator/output semantics(온엑스 연산자/출력 의미)만 좁게 다룬다. softmax axis(소프트맥스 축), fixed output shape(고정 출력 모양), explicit softmax graph(명시 소프트맥스 그래프), InpModelNoConversion(입력 모델 변환 없음) 설정을 비교한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.

## run350B Softmax Output Shape Conversion Probe(350B 소프트맥스 출력 모양 변환 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1`
- current_run_id(현재 실행 ID): `run350B_retry_softmax_output_shape_and_conversion_semantics_without_db_v1`
- judgment(판정): `blocked_runtime_interop_probe_mt5_outputs_missing_or_terminal_unavailable`

Action(행동): Stage350B(350B 실행)는 softmax/output shape/conversion(소프트맥스/출력 모양/변환) 조합을 MT5에서 비교했다.

Effect(효과): Stage350(350단계)의 다음 질문은 `run350B_retry_softmax_output_shape_and_conversion_semantics_without_db_v1`로 좁혀졌다.

## run350C ONNX Operator Ladder Runtime Contract Probe(350C 온엑스 연산자 사다리 런타임 계약 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1`
- current_run_id(현재 실행 ID): `run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1`
- first_failing_operator(첫 실패 연산자): `variable_matmul_add`

## run350D Matrix Tensor Gemm Runtime Repair Probe(350D 행렬 텐서 Gemm 런타임 수리 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `run350D_build_gemm_safe_or_table_runtime_model_family_pivot_without_db_v1`
- current_run_id(현재 실행 ID): `run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1`
- judgment(판정): `negative_runtime_contract_matrix_tensor_and_gemm_repair_failed_table_runtime_or_handoff_probe_required`
- matrix_matmul_passed(행렬 MatMul 통과): `False`
- matrix_gemm_passed(행렬 Gemm 통과): `False`

## run350E No Scaler Table Runtime Handoff Probe(350E 스케일러 없음 테이블 런타임 인계 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1`
- current_run_id(현재 실행 ID): `run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1`
- judgment(판정): `positive_runtime_repair_simplified_onnx_path_passed_scaler_broadcast_contract_is_suspect`
- no_scaler_passed(스케일러 없음 통과): `True`
- sub_only_passed(Sub 전용 통과): `True`
- one_d_scaler_passed(1D 스케일러 통과): `True`
- table_runtime_passed(테이블 런타임 통과): `True`

Action(행동): run350E(350E 실행)는 UTF-8/BOM(유니코드 인코딩/문서 시작 표시) 수리 뒤 no-scaler ONNX(스케일러 없음 온엑스), 1D scaler ONNX(1차원 스케일러 온엑스), table runtime(표 런타임)을 MT5에서 재검증했다.

Effect(효과): Stage350(350단계)은 런타임 입력 정렬 문제를 수리한 근거로 닫고, 거래 surface(거래 표면) 재구축은 Stage351(351단계)로 분리했다.

## Stage351 Branch(351단계 분기)

- branch_run_id(분기 실행 ID): `run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1`
- next_run_id(다음 실행 ID): `run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1`
- claim_boundary(주장 경계): `state_sync_stage_branch_no_scaler_or_1d_scaler_trade_surface_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
