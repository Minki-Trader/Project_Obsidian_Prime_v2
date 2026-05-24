# run305A Runtime-Realized Curve Attribution Materialization(305A 런타임 실제 곡선 기여도 물질화)

- status(상태): `completed_runtime_realized_curve_attribution_candidates_materialized_no_selection`
- judgment(판정): `runtime_realized_curve_attribution_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run305B_execute_runtime_realized_curve_attribution_mt5_probe`

Effect(효과): Stage304(304단계) 실제 MT5(메타트레이더5) 손실 방향을 repair(수리)하지 않고 anti-surface(반대 표면) 후보로 재구성했다.

| package(패키지) | transform(변환) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(거래우위) | curve(곡선) |
|---|---|---:|---:|---:|---:|---|---|---|
| cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface | hour19_direct_else_flip | 853.1 | 4.87 | 2559.4 | 5.86 | passed | passed | failed |
| cp305D_cp304C_broad_flip_density65_hold4_surface | full_flip_wide | 3947.6 | 4.18 | 44.0 | 4.63 | passed | failed | failed |
| cp305A_runtime_loss_flip_cp304D_mid_density65_hold4_surface | full_flip_mid | 1664.0 | 6.45 | 713.9 | 6.44 | passed | passed | failed |
| cp305B_runtime_loss_flip_cp304E_mid_density65_hold4_surface | full_flip_mid | 412.2 | 4.75 | 1388.1 | 5.76 | passed | failed | failed |
| cp305E_cp304D_lowvol_flip_density55_hold4_surface | lowvol_flip | 1446.3 | 4.05 | -140.0 | 5.24 | passed | failed | failed |
| cp305F_cp304F_aggressive_flip_mid_density85_hold6_surface | full_flip_mid | 1727.7 | 6.72 | -1365.7 | 8.49 | passed | failed | failed |

- mt5_queue_rows(MT5 대기열 행): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
