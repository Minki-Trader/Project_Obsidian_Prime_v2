# run329B Forward Feature Frame Materialization(329B 전진 피처 프레임 물질화)

- run_id(실행 ID): `run329B_materialize_forward_live_feature_frames_v1`
- status(상태): `completed_forward_feature_frames_materialized_with_session_boundary`
- judgment(판정): `research_materialization_completed_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## What changed(무엇이 바뀌었나)

Stage329A(329A 단계 실행)의 queue(대기열)를 실제 feature frame(피처 프레임)으로 만들었다. Foundation feature calculator(기반 피처 계산기)는 그대로 쓰고, Stage329B(329B 단계 실행) wrapper(래퍼)가 historical preload(기존 선적재)와 forward raw(전진 원천)를 붙였다.

Effect(효과): rolling window(롤링 창)는 기존 데이터로 연속성을 얻지만, 출력 행은 forward output start(전진 출력 시작) 이후로만 제한된다. Label(라벨), score threshold(점수 임계값), cp322A signal(322A 신호)은 만들거나 조정하지 않았다.

## Materialized Frames(물질화된 프레임)

| feature_set(피처 세트) | features(피처 수) | valid_rows(유효 행) | first_valid(첫 유효) | last_valid(마지막 유효) | status(상태) |
|---|---:|---:|---|---|---|
| core56_no_top3_weight_features | 56 | 2070 | 2026-04-14T16:35:00+00:00 | 2026-05-22T23:00:00+00:00 | materialized |
| macro48_no_equity_breadth_or_top3 | 48 | 5484 | 2026-04-14T03:05:00+00:00 | 2026-05-22T23:55:00+00:00 | materialized |
| us100_technical42_no_external | 42 | 7649 | 2026-04-14T01:05:00+00:00 | 2026-05-23T00:00:00+00:00 | materialized |

## Boundary(경계)

2026-05-25 row(행)는 raw data(원천 데이터)가 있어도 session feature(세션 피처)와 cash-session boundary(현물장 세션 경계) 때문에 유효 feature row(유효 피처 행)로는 끝까지 이어지지 않는다. 이것은 pass/fail(통과/실패)이 아니라 다음 train/WFO rebuild(학습/워크포워드 재구축) 전에 보존해야 하는 data boundary(데이터 경계)다.

`research_development_only_forward_features_materialized_no_labels_no_threshold_tuning_no_candidate_selected_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`run329C_train_wfo_rebuild_candidates_without_forward_tuning`
