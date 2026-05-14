# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AZ_stage56_cooldown12_broad_model_source_v1`
- current run(현재 실행): `run50AZ_stage56_cooldown12_broad_model_source_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `nf250c12_h4_s160l090_a`

## Latest Run50AZ Intermediate Evidence(최신 50AZ 중간 근거)

- packet(묶음): `stage56_run50AZ_cooldown12_broad_model_source_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AZ_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AZ_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AZ_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AZ_cooldown12_broad_model_source_v1/aggregate_summary.json`

Best read(최선 판독) `nf250c12_h4_s160l090_a` validation/OOS(검증/표본외) trades/day(일 거래 수) `4.513661` / `3.035897`, PF(수익 팩터) `1.03` / `0.91`, net(순손익) `45.74` / `-118.83`이다.

Failure(실패): validation_density(검증 밀도), oos_density(표본외 밀도), oos_net_positive(표본외 순손익 양수), validation_pf(검증 수익 팩터), oos_pf(표본외 수익 팩터), cost_stressed_expectancy(비용 압박 기대값), same_move_density(동일 이동 밀도). Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
