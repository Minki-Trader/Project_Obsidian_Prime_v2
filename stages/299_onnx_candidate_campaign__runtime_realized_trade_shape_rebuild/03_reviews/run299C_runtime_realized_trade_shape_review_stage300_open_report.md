# run299C Runtime-Realized Trade Shape Review(299C 런타임 실제 거래 형태 검토)

- run_id(실행 ID): `run299C_review_runtime_realized_trade_shape_mt5_probe_v1`
- source_run(원천 실행): `run299B_runtime_realized_trade_shape_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `111.68` from `cp299A_validation_safe_duration_veto_density50_surface`

Effect(효과): Stage299(299단계)는 validation(검증) 일부 회복을 만들었지만 OOS(표본외)가 음수라 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.

## Scoreboard(점수판)

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp299A_validation_safe_duration_veto_density50_surface | 132.83 | 1.13 | -21.15 | 0.97 | 4.90/4.88 | scale,eff,curve |
| cp299B_exit_loss_cluster_veto_density55_surface | 143.19 | 1.14 | -34.44 | 0.96 | 4.89/5.26 | scale,eff,curve |
| cp299C_oos_clue_val_guard_reexpand_density65_surface | -111.97 | 0.92 | -99.94 | 0.90 | 6.19/6.16 | scale,eff,curve |
| cp299D_short_hold_profit_burst_density45_surface | -71.82 | 0.91 | -136.09 | 0.78 | 4.07/4.20 | scale,eff,curve |
| cp299E_session_adverse_shape_router_density60_surface | 78.34 | 1.07 | -29.09 | 0.97 | 5.30/5.60 | scale,eff,curve |
| cp299F_loss_cluster_flip_control_density80_surface | -50.76 | 0.97 | -96.98 | 0.92 | 7.21/7.22 | scale,eff,curve |

## Gate Result(관문 결과)

- profit_scale_gate(수익 규모 관문): `0/6` 통과
- efficiency_gate(효율 관문): `0/6` 통과
- curve_pocket_gate(곡선 포켓 관문): `0/6` 통과

## Next Stage(다음 단계)

- opened_stage(열린 단계): `300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild`
- next_action(다음 행동): `run300A_design_split_forward_trade_shape_generalization_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
