# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50BP_stage56_extratrees_slot_lifecycle_v1`
- current run(현재 실행): `run50BP_stage56_extratrees_slot_lifecycle_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `v54_et40_slot20_first_h2c0_no_b`

## Latest Run50BP Intermediate Evidence(최신 50BP 중간 근거)

- packet(묶음): `stage56_run50BP_extratrees_slot_lifecycle_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BP_extratrees_slot_lifecycle.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BP_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BP_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50BP_extratrees_slot_lifecycle_v1/aggregate_summary.json`

Best read(최선 판독) `v54_et40_slot20_first_h2c0_no_b` validation/OOS(검증/표본외) trades/day(일 거래) `9.306011` / `7.205128`, PF(수익 팩터) `1.000000` / `1.000000`, net(순손익) `2.740000` / `-9.720000`이다.

Failure(실패): `oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
