# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AQ_stage56_extratrees_model_axis_density_v1`
- current run(현재 실행): `run50AQ_stage56_extratrees_model_axis_density_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et40s25b`

## Latest Run50AQ Intermediate Evidence(최신 50AQ 중간 근거)

- packet(묶음): `stage56_run50AQ_extratrees_model_axis_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AQ_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AQ_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AQ_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AQ_extratrees_model_axis_density_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AQ(실행50AQ)는 ExtraTrees(엑스트라트리스) model-axis branch(모델 축 분기)다. Action(행동): leaf20/leaf40(잎 20/40) ExtraTrees(엑스트라트리스)를 Tier A only(Tier A 단독)와 A+B routed(A+B 라우팅)로 실제 MT5 validation/OOS(검증/표본외)에 걸었다. Effect(효과): `et40s25b`는 OOS net/PF(표본외 순손익/수익 팩터) 단서를 만들었지만 validation density/PF(검증 밀도/수익 팩터), OOS density(표본외 밀도), cost(비용), same-move survival(동일 이동 생존), Tier B fallback damage(Tier B 대체 손상) 때문에 selected_research_baseline(선택 연구 기준선)이 아니다.

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 없으면 계속 open(열림)이다. 이번 파일은 reviewed_closed(검토 후 종료)가 아니다.
