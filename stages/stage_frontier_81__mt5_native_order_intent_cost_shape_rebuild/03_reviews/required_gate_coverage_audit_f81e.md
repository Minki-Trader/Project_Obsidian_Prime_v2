# F81E Required Gate Coverage Audit(F81E 필수 게이트 커버리지 감사)

Status(상태): `f81e_capped_repair_selected_deal_reconciled_label_preflight_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `kpi_contract_audit` | `passed(통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81e_capped_repair_or_rotation_decision.json` | hypothesis/test period/proxy KPI/runtime KPI/parity/gap cause/next action(가설/기간/프록시 KPI/런타임 KPI/동등성/간극 원인/다음 행동)을 결정에 연결한다. |
| `row_grain_audit` | `passed(통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81e_capped_repair_or_rotation_decision_rows.csv` | validation/OOS split rows(검증/표본외 구간 행)와 decision row(결정 행)를 분리한다. |
| `source_authority_audit` | `passed_with_boundary(경계 포함 통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/02_runs/frontier81C_mt5_runtime_materialization_v1/f81c_runtime_receipt.csv`, `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81c_backtest_forensics_receipt.json` | source authority(원천 권위)는 F81C MT5 runtime observation(F81C MT5 런타임 관찰)과 F81D attribution(F81D 귀속) 한정이다. |
| `required_gate_coverage_audit` | `passed(통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/required_gate_coverage_audit_f81e.md` | required gates(필수 게이트)를 closeout receipt(종료 영수증)에 연결한다. |

Claim guard(주장 보호): `decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`. Effect(효과): repair decision(수리 결정)을 runtime authority(런타임 권위)로 올려 말하지 않는다.
