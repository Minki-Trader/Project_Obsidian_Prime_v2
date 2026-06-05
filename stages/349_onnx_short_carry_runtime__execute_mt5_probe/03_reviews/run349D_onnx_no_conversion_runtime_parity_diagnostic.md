# run349D ONNX No-Conversion Runtime Parity Diagnostic(349D 온엑스 변환 없음 런타임 동등성 진단)

## Summary(요약)

- run_id(실행 ID): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`
- status(상태): `completed_stage349D_onnx_no_conversion_runtime_parity_still_mismatch_repair_required_no_selection`
- judgment(판정): `negative_no_conversion_failed_input_hash_matched_treeensemble_onnx_operator_repair_required`
- result_judgment(결과 판정): `negative(부정)`
- gates(게이트): `9/9`
- base_attempt(기준 시도): `c03_xtrees_cashopen_q95q90`
- variant(변형): `InpModelNoConversion=true`
- runtime_completed(런타임 완료): `True`
- report_completed(보고서 완료): `True`
- parity_passed(동등성 통과): `False`
- rows_compared(비교 행): `5827`
- probability_match_rows(확률 일치 행): `0`
- input_hash_match_rows(입력 해시 일치 행): `5827`
- input_hash_mismatch_rows(입력 해시 불일치 행): `0`
- input_hash_status(입력 해시 상태): `matched(일치)`
- max_abs_diff(최대 절대 차이): `0.9537997524862476`
- net_profit(순수익): `-197.95`
- profit_factor(수익 팩터): `0.89`
- trade_count(거래 수): `451`
- trade_density(거래 밀도): `4.254716981132075`
- next_run_id(다음 실행 ID): `run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1`

Action(행동): run349B c03의 ONNX(온엑스) 모델과 feature handoff(피처 인계)는 그대로 두고, MT5 `.set`의 `InpModelNoConversion`만 `true`로 바꿔 Strategy Tester(전략 테스터)를 실행했다.

Effect(효과): MT5 ONNX runtime(런타임) 확률 불일치가 conversion(변환) 문제인지, 아니면 TreeEnsembleClassifier/operator runtime(트리 앙상블 분류기/연산자 런타임) 문제인지 좁힌다.

Input hash effect(입력 해시 효과): input_hash(입력 해시)가 일치하면 feature parser(피처 파서)는 같은 CSV row(CSV 행)를 넣은 것이므로, 남은 원인은 MT5 ONNX operator/runtime(온엑스 연산자/런타임) 쪽으로 좁혀진다.

claim_boundary(주장 경계): `research_development_onnx_no_conversion_runtime_parity_diagnostic_only_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
