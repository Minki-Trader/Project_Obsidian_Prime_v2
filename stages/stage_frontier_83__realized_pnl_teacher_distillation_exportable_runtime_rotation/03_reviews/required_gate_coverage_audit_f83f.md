# F83F Required Gate Coverage Audit(F83F 필수 게이트 커버리지 감사)

Status(상태): `f83f_gap_attributed_runtime_winrate_erosion_after_signal_parity_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `parent_runtime_evidence(부모 런타임 근거)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83e_short_side_density_runtime_materialization_summary.json`, `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83E_short_side_density_runtime_materialization_v1/f83e_runtime_receipt.csv` | F83E Strategy Tester(전략 테스터) 2/2 완료 근거를 사용한다. |
| `proxy_runtime_gap_rows(프록시/런타임 간극 행)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_short_density_proxy_runtime_gap_rows.csv` | validation/OOS(검증/외표본) 차이를 행 단위로 기록한다. |
| `gap_cause_attribution(간극 원인 귀속)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_gap_cause_attribution_rows.csv` | fill gap(체결 간극)보다 win-rate/DD erosion(승률/손실폭 침식)이 주 원인임을 분리한다. |
| `runtime_report_identity(런타임 보고서 정체성)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_short_density_proxy_runtime_gap_analysis_summary.json` | Windows long path(윈도우 긴 경로) report(보고서)를 io_path(입출력 경로)로 확인한다. |
| `run_evidence_receipt(실행 근거 영수증)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_run_evidence_receipt.yaml` | KPI/정체성/판정 경계를 남긴다. |
| `performance_attribution_receipt(성과 귀속 영수증)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_performance_attribution_receipt.yaml` | 관찰 변화와 대안 설명을 분리한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_result_judgment_receipt.yaml` | negative(부정)과 invalid(무효)를 혼동하지 않는다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83f_task_force_review_receipt.yaml` | 8명 agent(요원) 검토를 기록한다. |
| `negative_memory_record(부정 기억 기록)` | `passed(통과)` | `docs/registers/negative_result_register.md#NR-FR83-SHORT-DENSITY-RUNTIME-WINRATE-EROSION` | 반복 금지와 재개 조건을 남긴다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `gap_attribution_negative_memory_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | 권위/승격/완성 주장을 만들지 않는다. |
