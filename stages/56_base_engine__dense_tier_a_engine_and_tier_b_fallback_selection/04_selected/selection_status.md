# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AX_stage56_source_composite_density_quality_v1`
- current run(현재 실행): `run50AX_stage56_source_composite_density_quality_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `v02_s45_primary_s47_flatfill_h4c6`

## Latest Run50AX Intermediate Evidence(최신 50AX 중간 근거)

- packet(묶음): `stage56_run50AX_source_composite_density_quality_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AX_source_composite_density_quality.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AX_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AX_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AX_source_composite_density_quality_v1/aggregate_summary.json`

Best read(최선 판독) `v02_s45_primary_s47_flatfill_h4c6` validation/OOS(검증/표본외) trades/day(일 거래 수) `7.770492` / `5.046154`, PF(수익 팩터) `1.010000` / `1.020000`, net(순손익) `34.380000` / `34.010000`이다.

Failure(실패): `validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
