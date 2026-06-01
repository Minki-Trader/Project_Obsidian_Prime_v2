# run360C Materialized Input Review(360C 구체화 입력 검토)

- run_id(실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run360B_materialize_regime_stability_pivot_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run361A_design_long_only_cost_buffer_probe_without_db_v1`
- status(상태): `reviewed_stage360C_regime_stability_inputs_long_only_seed_stage361_opened_no_selection_no_mt5`
- judgment(판정): `long_only_edge_positive_but_cost_fragile_stage361_seed_no_candidate_selection`
- gate_result(게이트 결과): `9/9`
- claim_boundary(주장 경계): `review_only_report_derived_stage_branch_no_new_model_training_no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Decision(결정)

Action(행동): `q05 long-only(롱 단독)`을 Stage361(361단계)의 primary seed(주 씨앗)로 분기했다.

Effect(효과): Stage360(360단계)의 OOS positive clue(표본외 긍정 단서)를 운영 후보로 승격하지 않고, cost buffer(비용 버퍼)를 회복하는 새 탐색 질문으로 넘긴다.

## Evidence(근거)

- q05 long-only validation(검증): net(순수익) `45.97`, PF(수익 팩터) `1.0257607173`, trades(거래) `642`, density(밀도) `3.5081967213`
- q05 long-only OOS(표본외): net(순수익) `237.56`, PF(수익 팩터) `1.1843780075`, trades(거래) `472`, density(밀도) `3.6030534351`
- q05 long-only +0.30 cost validation(+0.30 비용 검증): net(순수익) `-146.63`, survives(생존) `no`
- q05 no-late(후반 제외) OOS(표본외): net(순수익) `305.66`, 그러나 validation(검증): `-449.38`

## Judgment(판정)

Action(행동): `no-late(후반 제외)`, `late-only(후반 단독)`, `short-only(숏 단독)`을 failure memory(실패 기억)로 낮췄다.

Effect(효과): 다음 stage(단계)는 session hard veto(고정 세션 제외)나 short density filler(숏 밀도 채우기)를 반복하지 않고, long-only margin/regime/label(롱 단독 마진/국면/라벨) 탐색으로 간다.

## Stage361 Scope(361단계 범위)

- primary question(주 질문): q05 long-only edge(q05 롱 단독 우위)가 +0.30 cost buffer(+0.30 비용 버퍼)를 회복할 수 있는가?
- required guardrail(필수 가드레일): `trade_per_day_min_3_to_10_plus_no_trade_splitting`
- proxy/MT5 rule(프록시/MT5 규칙): proxy(프록시)를 만들면 MT5 runtime probe(MT5 런타임 탐침)와 비교해야 한다.
- operating claim(운영 주장): none(없음)
