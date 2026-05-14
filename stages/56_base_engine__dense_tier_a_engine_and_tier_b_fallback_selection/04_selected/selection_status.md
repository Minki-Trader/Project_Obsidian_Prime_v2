# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50BI_stage56_extratrees_raw_density_microcooldown_v1`
- current run(현재 실행): `run50BI_stage56_extratrees_raw_density_microcooldown_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et40h4c6_s240l150_r001_a`
- current_frontier_candidate(현재 최전선 후보): `run50BH/et40h6_r001_a`

## Latest Run50BI Intermediate Evidence(최신 50BI 중간 근거)

- packet(작업 묶음): `stage56_run50BI_extratrees_raw_density_microcooldown_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BI_extratrees_raw_density_microcooldown.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BI_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BI_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50BI_extratrees_raw_density_microcooldown_v1/aggregate_summary.json`

Latest best read(최신 최선 판독) `et40h4c6_s240l150_r001_a` validation/OOS(검증/표본외) trades/day(일 거래 수) `4.579235` / `3.435897`, PF(수익 팩터) `1.060000` / `1.270000`, net(순손익) `119.63` / `367.74`이다.

Failure(실패): `validation_density;oos_density;validation_pf;cost_stressed_expectancy;same_move_density;tier_b_rule`. Effect(효과): run50BI(실행50BI)는 selected_research_baseline(선택 연구 기준선)을 만들지 않고, raw-density/cooldown(원시 밀도/쿨다운) 보정만으로는 run50BH(실행50BH)의 병목을 해결하기 어렵다는 failure_memory(실패 기억)로 남긴다.

Current frontier(현재 최전선): `run50BH/et40h6_r001_a`는 validation/OOS(검증/표본외) trades/day(일 거래 수) `6.846995` / `5.102564`, PF(수익 팩터) `1.100000` / `1.260000`, net(순손익) `313.49` / `613.58`로 nominal density/PF/net(명목 밀도/수익 팩터/순손익)은 가장 낫지만, cost stress(비용 압박), same-move survival(동일 이동 생존), Tier B evidence(Tier B 근거)가 부족하다.

## Next Branch(다음 분기)

`run50BJ_cooldown_aware_independent_source_branch`를 연다. Effect(효과): 같은 ExtraTrees(엑스트라트리스) threshold/cooldown(문턱값/쿨다운) 축을 더 닦는 대신, 12봉 cooldown survival(쿨다운 생존)을 모델 원천(source, 원천) 단계에서 늘릴 수 있는 별도 기회 원천을 시험한다.
