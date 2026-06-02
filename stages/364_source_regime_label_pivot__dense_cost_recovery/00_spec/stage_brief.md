# Stage364 Brief(364단계 개요): Source Regime Label Pivot(원천 국면 라벨 전환)

- canonical_stage_id(정식 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run_id(현재 실행 ID): `run364U_materialize_density_side_balance_repair_inputs_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`
- source_stage_id(원천 단계 ID): `363_lower_floor_rank_surface__q05_long_density_recovery`
- source_run_id(원천 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- selection_status(선택 상태): `runtime_positive_density_side_balance_repair_required_no_operating_claim(런타임 양수, 밀도/방향 균형 수리 필요, 운영 주장 없음)`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

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

## run364F Runtime Probe Package Closeout(364F 런타임 탐침 패키지 종료)

Action(행동): feature_rows(피처 행) `1114`개와 expected tape(예상 테이프) `1114`개를 Common Files(공용 파일)에 동기화했다.

Effect(효과): 다음 단계 분기 없이 같은 Stage364(364단계)에서 `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`로 외부 검증을 이어간다.

## run364H MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- judgment(판정): `valid_negative_mt5_kpi_overlap_parity_positive_clue_sparse_runtime_tape_trade_shape_failure_no_authority`
- effect(효과): sparse runtime tape(희소 런타임 테이프) 실패를 다음 dense source/runtime exit repair(고밀도 원천/런타임 청산 수리)로 넘긴다.

## run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

Action(행동): q05 dense runtime cycles(q05 고밀도 런타임 사이클) `17428`개에 run364E ONNX cost filter(ONNX 비용 필터)를 적용하고 calendar exit proxy(캘린더 청산 프록시)를 탐색했다.

Effect(효과): sparse expected tape(희소 예상 테이프) 실패는 수리 가능하지만, strict cross-split success(엄격 교차 분할 성공)가 `0`개라 `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`로 직접 고밀도 모델 탐색을 연다.

## run364J Direct Dense M5 ONNX Scout Closeout(364J 직접 고밀도 5분봉 온엑스 탐색 종료)

Action(행동): all58/runtime_core feature set(전체58/런타임 핵심 피처셋)과 direct return label(직접 수익 라벨)을 학습했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `0`이고, 다음 실행은 `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`이다.

## run364K Direct Dense M5 ONNX Scout Review Closeout(364K 직접 고밀도 5분봉 온엑스 탐색 검토 종료)

Action(행동): run364J(364J 실행)의 192개 threshold row(임계값 행)를 review class(검토 분류)로 나눴다.

Effect(효과): strict_candidate_rows(엄격 후보 행)는 `0`이고, 다음 실행은 `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`이다.

## run364L Density Lift Trade Shape ONNX Scout Closeout(364L 밀도 상향 거래 형태 온엑스 탐색 종료)

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)로 3/day+(일 3회 이상) proxy candidate(프록시 후보)를 탐색했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `5`이고, 다음 실행은 `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`이다.

## run364N MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- external_verification_status(외부 검증 상태): `completed(완료)`
- matched_rows(일치 수): `17428`
- mismatch_rows(불일치 수): `0`
- effect(효과): 실제 MT5 실행 결과 또는 blocker(차단 사유)를 다음 review/repair(검토/수리)로 넘긴다.

## run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1

- action(행동): `run364N` MT5 runtime probe(MT5 런타임 탐침)를 KPI/performance attribution(KPI/성과 귀속)으로 review(검토)했다.
- effect(효과): positive net profit(양수 순수익) 단서는 유지하고, drawdown/long-only/hold tail(낙폭/롱 전용/보유 꼬리)을 다음 공격 탐색 입력으로 바꿨다.
- next(다음): `run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`

## run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1

- action(행동): run364O(364O 실행)의 MT5 review(MT5 검토)를 trade lifecycle/risk/side-balance inputs(거래 생명주기/위험/방향 균형 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `run364Q`에서 risk overlay(위험 오버레이), calendar hold cap(달력 보유 상한), short-side router(숏 방향 라우터)를 바로 탐색할 수 있다.
- next(다음): `run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`

## run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1

- action(행동): risk overlay ONNX scout(위험 오버레이 온엑스 탐색), hold cap proxy(보유 상한 프록시), short router proxy(숏 라우터 프록시)를 실행했다.
- effect(효과): run364O(364O 실행)의 positive clue(긍정 단서)를 다음 runtime package(런타임 패키지) 후보로 좁혔다.
- next(다음): `run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1`

## run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1

- action(행동): ADX side filter(ADX 방향 필터) MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.
- effect(효과): OOS expected net(표본외 예상 순수익) `403.359`와 trade density(거래 밀도) `3.4833333333`인 실행 가능 후보를 다음 MT5 실행으로 넘긴다.
- next(다음): `run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`

## run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1

- action(행동): `run364S` ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 review(검토)했다.
- effect(효과): net/PF/DD(순수익/수익 팩터/낙폭) 개선 단서는 보존하고, density floor(거래 밀도 하한)와 long-only(롱 전용) 실패를 `run364U` 입력으로 바꿨다.
- next(다음): `run364U_materialize_density_side_balance_repair_inputs_without_db_v1`
