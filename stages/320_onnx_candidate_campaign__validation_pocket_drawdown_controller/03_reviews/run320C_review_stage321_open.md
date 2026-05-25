# run320C Validation Pocket Drawdown Controller Review(320C 검증 포켓 드로다운 제어기 검토)

- run_id(실행 ID): `run320C_review_validation_pocket_drawdown_controller_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): 4-10 trades/day(일 4-10거래)는 유지했지만 validation(검증) DD%(드로다운 비율), PF(수익 팩터), recovery(회복)가 무너져 controller(제어기) 방향을 폐기한다.

| package(패키지) | val net(검증 순익) | val PF(검증 PF) | val DD%(검증 DD%) | OOS net(표본외 순익) | OOS PF(표본외 PF) | OOS DD%(표본외 DD%) | failed gates(실패 관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp320B_cp319D_score10_vix25_scale_surface | 145928.46 | 1.25 | 46.42 | 72298.33 | 1.31 | 26.65 | efficiency_gate,smooth_curve_gate |
| cp320E_cp319D_score10_vix25_lowrisk_surface | 58599.84 | 1.12 | 66.65 | 30046.18 | 1.35 | 22.61 | profit_scale_gate,efficiency_gate,smooth_curve_gate |
| cp320A_cp319D_vix30_pocket_controller_surface | 49484.73 | 1.09 | 74.16 | 19344.74 | 1.28 | 25.94 | profit_scale_gate,efficiency_gate,smooth_curve_gate |
| cp320C_cp319D_score20_quality80_guard_surface | 19787.78 | 1.07 | 76.40 | 23357.55 | 1.34 | 29.89 | profit_scale_gate,efficiency_gate,smooth_curve_gate |
| cp320D_cp319D_vix30_lowrisk_surface | 18152.15 | 1.08 | 76.15 | 9342.82 | 1.33 | 21.13 | profit_scale_gate,efficiency_gate,smooth_curve_gate |
| cp320F_cp319D_score20_quality80_lowrisk_surface | 9632.43 | 1.10 | 67.97 | 10893.54 | 1.39 | 24.60 | profit_scale_gate,efficiency_gate,smooth_curve_gate |

- opened_stage(열린 단계): `321_onnx_candidate_campaign__post_controller_profit_curve_rebuild`
- next_action(다음 행동): `run321A_design_post_controller_profit_curve_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
