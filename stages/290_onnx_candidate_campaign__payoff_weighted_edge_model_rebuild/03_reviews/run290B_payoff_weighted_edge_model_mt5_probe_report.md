# run290B Payoff Weighted Edge Model MT5 Probe(290B 손익가중 엣지 모델 MT5 탐침)

- run_id(실행 ID): `run290B_payoff_weighted_edge_model_mt5_probe_v1`
- stage_id(단계 ID): `290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild`
- source_run(원천 실행): `run290A_design_materialize_payoff_weighted_edge_model_rebuild_v1`
- status(상태): `completed_payoff_weighted_edge_model_mt5_probe_no_selection`
- judgment(판정): `runtime_probe_completed_requires_curve_quality_review_no_selection`
- external_verification_status(외부 검증 상태): `completed`
- attempts(시도): `36/36`
- completed_attempts(완료 시도): `36`
- blocked_attempts(차단 시도): `0`
- mt5_kpi_records(MT5 KPI 기록): `36`
- feature_order(피처 순서): `run290b_route_signal`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run290C_review_payoff_weighted_edge_model_mt5_probe`

Effect(효과): run290A(290A 실행)의 payoff-weighted route signal(손익가중 경로 신호)을 실제 MT5 tester(MT5 테스터)에 넘겼다. 선택 후보 판정은 run290C(290C 실행)에서 곡선/월/세션/거래 품질까지 본 뒤에만 한다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
