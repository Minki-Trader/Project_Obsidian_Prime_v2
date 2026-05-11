# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed`
- latest_run_id(최신 실행 ID): `stage56_closeout_v1`
- current run(현재 실행): `run50C_logreg_bracket_micro_grid_v1`
- current_judgment(현재 판정): `baseline_candidate_only`
- selected_research_baseline(선택 연구 기준선): `none`
- baseline_candidate_only(기준선 후보 전용): `d38h10_logreg_bracket_micro_grid`
- selected_shadow_candidate(선택 그림자 후보): `none`
- dense_engine_candidate(두꺼운 엔진 후보): `d38h10`
- preserved_density_frontier(보존 밀도 경계): `d35h07_routed_density_failed_quality`
- preserved_quality_frontier(보존 품질 경계): `d38h10_weak_routed_dense_engine_candidate`
- current_operating_reference(현재 운영 참조): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_promotion(운영 승격): `none`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Closeout Evidence(종료 근거)

- run50C(실행50C) LogReg(로지스틱 회귀) bracket micro-grid(구간 미세 격자)는 실제 MT5 closed trades(메타트레이더5 청산 거래) 기준으로 5개 variant(변형)를 비교했다.
- best candidate(최선 후보): `d38h10`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 817 trades(거래), 4.464481 trades/day(일 거래 수), net(순손익) 190.38, PF(수익 팩터) 1.07
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 672 trades(거래), 3.446154 trades/day(일 거래 수), net(순손익) 302.10, PF(수익 팩터) 1.13
- Tier B fallback(Tier B 대체) used bars(사용 봉): validation 2366, OOS 1062
- closeout packet(종료 묶음): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/stage56_closeout_packet.md`

## Next Condition(다음 조건)

다음 stage(단계)는 `d38h10`을 density/quality repair(밀도/품질 보정) 또는 WFO revalidation(워크포워드 재검증) 대상으로 열 수 있다. 효과(effect, 효과): 후보는 보존하지만 selected_research_baseline(선택 연구 기준선), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 만들지 않는다.
