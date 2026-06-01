# Stage362 Input Refs(362단계 입력 참조)

- source_final_decision(원천 최종 결정): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/final_decision.json`
- source_materialization_queue(원천 구체화 대기열): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/run361B_materialization_queue.csv`
- source_margin_grid_plan(원천 마진 격자 계획): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/margin_grid_plan.csv`
- source_evidence_snapshot(원천 근거 스냅샷): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/source_evidence_snapshot.csv`
- source_gate_audit(원천 게이트 감사): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/required_gate_coverage_audit.csv`
- source_report(원천 보고서): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/03_reviews/run361A_long_only_cost_buffer_design.md`
- input_manifest(입력 목록): `stages/362_long_only_margin_grid__cost_buffer_first_branch/01_inputs/stage362_input_manifest.csv`

Action(행동): Stage361A(361A 실행)의 5개 materialization queue(구체화 대기열) 중 첫 번째 margin grid(마진 격자) 입력만 Stage362(362단계)의 직접 입력으로 둔다.

Effect(효과): Stage362B(362B 실행)는 q05 long-only margin grid(q05 롱 단독 마진 격자)만 materialize(구체화)하므로 실행 단위가 작아진다.
