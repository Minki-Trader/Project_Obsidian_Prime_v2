# Decision(결정): Stage350A Branch(350A 단계 분기)

- date(날짜): `2026-06-01`
- run_id(실행 ID): `run350A_branch_stage349_to_onnx_runtime_interop_repair_without_db_v1`
- decision(결정): `stage350A_open_run350B_probe_softmax_output_shape_and_conversion_semantics`
- next_stage(다음 단계): `350_onnx_runtime_interop__softmax_output_shape_repair_probe`
- next_run(다음 실행): `run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1`
- judgment(판정): `stage_branch_completed_stage349_heavy_runtime_probe_handoff_to_stage350_onnx_runtime_interop_repair_no_operating_claim`
- claim_boundary(주장 경계): `state_sync_stage_branch_onnx_runtime_interop_repair_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): Stage349(349단계)의 무거운 런타임 탐침 흐름을 Stage350(350단계)으로 분기한다.

Effect(효과): 다음 실행은 ONNX output semantics(온엑스 출력 의미) 수리에 집중하고, Stage349의 negative runtime parity evidence(부정 런타임 동등성 근거)는 보존한다.
