# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50BG_stage56_context_timed_hold3_topup_v1`
- current run(현재 실행): `run50BG_stage56_context_timed_hold3_topup_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `v40_v22_slot3_5_8_relax_h3c0_no_b`

## Latest Run50BG Intermediate Evidence(최신 50BG 중간 근거)

- packet(작업 묶음): `stage56_run50BG_context_timed_hold3_topup_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BG_context_timed_hold3_topup.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BG_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BG_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50BG_context_timed_hold3_topup_v1/aggregate_summary.json`

Best read(최선 판독) `v40_v22_slot3_5_8_relax_h3c0_no_b` validation/OOS(검증/표본외) trades/day(일 거래 수) `6.688525` / `4.666667`, PF(수익 팩터) `1.150000` / `0.950000`, net(순손익) `409.35` / `-108.13`이다.

Failure(실패): `oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
