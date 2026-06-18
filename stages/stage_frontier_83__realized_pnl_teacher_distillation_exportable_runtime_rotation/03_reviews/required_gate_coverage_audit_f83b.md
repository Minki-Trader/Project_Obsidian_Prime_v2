# F83B Required Gate Coverage Audit(F83B 필수 게이트 커버리지 감사)

Status(상태): `completed_mt5_runtime_materialization_observation_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target(물질화 대상)` | `passed(통과)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83b_runtime_materialization_target_selection.json` | F83A best seed(F83A 최선 씨앗)만 물질화한다. |
| `onnx_probability_parity(온엑스 확률 동등성)` | `3` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1/f83b_probability_parity.csv` | F83A raw ONNX(원본 온엑스)와 patched ONNX(패치 온엑스)를 비교한다. |
| `runtime_signal_veto_parity(런타임 신호 차단 동등성)` | `3` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1/f83b_signal_parity.csv` | F83A 선택 진입 시각이 MT5 입력으로 보존되는지 확인한다. |
| `source_reproduction(원천 재현)` | `3` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1/f83b_source_reproduction.csv` | F83A validation/OOS(검증/표본외) 거래 수를 재현한다. |
| `strategy_tester_attempt(전략 테스터 시도)` | `2/2` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/02_runs/frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1/run_manifest.json` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `recorded(기록됨)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83b_backtest_forensics_receipt.json` | tester identity/report gap(테스터 정체성/보고서 간극)을 분리한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `recorded(기록됨)` | `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/f83b_task_force_review_receipt.yaml` | 8명 agent(요원) 검토와 local verification(로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | 런타임 권위/실거래 준비를 만들지 않는다. |
