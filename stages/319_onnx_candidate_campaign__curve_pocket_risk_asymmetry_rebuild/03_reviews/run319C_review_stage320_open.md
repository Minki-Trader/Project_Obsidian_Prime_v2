# run319C Curve-Pocket Risk Asymmetry Review(319C 곡선 포켓 위험 비대칭 검토)

- run_id(실행 ID): `run319C_review_curve_pocket_risk_asymmetry_mt5_probe_v1`
- source_run(원천 실행): `run319B_execute_curve_pocket_risk_asymmetry_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `632278.89`; package(패키지): `cp319D_adx90_dense60_trend_cap_surface`

Effect(효과): actual MT5(실제 메타트레이더5) 결과에서 거래수, 수익 규모, 효율은 좋아졌지만 validation pocket(검증 포켓)이 아직 깊은지 확인했다.

| package(패키지) | val net(검증 순익) | val DD%(검증 DD%) | val t/day(검증 일거래) | OOS net(표본외 순익) | OOS DD%(표본외 DD%) | OOS t/day(표본외 일거래) | combined(합산) | failed gates(실패 관문) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| cp319D_adx90_dense60_trend_cap_surface | 392964.03 | 28.51 | 5.98 | 239314.86 | 13.66 | 6.21 | 632278.89 | smooth_curve,stability_pressure |
| cp319B_vol90_dense50_scale_guard_surface | 362947.86 | 28.61 | 6.09 | 201667.63 | 17.79 | 6.27 | 564615.49 | smooth_curve,stability_pressure |
| cp319F_histvol85_dense55_balanced_surface | 325097.81 | 27.46 | 5.42 | 161313.81 | 18.80 | 5.47 | 486411.62 | smooth_curve,stability_pressure |
| cp319A_vol85_dense45_curve_pocket_veto_surface | 288170.22 | 27.92 | 4.48 | 143095.49 | 19.49 | 4.45 | 431265.71 | smooth_curve,stability_pressure |
| cp319E_bbw90_dense55_bandwidth_guard_surface | 184554.40 | 44.14 | 5.43 | 221867.54 | 17.25 | 5.87 | 406421.94 | efficiency,smooth_curve,stability_pressure |
| cp319C_atr80_dense55_defensive_surface | 164363.64 | 54.47 | 5.32 | 35933.23 | 47.27 | 5.64 | 200296.87 | efficiency,smooth_curve,stability_pressure |

## Judgment(판정)

Stage319(319단계)은 profit scale(수익 규모)과 4-10 trades/day(일 4-10거래)를 크게 개선했지만, validation(검증) DD%(드로다운 비율)와 긴 underwater stretch(수중 구간) 때문에 선택 후보로 닫지 않는다.
cp319D(319D 후보)는 combined net profit(합산 순수익)이 가장 크고 OOS(표본외) 곡선은 좋지만 validation(검증) 포켓이 남아 있다.

- survivor_seed_count(생존 씨앗 수): `4`
- opened_stage(열린 단계): `320_onnx_candidate_campaign__validation_pocket_drawdown_controller`
- next_action(다음 행동): `run320A_design_validation_pocket_drawdown_controller_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
