# run329D Forward Holdout Score Replay(329D 전진 보류 점수 재생)

- run_id(실행 ID): `run329D_forward_holdout_score_replay_without_threshold_retuning_v1`
- status(상태): `completed_forward_holdout_score_replay_without_threshold_retuning`
- judgment(판정): `forward_score_replay_completed_session_parity_warning_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Scope(범위)

run329D(329D 실행)는 run329C(329C 실행)의 ONNX(온엑스), sklearn model(사이킷런 모델), fixed threshold(고정 임계값)를 그대로 사용했다. Forward label(전진 라벨), profit(수익), MT5 tester(MT5 테스터), threshold retuning(임계값 재튜닝)은 만들지 않았다.

Effect(효과): 새 데이터에서 score supply(점수 공급), signal density(신호 밀도), side attribution(방향 기여), session parity(세션 동등성), ONNX parity(온엑스 동등성)만 확인한다.

## Session Parity View(세션 동등 보기)

| candidate(후보) | rows/day(일 행수) | signals/day(일 신호) | OOS signals/day(OOS 일 신호) | ratio(비율) | long share(롱 비중) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---|
| core56_no_top3_weight_features__l2_balanced_c025 | 61.69 | 14.52 | 19.01 | 0.764 | 0.615 | session_parity_signal_supply_within_predeclared_band |
| core56_no_top3_weight_features__l2_plain_c025 | 61.69 | 16.28 | 20.05 | 0.812 | 0.831 | session_parity_signal_supply_within_predeclared_band |
| macro48_no_equity_breadth_or_top3__l2_balanced_c025 | 61.69 | 14.21 | 18.89 | 0.752 | 0.595 | session_parity_signal_supply_within_predeclared_band |
| macro48_no_equity_breadth_or_top3__l2_plain_c025 | 61.69 | 15.79 | 19.94 | 0.792 | 0.832 | session_parity_signal_supply_within_predeclared_band |
| us100_technical42_no_external__l2_balanced_c025 | 66.00 | 13.83 | 18.76 | 0.737 | 0.559 | session_parity_signal_supply_within_predeclared_band |
| us100_technical42_no_external__l2_plain_c025 | 66.00 | 15.97 | 19.70 | 0.810 | 0.810 | session_parity_signal_supply_within_predeclared_band |

## Raw Forward Warning(원본 전진 경고)

- raw_warning_count(원본 경고 수): `4`
- session_supply_ok_count(세션 공급 통과 수): `6`
- effect(효과): raw_forward(원본 전진)는 macro48/us100-only에서 기존 OOS(표본외)보다 rows/day(일 행수)가 크게 많아 직접 비교하면 안 된다. old_session_parity(기존 세션 동등) view(보기)가 비교 가능한 진단 기준이다.

## Boundary(경계)

`research_development_only_forward_score_replay_no_label_no_profit_no_mt5_runtime_no_threshold_retuning_no_selected_candidate_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_or_block`
