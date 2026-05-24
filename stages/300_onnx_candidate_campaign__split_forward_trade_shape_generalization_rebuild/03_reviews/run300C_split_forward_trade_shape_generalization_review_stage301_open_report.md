# run300C Split-Forward Trade Shape Generalization Review(300C 런타임 실제 거래 형태 검토)

- run_id(실행 ID): `run300C_review_split_forward_trade_shape_generalization_mt5_probe_v1`
- source_run(원천 실행): `run300B_split_forward_trade_shape_generalization_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `0.00` from `cp300B_late_validation_veto_density55_surface`

Effect(효과): Stage300(300단계)는 validation(검증) 일부 회복을 만들었지만 OOS(표본외)가 음수라 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.

## Scoreboard(점수판)

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp300A_fold_consensus_shape_density50_surface | -11.43 | 0.99 | -74.03 | 0.89 | 4.78/4.79 | scale,eff,curve |
| cp300B_late_validation_veto_density55_surface | 0.00 | 0.00 | 0.00 | 0.00 | 0.00/0.00 | scale,eff,curve |
| cp300C_stable_session_directional_density60_surface | -20.51 | 0.98 | -35.81 | 0.95 | 5.48/5.63 | scale,eff,curve |
| cp300D_low_dd_microburst_density45_surface | -49.38 | 0.93 | -254.65 | 0.65 | 4.19/4.22 | scale,eff,curve |
| cp300E_regime_consensus_density70_surface | -28.83 | 0.97 | -97.17 | 0.89 | 5.85/6.24 | scale,eff,curve |
| cp300F_aggressive_forward_reexpand_density80_surface | -489.29 | 0.80 | -33.41 | 0.98 | 7.26/7.44 | scale,eff,curve |

## Gate Result(관문 결과)

- profit_scale_gate(수익 규모 관문): `0/6` 통과
- efficiency_gate(효율 관문): `0/6` 통과
- curve_pocket_gate(곡선 포켓 관문): `0/6` 통과

## Next Stage(다음 단계)

- opened_stage(열린 단계): `301_onnx_candidate_campaign__orthogonal_profit_source_rebuild`
- next_action(다음 행동): `run301A_design_orthogonal_profit_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
