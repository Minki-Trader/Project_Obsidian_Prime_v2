# run350B Softmax Output Shape Conversion Probe(350B 소프트맥스 출력 모양 변환 탐침)

- run_id(실행 ID): `run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1`
- status(상태): `completed_stage350B_output_buffer_canary_passed_model_variants_failed_no_selection`
- judgment(판정): `negative_canary_passed_model_graph_or_numeric_saturation_still_blocks_runtime_parity`
- result_judgment(결과 판정): `negative_runtime_parity(부정 런타임 동등성)`
- gates(게이트): `11/11`
- attempts(시도): `6`
- runtime_completed_rows(런타임 완료 행): `6`
- probability_parity_pass_rows(확률 동등성 통과 행): `1`
- canary_passed(카나리 통과): `True`
- best_attempt(최고 시도): `b01_e02_softmax_fixed_noconv`
- best_attribution(최고 시도 귀속): `model_numeric_saturation_or_softmax_semantics`
- best_net_profit(최고 순수익): `-250.9`
- best_profit_factor(최고 수익 팩터): `0.86`
- best_trade_count(최고 거래 수): `466`
- next_run_id(다음 실행 ID): `run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1`

Action(행동): fixed output shape(고정 출력 모양), explicit softmax(명시 소프트맥스), temperature scaling(온도 스케일링), conversion flag(변환 플래그)를 MT5 Strategy Tester(전략 테스터)에서 비교했다.

Effect(효과): ONNX probability mismatch(온엑스 확률 불일치)를 output buffer(출력 버퍼), graph semantics(그래프 의미), numeric saturation(숫자 포화), model KPI(모델 핵심 성과) 중 어디에 붙일지 좁혔다.

claim_boundary(주장 경계): `research_development_onnx_runtime_interop_probe_only_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
