# run279C Report(279C 보고서): Directional Runtime Mapping MT5 Signal Replay(방향 런타임 매핑 MT5 신호 재생)

- run_id(실행 ID): `run279C_directional_runtime_mapping_mt5_signal_replay_v1`
- stage_id(단계 ID): `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild`
- source_run(원천 실행): `run279B_materialize_directional_runtime_mapping_inputs_v1`
- status(상태): `completed_directional_runtime_mapping_mt5_signal_replay_no_candidate_selection`
- judgment(판정): `runtime_probe_completed_inconclusive_no_candidate_selection`
- external_verification_status(외부 검증 상태): `completed`
- attempts(시도): `72/72`
- completed_attempts(완료 시도): `72`
- blocked_attempts(차단 시도): `0`
- mt5_kpi_records(MT5 핵심 성과 지표 기록): `72`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run279D_review_directional_runtime_mapping_mt5_probe`

## Meaning(의미)

run279C(279C 실행)는 run279B(279B 실행)의 directional payload(방향 페이로드)를 one-feature EBM table(단일 피처 EBM 표)로 MT5(`MetaTrader 5`, 메타트레이더5)에 넘긴다.
Effect(효과): runtime probe(런타임 탐침) 근거를 만들 수 있지만, reviewed candidate(검토된 후보)나 ONNX readiness(온엑스 준비)는 아직 아니다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
