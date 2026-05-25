# run329A Live Feature Rebuild Control Design(329A 실시간 피처 재구축 대조 설계)

- run_id(실행 ID): `run329A_design_live_feature_rebuild_control_after_cp322a_block_v1`
- status(상태): `completed_live_feature_rebuild_control_design_ready_for_materialization`
- judgment(판정): `research_rebuild_control_open_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Why this stage exists(이 단계가 필요한 이유)

Stage328B(328B 단계 실행)는 cp318A(318A 후보)가 Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류)이라고 판정했다. 따라서 cp322A(322A 후보)를 forward(전진)에 억지로 통과시키는 대신, raw/live-computable feature(원천/실시간 계산 가능 피처)만 쓰는 rebuild-control(재구축 대조)을 새 단계로 연다.

## Data Readiness(데이터 준비도)

- forward_raw_requested(전진 원천 요청): `2026-04-14T00:00:00Z` to `2026-05-25T21:05:00Z`
- core58_common_ready_end(핵심58 공통 준비 종료): `2026-05-22T23:00:00Z`
- macro48_common_ready_end(거시48 공통 준비 종료): `2026-05-25T18:30:00Z`
- top3_weight_month_coverage(상위3 가중치 월 범위): `2022-08` to `2026-04`

Effect(효과): forward raw data(전진 원천 데이터)는 존재하지만, core58(핵심58)은 2026-05 top3 weight contract(상위3 가중치 계약)과 equity session calendar(주식 세션 달력) 경계가 필요하다. 그래서 core56(상위3 제외)와 macro48(거시 전용)을 먼저 materialization control(물질화 대조)로 둔다.

## Feature Set Queue(피처 세트 대기열)

| feature_set(피처 세트) | count(수) | status(상태) | reason(이유) |
|---|---:|---|---|
| core56_no_top3_weight_features | 56 | preferred_first_materialization_control | May top3 weight(5월 상위3 가중치) 문제를 피한다. |
| macro48_no_equity_breadth_or_top3 | 48 | parallel_resilience_control | 주식 바스켓 의존성을 줄인다. |
| us100_technical42_no_external | 42 | minimal_parity_control | Python/MT5 parity(파이썬/MT5 동등성) 격리 대조다. |
| core58_full_contract | 58 | blocked | 2026-05 top3 weight contract(상위3 가중치 계약)이 없다. |

## Decision(결정)

Stage329(329단계)는 candidate selection(후보 선택)이 아니라 rebuild-control materialization(재구축 대조 물질화)로 열린다. 다음 실행은 `run329B_parameterize_forward_feature_materializer_and_build_live_feature_frames`이다.

`research_development_only_no_new_data_tuning_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
