# Stage357 High-Density Label Pivot(357단계 고밀도 라벨 전환)

- canonical_stage_id(정식 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- current_run_id(현재 실행 ID): `run357B_design_high_density_label_pivot_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run357A_branch_stage356_to_high_density_label_pivot_without_db_v1`
- source_stage_id(원천 단계 ID): `356_density_recovery_training__proxy_model_queue_scout`
- source_run_id(원천 실행 ID): `run356C_expand_density_recovery_proxy_training_search_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run356D_design_high_density_label_pivot_without_db_v1`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_high_density_label_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Stage356C(356C 실행)에서 trade/day(일별 거래수) 3 미만으로 막힌 density recovery(밀도 회복)를 H12 train-quantile high-density label(학습 분위수 고밀도 H12 라벨)과 ONNX classifier(온엑스 분류기)로 회복할 수 있는가?

## Source Truth(원천 진실)

- trained_regression_models(학습 회귀 모델): `12`
- onnx_parity_rows(온엑스 동등성 행): `12`
- regression_paired_rows(회귀 쌍 탐색 행): `2268`
- union_paired_rows(합집합 쌍 탐색 행): `1`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `0`
- best_validation_trade_per_day(최선 검증 일별 거래수): `2.4451219512195124`
- best_validation_stress_pf(최선 검증 압박 수익 팩터): `1.013945130731893`
- best_oos_trade_per_day(최선 표본외 일별 거래수): `2.6814159292035398`
- best_oos_stress_pf(최선 표본외 압박 수익 팩터): `1.0744976620172675`
- candidate_gate(후보 게이트): `failed_proxy_scout_queue(프록시 탐색 대기열 실패)`

## Scope(범위)

Stage357(357단계)는 high-density label pivot(고밀도 라벨 전환), ONNX classifier parity(온엑스 분류기 동등성), non-overlap proxy queue(비중첩 프록시 대기열)까지만 다룬다. MT5 runtime probe(MT5 런타임 탐침)는 positive queue(긍정 대기열)가 생긴 뒤 별도 run(실행)에서 다룬다.

## Exploration Plan(탐색 계획)

- idea_id(아이디어 ID): `IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT`
- hypothesis(가설): H12 train-quantile band label(학습 분위수 H12 밴드 라벨)이 trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3+와 positive stress net/PF(양수 압박 순수익/수익 팩터)를 동시에 회복한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): q40/q60, q45/q55 label bands(라벨 밴드), shallow ExtraTrees classifier(얕은 엑스트라트리스 분류기), probability score policy(확률 점수 정책), ADX/session filter(ADX/세션 필터)
- extreme_sweep(극단 탐색): no-flat sign label(무평탄 방향 라벨), soft cost flat label(완화 비용 평탄 라벨), low score quantile(낮은 점수 분위수), high ADX(높은 ADX)
- micro_search_gate(미세 탐색 게이트): validation/OOS proxy trade/day(검증/표본외 프록시 일별 거래수) 3+와 stress PF(압박 수익 팩터) 1.02+
- wfo_plan(WFO 계획): scout pass(탐색 회차) 뒤 WFO(walk-forward optimization, 워크포워드 최적화) 프레임으로 재검증
- failure_memory(실패 기억): Stage356C(356C 실행)는 OOS PF(표본외 수익 팩터)는 양수였지만 validation PF(검증 수익 팩터)와 trade/day(일별 거래수)가 후보 게이트를 넘지 못했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## Density Constraint(밀도 제약)

`trade_per_day_min_3_to_10_plus_no_trade_splitting`

Action(행동): trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3~10+ 조건을 Stage357B(357B 실행)의 기본 제약으로 둔다.

Effect(효과): 낮은 거래수로 예쁜 net profit(순수익)을 만든 후보가 운영 후보처럼 보이지 않게 한다.
