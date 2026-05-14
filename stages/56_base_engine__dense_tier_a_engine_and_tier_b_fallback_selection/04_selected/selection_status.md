# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50BH_stage56_extratrees_light_rearm_density_recovery_v1`
- current run(현재 실행): `run50BH_stage56_extratrees_light_rearm_density_recovery_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et40h6_r001_a`

## Latest Run50BH Intermediate Evidence(최신 50BH 중간 근거)

- packet(작업 묶음): `stage56_run50BH_extratrees_light_rearm_density_recovery_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BH_extratrees_light_rearm_density_recovery.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BH_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BH_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50BH_extratrees_light_rearm_density_recovery_v1/aggregate_summary.json`

Best read(최선 판독) `et40h6_r001_a` validation/OOS(검증/표본외) trades/day(일 거래 수) `6.846995` / `5.102564`, PF(수익 팩터) `1.100000` / `1.260000`, net(순손익) `313.49` / `613.58`이다.

Failure(실패): `cost_stressed_expectancy;same_move_density;tier_b_rule`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.

## Next Branch(다음 분기)

`run50BI_et40h6_r001_validation_cost_same_move_repair`를 연다. Effect(효과): run50BH(실행50BH)가 보여준 OOS density/PF/net(표본외 밀도/수익 팩터/순손익)을 보존하면서 validation cost(검증 비용), same-move split(동일 이동 분할), Tier B disablement evidence(Tier B 비활성 근거)를 보정한다.
