# run275D Fresh Candidate Score Surface Materialization(275D 새 후보 점수 표면 물질화)

- run_id(실행 ID): `run275D_execute_fresh_candidate_scoring_materialization_probe_v1`
- source_run(원천 실행): `run275C_materialize_fresh_candidate_scoring_handoff_inputs_v1`
- status(상태): `completed_fresh_candidate_score_surface_materialization_no_candidate_selection`
- judgment(판정): `fresh_candidate_score_surfaces_materialized_no_candidate_selection`
- packages(패키지): `5`
- selectable_packages(선택 가능 패키지): `4`
- support_controls(보조 대조): `1`
- score_tables(점수표): `5`
- handoff_json(인계 JSON): `5`
- summary_rows(요약 행): `15`
- split_rows(분할 행): `45`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run275E_screen_fresh_candidate_score_surfaces`

## Plain Result(쉬운 결과)

run275D(275D 실행)는 run275C(275C 실행)의 package specs(패키지 규격)를 Tier A/Tier B model input dataset(티어 A/B 모델 입력 데이터셋)에 적용했다.
효과(effect, 효과): selectable seed(선택 가능 씨앗)와 support control(보조 대조)를 모두 score table(점수표)과 handoff JSON(인계 JSON)으로 만들었고, 아직 후보 선택이나 ONNX 준비를 주장하지 않는다.

## Tier Records(티어 기록)

- Tier A separate: rows(행) `46650`, missing_required_features(필수 누락 피처) `none`
- Tier B separate: rows(행) `46650`, missing_required_features(필수 누락 피처) `top3_weighted_return_1;us100_minus_top3_weighted_return_1`
- Tier A+B combined: rows(행) `93300`, missing_required_features(필수 누락 피처) `see_component_rows`

## Combined Score Surface Summary(합산 점수 표면 요약)

- `cp275A_volatility_pullback_breakout_surface`: active_signal_rate(활성 신호율) `0.35275456`, long/short(매수/매도) `12752/20160`, score_table(점수표) `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/s/cp275A.parquet`
- `cp275B_cross_asset_divergence_reversal_surface`: active_signal_rate(활성 신호율) `0.32580922`, long/short(매수/매도) `11946/18452`, score_table(점수표) `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/s/cp275B.parquet`
- `cp275C_cash_session_impulse_continuation_surface`: active_signal_rate(활성 신호율) `0.11232583`, long/short(매수/매도) `9060/1420`, score_table(점수표) `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/s/cp275C.parquet`
- `cp275D_macro_volatility_squeeze_release_surface`: active_signal_rate(활성 신호율) `0.36441586`, long/short(매수/매도) `16082/17918`, score_table(점수표) `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/s/cp275D.parquet`
- `cp275E_q04_stage274_failure_signature_guard`: active_signal_rate(활성 신호율) `0.42855305`, long/short(매수/매도) `16374/23610`, score_table(점수표) `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/s/cp275E.parquet`

## Evidence Paths(근거 경로)

- summary(요약): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/summary.csv`
- split_summary(분할 요약): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/split.csv`
- normalization_receipt(정규화 영수증): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/norm.json`
- tier_receipt(티어 영수증): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/tier.csv`
- data_integrity_receipt(데이터 무결성 영수증): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/data.json`
- model_validation_receipt(모델 검증 영수증): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/model.json`
- lineage(계보): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275D/lineage.json`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
