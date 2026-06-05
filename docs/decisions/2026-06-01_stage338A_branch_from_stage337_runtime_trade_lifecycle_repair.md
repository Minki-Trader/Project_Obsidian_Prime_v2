# 2026-06-01 Stage338A Branch Decision(338A 분기 결정)

- decision(결정): `stage338A_open_run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair`
- from(출발): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild` / `run337JR_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db_v1`
- to(도착): `338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair` / `run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_without_db_v1`
- reason(이유): Stage337(337단계)이 너무 무거워졌고, 다음 질문은 trade lifecycle repair(거래 생명주기 수리)다.
- evidence(근거): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/final_decision.json`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_mt5_runtime_probe_review_scorecard.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_failure_memory_and_repair_constraints.csv`

Action(행동): Stage338(338단계)을 새 canonical stage(정식 단계)로 열었다.
Effect(효과): 실패 기억은 보존하고, stage scope(단계 범위)는 가볍게 만든다.

claim_boundary(주장 경계): `state_sync_stage_branch_only_no_model_selection_no_training_no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
