# run274E Score Surface Screen(274E 점수 표면 선별)

- run_id(실행 ID): `run274E_screen_post_q04_failure_score_surfaces_v1`
- source_run(원천 실행): `run274D_execute_post_q04_failure_scoring_materialization_probe_v1`
- status(상태): `completed_post_q04_failure_score_surface_screen_no_survivor_no_candidate_selection`
- judgment(판정): `negative_valid_filter_like_score_surfaces_no_probe_survivor`
- judgment_class(판정 분류): `negative`
- probe_queue_rows(탐침 대기열 행): `0`
- failure_memory_rows(실패 기억 행): `3`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run274F_close_stage274_open_stage275_fresh_candidate_construction`

## Plain Result(쉬운 결과)

run274E(274E 실행)는 run274D(274D 실행)의 score surface(점수 표면)를 q04 control(q04 대조)과 비교했다.
효과(effect, 효과): 세 selectable package(선택 가능 패키지)가 새 active signal(활성 신호)을 만들지 못하고 q04 signal(q04 신호)을 복제하거나 줄이는 데 그쳤음을 failure memory(실패 기억)로 남긴다.

## Decisions(결정)

- `cp274A_session_loss_asymmetry_router`: `reject_duplicate_or_near_duplicate_signal_surface`, changed_signal_rate(변경 신호율) `0.0`, new_active_count(새 활성 수) `0`, removed_active_count(제거 활성 수) `0`
- `cp274B_month_regime_resilience_surface`: `reject_filter_like_trade_reduction_surface`, changed_signal_rate(변경 신호율) `0.02535906`, new_active_count(새 활성 수) `0`, removed_active_count(제거 활성 수) `2366`
- `cp274C_drawdown_recovery_context_router`: `reject_duplicate_or_near_duplicate_signal_surface`, changed_signal_rate(변경 신호율) `0.00055734`, new_active_count(새 활성 수) `0`, removed_active_count(제거 활성 수) `52`

## Evidence Paths(근거 경로)

- screening_decision_matrix(선별 결정 행렬): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274E/screening_decision_matrix.csv`
- failure_memory(실패 기억): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274E/failure_memory.csv`
- probe_queue(탐침 대기열): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274E/probe_queue.csv`
- stage275_handoff_recommendation(275단계 인계 권고): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274E/stage275_handoff_recommendation.json`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
