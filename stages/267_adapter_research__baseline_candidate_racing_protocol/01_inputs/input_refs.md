# Stage267 Input References(267단계 입력 참조)

- superseded_stage(대체된 단계): `266_adapter_research__late_segment_stability_repair_after_stage265_review`
- superseded_run(대체된 실행): `run266A_stage266_late_segment_stability_repair_after_stage265_review_v1`
- superseded_boundary(대체 경계): `planning_only_no_run_execution_no_result_judgment`
- durable_decision(지속 판정): `docs/decisions/2026-05-20_stage266_superseded_stage267_baseline_racing_open.md`
- candidate_pool_manifest(후보군 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/01_inputs/baseline_candidate_pool.csv`
- experiment_design_receipt(실험 설계 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_experiment_design_receipt.md`

## Source Evidence(원천 근거)

- Stage258(258단계) `s258_short_tight_control`: `stages/258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff/03_reviews/stage258_quality_matrix.csv`
- Stage258(258단계) source KPI(원천 핵심 성과 지표): `stages/258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff/03_reviews/stage258_source_feature_kpi_summary.csv`
- Stage258(258단계) monthly/segment/equity risk(월별/구간/평가금 위험): `stages/258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff/03_reviews/`
- Stage262(262단계) `s262_lowrank_inner_half_filter`: `stages/262_adapter_research__lowrank_lowedge_oos_recovery_repair/03_reviews/stage262_quality_matrix.csv`
- Stage262(262단계) source KPI(원천 핵심 성과 지표): `stages/262_adapter_research__lowrank_lowedge_oos_recovery_repair/03_reviews/stage262_source_feature_kpi_summary.csv`
- Stage264(264단계) `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s264_allow_inner_all_oos_anchor`: `stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/03_reviews/stage264_quality_matrix.csv`
- Stage264(264단계) source KPI(원천 핵심 성과 지표): `stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/03_reviews/stage264_source_feature_kpi_summary.csv`
- Stage265(265단계) candidate review(후보 검토): `stages/265_adapter_research__stage264_dual_objective_followup_review/03_reviews/stage265_stage264_dual_objective_followup_review.md`
- Stage265(265단계) failure memory(실패 기억): `stages/265_adapter_research__stage264_dual_objective_followup_review/03_reviews/stage265_failure_memory.csv`

Effect(효과): Stage267(267단계)는 기존 후보의 headline KPI(표면 핵심 성과 지표)만 보지 않고, source evidence(원천 근거), segment weakness(구간 약점), monthly weakness(월별 약점), drawdown/recovery(손실폭/회복), Tier B disabled state(티어 B 비활성 상태)를 함께 읽는다.
