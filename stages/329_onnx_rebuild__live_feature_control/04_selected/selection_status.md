# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- source_feature_frame_queue(원천 피처 프레임 대기열): `core56_no_top3_weight_features, macro48_no_equity_breadth_or_top3, us100_technical42_no_external`
- research_onnx_status(연구 온엑스 상태): `exported_with_onnxruntime_parity_not_runtime_handoff`
- forward_replay_queue(전진 재생 대기열): `core56_no_top3_weight_features__l2_balanced_c025, core56_no_top3_weight_features__l2_plain_c025, macro48_no_equity_breadth_or_top3__l2_balanced_c025, macro48_no_equity_breadth_or_top3__l2_plain_c025, us100_technical42_no_external__l2_balanced_c025, us100_technical42_no_external__l2_plain_c025`
- forward_dataset_status(전진 데이터셋 상태): `feature_frames_materialized_with_session_boundary`
- common_valid_boundary(공통 유효 경계): `2026-05-22T23:00:00+00:00`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run329D_forward_holdout_score_replay_without_threshold_retuning`
- effect(효과): old train/validation/OOS(기존 학습/검증/표본외)에서만 후보를 걸렀고, forward holdout(전진 보류 표본)은 다음 실행의 judgment-only replay(판정 전용 재생)에 남긴다.
