# run286B Report(286B 보고서): Trade Density Curve Quality MT5 Probe(거래 밀도/곡선 품질 MT5 탐침)

- run_id(실행 ID): `run286B_trade_density_curve_quality_mt5_probe_v1`
- stage_id(단계 ID): `286_onnx_candidate_campaign__trade_density_curve_quality_rebuild`
- source_run(원천 실행): `run286A_design_materialize_trade_density_curve_quality_candidates_v1`
- status(상태): `completed_trade_density_curve_quality_mt5_probe_no_selection`
- judgment(판정): `runtime_probe_completed_requires_curve_quality_review_no_selection`
- external_verification_status(외부 검증 상태): `completed`
- attempts(시도): `30/30`
- completed_attempts(완료 시도): `30`
- blocked_attempts(차단 시도): `0`
- mt5_kpi_records(MT5 핵심 성과 지표 기록): `30`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run286C_review_trade_density_curve_quality_mt5_probe`

## Meaning(의미)

run286B(286B 실행)는 run286A(286A 실행)의 trade density payload(거래 밀도 페이로드)를 one-feature EBM table(단일 피처 EBM 표)로 MT5(`MetaTrader 5`, 메타트레이더5)에 넘긴다.
Effect(효과): 4-10 trades/day(일 4-10거래), net profit(순수익), PF(수익 팩터), DD(손실폭), recovery(회복)를 외부 검증으로 측정하지만, reviewed candidate(검토된 후보)나 ONNX readiness(온엑스 준비)는 아직 아니다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
