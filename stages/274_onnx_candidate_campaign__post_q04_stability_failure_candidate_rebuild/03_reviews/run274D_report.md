# run274D Score Surface Materialization(274D 점수 표면 물질화)

- run_id(실행 ID): `run274D_execute_post_q04_failure_scoring_materialization_probe_v1`
- source_run(원천 실행): `run274C_materialize_post_q04_failure_scoring_handoff_inputs_v1`
- status(상태): `completed_post_q04_failure_score_surface_materialization_no_candidate_selection`
- judgment(판정): `score_surfaces_materialized_no_candidate_selection`
- judgment_class(판정 분류): `inconclusive`
- packages(패키지): `4`
- summary_rows(요약 행): `12`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run274E_screen_post_q04_failure_score_surfaces`

## Plain Result(쉬운 결과)

run274D(274D 실행)는 run274C(274C 실행)의 scoring/handoff input(점수/인계 입력)을 deterministic score table(결정 점수표)로 물질화했다.
효과(effect, 효과): run274E(274E 실행)가 Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) 관점에서 점수 표면을 선별할 수 있다.

## Combined View(합산 보기)

- `cp274A_session_loss_asymmetry_router` `Tier A+B combined`: active_signal_rate(활성 신호율) `0.24237942`, mean_primary_score(평균 주 점수) `0.54115114`
- `cp274B_month_regime_resilience_surface` `Tier A+B combined`: active_signal_rate(활성 신호율) `0.21702036`, mean_primary_score(평균 주 점수) `0.54608541`
- `cp274C_drawdown_recovery_context_router` `Tier A+B combined`: active_signal_rate(활성 신호율) `0.24182208`, mean_primary_score(평균 주 점수) `0.51201847`
- `cp274D_q04_failure_boundary_control` `Tier A+B combined`: active_signal_rate(활성 신호율) `0.24237942`, mean_primary_score(평균 주 점수) `0.42900715`

## Evidence Paths(근거 경로)

- score_surface_summary(점수 표면 요약): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274D/score_surface_summary.csv`
- summary_by_view(보기별 요약): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/03_reviews/run274D_score_surface_summary.csv`
- normalization_receipt(정규화 영수증): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274D/normalization_receipt.json`
- score_tables(점수표): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274D/score_tables`
- handoff(인계): `stages/274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild/02_runs/run274D/handoff`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
