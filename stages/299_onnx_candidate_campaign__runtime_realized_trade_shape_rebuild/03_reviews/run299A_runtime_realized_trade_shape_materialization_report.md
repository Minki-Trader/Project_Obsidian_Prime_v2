# run299A Runtime-Realized Trade Shape Materialization(299A 런타임 실제 거래 형태 물질화)

- status(상태): `completed_runtime_realized_trade_shape_candidates_materialized_no_selection`
- judgment(판정): `runtime_realized_trade_shape_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run299B_execute_runtime_realized_trade_shape_mt5_probe`

Effect(효과): Stage298(298단계)의 실제 MT5(메타트레이더5) 거래 생애, 보유 시간, 손실 군집을 써서 새 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp299A_validation_safe_duration_veto_density50_surface | -930.3 | 5.01 | -1358.5 | 4.98 | passed | failed | failed |
| cp299B_exit_loss_cluster_veto_density55_surface | -545.9 | 4.92 | -1363.5 | 5.32 | passed | failed | failed |
| cp299C_oos_clue_val_guard_reexpand_density65_surface | -4367.6 | 6.46 | -2285.2 | 6.46 | passed | failed | failed |
| cp299D_short_hold_profit_burst_density45_surface | -2212.4 | 4.44 | -1521.0 | 4.60 | passed | failed | failed |
| cp299E_session_adverse_shape_router_density60_surface | -983.2 | 5.42 | -1071.8 | 5.76 | passed | failed | failed |
| cp299F_loss_cluster_flip_control_density80_surface | -4528.6 | 7.94 | -2028.8 | 7.90 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
