# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AU_stage56_composite_qda_route_density_repair_v1`
- current run(현재 실행): `run50AU_stage56_composite_qda_route_density_repair_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `qda85_s800_flat_trans_r060_h8`

## Latest Run50AU Intermediate Evidence(최신 50AU 중간 근거)

- packet(묶음): `stage56_run50AU_composite_qda_route_density_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AU_composite_qda_route_density_repair.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AU_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AU_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AU_composite_qda_route_density_repair_v1/aggregate_summary.json`

Run50AU(실행50AU)는 QDA composite route density repair(QDA 합성 라우트 밀도 수정) 묶음이다. Effect(효과): selected_research_baseline(선택 연구 기준선)이 없으면 Stage56(56단계)은 계속 open(열림)이다.

Best quality(최선 품질) `qda85_s800_flat_trans_r060_h8`은 validation/OOS(검증/표본외) trades/day(일 거래 수) `5.262295` / `3.389744`, PF(수익 팩터) `1.11` / `1.12`, net(순손익) `277.91` / `213.64`이다. Failure(실패): OOS density(표본외 밀도), cost-stressed expectancy(비용 압박 기대값), same-move density(동일 이동 밀도)가 부족해 selected_research_baseline(선택 연구 기준선)이 아니다.

Closest density(밀도 최접근) `qda85_s800_flat_trans_r030_h6`은 validation/OOS(검증/표본외) trades/day(일 거래 수) `6.726776` / `4.405128`까지 올라갔지만 PF(수익 팩터) `1.06` / `1.07`과 cost-stressed expectancy(비용 압박 기대값) `-0.365613` / `-0.334680` 때문에 실패했다. Effect(효과): QDA route threshold repair(QDA 라우트 문턱값 수정)는 density(밀도)를 조금 보탰지만 hardening(경화)할 후보가 아니다.

Attribution(기여도): quality branch(품질 분기)는 OOS range/adx_lt20(표본외 횡보/ADX 20 미만)이 강하고, density branch(밀도 분기)는 OOS early/adx_20_25(표본외 초반/ADX 20-25)가 강하다. Effect(효과): 단순 filter(필터)는 필요한 5/day(일 5회) 밀도를 더 깎을 가능성이 높아 다음은 `run50AV_new_source_density_survival_branch`로 연다.
