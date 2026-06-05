# run350E No Scaler Table Runtime Handoff Probe(350E 스케일러 없음 테이블 런타임 인계 탐침)

- run_id(실행 ID): `run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1`
- status(상태): `completed_stage350E_onnx_simplified_path_parity_passed_no_selection`
- judgment(판정): `positive_runtime_repair_simplified_onnx_path_passed_scaler_broadcast_contract_is_suspect`
- result_judgment(결과 판정): `positive_runtime_repair_clue(긍정 런타임 수리 단서)`
- gates(게이트): `8/8`
- attempts(시도): `5`
- runtime_completed_rows(런타임 완료 행): `5`
- probability_parity_pass_rows(확률 동등성 통과 행): `5`
- no_scaler_passed(스케일러 없음 통과): `True`
- sub_only_passed(Sub 전용 통과): `True`
- one_d_scaler_passed(1D 스케일러 통과): `True`
- table_runtime_passed(테이블 런타임 통과): `True`
- next_run_id(다음 실행 ID): `run350F_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1`

Action(행동): run350E(350E 실행)는 no-scaler ONNX(스케일러 없음 온엑스), 1D scaler ONNX(1차원 스케일러 온엑스), table runtime(테이블 런타임)을 MT5에서 비교했다.

Effect(효과): scaler/broadcast(스케일러/브로드캐스트) 문제와 ONNX 우회(table runtime, 테이블 런타임) 가능성을 분리했다.

claim_boundary(주장 경계): `research_development_no_scaler_table_runtime_handoff_probe_only_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
