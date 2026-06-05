# Stage351 Input References(351단계 입력 참조)

- parent_run_id(부모 실행 ID): `run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1`
- source_final_decision(원천 최종 결정): `stages/350_onnx_runtime_interop__softmax_output_shape_repair_probe/02_runs/run350E/final_decision.json`
- source_report(원천 보고서): `stages/350_onnx_runtime_interop__softmax_output_shape_repair_probe/03_reviews/run350E_no_scaler_table_runtime_handoff_probe.md`
- source_difference(원천 차이): `stages/350_onnx_runtime_interop__softmax_output_shape_repair_probe/02_runs/run350E/proxy_mt5_runtime_difference.csv`
- input_manifest(입력 목록): `stages/351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract/01_inputs/stage351_input_manifest.csv`

Action(행동): Stage350E(350E 실행) 산출물을 Stage351A(351A 실행)의 입력으로 등록한다.

Effect(효과): Stage351B(351B 실행)가 같은 근거에서 재시작할 수 있다.
