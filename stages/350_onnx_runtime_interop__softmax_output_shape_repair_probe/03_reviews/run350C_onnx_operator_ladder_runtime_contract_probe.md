# run350C ONNX Operator Ladder Runtime Contract Probe(350C 온엑스 연산자 사다리 런타임 계약 탐침)

- run_id(실행 ID): `run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1`
- status(상태): `completed_stage350C_operator_ladder_found_runtime_contract_break_no_selection`
- judgment(판정): `negative_runtime_contract_first_failing_operator_variable_matmul_add_repair_required`
- result_judgment(결과 판정): `negative_runtime_contract(부정 런타임 계약)`
- gates(게이트): `10/10`
- attempts(시도): `6`
- runtime_completed_rows(런타임 완료 행): `6`
- probability_parity_pass_rows(확률 동등성 통과 행): `3`
- first_failing_operator(첫 실패 연산자): `variable_matmul_add`
- next_run_id(다음 실행 ID): `run350D_build_gemm_safe_or_table_runtime_model_family_pivot_without_db_v1`

Action(행동): Constant(상수), MatMul/Add(행렬곱/더하기), Sub/Div scaler(스케일러), variable linear output(가변 선형 출력), full MLP logits(전체 MLP 로짓), Softmax(소프트맥스)를 순서대로 MT5에서 실행했다.

Effect(효과): Stage350B(350B 실행)의 ONNX mismatch(온엑스 불일치)가 어느 연산자 경계에서 시작되는지 분리한다.

claim_boundary(주장 경계): `research_development_onnx_operator_ladder_runtime_contract_probe_only_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
