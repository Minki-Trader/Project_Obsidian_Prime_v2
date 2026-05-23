# run274A Post-Q04 Failure Candidate Rebuild Design(274A q04 실패 이후 후보 재구성 설계)

- run_id(실행 ID): `run274A_design_post_q04_failure_candidate_rebuild_packet_v1`
- source_run(원천 실행): `run273C_close_stage273_open_stage274_candidate_rebuild_v1`
- status(상태): `completed_post_q04_failure_candidate_rebuild_packet_design_no_candidate_selection`
- judgment(판정): `fresh_candidate_rebuild_queue_ready_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run274B_materialize_post_q04_failure_candidate_package_blueprints`

## Plain Result(쉬운 결과)

run274A(274A 실행)는 q04(4번 분기)를 고치지 않고, q04 failure memory(q04 실패 기억)를 새 candidate package(후보 패키지) 설계 조건으로 바꿨다.
효과(effect, 효과): 다음 run274B(274B 실행)는 같은 q04 repair(수리)가 아니라 fresh thesis(새 논제) 후보 표면을 물질화한다.

## Candidate Queue(후보 대기열)

- `cp274A_session_loss_asymmetry_router`: Session/hour loss pockets(세션/시간 손실 구간)는 no-trade filter(무거래 필터)가 아니라 direction-specific route asymmetry(방향별 경로 비대칭)로 바뀔 수 있다.
- `cp274B_month_regime_resilience_surface`: Worst-month losses(최악 월 손실)는 calendar exclusion(달력 제외)이 아니라 regime-pressure reward budget(국면 압박 보상 예산) 문제다.
- `cp274C_drawdown_recovery_context_router`: q04 drawdown(손실폭)은 single-entry signal(단일 진입 신호)보다 recovery context(회복 문맥) 부족에서 온다.
- `cp274D_q04_failure_boundary_control`: q04(4번 분기) 그대로의 failure signature(실패 서명)를 대조군으로 보존한다.

## Evidence Paths(근거 경로)

- candidate_rebuild_thesis_queue(후보 재구성 논제 대기열): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274A/candidate_rebuild_thesis_queue.csv`
- failure_to_requirement_map(실패-요구조건 지도): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274A/failure_to_requirement_map.csv` rows(행) `12`
- candidate_package_blueprint_seeds(후보 패키지 청사진 씨앗): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274A/candidate_package_blueprint_seeds.csv`
- discard_conditions(폐기 조건): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274A/discard_conditions.csv`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
