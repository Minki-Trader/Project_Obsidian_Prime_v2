# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AS_stage56_extratrees_rearm_real_density_guard_v1`
- current run(현재 실행): `run50AS_stage56_extratrees_rearm_real_density_guard_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et40h6_r030_b`

## Latest Run50AS Intermediate Evidence(최신 50AS 중간 근거)

- packet(묶음): `stage56_run50AS_extratrees_rearm_real_density_guard_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AS_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AS_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AS_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AS_extratrees_rearm_real_density_guard_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AS(실행50AS)는 ExtraTrees(엑스트라트리스) rearm/transition guard(재허용/전환 가드) 묶음이다. Action(행동): leaf40(잎 40) `et40s25_c0_h6_a` 계열에 entry transition gate(진입 전환 게이트)와 confidence rearm delta(신뢰도 재허용 증가폭)를 실제 MT5 validation/OOS(검증/표본외)에 걸었다. Effect(효과): `et40h6_r030_b`는 validation/OOS(검증/표본외) PF(수익 팩터) `1.16` / `1.39`와 net(순손익) `385.93` / `639.18`로 품질은 개선했지만 OOS density(표본외 밀도) `3.892308`, same-move ratio(동일 이동 비율) `0.573386` / `0.552042`, cooldown survival(쿨다운 생존) 실패 때문에 selected_research_baseline(선택 연구 기준선)이 아니다.

Run50AS attribution(실행50AS 기여도): `et40h6_r030_b`와 `et40h6_r015_a`는 OOS(표본외) major buckets(주요 구간)가 양수다. Effect(효과): 단순 market-state filter(시장 상태 필터)보다 model granularity/source(모델 세분도/원천) 변경으로 transition-gated density(전환 게이트 밀도)를 회복하는 run50AT(실행50AT)가 다음 분기다.

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 없으면 계속 open(열림)이다. 이번 파일은 reviewed_closed(검토 후 종료)가 아니다.
