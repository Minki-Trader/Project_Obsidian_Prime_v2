# Stage364 Brief(364단계 개요): Source Regime Label Pivot(원천 국면 라벨 전환)

- canonical_stage_id(정식 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run_id(현재 실행 ID): `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run364E_train_timestamp_context_cost_filter_model_without_db_v1`
- source_stage_id(원천 단계 ID): `363_lower_floor_rank_surface__q05_long_density_recovery`
- source_run_id(원천 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- selection_status(선택 상태): `model_trained_onnx_exported_runtime_probe_opened_no_operating_claim(모델 학습 및 ONNX 내보내기 완료, 런타임 탐침 열림, 운영 주장 없음)`
- claim_boundary(주장 경계): `research_development_model_training_and_onnx_export_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Can timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥) recover q05 dense cost(고밀도 q05 비용 회복) while keeping trade density >= 3/day(거래 밀도 일 3회 이상 유지)를 달성할 수 있는가?

## Source Truth(원천 진실)

- source_failure(원천 실패): Stage363B(363B 실행)는 passing_cross_split_rows(교차 분할 통과 행) `0`.
- preserved_clue(보존 단서): sparse cost-positive variants(희소 비용 양수 변형)와 open-hour clue(진입 시간 단서)는 남았다.
- no_selection_boundary(선택 없음 경계): candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격) 없음.

## Scope(범위)

Action(행동): Stage364(364단계)는 Stage363C(363C 실행)의 design queue(설계 대기열)를 작게 구체화한다.

Effect(효과): 같은 threshold micro-tuning(임계값 미세조정)을 반복하지 않고, 진입 시점에 알려진 context(문맥)와 label/source pivot(라벨/원천 전환)을 분리해 판단한다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY`
- hypothesis(가설): timestamp-safe context/regime/label source pivot(시점 안전 문맥/국면/라벨 원천 전환)이 dense trade count(고밀도 거래수)를 유지하며 cost drag(비용 끌림)를 줄인다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): open hour(진입 시간), day/hour(요일/시간), closed-bar regime(닫힌 봉 국면), label source(라벨 원천), sparse clue expansion(희소 단서 확장)
- extreme_sweep(극단 탐색): dense all-long control(전체 롱 고밀도 대조), no-context probability control(무문맥 확률 대조)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): Stage364B(364B 실행)가 positive scout(긍정 탐색)를 만들 때만 WFO(walk-forward optimization, 워크포워드 최적화)로 강화한다.
- failure_memory(실패 기억): Stage363C(363C 실행)는 lower-floor/rank threshold micro-tuning(낮은 하한/순위 임계값 미세조정)을 반복 금지로 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## run364B Materialization Closeout(364B 구체화 종료)

Action(행동): timestamp-safe context cost surface(시점 안전 문맥 비용 표면)를 `183`개 cross-split row(교차 분할 행)로 구체화했다.

Effect(효과): passing_cross_split_rows(교차 분할 통과 행)는 `33`개이고, 다음 작업은 `run364C_review_timestamp_context_cost_surface_without_db_v1` 검토다.

## run364C Review Closeout(364C 검토 종료)

Action(행동): timestamp context pass rows(시점 문맥 통과 행) `33`개를 monthly stability(월별 안정성)와 family attribution(계열 귀속)으로 검토했다.

Effect(효과): best seed(최선 씨앗)는 `s364_r02_drop_worst_open_hour_minute_bucket15_k2`이지만, candidate selection(후보 선택) 없이 `run364D_materialize_timestamp_context_training_seed_without_db_v1`로 넘긴다.

## run364D Training Seed Closeout(364D 학습 씨앗 종료)

Action(행동): timestamp-safe feature/label seed table(시점 안전 피처/라벨 씨앗 표) `1114`행을 만들었다.

Effect(효과): 다음 작업은 `run364E_train_timestamp_context_cost_filter_model_without_db_v1`에서 model training(모델 학습)과 ONNX precheck(ONNX 사전 점검)를 시작한다.

## run364E Model Training Closeout(364E 모델 학습 종료)

Action(행동): cost-filter model(비용 필터 모델)을 학습하고 ONNX smoke(ONNX 스모크)를 `3/4` 통과시켰다.

Effect(효과): best ONNX model(최선 ONNX 모델)은 `rf_depth3_balanced`이고 다음 작업은 `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`다.
