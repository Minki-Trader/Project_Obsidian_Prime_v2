# Stage 347 Brief(347단계 개요)

## Stage ID(단계 ID)

`347_cash_open_asymmetric_source__long_short_head_design`

## Question(질문)

Can the cash-open runtime clue(현금장 런타임 단서)를 asymmetric long/short model-source design(비대칭 롱/숏 모델-원천 설계)으로 바꿔, short carry(숏 기여)를 보존하면서 long quality supply(롱 품질 공급)를 늘릴 수 있는가?

## Source Inputs(원천 입력)

- review_run(검토 실행): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- source_runtime_probe(원천 런타임 탐침): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- seed_queue(씨앗 대기열): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346B/stage347_asymmetric_source_seed_queue.csv`
- positive_clues(긍정 단서): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346B/positive_clues.csv`
- failure_memory(실패 기억): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346B/failure_memory.csv`

## Scope(범위)

Stage347(347단계)는 design/materialization(설계/물질화)부터 시작한다. Single side-filter micro-tuning(단일 방향 필터 미세조정)은 중심 주제가 아니다.

## Claim Boundary(주장 경계)

No candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.

## run347A Design Packet(347A 설계 묶음)

- run_id(실행 ID): `run347A_design_cash_open_asymmetric_long_short_source_without_db_v1`
- decision(결정): `stage347A_open_run347B_materialize_cash_open_asymmetric_source_inputs`
- design_rows(설계 행): `3`
- next_run(다음 실행): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`
- effect(효과): long-quality/short-carry(롱 품질/숏 기여)를 separate heads(분리 헤드)와 allocator(배분기)로 설계한다.

## run347B Input Materialization(347B 입력 물질화)

- run_id(실행 ID): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`
- decision(결정): `stage347B_open_run347C_train_cash_open_asymmetric_source_proxy_models`
- materialized_rows(물질화 행): `5827`
- proxy_grid_rows(프록시 격자 행): `225`
- next_run(다음 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- effect(효과): Stage347(347단계)의 설계를 학습/프록시 선별 입력으로 바꿨다.

## run347C Proxy Training(347C 프록시 학습)

- run_id(실행 ID): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- decision(결정): `stage347C_open_run347D_review_cash_open_asymmetric_source_proxy_training`
- trained_model_artifacts(학습 모델 산출물): `9`
- onnx_smoke_passes(온엑스 점검 통과): `2`
- next_run(다음 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- effect(효과): Stage347(347단계)의 설계/물질화 결과를 proxy model review(프록시 모델 검토)로 넘긴다.

## run348A Proxy Review Branch(348A 프록시 검토 분기)

- branch_run(분기 실행): `run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1`
- next_stage(다음 단계): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage`
- next_run(다음 실행): `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- action(행동): run347D review(347D 검토)를 Stage348(348단계)로 넘겼다.
- effect(효과): Stage347(347단계)은 설계/물질화/학습 산출물까지만 보존하고, 검토 무게는 새 stage(단계)로 분리한다.
