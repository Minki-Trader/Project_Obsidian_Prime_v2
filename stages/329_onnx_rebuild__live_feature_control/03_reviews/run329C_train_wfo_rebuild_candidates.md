# run329C Train/WFO Rebuild Candidates(329C 학습/워크포워드 재구축 후보)

- run_id(실행 ID): `run329C_train_wfo_rebuild_candidates_v1`
- status(상태): `completed_train_wfo_rebuild_candidates_no_forward_tuning`
- judgment(판정): `research_wfo_candidates_ready_for_forward_replay_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Scope(범위)

run329C(329C 실행)는 forward holdout(전진 보류 표본)을 읽지 않고 기존 train/validation/OOS(학습/검증/표본외)만 사용했다. 모델군(model family, 모델군)은 LogisticRegression(로지스틱 회귀)로 고정했고, threshold(임계값)는 train-only q60 nonflat margin(학습 전용 비관망 마진 60 분위)로 고정했다.

Effect(효과): cp322A(322A 후보)의 outcome-distilled signal(결과 증류 신호)을 쓰지 않고도 live-computable feature(실시간 계산 가능 피처)에서 학습 가능한지 보는 압박 시험이다.

## Candidate Screen(후보 선별표)

| candidate(후보) | val BA(검증 균형정확도) | OOS BA(표본외 균형정확도) | WFO min(WFO 최소) | ONNX(온엑스) | queue(대기열) |
|---|---:|---:|---:|---|---|
| core56_no_top3_weight_features__l2_balanced_c025 | 0.4313 | 0.4385 | 0.3837 | True | forward_replay_queue_not_selected_candidate |
| core56_no_top3_weight_features__l2_plain_c025 | 0.4403 | 0.4435 | 0.3947 | True | forward_replay_queue_not_selected_candidate |
| macro48_no_equity_breadth_or_top3__l2_balanced_c025 | 0.4327 | 0.4376 | 0.3886 | True | forward_replay_queue_not_selected_candidate |
| macro48_no_equity_breadth_or_top3__l2_plain_c025 | 0.4377 | 0.4435 | 0.3944 | True | forward_replay_queue_not_selected_candidate |
| us100_technical42_no_external__l2_balanced_c025 | 0.4343 | 0.4541 | 0.3877 | True | forward_replay_queue_not_selected_candidate |
| us100_technical42_no_external__l2_plain_c025 | 0.4400 | 0.4482 | 0.3889 | True | forward_replay_queue_not_selected_candidate |

## Forward Replay Queue(전진 재생 대기열)

`core56_no_top3_weight_features__l2_balanced_c025, core56_no_top3_weight_features__l2_plain_c025, macro48_no_equity_breadth_or_top3__l2_balanced_c025, macro48_no_equity_breadth_or_top3__l2_plain_c025, us100_technical42_no_external__l2_balanced_c025, us100_technical42_no_external__l2_plain_c025`

## Boundary(경계)

ONNX export/parity(온엑스 내보내기/동등성)는 통과 여부를 기록했지만, MT5 runtime handoff(MT5 런타임 인계), risk logic(위험 로직), lot logic(랏 로직), operating promotion(운영 승격)은 없다. 다음 실행에서 fixed threshold(고정 임계값) 그대로 forward feature frame(전진 피처 프레임)에 점수만 매긴다.

`research_development_only_old_train_validation_oos_used_no_forward_tuning_research_onnx_exports_not_runtime_handoff_no_selected_candidate_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`run329D_forward_holdout_score_replay_without_threshold_retuning`
