# Stage364 Brief(364단계 개요): Source Regime Label Pivot(원천 국면 라벨 전환)

- canonical_stage_id(정식 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run_id(현재 실행 ID): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- source_stage_id(원천 단계 ID): `363_lower_floor_rank_surface__q05_long_density_recovery`
- source_run_id(원천 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- selection_status(선택 상태): `completed_stage364HR_trade_quality_density_repair_scout_no_strict_joint_pass_review_required_no_authority`
- claim_boundary(주장 경계): `research_development_proxy_replay_scout_only_single_source_probability_bin_veto_trade_quality_density_repair_no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

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

## run364U_materialize_density_side_balance_repair_inputs_without_db_v1

- action(행동): run364T(실행 364T)의 density failure(밀도 실패)와 long-only failure(롱 전용 실패)를 ADX/hold/short/session repair inputs(ADX/보유/숏/세션 수리 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `run364V_train_density_side_balance_repair_onnx_scout_without_db_v1`에서 density repair(밀도 수리)와 side-balance(방향 균형)를 바로 scout(탐색)할 수 있다.
- best repair(최선 수리): `adx_block_min_40_0__maxhold_6` validation/combined density(검증/합산 밀도) `3.1701030928` / `3.3843843844`.

## run364V_train_density_side_balance_repair_onnx_scout_without_db_v1

- action(행동): existing ONNX probabilities(기존 온엑스 확률)에 short threshold(숏 임계값)와 ADX/maxhold(ADX/최대보유)를 조합한 dual-side runtime surface(양방향 런타임 표면)를 만들었다.
- effect(효과): `dual_pshort_0_45__adx_block_40_0__maxhold_8`가 validation/combined density(검증/합산 밀도) `3.0721649485` / `3.2462462462`와 long/short(롱/숏) `952` / `129`를 보여 다음 MT5 package(MT5 패키지) 후보가 됐다.
- next(다음): `run364W_package_density_side_balance_repair_runtime_probe_without_db_v1`

## run364W density side-balance runtime package(밀도 방향 균형 런타임 패키지)

- current truth(현재 진실): selected dual-side candidate(선택 양방향 후보)를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run364X Strategy Tester(전략 테스터) 실행 준비가 됐다.

## run364X MT5 runtime probe(MT5 런타임 탐침)

- current truth(현재 진실): run364W package(패키지)를 Strategy Tester(전략 테스터)로 실행 시도했다.
- effect(효과): proxy-vs-MT5 diff(프록시-MT5 차이) review(검토) 입력을 만들었다.

## run364Y MT5 runtime review(MT5 런타임 검토)

- current truth(현재 진실): density/side repair(밀도/방향 수리)가 MT5에서 positive(긍정)였지만 cost/session stress(비용/세션 압박)가 남았다.

## run364AI Session/Side PF Lift Density Repair Inputs Closeout(364AI 세션/방향 PF 상승 밀도 수리 입력 종료)

Action(행동): run364AH(364AH 실행)의 세션/방향 단서를 `12`개 고정 규칙 대기열로 구체화했다.

Effect(효과): 다음 실행은 `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`이고, top_n(상위 N개 자르기)과 trade splitting(거래 쪼개기)은 금지 상태로 남긴다.

## run364AJ Session/Side PF Lift Density Repair Scout Closeout(364AJ 세션/방향 PF 상승 밀도 수리 정찰 종료)

Action(행동): run364AI(364AI 실행) queue(대기열) `12`개를 timestamp-safe session/side proxy replay(시점 안전 세션/방향 프록시 재생)로 실행했다.

Effect(효과): `selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8`를 `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1` review(검토) 대상으로 넘기며, operating claim(운영 주장)은 없다.

## run364AK Session-Side PF Lift Density Repair Review Closeout(364AK 세션/방향 PF 상승 밀도 수리 검토 종료)

Action(행동): run364AJ(364AJ 실행) proxy scout(프록시 정찰)를 package gate(패키지 게이트), session/side(세션/방향), month/side(월/방향), policy attribution(정책 귀속)으로 검토했다.

Effect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, PF-pass density-fail(PF 통과 밀도 실패) 단서를 `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1` 입력으로 넘겼다.

## run364AL PF-Pass Density Restore Offensive Inputs Closeout(364AL PF 통과 밀도 복원 공격 입력 종료)

Action(행동): run364AK(364AK 실행) offensive queue(공격 대기열) 12개를 run364AM(364AM 실행) scout queue(정찰 대기열)로 구체화했다.

Effect(효과): 거래 쪼개기와 top_n(상위 N개)을 금지한 채 PF-pass density restore(PF 통과 밀도 복원) 탐색을 다음 실행으로 넘긴다.

## run364AM PF-Pass Density Restore Offensive Scout Closeout(364AM PF 통과 밀도 복원 공격 정찰 종료)

Action(행동): run364AL(364AL 실행) queue(대기열) `12`개를 timestamp-safe proxy replay(시점 안전 프록시 재생)로 실행했다.

Effect(효과): `density_anchor_hold6_pf_probe_밀도_기준_보유6_PF_탐침__seed_selected_control_full_session_선택_대조_전체_세션_ps0_45_floor0_0_hold8__ps0_45__floor0_00__hold6`를 `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1` review(검토) 대상으로 넘기며, operating claim(운영 주장)은 없다.

## run364AN PF-Pass Density Restore Offensive Review Closeout(364AN PF 통과 밀도 복원 공격 검토 종료)

Action(행동): run364AM(364AM 실행) proxy scout(프록시 정찰) 12개 행을 package gate(패키지 게이트), policy attribution(정책 귀속), positive clue(긍정 단서), failure memory(실패 기억)로 검토했다.

Effect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터) 단서를 `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1` 입력으로 넘겼다.

## run364AO Hold6 PF/DD Repair Inputs Closeout(364AO 6봉 PF/DD 수리 입력 종료)

Action(행동): run364AN(364AN 실행) review queue(검토 대기열) 7개를 run364AP(364AP 실행) scout queue(정찰 대기열) 8개로 구체화했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터) 단서를 이어간다.

## run364AP Hold6 PF/DD Repair Scout Closeout(364AP 6봉 PF/DD 수리 정찰 종료)

Action(행동): run364AO(364AO 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.

Effect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 PF/DD repair(PF/DD 수리) 표면을 만들었다.

## run364AQ Hold6 PF/DD Repair Review Closeout(364AQ 6봉 PF/DD 수리 검토 종료)

Action(행동): run364AP(364AP 실행) proxy surface(프록시 표면)를 검토해 package(패키지)를 부정하고 threshold edge(임계값 경계) PF/DD 개선 단서를 보존했다.

Effect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 run364AR(364AR 실행) materialization(구체화)로 이어간다.

## run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364AR_threshold_edge_pf_gap_repair_materialization.md`
- judgment(판정): `materialization_completed_threshold_edge_pf_gap_repair_inputs_no_authority`
- queue_rows(대기열 행): `8`
- effect(효과): `run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1` scout queue(정찰 대기열)를 만들었다.

## run364AS Threshold-Edge PF Gap Repair Scout Closeout(364AS 임계값 경계 PF 간극 수리 정찰 종료)

Action(행동): run364AR(364AR 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.

Effect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 threshold-edge(임계값 경계) 표면을 만들었다.

## run364AT Threshold-Edge PF Gap Review Closeout(364AT 임계값 경계 PF 간극 검토 종료)

Action(행동): run364AS(364AS 실행)의 floor001 strict pass(하한 0.001 엄격 통과)를 검토했다.

Effect(효과): runtime authority(런타임 권위) 없이 `run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1` runtime probe package(런타임 탐침 패키지)로 넘길 후보를 기록했다.

## run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1

Action(행동): threshold edge floor001 package(임계값 경계 하한 0.001 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했다.

Effect(효과): proxy/MT5 diff(프록시/MT5 차이)와 runtime parity(런타임 동등성) review(검토) 입력을 만들었다. operating promotion(운영 승격)과 runtime authority(런타임 권위)는 없다.

## run364AW Threshold Edge Floor001 MT5 Review Closeout(364AW 임계값 경계 하한 0.001 MT5 검토 종료)

Action(행동): run364AV(364AV 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side(핵심 성과 지표/밀도/세션/방향)로 검토했다.

Effect(효과): net/PF/RF(순수익/수익 팩터/회복 계수)는 긍정 단서지만 실제 density(밀도)가 `2.9159159159`로 3/day(일 3회) 하한 아래라 운영 주장 없이 `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1` 수리 입력으로 넘긴다.

## run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1

Action(행동): AW MT5 runtime probe review(AW MT5 런타임 탐침 검토)를 AY scout queue(AY 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 다음 proxy scout(프록시 스카우트) 입력으로 넘긴다.

## run364AY Density Restore Cost/Session Proxy Scout Closeout(364AY 밀도 복원 비용/세션 프록시 스카우트 종료)

Action(행동): AX queue(대기열) 중 실행 가능한 행을 proxy replay(프록시 재생)로 실행했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1` review(검토)로 이어간다.

## run364AZ Density Restore Scout Review Closeout(364AZ 밀도 복원 스카우트 검토 종료)

Action(행동): AY proxy surface(AY 프록시 표면)를 검토했다.

Effect(효과): package_eligible_rows(패키지 가능 행) 0을 운영 주장 없이 닫고 `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1` 물질화로 이어간다.

## run364BA Density Restore Stress-To-Candidate Materialization Closeout(364BA 밀도 복원 압박-후보 물질화 종료)

Action(행동): AZ BA queue(AZ BA 대기열)를 BB scout queue(BB 스카우트 대기열)로 물질화했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1`로 이어간다.

## run364BB Density Restore Stress-To-Candidate Proxy Scout Closeout(364BB 밀도 복원 압박-후보 프록시 스카우트 종료)

Action(행동): BA queue(BA 대기열)의 실행 가능 후보 4개를 proxy replay(프록시 재생)로 평가했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1` review(검토)로 이어간다.

## run364BC Density Restore Stress Candidate Review Closeout(364BC 밀도 복원 압박 후보 검토 종료)

Action(행동): BB surface(BB 표면)를 검토해 package candidate(패키지 후보) 3개와 selected primary(선택 주 후보)를 확정했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1` package(패키지)로 이어간다.

## run364BD Density Restore Stress Candidate Runtime Package(밀도 복원 압박 후보 런타임 패키지)

- action(행동): selected primary(선택 주 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.
- effect(효과): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1` Strategy Tester(전략 테스터) 실행 준비가 끝났다.

## run364BF Density Restore Stress Candidate MT5 Review Closeout(364BF 밀도 복원 압박 후보 MT5 검토 종료)

Action(행동): run364BE(364BE 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side(핵심 성과 지표/밀도/세션/방향)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도)는 `3.0510510511`로 3/day(일 3회)를 통과했다. 다만 forward/regime stress(전진/국면 압박) 전까지 운영 주장은 닫지 않는다.

## run364BG Forward/Regime Stress Inputs Closeout(364BG 전진/국면 압박 입력 종료)

Action(행동): run364BF(364BF 실행)의 MT5 positive clue(MT5 긍정 단서)를 forward/regime stress inputs(전진/국면 압박 입력)와 BH scout queue(BH 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고, 운영 주장 없이 `run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1`에서 forward-like replay(전진 유사 재생)와 soft firewall(소프트 방화벽)을 시험할 수 있게 했다.

## run364BH Forward Regime Stress Proxy Scout Closeout(364BH 전진 국면 압박 프록시 탐색 종료)

Action(행동): BG queue(BG 대기열)를 closed-trade probability replay(종료 거래 확률 재생)로 평가했다.

Effect(효과): `bh02_long_h19_margin_opp_0020`를 `run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1` 검토로 넘기고, hard delete repair(강한 삭제 수리)는 밀도 붕괴로 닫았다.

## run364BK H19 Opposite-Margin Runtime Probe Review Closeout(364BK 19시 반대마진 런타임 탐침 검토 종료)

Action(행동): run364BJ(364BJ 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side/equity(핵심 성과 지표/밀도/세션/방향/평가손익)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도) `3.021021021`는 3/day(일 3회)를 통과했다. 다만 short share(숏 비중) `0.0984095427`와 equity DD(평가손익 낙폭) `18.24%` 때문에 운영 주장은 닫지 않고 `run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1` 입력으로 넘긴다.

## run364BL H19 Stress Short-Balance Materialization Closeout(364BL h19 압박 숏 균형 물질화 종료)

Action(행동): run364BK(364BK 실행)의 MT5 runtime probe review(MT5 런타임 탐침 검토)를 BM scout queue(BM 정찰 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 short source(숏 원천), forward/regime stress(전진/국면 압박), equity DD guardrail(평가손익 낙폭 가드레일)을 다음 실행 `run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1`로 넘긴다.

## run364BM H19 Stress Short-Balance Proxy Scout Closeout(364BM h19 압박 숏 균형 프록시 정찰 종료)

Action(행동): BL queue(BL 대기열)를 telemetry + US100 raw M5(실행기록 + US100 원천 5분봉)로 실행해 `bm04_short_router_ps0440_h17_20_overlay_fixed6`를 찾았다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1` review(검토)로 이어가며, runtime authority(런타임 권위)는 주장하지 않는다.

## run364BN H19 Stress Short-Balance Proxy Review Closeout(364BN h19 압박 숏 균형 프록시 검토 종료)

Action(행동): BM combined proxy(BM 합산 프록시)를 package reject(패키지 거절)와 repair seed(수리 씨앗)으로 분리했다.

Effect(효과): `bn02_h17_or_h20_margin_08_10_quality_repair`를 `run364BO_train_short_source_quality_repair_scout_without_db_v1`로 넘기고, 운영 주장은 계속 닫는다.

## run364BO Short Source Quality Repair Scout Closeout(364BO 숏 원천 품질 수리 정찰 종료)

Action(행동): BN repair seed(BN 수리 씨앗)를 entry-known rule surface(진입기지 규칙 표면)와 broad negative control(넓은 부정 대조)로 재생했다.

Effect(효과): `bo00_bn_seed_h17_or_h20_margin_08_10_reference`는 proxy(프록시) 단서로 남았지만 month stress watch(월 압박 관찰) 때문에 package(패키지)는 열지 않고 `run364BP_review_short_source_quality_repair_scout_without_db_v1`로 검토를 넘긴다.

## run364BP Short Source Quality Repair Review Closeout(364BP 숏 원천 품질 수리 검토 종료)

Action(행동): BO selected proxy(BO 선택 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BQ offensive seed(BQ 공격 씨앗)으로 분리했다.

Effect(효과): `run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1`에서 bo90/bo91/bo05 단서를 broad clean short-share lift(넓은 클린 숏 비중 보강)로 공격 탐색한다.

## run364BQ Broad Clean Short-Share Lift Scout Closeout(364BQ 넓은 클린 숏비중 상승 정찰 종료)

Action(행동): bo90/bo91/bo05 positive clue(긍정 단서)를 broad clean short-share lift(넓은 클린 숏비중 상승) surface(표면)로 재생했다.

Effect(효과): `bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__raw`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1047.85` / `1.4129932946` / `3.0870870871` / `0.1215953307`를 냈지만 month stress(월 압박)와 MT5 미실행 때문에 `run364BR_review_broad_clean_short_share_lift_scout_without_db_v1` 검토로 넘긴다.

## run364BR Broad Clean Short-Share Lift Review Closeout(364BR 넓은 클린 숏비중 상승 검토 종료)

Action(행동): BQ proxy(BQ 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BS repair seed(BS 수리 씨앗)으로 분리했다.

Effect(효과): `run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1`에서 exact 2025-12 memorization(정확한 2025-12 암기) 없이 late-year/month-of-year short-share stress(연말/월중 숏비중 압박)를 공격 탐색한다.

## run364BS Late-Year Short-Share Stress Repair Scout Closeout(364BS 연말 숏비중 압박 수리 탐색 종료)

Action(행동): BR late-year failure memory(BR 연말 실패 기억)를 month-of-year/session repair(월중/세션 수리) surface(표면)로 실행했다.

Effect(효과): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1063.14` / `1.4220035161` / `3.0720720721` / `0.1221896383`와 month_bad_count(월 나쁨 수) `0`를 만들었지만, MT5(메타트레이더5) 검토 전이라 `run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1`로 넘겼다.

## run364BT Late-Year Stress Repair Review Closeout(364BT 연말 압박 수리 검토 종료)

Action(행동): BS selected proxy(BS 선택 프록시)를 precheck eligible(사전검사 적격)로 검토했다.

Effect(효과): `run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1`에서 MT5 Strategy Tester probe(MT5 전략 테스터 탐침)를 시도하도록 current truth(현재 진실)를 넘겼고, 운영 권위는 주장하지 않았다.

## run364CG Cost-Stable H17 Source Guard Proxy Scout Closeout(364CG 비용 안정 17시 원천 가드 프록시 정찰 종료)

Action(행동): CF queue(CF 대기열) 12개를 existing MT5 closed-trade replay(기존 MT5 종료 거래 재생)로 정찰했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`가 no-split(무분할) 기준으로 small lift(작은 우위)를 보여 `run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1` review(검토)로 넘기며, runtime authority(런타임 권위)는 주장하지 않는다.

## run364CH Cost-Stable H17 Source Guard Review Closeout(364CH 비용 안정 17시 원천 가드 검토 종료)

Action(행동): CG selected h17 focus(CG 선택 17시 집중)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 거절하고 `run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1`에서 같은 Stage364(364단계) 안의 수리 입력으로 이어간다.

## run364CI H17 Focus Month Cost Stress Repair Inputs Closeout(364CI 17시 집중 월/비용 압박 수리 입력 종료)

Action(행동): CH failure memory(CH 실패 기억)를 `16`개 CJ scout queue(CJ 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1`로 비용/월/숏 하한 수리를 공격 탐색한다.

## run364CK H17 Repair Review Closeout(364CK 17시 수리 검토 종료)

Action(행동): CJ selected repair(CJ 선택 수리)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 손실 월 2개 때문에 거절하고 `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1`로 같은 Stage364(364단계) 안에서 CL repair input(CL 수리 입력)을 연다.



<!-- run364CL__run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1 -->

## run364CL H17 Bad Month Source Balance Repair Inputs Closeout(364CL 17시 손실 월 원천 균형 수리 입력 종료)

Action(행동): CK package rejection(CK 패키지 거절)을 `16`개 CM scout queue(CM 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1`로 손실 월/원천 균형 수리를 공격 탐색한다.

<!-- run364CM__run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1 -->

## run364CM H17 Bad Month Source Balance Repair Scout Closeout(364CM 17시 손실 월 원천 균형 수리 정찰 종료)

Action(행동): CL queue(CL 대기열) `16`개 후보를 proxy replay(프록시 재생)했다.

Effect(효과): `cm04_cj09_month08_12_pair_guard`가 bad_month_count(손실 월 수) `0`을 만들었고, 같은 Stage364(364단계) 안에서 `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1` 검토로 이어간다.

## run364CN H17 Bad-Month Source-Balance Repair Review Closeout(364CN 17시 손실 월/원천 균형 수리 검토 종료)

Action(행동): CM 후보를 package/source/month/cost/MT5 boundary(패키지/원천/월/비용/MT5 경계)로 검토했습니다.

Effect(효과): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`를 열어 MT5 runtime probe input(MT5 런타임 탐침 입력)을 구체화하고, 운영 주장(operating claim, 운영 주장)은 닫아둡니다.

## run364CO MT5 Runtime Probe Package Closeout(MT5 런타임 탐침 패키지 종료)

Action(행동): CM04 rule package(CM04 규칙 패키지)를 RuntimeProbeEA set/ini(런타임 탐침 EA 설정/INI)로 만들었습니다.

Effect(효과): `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 MT5 실행을 시도할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CQ MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CP MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): positive net/PF/density(양수 순수익/PF/밀도)는 보존하고, month12/equity DD(12월/수익곡선 낙폭)를 `run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CQ MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CP MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): positive net/PF/density(양수 순수익/PF/밀도)는 보존하고, month12/equity DD(12월/수익곡선 낙폭)를 `run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CR Repair Inputs(수리 입력)

Action(행동): 12월 롱 손실과 equity DD(수익곡선 낙폭) 수리 후보 `8`개를 만들었습니다.

Effect(효과): `run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

<!-- run364CS__run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->

## run364CS Month12 Long Repair Scout(364CS 12월 롱 수리 정찰)

Action(행동): CR queue(CR 대기열) `8`개를 proxy replay(프록시 재생)했습니다.

Effect(효과): selected variant(선택 변형) `cr04_month12_long_hours17_20_floor002`를 `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1` review(검토)로 넘겼고, 운영 권위는 주장하지 않습니다.

<!-- run364CT__run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->

## run364CT Runtime Representation Review(364CT 런타임 표현 검토)

Action(행동): `cr04` 프록시 후보를 EA 표현 가능성까지 검토했습니다.

Effect(효과): 두 번째 month margin guard(월 마진 가드)가 필요하므로 `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`에서 런타임 패키지 수리로 이어갑니다.

<!-- run364CU__run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1 -->

## run364CU Secondary Month Guard Runtime Package(364CU 보조 월 가드 런타임 패키지)

Action(행동): EA(전문가 자문)에 secondary month margin guard(보조 월 마진 가드)를 추가하고 `cr04` set/ini(설정/INI)를 만들었습니다.

Effect(효과): `run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터) 실행을 시도할 수 있습니다.

<!-- run364CV__run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1 -->

## run364CV MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): cr04 secondary month guard package(cr04 보조 월 가드 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CW MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CV MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): month12 repair(12월 수리)는 통과했지만 equity DD/long skew/proxy gap(수익곡선 낙폭/롱 쏠림/프록시 차이)을 `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CX Repair Inputs(수리 입력)

Action(행동): equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 후보 `12`개를 만들었습니다.

Effect(효과): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

## run364CX Repair Inputs(수리 입력)

Action(행동): equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 후보 `12`개를 만들었습니다.

Effect(효과): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

## run364CY Proxy Scout(프록시 정찰)

Action(행동): CX queue(CX 대기열) 12개를 risk-scale proxy replay(위험비율 프록시 재생)로 실행했습니다.

Effect(효과): `cx05_high_quality_short_boost110_h17_20`를 `run364CZ` review(검토) 대상으로 넘깁니다.

<!-- run364CZ__run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->

## run364CZ Runtime Representation Review(364CZ 런타임 표현 검토)

Action(행동): `cx05_high_quality_short_boost110_h17_20` proxy candidate(프록시 후보)를 EA 표현 가능성까지 검토했습니다.

Effect(효과): short quality risk-scale overlay(숏 품질 위험비율 오버레이)가 필요하므로 `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`에서 런타임 패키지 수리로 이어갑니다.

<!-- run364DA__run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1 -->

## run364DA Short Quality Risk-Scale Runtime Package(364DA 숏 품질 위험비율 런타임 패키지)

Action(행동): EA(전문가 자문)에 risk-scale overlay(위험비율 오버레이)를 추가하고 `cx05` set/ini(설정/INI)를 만들었습니다.

Effect(효과): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터) 실행을 시도할 수 있습니다.

<!-- run364DB__run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->

## run364DB MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): cx05 short-quality risk-scale package(cx05 숏 품질 위험비율 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

<!-- run364DC__run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->

## run364DC Short-Quality Risk-Scale Review(숏 품질 위험비율 검토)

Action(행동): DB MT5 probe(DB MT5 탐침)를 CV anchor(CV 기준점)와 비교했습니다.

Effect(효과): risk-scale overlay(위험비율 오버레이)는 긍정 단서로 남기고, side balance(방향 균형)는 다음 탐색 제약으로 남깁니다.

## run364DD Short-Source Expansion(숏 원천 확장)

Action(행동): DB telemetry(DB 텔레메트리)를 single-position proxy replay(단일 포지션 프록시 재생)로 변형했습니다.

Effect(효과): `dd05_h17_21_short_source_m050_ex_aug`를 `run364DE` review(검토) 대상으로 넘깁니다.

## run364DE Runtime Review(런타임 검토)

Action(행동): DD short-source rule(DD 숏 원천 규칙)의 RuntimeProbeEA(런타임 탐침 EA) 표현 가능성을 검토했습니다.

Effect(효과): flat-margin guard(flat 마진 조건) 보정이 필요해 `run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1`를 열었습니다.

## run364DF Runtime Package(런타임 패키지)

Action(행동): DD05 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.

## run364DF Runtime Package(런타임 패키지)

Action(행동): DD05 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
## run364DG MT5 Runtime Probe(MT5 런타임 탐침)

Action(행동): DD05 package(DD05 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.
<!-- run364DH__run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1 -->

## run364DH Short-Source Expansion Review(숏 원천 확장 검토)

Action(행동): DG MT5 probe(DG MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 확장은 거래수와 숏 비중을 늘렸지만 순수익/수익 팩터 회복이 필요하므로 `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`로 profit recovery(수익 회복) 탐색을 엽니다.
<!-- run364DI__run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1 -->

## run364DI Short-Source Profit Recovery Scout(숏 원천 수익 회복 스카우트)

Action(행동): hour veto(시간 배제), margin filter(마진 필터), month stress(月 스트레스)를 proxy scout(프록시 스카우트)로 비교했습니다.

Effect(효과): `di02_h17_18_20_21_no19_m050`를 runtime-ready(런타임 준비) review candidate(검토 후보)로 남겼고, `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`에서 패키지 가능성을 검토합니다.
<!-- run364DJ__run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1 -->

## run364DJ Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)

Action(행동): DI 선택 후보를 검토하고 DK runtime package(DK 런타임 패키지)를 열었습니다.

Effect(효과): 19시 배제(hour19 veto, 19시 배제)를 MT5 set file(설정 파일)로 표현할 수 있게 다음 작업을 고정했습니다.
## run364DK Runtime Package(런타임 패키지)

Action(행동): DI02 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DL_execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
## run364DL MT5 Runtime Probe(MT5 런타임 탐침)

Action(행동): DI02 no19 package(DI02 no19 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.
<!-- run364DM__run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1 -->

## run364DM Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)

Action(행동): DL MT5 probe(DL MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 수익 회복은 DG보다 순수익을 회복했지만 DB 초과가 필요하므로 `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`로 PF/net polish(PF/순수익 다듬기) 탐색을 엽니다.
## run364DN PF/Net Polish Scout(PF/순수익 다듬기 스카우트)

Action(행동): DL 보정값을 사용해 source/risk parameter(원천/위험 파라미터)를 비교했습니다.

Effect(효과): `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`에서 패키지 가능 여부를 검토할 후보와 실패 경계를 만들었습니다.
<!-- run364DO__run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1 -->

## run364DO PF/net Polish Review(PF/순수익 다듬기 검토)

Action(행동): DN의 parameter-only polish(파라미터 전용 다듬기)를 엄격 보정 기준으로 판정했습니다.

Effect(효과): strict pass(엄격 통과)가 0개라 runtime package(런타임 패키지)를 열지 않고 `run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1`로 model/label/feature offensive reseed(모델/라벨/피처 공격 재시드)를 엽니다.
<!-- run364DP__run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1 -->

## run364DP Short-Source Model/Label Reseed(숏 원천 모델/라벨 재시드)

Action(행동): train split(학습 분할)로 short-source gate model(숏 원천 게이트 모델)을 학습하고 ONNX smoke(온엑스 스모크)를 확인했습니다.

Effect(효과): parameter-only polish(파라미터 전용 다듬기) 실패를 model/label/feature(모델/라벨/피처) 새 씨앗으로 전환했고 `run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1`에서 package(패키지) 여부를 검토합니다.
<!-- run364DQ__run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1 -->

## run364DQ Short-Source Model/Label Review(숏 원천 모델/라벨 검토)

Action(행동): DP ONNX seed(DP ONNX 씨앗)의 OOS clue(표본외 단서)와 density gap(밀도 차이)을 검토했습니다.

Effect(효과): 패키지는 열지 않고 `run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1`에서 density/PF bridge(밀도/PF 브리지)를 탐색합니다.
<!-- run364DR__run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->

## run364DR Density/PF Bridge Reseed(밀도/PF 브리지 재시드)

Action(행동): DP model score(DP 모델 점수)와 native probability/session filter(기존 확률/세션 필터)를 결합했습니다.

Effect(효과): selected OOS clue(선택 표본외 단서)를 검증 밀도/PF 경계와 함께 `run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1`로 넘깁니다.
<!-- run364DS__run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->

## run364DS Density/PF Bridge Review(밀도/PF 브리지 검토)

Action(행동): DR bridge(DR 브리지)를 검토하고 package(패키지)를 거절했습니다.

Effect(효과): `run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 regime/market-behavior reseed(국면/시장 현상 재시드)를 엽니다.
<!-- run364DT__run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1 -->

## run364DT Regime/Behavior Reseed(국면/현상 재시드)

Action(행동): 3-class direction label(3분류 방향 라벨)과 derived regime features(파생 국면 피처)로 모델을 학습했습니다.

Effect(효과): `run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DU__run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1 -->

## run364DU Regime/Behavior Review(국면/현상 검토)

Action(행동): DT OOS clue(DT 표본외 단서)와 validation failure(검증 실패)를 분리 판정했습니다.

Effect(효과): package(패키지)는 거절하고 `run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1`에서 validation-stability source(검증 안정성 원천)를 탐색합니다.
<!-- run364DV__run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1 -->

## run364DV Validation-Stability Reseed(검증 안정성 재시드)

Action(행동): 검증 안정성 라벨/필터로 새 모델을 학습했습니다.

Effect(효과): `run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DW__run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1 -->

## run364DW Validation-Stability Review(검증 안정성 검토)

Action(행동): DV 수익성 회복과 밀도 실패를 분리했습니다.

Effect(효과): `run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 density recovery(밀도 회복)를 탐색합니다.
<!-- run364DX__run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1 -->

## run364DX Density Recovery Reseed(밀도 회복 재시드)

Action(행동): 짧은 보유 라벨과 밀도 회복 필터로 새 모델을 학습했습니다.

Effect(효과): `run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DY__run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1 -->

## run364DY Density Recovery Review(밀도 회복 검토)

Action(행동): DX 밀도 회복과 OOS 실패를 분리했습니다.

Effect(효과): `run364DZ_train_h17_density_pf_balance_reseed_without_db_v1`에서 density/PF balance(밀도/PF 균형)를 탐색합니다.
<!-- run364DZ__run364DZ_train_h17_density_pf_balance_reseed_without_db_v1 -->

## run364DZ Density/PF Balance Reseed(밀도/PF 균형 재시드)

Action(행동): PF 인식 필터로 새 모델을 학습했습니다.

Effect(효과): `run364EA_review_h17_density_pf_balance_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364EA__run364EA_review_h17_density_pf_balance_reseed_without_db_v1 -->

## run364EA Density/PF Balance Review(밀도/PF 균형 검토)

Action(행동): DZ proxy/ONNX smoke(DZ 프록시/온엑스 스모크) 결과를 검토했습니다.

Effect(효과): package(패키지)는 거절하고 EB validation PF floor(검증 PF 바닥) 탐색으로 넘깁니다.
<!-- run364EB__run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->

## run364EB Validation PF Floor Density Recovery(검증 PF 바닥 밀도 회복)

Action(행동): validation PF floor(검증 PF 바닥)를 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364EC__run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->

## run364EC Validation PF Floor Review(검증 PF 바닥 검토)

Action(행동): EB proxy/ONNX smoke(EB 프록시/온엑스 스모크) 결과를 검토했습니다.

Effect(효과): package(패키지)는 거절하고 ED dual PF floor bridge(양쪽 PF 바닥 연결) 탐색으로 넘깁니다.
<!-- run364ED__run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->

## run364ED Dual PF Floor Bridge(양쪽 PF 바닥 연결)

Action(행동): validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1`에서 PF 바닥 회복 여부와 package(패키지) 가능성을 검토합니다.
<!-- run364EE__run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->

## run364EE Dual PF Floor Bridge Review(양쪽 PF 바닥 연결 검토)

Action(행동): ED 결과를 검토하고 package rejected(패키지 거절)로 닫았습니다.

Effect(효과): `run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1`에서 validation source rotation(검증 원천 회전)을 다음 공격 탐색으로 엽니다.
<!-- run364EF__run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1 -->

## run364EF Validation Source Rotation Density Recovery(검증 원천 회전 밀도 회복)

Action(행동): feature source rotation(피처 원천 회전)으로 검증 PF 회복을 탐색했습니다.

Effect(효과): `run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1`에서 패키지 가능성과 실패 기억을 검토합니다.
<!-- run364EG__run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1 -->

## run364EG Validation Source Rotation Review(검증 원천 회전 검토)

Action(행동): EF 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1`에서 OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 다음 공격 탐색으로 엽니다.
<!-- run364EH__run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->

## run364EH OOS PF108 Bridge Density Preserve(표본외 PF108 연결 밀도 보존)

Action(행동): OOS PF 1.08(표본외 PF 1.08)을 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1`에서 PF bridge(수익 팩터 연결)와 package(패키지) 가능성을 검토합니다.
<!-- run364EI__run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->

## run364EI OOS PF108 Bridge Review(표본외 PF108 연결 검토)

Action(행동): EH 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1`에서 density floor OOS PF salvage(밀도 바닥 표본외 PF 회수)를 다음 공격 탐색으로 엽니다.
<!-- run364EJ__run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1 -->

## run364EJ Density Floor OOS PF Salvage(밀도 바닥 표본외 PF 회수)

Action(행동): EH high OOS PF clue(EH 높은 표본외 PF 단서)를 density>=3(밀도 3 이상) 조건 안으로 회수하는 모델을 학습했습니다.

Effect(효과): `run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1`에서 package(패키지) 가능성과 다음 수리 조건을 검토합니다.
<!-- run364EK__run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1 -->

## run364EK Density Floor OOS PF Salvage Review(밀도 바닥 표본외 PF 회수 검토)

Action(행동): EJ 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1`에서 OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 다음 공격 탐색으로 엽니다.
<!-- run364EL__run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1 -->

## run364EL OOS108 Validation Floor Bridge(표본외108 검증 바닥 연결)

Action(행동): density>=3과 OOS PF>=1.08(밀도 3 이상과 표본외 PF 1.08 이상)을 보존하며 validation PF floor(검증 PF 바닥)를 수리하는 모델을 학습했습니다.

Effect(효과): `run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1`에서 package(패키지) 가능성과 다음 조건을 검토합니다.
<!-- run364EM__run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1 -->

## run364EM OOS108 Validation Floor Bridge Review(표본외108 검증 바닥 연결 검토)

Action(행동): EL 후보를 package eligible(패키지 가능)로 검토하고 cost stress caution(비용 압박 주의)을 남겼습니다.

Effect(효과): `run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1`에서 MT5 probe(MT5 탐침) 전 runtime package(런타임 패키지)를 물질화합니다.
<!-- run364EN__run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1 -->

## run364EN Runtime Package(런타임 패키지)

Action(행동): OOS108 validation floor bridge(표본외108 검증 바닥 연결) set/ini(설정/초기화 파일), feature matrix(피처 행렬), ONNX(온엑스)를 물질화했습니다.

Effect(효과): `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
<!-- run364EO__run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->

## run364EO MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): OOS108 runtime package(OOS108 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시와 MT5 차이)를 검토할 수 있습니다.
<!-- run364EP__run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->

## run364EP OOS108 MT5 Runtime Review(OOS108 MT5 런타임 검토)

Action(행동): EO MT5 probe(EO MT5 탐침)를 scope-aligned proxy(범위 정렬 프록시), cost stress(비용 압박), side balance(방향 균형)로 검토했습니다.

Effect(효과): MT5 net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서지만 short-heavy/cost stress(숏 편중/비용 압박)가 남아 `run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1`로 수리 탐색을 엽니다.
## run364EQ note(EQ 메모)

- strict pass(엄격 통과): `0`.
- effect(효과): 기존 표면 반복을 멈추고 `run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1` 재시드로 이동합니다.
## run364EQ note(EQ 메모)

- strict pass(엄격 통과): `0`.
- effect(효과): 기존 표면 반복을 멈추고 `run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1` 재시드로 이동합니다.
<!-- run364ER__run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->

## run364ER Cost/Side Reseed(비용/방향 재시드)

Action(행동): cost-aware labels(비용 인식 라벨)와 regime/behavior features(국면/현상 피처)로 모델을 학습했습니다.

Effect(효과): `run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364ES__run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->

## run364ES Cost/Side Reseed Review(비용/방향 재시드 검토)

Action(행동): ER 결과를 package(패키지)와 failure memory(실패 기억)로 분리했습니다.

Effect(효과): `run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1`에서 density/cost/short balance(밀도/비용/숏 균형)를 직접 재탐색합니다.
<!-- run364ET__run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->

## run364ET Density/Cost/Short Balance Reseed(밀도/비용/숏 균형 재시드)

Action(행동): 비용 가중 고밀도 라벨과 방향/세션 벌점으로 모델을 재학습했습니다.

Effect(효과): `run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1`에서 패키지 가능성과 실패 기억을 분리합니다.
<!-- run364EU__run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->

## run364EU Density/Cost/Short Balance Review(밀도/비용/숏 균형 검토)

Action(행동): ET 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1`에서 cost09/density edge recovery(비용0.9/밀도 엣지 회복)를 다음 공격 탐색으로 엽니다.
<!-- run364EV__run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->

## run364EV Cost09/Density Edge Recovery(비용0.9/밀도 엣지 회복)

Action(행동): 비용0.9/밀도 엣지 회복 모델을 학습했습니다.

Effect(효과): `run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364EW__run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->

## run364EW Cost09/Density Edge Review(비용0.9/밀도 엣지 검토)

Action(행동): EV 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`에서 OOS-preserving cost09/short rebalance(표본외 보존 비용0.9/숏 재균형)를 다음 공격 탐색으로 엽니다.
<!-- run364EX__run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->

## run364EX OOS Preserve Cost09/Short Rebalance(표본외 보존 비용0.9/숏 재균형)

Action(행동): 표본외 보존 우선 모델을 학습했습니다.

Effect(효과): `run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364EY__run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->

## run364EY OOS Preserve Cost09/Short Review(표본외 보존 비용0.9/숏 검토)

Action(행동): EX 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`에서 OOS PF/cost09 gap repair(표본외 PF/비용0.9 간격 수리)를 다음 공격 탐색으로 엽니다.
<!-- run364EZ__run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->

## run364EZ OOS PF125 Cost09 Gap Repair(표본외 PF 1.25 비용0.9 간격 수리)

Action(행동): 표본외 PF/비용0.9 수리 모델을 학습했습니다.

Effect(효과): `run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FA__run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->

## run364FA OOS PF125 Cost09 Gap Review(표본외 PF 1.25 비용0.9 간격 검토)

Action(행동): EZ 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1`에서 PF125 density bridge repair(PF125 밀도 연결 수리)를 다음 공격 탐색으로 엽니다.
<!-- run364FB__run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->

## run364FB PF125 Density Bridge Repair(PF125 밀도 연결 수리)

Action(행동): PF125 밀도 연결 수리 모델을 학습했습니다.

Effect(효과): `run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FC__run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->

## run364FC PF125 Density Bridge Review(PF125 밀도 연결 검토)

Action(행동): FB 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`에서 숏/비용0.9 균형 수리를 다음 공격 탐색으로 엽니다.
<!-- run364FD__run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->

## run364FD PF125 Short/Cost09 Balance Repair(PF125 숏/비용0.9 균형 수리)

Action(행동): PF125 숏/비용0.9 균형 수리 모델을 학습했습니다.

Effect(효과): `run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FE__run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->

## run364FE PF125 Short/Cost09 Balance Review(PF125 숏/비용0.9 균형 검토)

Action(행동): FD 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`에서 비용/숏 가드를 보존한 밀도 재결합을 다음 공격 탐색으로 엽니다.
<!-- run364FF__run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->

## run364FF PF125 Density Rejoin Cost09 Short Guard(PF125 밀도 재결합 비용0.9 숏 가드)

Action(행동): 비용/숏 가드가 있는 밀도 재결합 모델을 학습했습니다.

Effect(효과): `run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FG__run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->

## run364FG PF125 Density Rejoin Review(PF125 밀도 재결합 검토)

Action(행동): FF 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`에서 검증 밀도와 수익을 함께 수리합니다.
<!-- run364FH__run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->

## run364FH Validation Density Profit Repair(검증 밀도 수익 수리)

Action(행동): 검증 밀도 수익 목적을 직접 넣은 모델을 학습했습니다.

Effect(효과): `run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FI__run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->

## run364FI Validation Density Profit Review(검증 밀도 수익 검토)

Action(행동): FH 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`에서 validation-positive density3(검증 양수 밀도3)를 보존하며 OOS PF/cost(표본외 PF/비용)를 회복합니다.
<!-- run364FJ__run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->

## run364FJ OOS Density Preserve Repair(표본외 밀도 보존 수리)

Action(행동): 표본외 PF/비용 보존과 검증/합산 밀도 복구를 함께 점수화했습니다.

Effect(효과): `run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FK__run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->

## run364FK OOS Density Preserve Review(표본외 밀도 보존 검토)

Action(행동): FJ 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`에서 hard density floor(강제 밀도 바닥)와 표본외 비용 보존을 동시에 요구합니다.
<!-- run364FL__run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->

## run364FL Dual Density OOS Cost Bridge(양쪽 밀도 표본외 비용 연결)

Action(행동): hard density floor(강제 밀도 바닥)와 표본외 비용 보존을 같은 선택 점수에 넣었습니다.

Effect(효과): `run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FM__run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->

## run364FM Dual Density OOS Cost Bridge Review(양쪽 밀도 표본외 비용 연결 검토)

Action(행동): FL 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`에서 density/cost decoupled bridge(밀도/비용 분리 연결)를 실행합니다.
<!-- run364FN__run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->

## run364FN Density Cost Decoupled Bridge(밀도 비용 분리 연결)

Action(행동): density leg(밀도 다리)와 cost leg(비용 다리)의 overlap score(겹침 점수)를 학습했습니다.

Effect(효과): `run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FO__run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->

## run364FO Density Cost Decoupled Bridge Review(밀도 비용 분리 연결 검토)

Action(행동): FN 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`에서 positive density floor reseed(양수 밀도 바닥 재시드)를 실행합니다.
<!-- run364FP__run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->

## run364FP Positive Density Floor Reseed(양수 밀도 바닥 재시드)

Action(행동): validation positive density3(검증 양수 밀도3)를 먼저 복구하도록 모델을 학습했습니다.

Effect(효과): `run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FQ__run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->

## run364FQ Positive Density Floor Reseed Review(양수 밀도 바닥 재시드 검토)

Action(행동): FP 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`에서 density3 regime split repair(밀도3 국면 분할 수리)를 실행합니다.
<!-- run364FR__run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->

## run364FR Density3 Regime Split Repair(밀도3 국면 분할 수리)

Action(행동): 고밀도 손실 행을 국면/세션/방향으로 분리해 모델을 학습했습니다.

Effect(효과): `run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FS__run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->

## run364FS Density3 Regime Split Repair Review(밀도3 국면 분할 수리 검토)

Action(행동): FR 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`에서 regime profit density reexpand(국면 수익 밀도 재확장)를 실행합니다.
<!-- run364FT__run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->

## run364FT Regime Profit Density Reexpand(국면 수익 밀도 재확장)

Action(행동): 수익 회수 단서를 보존하면서 시간/필터 폭과 라벨 장벽을 다시 넓혔습니다.

Effect(효과): `run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FU__run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->

## run364FU Regime Profit Density Reexpand Review(국면 수익 밀도 재확장 검토)

Action(행동): FT 결과를 밀도 회복과 표본외 수익 실패로 분리했습니다.

Effect(효과): `run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`에서 밀도3을 보존한 표본외 수익 연결을 실행합니다.
<!-- run364FV__run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->

## run364FV Density3 OOS Profit Bridge(밀도3 표본외 수익 연결)

Action(행동): 밀도3 보존과 표본외 수익 연결을 같은 선택 점수로 학습했습니다.

Effect(효과): `run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FW__run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->

## run364FW Density3 OOS Profit Bridge Review(밀도3 표본외 수익 연결 검토)

Action(행동): FV 결과를 표본외 수익 회복과 밀도 손실로 분리했습니다.

Effect(효과): `run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`에서 수익-밀도 이중 앵커 재결합을 실행합니다.
<!-- run364FX__run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->

## run364FX Profit Density Dual Anchor Rejoin(수익 밀도 이중 앵커 재결합)

Action(행동): FT density anchor(FT 밀도 앵커)와 FV OOS profit anchor(FV 표본외 수익 앵커)를 같은 선택 점수로 재결합했습니다.

Effect(효과): `run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364FY__run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->

## run364FY Profit Density Dual Anchor Rejoin Review(수익 밀도 이중 앵커 재결합 검토)

Action(행동): FX 결과를 밀도 회복과 표본외 수익 실패로 분리했습니다.

Effect(효과): `run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`에서 밀도-수익 충돌 재혼합을 실행합니다.
<!-- run364FZ__run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->

## run364FZ Density Profit Conflict Reblend(밀도 수익 충돌 재혼합)

Action(행동): FY failure memory(FY 실패 기억)의 density3 negative rows(밀도3 음수 행)와 low-density OOS-positive rows(저밀도 표본외 양수 행)를 conflict constraints(충돌 제약)로 재혼합했습니다.

Effect(효과): `run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364GA__run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->

## run364GA Density Profit Conflict Reblend Review(밀도 수익 충돌 재혼합 검토)

Action(행동): FZ 결과를 수익-밀도 동시 악화와 손실 군집으로 분리했습니다.

Effect(효과): `run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`에서 session/side loss veto rescue(세션/방향 손실 차단 회수)를 실행합니다.
<!-- run364GB__run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->

## run364GB Session Side Loss Veto Rescue(세션 방향 손실 차단 회수)

Action(행동): GA failure memory(GA 실패 기억)의 FZ loss clusters(FZ 손실 군집)를 session/side veto(세션/방향 차단)로 시험했습니다.

Effect(효과): `run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364GC__run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->

## run364GC Session Side Loss Veto Rescue Review(세션 방향 손실 차단 회수 검토)

Action(행동): GB 결과를 수익 회복과 밀도/비용 실패로 분리했습니다.

Effect(효과): `run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`에서 profit-preserving density recovery(수익 보존 밀도 회복)를 실행합니다.
<!-- run364GD__run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->

## run364GD Profit Preserving Density Recovery(수익 보존 밀도 회복)

Action(행동): GC failure memory(GC 실패 기억)의 GB profit recovery(GB 수익 회복)를 보존 조건으로 두고 density/cost(밀도/비용)를 수리했습니다.

Effect(효과): `run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`에서 패키지 가능성과 실패 경계를 검토합니다.
<!-- run364GE__run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->

## run364GE Profit Preserving Density Recovery Review(수익 보존 밀도 회복 검토)

Action(행동): GD 결과를 표본외 수익 개선과 검증/밀도 실패로 분리했습니다.

Effect(효과): `run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`에서 profit-floor density lift(수익 바닥 밀도 상승)를 실행합니다.
<!-- run364GF__run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->

## run364GF Profit-Floor Density Lift(수익 바닥 밀도 상승)

Action(행동): GE 실패 기억을 수익 바닥과 밀도 상승 제약으로 바꾸어 재학습했습니다.

Effect(효과): `run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`에서 패키지 가능성 없이 결과 판정을 먼저 검토합니다.
<!-- run364GG__run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->

## run364GG Profit-Floor Density Lift Review(수익 바닥 밀도 상승 검토)

Action(행동): GF 결과를 검증 개선, 표본외 바닥 보존, 밀도3 실패로 분리했습니다.

Effect(효과): `run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`에서 density3 profit-floor repair(밀도3 수익 바닥 수리)를 실행합니다.
<!-- run364GH__run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->

## run364GH Density3 Profit-Floor Repair(밀도3 수익 바닥 수리)

Action(행동): GG 실패 기억을 밀도3 공급과 수익 바닥 보존 제약으로 바꾸어 재학습했습니다.

Effect(효과): `run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`에서 패키지 가능성 없이 결과 판정을 먼저 검토합니다.
<!-- run364GI__run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->

## run364GI Density3 Profit-Floor Repair Review(밀도3 수익 바닥 수리 검토)

Action(행동): GH 결과를 밀도 상승과 비용/검증 바닥 실패로 분리했습니다.

Effect(효과): `run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`에서 density-cost floor rejoin(밀도-비용 바닥 재결합)을 실행합니다.
<!-- run364GK__run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->

## run364GK Density-Cost Floor Rejoin Review(밀도-비용 바닥 재결합 검토)

Action(행동): GJ 결과를 비용 회복과 밀도 손실로 분리했습니다.

Effect(효과): `run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`에서 cost-repaired density reexpand(비용 수리 후 밀도 재확장)를 실행합니다.
<!-- run364GJ__run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->

## run364GJ Density-Cost Floor Rejoin(밀도-비용 바닥 재결합)

Action(행동): GI 실패 기억을 비용 바닥과 밀도 보존 제약으로 바꾸어 재학습했습니다.

Effect(효과): `run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`에서 GJ 결과를 검토합니다.
<!-- run364GL__run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->

## run364GL Cost-Repaired Density Reexpand(비용 수리 후 밀도 재확장)

Action(행동): GK 실패 기억을 비용 보존 밀도 재확장 제약으로 바꾸어 재학습했습니다.

Effect(효과): `run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`에서 GL 결과를 검토합니다.
<!-- run364GM__run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->

## run364GM Cost-Repaired Density Reexpand Review(비용 수리 후 밀도 재확장 검토)

Action(행동): GL 결과를 밀도 회복과 비용 재붕괴로 분리했습니다.

Effect(효과): `run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`에서 density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)를 실행합니다.
<!-- run364GN__run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->

## run364GN Density-Cost Dual-Anchor Router(밀도-비용 이중 앵커 라우터)

Action(행동): GM 실패 기억을 받아 비용 앵커와 밀도 앵커를 분리한 라우터 탐색을 실행했습니다.

Effect(효과): `run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`에서 GN 결과를 검토합니다.
<!-- run364GO__run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->

## run364GO Density-Cost Dual-Anchor Router Review(밀도-비용 이중 앵커 라우터 검토)

Action(행동): GN의 sparse PF999 선택 실패를 검토했습니다.

Effect(효과): `run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`에서 PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 수리합니다.
<!-- run364GP__run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->

## run364GP Density-Floor PF-Capped Router(밀도 바닥 PF 캡 라우터)

Action(행동): GO 실패 기억을 받아 PF cap(PF 캡)과 hard density/trade floor(하드 밀도/거래수 바닥)를 적용했습니다.

Effect(효과): `run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`에서 GP 결과를 검토합니다.
<!-- run364GQ__run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->

## run364GQ Density-Floor PF-Capped Router Review(밀도 바닥 PF 캡 라우터 검토)

Action(행동): GP의 PF cap(PF 캡) 수리 효과와 비용-밀도 미완을 검토했습니다.

Effect(효과): `run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`에서 cost-near density floor(비용 근접 밀도 바닥)를 먼저 고정합니다.
<!-- run364GR__run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->

## run364GR Cost-Near Density Floor Router(비용 근접 밀도 바닥 라우터)

Action(행동): GQ의 cost-density incomplete(비용-밀도 미완) 실패를 cost-near first(비용 근접 우선) 선택 점수로 수리했습니다.

Effect(효과): `run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`에서 비용 수리와 밀도 유지가 실제로 같이 되는지 검토합니다.
<!-- run364GS__run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->

## run364GS Cost-Near Density Floor Router Review(비용 근접 밀도 바닥 라우터 검토)

Action(행동): GR의 비용 수리 단서와 표본외 약점을 분리했습니다.

Effect(효과): `run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`에서 합산 비용 수리 보존 + 표본외 비용0.6/밀도 상승을 함께 탐색합니다.
<!-- run364GT__run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->

## run364GT Cost-Near Density Lift Router(비용 근접 밀도 상승 라우터)

Action(행동): GS의 partial cost repair(부분 비용 수리) 단서를 비용 보존 + 밀도 상승 점수로 재탐색했습니다.

Effect(효과): `run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`에서 비용/밀도/패키지 가능성을 분리 검토합니다.
<!-- run364GU__run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->

## run364GU Cost-Near Density Lift Router Review(비용 근접 밀도 상승 라우터 검토)

Action(행동): GT의 density lift(밀도 상승)와 cost failure(비용 실패)를 분리했습니다.

Effect(효과): `run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`에서 OOS density(표본외 밀도)를 보존하면서 OOS cost0.6(표본외 비용0.6)을 수리합니다.
<!-- run364GV__run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->

## run364GV OOS Cost0.6 Density Preserve Router(표본외 비용0.6 밀도 보존 라우터)

Action(행동): GU의 비용 실패 기억을 OOS cost0.6(표본외 비용0.6) 수리 점수로 바꿨습니다.

Effect(효과): `run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`에서 비용 수리와 밀도 보존이 실제로 같이 왔는지 검토합니다.
<!-- run364GW__run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->

## run364GW OOS Cost0.6 Density Preserve Router Review(표본외 비용0.6 밀도 보존 라우터 검토)

Action(행동): GV의 cost repair(비용 수리)와 density failure(밀도 실패)를 분리했습니다.

Effect(효과): `run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`에서 비용 수리 유지 + 밀도 회복을 같이 탐색합니다.
<!-- run364GX__run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->

## run364GX Density Recover Cost0.6 Hold Router(밀도 회복 비용0.6 유지 라우터)

Action(행동): GW의 cost repair positive clue(비용 수리 긍정 단서)를 density recovery(밀도 회복) 점수로 다시 공격했습니다.

Effect(효과): `run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`에서 비용 유지와 밀도 회복을 함께 검토합니다.
<!-- run364GY__run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->

## run364GY Density Recover Cost0.6 Hold Router Review(밀도 회복 비용0.6 유지 라우터 검토)

Action(행동): GX의 OOS profit/cost0.6(표본외 수익/비용0.6) 개선과 density failure(밀도 실패)를 분리했습니다.

Effect(효과): `run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`에서 profit/cost clue(수익/비용 단서)를 보존하면서 density/cost frontier(밀도/비용 경계)를 다시 탐색합니다.
<!-- run364GZ__run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->

## run364GZ Cost-Density Joint Frontier Router(비용-밀도 공동 경계 라우터)

Action(행동): GX의 OOS profit/cost clue(표본외 수익/비용 단서)를 density/cost frontier(밀도/비용 경계)와 결합했습니다.

Effect(효과): `run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`에서 수익, 밀도, 비용을 함께 검토합니다.
<!-- run364HA__run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->

## run364HA Cost-Density Joint Frontier Router Review(비용-밀도 공동 경계 라우터 검토)

Action(행동): GZ의 OOS density/combined cost0.9(표본외 밀도/합산 비용0.9) 회복과 OOS profit/cost0.6(표본외 수익/비용0.6) 실패를 분리했습니다.

Effect(효과): `run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`에서 수익-밀도 재균형과 비용 바닥을 함께 탐색합니다.
<!-- run364HB__run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->

## run364HB OOS Profit-Density Rebalance Cost Floor Router(표본외 수익-밀도 재균형 비용 바닥 라우터)

Action(행동): HA의 수익/비용0.6 실패와 밀도/비용 단서를 HB 점수로 재균형했습니다.

Effect(효과): `run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`에서 profit repair(수익 수리), density repair(밀도 수리), cost floor(비용 바닥)를 분리 검토합니다.
<!-- run364HC__run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->

## run364HC OOS Profit-Density Rebalance Review(표본외 수익-밀도 재균형 검토)

Action(행동): HB를 GZ와 비교해 비용 개선과 밀도/수익 후퇴를 분리했습니다.

Effect(효과): `run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`에서 GZ anchor(GZ 기준점)와 HB profit rows(HB 수익 행)를 dual-surface switch(이중 표면 전환)로 결합합니다.
<!-- run364HD__run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->

## run364HD Dual-Surface Density-Profit Switch Router(이중 표면 밀도-수익 전환 라우터)

Action(행동): GZ 기준 기록에 HB 수익 대체 기록을 비겹침으로 붙였습니다.

Effect(효과): `run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`에서 수익 복구와 밀도 보존의 동시성을 검토합니다.
<!-- run364HE__run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->

## run364HE Dual-Surface Router Review(이중 표면 라우터 검토)

Action(행동): HD 근접 실패를 검토하고 package(패키지)는 열지 않았습니다.

Effect(효과): `run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`에서 수익/PF 미세 리프트를 시도합니다.
<!-- run364HF__run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1 -->

## run364HF Near-Miss Profit/PF Lift Switch Router(근접 실패 수익/PF 리프트 전환 라우터)

Action(행동): HD source neighborhood(HD 원천 이웃)에 validation-derived micro veto(검증 유래 미세 차단)를 적용했습니다.

Effect(효과): `run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`에서 strict proxy(엄격 프록시) 후보의 패키지 가능성과 과적합 위험을 검토합니다.
<!-- run364HG__run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1 -->

## run364HG Near-Miss Profit/PF Lift Review(근접 실패 수익/PF 리프트 검토)

Action(행동): HF strict proxy(HF 엄격 프록시)를 검토하고 package(패키지)는 열지 않았습니다.

Effect(효과): `run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1`에서 runtime capability inputs(런타임 기능 입력)를 구체화합니다.
<!-- run364HH__run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1 -->

## run364HH Runtime Capability Input Materialization(런타임 기능 입력 물질화)

Action(행동): HF/HG의 runtime capability inputs(런타임 기능 입력)를 계약과 목록으로 물질화했습니다.

Effect(효과): `run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1`에서 probability-bin veto(확률 구간 차단) EA 구현을 바로 시작할 수 있습니다.
<!-- run364HI__run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1 -->

## run364HI Probability-Bin Veto Runtime Support(확률 구간 차단 런타임 지원)

Action(행동): EA probability-bin veto(확률 구간 차단)를 구현하고 MetaEditor compile(메타에디터 컴파일)을 통과했습니다.

Effect(효과): `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`에서 runtime package(런타임 패키지)를 만들 수 있습니다.
<!-- run364HJ__run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1 -->

## run364HJ Probability-Bin Veto Runtime Package(확률 구간 거부 런타임 패키지)

Action(행동): GZ primary + HB fallback(GZ 우선 + HB 대체) ONNX(온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일)를 물질화했습니다.

Effect(효과): `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다. 운영 권위는 없습니다.
<!-- run364HK__run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->

## run364HK MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): probability-bin veto runtime package(확률 구간 거부 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시 대 MT5 차이) 또는 차단 원인(blocker, 차단 원인)을 검토할 수 있습니다.
<!-- run364HL__run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->

## run364HL Probability-Bin Veto MT5 Review(확률 구간 거부 MT5 검토)

Action(행동): HK MT5 probe(HK MT5 탐침)를 scope alignment(범위 정렬), route mix(라우트 혼합), density/side/cost guardrail(밀도/방향/비용 가드레일)로 검토했습니다.

Effect(효과): MT5 net/PF(순수익/수익 팩터) 단서는 보존하지만 trade density(거래 밀도)와 short-heavy(숏 편중)가 남아 `run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`에서 공격 탐색을 이어갑니다.
<!-- run364HM__run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->

## run364HM Probability-Bin Veto Density/Side/Cost Repair Scout(확률 구간 거부 밀도/방향/비용 수리 탐색)

Action(행동): Stage364 prior surfaces(Stage364 이전 표면)를 HL MT5 density ratio(HL MT5 밀도 비율)로 재평가했습니다.

Effect(효과): direct strict pass(직접 엄격 통과)는 0개지만, `run364FJ` single-source seed(단일 원천 씨앗)가 scaled density/cost/side(스케일 밀도/비용/방향) 수리 후보로 남아 `run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`로 넘깁니다.
<!-- run364HN__run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->

## run364HN Single-Source Package Review(단일 원천 패키지 검토)

Action(행동): HM selected FJ seed(HM 선택 FJ 씨앗)의 ONNX/joblib(온엑스/잡립), feature order(피처 순서), no-trade-splitting(거래 쪼개기 금지), cost/side guardrail(비용/방향 가드레일)을 검토했습니다.

Effect(효과): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`에서 single-source MT5 runtime package(단일 원천 MT5 런타임 패키지)를 물질화할 수 있습니다. 운영 권위는 없습니다.
<!-- run364HO__run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1 -->

## run364HO Single-Source Runtime Package(단일 원천 런타임 패키지)

Action(행동): FJ ONNX(FJ 온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일)를 물질화했습니다.

Effect(효과): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다. 운영 권위는 없습니다.
<!-- run364HP__run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->

## run364HP Single-Source MT5 Runtime Probe(단일 원천 MT5 런타임 탐침)

Action(행동): HO single-source probability-bin veto package(HO 단일 원천 확률 구간 거부 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시 대 MT5 차이) 또는 blocker(차단 원인)를 검토할 수 있습니다.
<!-- run364HQ__run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->

## run364HQ Single-Source MT5 Review(단일 원천 MT5 검토)

Action(행동): HP MT5 runtime probe(HP MT5 런타임 탐침)를 KPI/guardrail/attribution(KPI/가드레일/귀속)으로 검토했습니다.

Effect(효과): net profit(순수익) 양수 단서는 보존하지만 PF/expectancy/drawdown/density(PF/기대값/낙폭/밀도) 실패 때문에 `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`에서 trade quality density repair(거래 품질 밀도 수리)를 실행합니다.
<!-- run364HR__run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1 -->

## run364HR Trade-Quality Density Repair Scout(거래 품질 밀도 수리 탐색)

Action(행동): HP MT5 telemetry(HP MT5 런타임 기록)를 replay(재생)해 hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향) 수리 표면을 만들었습니다.

Effect(효과): strict joint pass(엄격 동시 통과)는 없지만 `hold4_margin_0.01` 같은 수리 단서를 `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1` 검토로 넘깁니다. 운영 권위는 없습니다.
