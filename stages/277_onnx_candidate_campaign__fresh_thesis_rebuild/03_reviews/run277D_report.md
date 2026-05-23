# run277D Report(277D 보고서): Fresh Thesis Scoring Probe(새 논제 점수 탐침)

- run_id(실행 ID): `run277D_execute_fresh_thesis_scoring_probe_v1`
- stage_id(단계 ID): `277_onnx_candidate_campaign__fresh_thesis_rebuild`
- source_run(원천 실행): `run277C_materialize_fresh_thesis_scoring_handoff_inputs_v1`
- status(상태): `completed_fresh_thesis_scoring_probe_no_candidate_selection`
- judgment(판정): `fresh_thesis_score_tables_materialized_no_candidate_selection`
- package_rows(패키지 행): `4`
- summary_rows(요약 행): `36`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run277E_screen_fresh_thesis_score_surfaces`

## OOS Combined Read(표본외 합산 판독)

- `cp277A_session_loss_avoidance_surface` combined OOS(합산 표본외): decision_rate(판단 비율) `0.3051`, mean_score(평균 점수) `0.2657`
- `cp277B_validation_pf_floor_rebalanced_entry_surface` combined OOS(합산 표본외): decision_rate(판단 비율) `0.3903`, mean_score(평균 점수) `0.2921`
- `cp277C_directional_asymmetry_reversal_surface` combined OOS(합산 표본외): decision_rate(판단 비율) `0.2786`, mean_score(평균 점수) `0.5751`
- `cp277D_macro_squeeze_failure_contrast_surface` combined OOS(합산 표본외): decision_rate(판단 비율) `0.3116`, mean_score(평균 점수) `0.5312`

## Boundary(경계)

run277D(277D 실행)는 score table(점수표)와 handoff JSON(인계 JSON)을 만들었다.
Effect(효과): 다음 run277E(277E 실행)에서 score surface(점수 표면)를 선별할 수 있지만, selected candidate(선택 후보), MT5 runtime result(MT5 런타임 결과), ONNX readiness(온엑스 준비)는 아직 없다.
