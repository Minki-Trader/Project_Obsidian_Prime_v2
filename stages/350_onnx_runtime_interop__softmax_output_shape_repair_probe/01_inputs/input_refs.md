# Stage350 Input Refs(350단계 입력 참조)

- input_manifest(입력 목록): `stages/350_onnx_runtime_interop__softmax_output_shape_repair_probe/01_inputs/stage350_input_manifest.csv`
- source_run(원천 실행): `run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1`
- diagnostic_memory(진단 기억): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`

Action(행동): Stage349(349단계)의 MT5 runtime probe(런타임 탐침) 실패 기억을 Stage350(350단계)의 입력으로 고정한다.

Effect(효과): 다음 수리 실행에서 같은 ONNX probability mismatch(온엑스 확률 불일치)를 원인 없이 반복하지 않는다.
