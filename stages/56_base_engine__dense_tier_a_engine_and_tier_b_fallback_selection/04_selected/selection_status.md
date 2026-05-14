# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AV_stage56_cooldown12_new_source_density_survival_v1`
- current run(현재 실행): `run50AV_stage56_cooldown12_new_source_density_survival_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `nf200c12_h4_s240l150_a`

## Latest Run50AV Intermediate Evidence(최신 50AV 중간 근거)

- packet(묶음): `stage56_run50AV_cooldown12_new_source_density_survival_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AV_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AV_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AV_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AV_cooldown12_new_source_density_survival_v1/aggregate_summary.json`

Run50AV(실행50AV)는 actual cooldown12 new source density survival(실제 12봉 쿨다운 새 원천 밀도 생존) 묶음이다. Effect(효과): selected_research_baseline(선택 연구 기준선)이 없으면 Stage56(56단계)은 계속 open(열림)이다.

Best overall(전체 최선) `nf200c12_h4_s240l150_a`은 validation/OOS(검증/표본외) trades/day(일 거래 수) `4.295082` / `3.041026`, PF(수익 팩터) `1.29` / `1.01`, net(순손익) `435.08` / `7.66`이다. Failure(실패): validation/OOS density(검증/표본외 밀도), OOS PF(표본외 수익 팩터), OOS cost-stressed expectancy(표본외 비용 압박 기대값)가 부족해 selected_research_baseline(선택 연구 기준선)이 아니다.

Real density(실제 밀도): same-move ratio(동일 이동 비율)는 `0.133221`~`0.209738`까지 낮아졌지만 cooldown density(쿨다운 후 밀도)는 최고 validation/OOS(검증/표본외) `3.655738` / `2.635897`에 머물렀다. Effect(효과): actual cooldown12(실제 12봉 쿨다운)는 split re-entry(분할 재진입)를 줄였지만 현재 source(원천)는 5/day(일 5회) 독립 기회를 만들지 못했다.

Attribution(기여도): `nf200c12_h4_s240l150_a` OOS(표본외)는 early/vol_high(초반/고변동)이 강하고 late/vol_low(후반/저변동)가 약하다. `et40c12_h4_s220l140_b` OOS(표본외)는 early/downtrend/adx_gt25(초반/하락 추세/ADX 25 초과)가 강하지만 validation(검증)에서 mid/range/adx_20_25(중간/횡보/ADX 20-25)가 손상됐다. Effect(효과): 다음은 `run50AW_independent_event_source_route_branch`에서 독립 event source(이벤트 원천)를 라우팅 원천으로 열어야 한다.
