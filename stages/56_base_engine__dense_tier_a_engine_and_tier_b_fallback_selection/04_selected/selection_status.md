# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
- current run(현재 실행): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `et20h6_r030_b`

## Latest Run50AT Intermediate Evidence(최신 50AT 중간 근거)

- packet(묶음): `stage56_run50AT_extratrees_leaf_granularity_transition_density_source_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AT_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AT_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AT_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AT_extratrees_leaf_granularity_transition_density_source_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AT(실행50AT)는 ExtraTrees(엑스트라트리스) leaf granularity/source(잎 세분도/원천) 묶음이다. Action(행동): leaf20/leaf30/leaf60(잎 20/30/60) ExtraTrees(엑스트라트리스)에 entry transition gate(진입 전환 게이트)를 유지한 채 실제 MT5 validation/OOS(검증/표본외)를 실행했다. Effect(효과): `et20h6_r030_b`는 validation/OOS(검증/표본외) PF(수익 팩터) `1.13` / `1.13`과 net(순손익) `346.02` / `249.83`이지만 OOS density(표본외 밀도) `4.271795`, cost-stressed expectancy(비용 압박 기대값) `-0.184000` / `-0.200084`, same-move ratio(동일 이동 비율) `0.581735` / `0.596639` 때문에 selected_research_baseline(선택 연구 기준선)이 아니다.

Run50AT attribution(실행50AT 기여도): `et20h6_r030_b`는 OOS(표본외) adx_gt25(ADX 25 초과)와 vol_high(고변동)가 약하고, `et20h6_r015_b`는 OOS late session(후반 세션)과 vol_high(고변동)가 약하다. Effect(효과): ExtraTrees(엑스트라트리스) market-state filter(시장 상태 필터)는 밀도를 더 줄 가능성이 높아, 다음 분기는 QDA composite route(QDA 합성 라우트) density repair(밀도 수정)로 넘긴다.

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 없으면 계속 open(열림)이다. 이번 파일은 reviewed_closed(검토 후 종료)가 아니다.
