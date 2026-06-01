# Stage356 Density Recovery Training(356단계 밀도 회복 학습)

- canonical_stage_id(정식 단계 ID): `356_density_recovery_training__proxy_model_queue_scout`
- current_run_id(현재 실행 ID): `run356B_train_density_recovery_proxy_models_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1`
- source_stage_id(원천 단계 ID): `355_density_recovery_model_family__new_label_source_probe`
- source_run_id(원천 실행 ID): `run355B_materialize_density_recovery_label_inputs_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run355C_train_density_recovery_proxy_models_without_db_v1`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_proxy_training_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Stage355B(355B 실행)에서 만든 timestamp-safe label variants(시점 안전 라벨 변형) 4개가 proxy model training(프록시 모델 학습)에서 trade/day(일별 거래수) 3+와 net/PF/stress(순수익/수익 팩터/압박)를 동시에 회복하는 후보 대기열(candidate queue, 후보 대기열)을 만들 수 있는가?

## Source Truth(원천 진실)

- feature_rows(피처 행): `46650`
- raw_rows(원시 행): `261345`
- label_table_rows(라벨 표 행): `186600`
- label_variant_count(라벨 변형 수): `4`
- training_queue_rows(학습 대기열 행): `4`
- distribution_rows(분포 행): `12`
- source_gates(원천 게이트): `12/12`
- label_variant_ids(라벨 변형 ID): `d01_h6_cost_buffer, d01_h8_cost_buffer, d02_tb12_path_quality, d03_h6_dual_head_allocator`

## Scope(범위)

Stage356(356단계)는 proxy model training(프록시 모델 학습), non-overlap proxy evaluation(비중첩 프록시 평가), candidate queue triage(후보 대기열 선별)까지만 다룬다. MT5 runtime probe(MT5 런타임 탐침)와 ONNX handoff(온엑스 인계)는 positive queue(긍정 대기열)가 생긴 뒤 별도 stage/run(단계/실행)에서 다룬다.

## Exploration Plan(탐색 계획)

- idea_id(아이디어 ID): `IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING`
- hypothesis(가설): cost-buffer/path-quality/dual-head labels(비용 완충/경로 품질/이중 헤드 라벨)이 기존 surface(표면)보다 trade density(거래 밀도)를 유지하면서 stress net(압박 순수익)을 회복한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): logreg/MLP/tree fallback(로지스틱/MLP/트리 대체), threshold(임계값), margin(마진), ADX/session filter(ADX/세션 필터)
- extreme_sweep(극단 탐색): very-low threshold(매우 낮은 임계값), high margin(높은 마진), short horizon hold(짧은 보유기간), stress cost(압박 비용)
- micro_search_gate(미세 탐색 게이트): validation/OOS proxy trade/day(검증/OOS 프록시 일별 거래수) 3+와 stress net(압박 순수익) 양수
- wfo_plan(WFO 계획): scout pass(탐색 회차) 뒤 WFO(walk-forward optimization, 워크포워드 최적화) 프레임으로 재검증
- failure_memory(실패 기억): density(밀도)만 좋거나 stress net(압박 순수익)이 깨지면 label/model clue(라벨/모델 단서)만 보존하고 selection(선정)은 금지
- evidence_boundary(근거 경계): `scout-only(탐색 전용)`

## Density Constraint(밀도 제약)

`trade_per_day_min_3_to_10_plus_no_trade_splitting`

Action(행동): trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3~10+ 조건을 유지한다.

Effect(효과): 낮은 거래수로 예쁜 net profit(순수익)을 만든 후보가 운영 후보처럼 보이지 않게 한다.
