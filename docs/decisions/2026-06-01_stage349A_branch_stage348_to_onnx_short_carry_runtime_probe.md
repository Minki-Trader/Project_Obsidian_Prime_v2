# 2026-06-01 Stage349A Branch Decision(349A 단계 분기 결정)

## Decision(결정)

`stage349A_open_run349B_execute_onnx_deployable_short_carry_mt5_probe`

## Source(원천)

- source_stage(원천 단계): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage`
- source_package(원천 패키지): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- superseded_run(대체 실행): `run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- new_stage(새 단계): `349_onnx_short_carry_runtime__execute_mt5_probe`
- next_run(다음 실행): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`

## Action/Effect(행동/효과)

Action(행동): Stage348(348단계)의 MT5 runtime probe(MT5 런타임 탐침)를 Stage349(349단계)로 분기했다.
Effect(효과): Stage348(348단계)은 package handoff(패키지 인계)까지만 유지하고, MT5 execution evidence(MT5 실행 근거)는 Stage349(349단계)에서 수집한다.

## Claim Boundary(주장 경계)

`state_sync_stage_branch_onnx_short_carry_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
