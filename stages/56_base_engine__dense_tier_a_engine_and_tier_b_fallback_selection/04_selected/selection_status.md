# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AR_stage56_extratrees_validation_density_repair_v1`
- current run(현재 실행): `run50AR_stage56_extratrees_validation_density_repair_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et40s25_c0_h6_a`

## Latest Run50AR Intermediate Evidence(최신 50AR 중간 근거)

- packet(묶음): `stage56_run50AR_extratrees_validation_density_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AR_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AR_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AR_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AR_extratrees_validation_density_repair_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AR(실행50AR)는 ExtraTrees(엑스트라트리스) validation-density repair(검증-밀도 수정) 묶음이다. Action(행동): leaf40(잎 40) A-only(A 단독)에서 cooldown(쿨다운), hold(보유), ADX weak-trend firewall(ADX 약추세 방화벽), Tier B comparison(Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)에 걸었다. Effect(효과): `et40s25_c0_h6_a`는 density(밀도)는 통과했지만 validation PF/cost(검증 수익 팩터/비용)와 same-move survival(동일 이동 생존)이 실패해 selected_research_baseline(선택 연구 기준선)이 아니다.

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 없으면 계속 open(열림)이다. 이번 파일은 reviewed_closed(검토 후 종료)가 아니다.
