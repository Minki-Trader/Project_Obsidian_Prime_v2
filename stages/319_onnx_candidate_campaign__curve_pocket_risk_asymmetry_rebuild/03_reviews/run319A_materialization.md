# run319A Curve-Pocket Risk Asymmetry Materialization(319A 곡선 포켓 위험 비대칭 물질화)

- run_id(실행 ID): `run319A_design_curve_pocket_risk_asymmetry_rebuild_packet_v1`
- source_run(원천 실행): `run318C_review_post_non_time_curve_stability_mt5_probe_v1`
- candidates(후보): `6`
- mt5_queue_rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): Stage318(318단계)의 큰 수익 조각을 보존하되 volatility/trend cap(변동성/추세 상한)과 lower risk sizing(낮은 위험 크기)으로 곡선 포켓을 줄이는 후보를 MT5(메타트레이더5) 탐침으로 넘긴다.

| package(패키지) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | val DD/net(검증 DD/순익) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| cp319E_bbw90_dense55_bandwidth_guard_surface | 20774.57 | 5.32 | 1.95 | 0.22 | 26087.18 | 5.79 | 2.64 | passed |
| cp319D_adx90_dense60_trend_cap_surface | 21141.43 | 5.90 | 1.94 | 0.25 | 25667.19 | 6.14 | 2.53 | passed |
| cp319A_vol85_dense45_curve_pocket_veto_surface | 23965.14 | 4.35 | 2.82 | 0.18 | 22685.91 | 4.37 | 2.84 | passed |
| cp319B_vol90_dense50_scale_guard_surface | 22986.69 | 6.01 | 2.09 | 0.23 | 22854.38 | 6.19 | 2.35 | passed |
| cp319F_histvol85_dense55_balanced_surface | 21978.85 | 5.32 | 2.19 | 0.21 | 21227.67 | 5.38 | 2.37 | passed |
| cp319C_atr80_dense55_defensive_surface | 17346.90 | 5.24 | 1.90 | 0.18 | 22873.16 | 5.56 | 2.69 | passed |

- next_action(다음 행동): `run319B_execute_curve_pocket_risk_asymmetry_mt5_probe`

Caution(주의): 이 설계 추정은 Stage318(318단계) 실제 MT5(메타트레이더5) 거래를 재사용한다. 선택 후보(candidate, 후보)는 run319B/run319C(319B/319C 실행) 이후에만 판단한다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
