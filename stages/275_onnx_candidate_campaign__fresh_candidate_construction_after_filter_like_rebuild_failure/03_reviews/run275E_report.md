# run275E Fresh Candidate Score Surface Screen(275E 새 후보 점수 표면 선별)

- run_id(실행 ID): `run275E_screen_fresh_candidate_score_surfaces_v1`
- source_run(원천 실행): `run275D_execute_fresh_candidate_scoring_materialization_probe_v1`
- status(상태): `completed_fresh_candidate_score_surface_screen_probe_queue_no_candidate_selection`
- judgment(판정): `screened_stage276_probe_seeds_and_failure_memory_no_candidate_selection`
- judgment_class(판정 분류): `inconclusive_probe_seed`
- screened_packages(선별 패키지): `5`
- stage276_queue_rows(276단계 대기열 행): `3`
- failure_memory_rows(실패 기억 행): `1`
- support_control_rows(보조 대조 행): `1`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run275F_close_stage275_open_stage276_aggressive_fresh_surface_probe`

## Plain Result(쉬운 결과)

run275E(275E 실행)는 run275D(275D 실행)의 score table(점수표)을 q04 guard(q04 방어 기준)와 비교했다.
효과(effect, 효과): Stage276 aggressive probe seed(276단계 공격형 탐침 씨앗) `3`개, failure memory(실패 기억) `1`개, support control(보조 대조) `1`개를 분리했고 선택 후보는 아직 없다.

## Screening Decisions(선별 결정)

- `cp275A_volatility_pullback_breakout_surface`: judgment(판정) `stage276_aggressive_probe_seed(276단계 공격형 탐침 씨앗)`, changed_rate(변경률) `0.29674169`, new_active(새 활성) `9854`, direction_changed(방향 변경) `906`, score(점수) `18.110982`
- `cp275B_cross_asset_divergence_reversal_surface`: judgment(판정) `stage276_aggressive_probe_seed(276단계 공격형 탐침 씨앗)`, changed_rate(변경률) `0.51745981`, new_active(새 활성) `16274`, direction_changed(방향 변경) `6145`, score(점수) `30.748786`
- `cp275C_cash_session_impulse_continuation_surface`: judgment(판정) `failure_memory_route_bias(실패 기억: 경로 편향)`, changed_rate(변경률) `0.45965702`, new_active(새 활성) `5332`, direction_changed(방향 변경) `2718`, score(점수) `17.540038`
- `cp275D_macro_volatility_squeeze_release_surface`: judgment(판정) `stage276_aggressive_probe_seed(276단계 공격형 탐침 씨앗)`, changed_rate(변경률) `0.54730975`, new_active(새 활성) `20574`, direction_changed(방향 변경) `3932`, score(점수) `34.858474`
- `cp275E_q04_stage274_failure_signature_guard`: judgment(판정) `support_control_carry(보조 대조 유지)`, changed_rate(변경률) `0.0`, new_active(새 활성) `0`, direction_changed(방향 변경) `0`, score(점수) `3.222223`

## Queue And Failure(대기열과 실패)

- stage276_queue(276단계 대기열): `cp275D_macro_volatility_squeeze_release_surface, cp275B_cross_asset_divergence_reversal_surface, cp275A_volatility_pullback_breakout_surface`
- failure_memory(실패 기억): `cp275C_cash_session_impulse_continuation_surface`

## Evidence Paths(근거 경로)

- screen(선별): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/screen.csv`
- stage276_queue(276단계 대기열): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/stage276_queue.csv`
- failure_memory(실패 기억): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/failure.csv`
- support_control(보조 대조): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/support.csv`
- lineage(계보): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/lineage.json`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
