# Stage363 Brief(363단계 개요): Lower-Floor Rank Surface(낮은 하한 순위 표면)

- canonical_stage_id(정식 단계 ID): `363_lower_floor_rank_surface__q05_long_density_recovery`
- current_run_id(현재 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run363B_materialize_q05_lower_floor_rank_surface_without_db_v1`
- source_stage_id(원천 단계 ID): `362_long_only_margin_grid__cost_buffer_first_branch`
- source_run_id(원천 실행 ID): `run362C_review_q05_long_only_margin_grid_without_db_v1`
- selection_status(선택 상태): `materialized_review_required_no_selection(구체화 완료, 검토 필요, 선택 없음)`
- claim_boundary(주장 경계): `research_development_materialization_only_q05_lower_floor_rank_surface_report_derived_validation_thresholds_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Can lower p_long floor and validation-derived rank/quantile surface(낮은 p_long 하한 및 검증 파생 순위/분위수 표면) recover +0.30 cost buffer(+0.30 비용 버퍼) without density collapse(밀도 붕괴 없이 회복할 수 있는가)?

## Source Truth(원천 진실)

- source_failure(원천 실패): Stage362B margin-only filter(362B 마진 단독 필터)는 passing_cross_split_rows(교차 분할 통과 행) `0`.
- preserved_clue(보존 단서): margin_q20 near miss(q20 마진 근접 실패)는 validation loss(검증 손실)를 크게 줄였지만 아직 cost positive(비용 양수)가 아니다.
- no_selection_boundary(선택 없음 경계): candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격) 없음.

## Scope(범위)

Action(행동): Stage363(363단계)는 Stage362C(362C 실행)의 design queue(설계 대기열)만 먼저 구체화한다.

Effect(효과): regime/label/router(국면/라벨/라우터)를 아직 붙이지 않고 lower-floor/rank(낮은 하한/순위) 질문만 작게 확인한다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST363-Q05-LOWER-FLOOR-RANK-SURFACE`
- hypothesis(가설): absolute p_long floor(절대 p_long 하한)를 낮추고 validation-derived rank(검증 파생 순위)를 쓰면 density(밀도)를 보존하면서 cost drag(비용 끌림)를 줄일 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): lower p_long floor(낮은 p_long 하한), margin rank(마진 순위), long-short rank(롱-숏 순위), target density boundary(목표 밀도 경계)
- extreme_sweep(극단 탐색): all-long dense control(전체 롱 고밀도 대조), sparse upper bound(희소 상한), hour attribution only(시간 귀속 전용)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): Stage363B(363B 실행)가 positive scout(긍정 탐색)를 만들 때만 WFO(walk-forward optimization, 워크포워드 최적화)로 강화한다.
- failure_memory(실패 기억): Stage362C(362C 실행)는 p_long_floor>=0.40 margin-only tightening(마진 단독 조임)을 반복 금지로 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## run363B Materialization Closeout(363B 구체화 종료)

Action(행동): lower-floor/rank surface(낮은 하한/순위 표면) `90`개 cross-split row(교차 분할 행)를 구체화했다.

Effect(효과): validation/OOS(검증/표본외) +0.30 cost positive(비용 양수)와 density >= 3(밀도 3 이상)를 동시에 통과한 행은 `0`개이며, 다음 작업은 `run363C_review_q05_lower_floor_rank_surface_without_db_v1` 검토다.
