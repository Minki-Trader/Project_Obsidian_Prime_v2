# Stage 349(349단계)

Stage349(349단계)는 ONNX short-carry runtime probe(온엑스 숏 기여 런타임 탐침) 실행만 얇게 맡는다.

- current_run(현재 실행): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1`
- source_package(원천 패키지): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- retargeted_queue(재지정 대기열): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349A/run349B_onnx_short_carry_mt5_probe_queue.csv`

Effect(효과): Stage348(348단계)의 package artifact(패키지 산출물)는 복사하지 않고 참조해 heavy artifact duplication(무거운 산출물 중복)을 줄인다.

## run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

- run_id(실행 ID): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- summary(요약): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/onnx_short_carry_mt5_probe_summary.csv`
- diff(차이): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/proxy_mt5_runtime_difference.csv`
- effect(효과): run349C review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판단하게 한다.

## run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

- run_id(실행 ID): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- summary(요약): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/onnx_short_carry_mt5_probe_summary.csv`
- diff(차이): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/proxy_mt5_runtime_difference.csv`
- effect(효과): run349C review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판단하게 한다.

## run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

- run_id(실행 ID): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- summary(요약): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/onnx_short_carry_mt5_probe_summary.csv`
- diff(차이): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349B/proxy_mt5_runtime_difference.csv`
- effect(효과): run349C review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판단하게 한다.

## run349C ONNX Short-Carry MT5 Probe Review(349C 온엑스 숏 기여 MT5 탐침 검토)

- run_id(실행 ID): `run349C_review_onnx_short_carry_mt5_probe_without_db_v1`
- review(검토): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/03_reviews/run349C_onnx_short_carry_mt5_probe_review.md`
- diagnostic(진단): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349C/python_onnx_vs_expected_vs_mt5_diagnostic.csv`
- next_run(다음 실행): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`
- effect(효과): 런타임 동등성 결함을 수리 조건으로 좁힌다.

## run349D ONNX No-Conversion Runtime Parity Diagnostic

- run_id(실행 ID): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`
- parity_passed(동등성 통과): `False`
- max_abs_diff(최대 절대 차이): `0.9537997524862476`
- next_run_id(다음 실행 ID): `run349E_repair_tensor_output_handling_runtime_module_without_db_v1`
- effect(효과): MT5 ONNX conversion(변환) 가설을 실제 Strategy Tester(전략 테스터)로 검증했다.

## run349E Runtime-Compatible MLP Operator Pivot Probe

- run_id(실행 ID): `run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1`
- best_attempt(최고 시도): `e01_mlp_teacher_balanced`
- best_net_profit(최고 순수익): `0.0`
- effect(효과): TreeEnsembleClassifier(트리 앙상블 분류기) 실패 뒤 pure tensor MLP(순수 텐서 MLP) 경로를 검증했다.
