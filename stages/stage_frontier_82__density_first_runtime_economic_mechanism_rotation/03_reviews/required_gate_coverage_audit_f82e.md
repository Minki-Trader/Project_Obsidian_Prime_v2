# F82E Required Gate Coverage Audit(F82E 필수 게이트 커버리지 감사)

Status(상태): `f82e_capped_repair_selected_deal_reconciled_runtime_label_preflight_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `kpi_contract_audit(KPI 계약 감사)` | `passed(통과)` | `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82e_capped_repair_or_rotation_decision.json`, `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/frontier82E_capped_repair_or_rotation_decision_report.md` | proxy/runtime KPI(프록시/런타임 KPI), gross/win/payoff/expectancy(총손익/승률/손익비/기대값)를 함께 기록한다. |
| `row_grain_audit(행 단위 감사)` | `passed(통과)` | `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82e_capped_repair_or_rotation_decision_rows.csv` | validation/OOS/decision(검증/표본외/결정)을 분리한다. |
| `source_authority_audit(원천 권위 감사)` | `passed_with_boundary(경계 통과)` | `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/02_runs/frontier82C_mt5_runtime_materialization_v1/f82c_runtime_receipt.csv`, `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82d_proxy_runtime_gap_attribution.json` | MT5 output(출력)은 관찰 근거이고 권위가 아니다. |
| `task_force_review_packet(태스크포스 검토 묶음)` | `passed(통과)` | `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82e_task_force_review_receipt.yaml` | agent(요원) 검토를 Codex local verification(로컬 검증)과 분리한다. |
| `required_gate_coverage_audit(필수 게이트 커버리지 감사)` | `passed(통과)` | this file(이 파일) | gate(게이트)와 decision claim(결정 주장)을 연결한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | 권위/승격/완성 주장을 막는다. |
