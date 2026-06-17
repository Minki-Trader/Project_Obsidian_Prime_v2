# F80D Required Gate Coverage Audit(F80D 필수 게이트 커버리지 감사)

Status(상태): `completed_mt5_runtime_probe_quality_observation_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target` | `passed(통과)` | `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/03_reviews/f80c_runtime_materialization_target_selection.json` | F80C(전선80C) 대상만 물질화한다. |
| `onnx_probability_parity` | `3` | `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/02_runs/frontier80D_mt5_runtime_probe_quality_v1/f80d_probability_parity.csv` | Python/ONNX(파이썬/온엑스) 확률 차이를 확인한다. |
| `runtime_signal_veto_parity` | `3` | `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/02_runs/frontier80D_mt5_runtime_probe_quality_v1/f80d_signal_parity.csv` | 선택 진입 시각이 런타임 입력으로 보존되는지 확인한다. |
| `strategy_tester_attempt` | `1/1` | `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/02_runs/frontier80D_mt5_runtime_probe_quality_v1/run_manifest.json` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `final_claim_guard` | `passed(통과)` | `runtime_probe_quality_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | 런타임 권위/실거래 준비를 만들지 않는다. |
