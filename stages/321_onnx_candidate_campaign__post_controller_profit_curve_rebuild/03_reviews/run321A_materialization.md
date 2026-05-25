# run321A Post Controller Profit Curve Materialization(321A 제어기 이후 수익 곡선 물질화)

- run_id(실행 ID): `run321A_design_post_controller_profit_curve_rebuild_packet_v1`
- candidates(후보): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Stage320(320단계)의 VIX/quality controller(VIX/품질 제어기)를 버리고 Stage319(319단계) 여러 수익 표면의 consensus/union(합의/합집합)을 새 decision surface(판단 표면)로 만들었다.

| package(패키지) | lane(갈래) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | val rec(검증 회복) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| cp321B_d_or_b_score60_scale_curve_surface | balanced_scale | 21460.07 | 4.64 | 2.04 | 4.11 | 25267.59 | 4.66 | 3.17 | passed |
| cp321A_d_a_confirm_efficiency_surface | defensive_efficiency | 20549.17 | 4.12 | 2.15 | 3.93 | 19327.51 | 4.24 | 2.76 | passed |
| cp321C_d_or_b_score50_aggressive_scale_surface | aggressive_scale | 18868.37 | 5.55 | 1.69 | 2.41 | 26291.25 | 5.72 | 2.75 | failed |
| cp321E_three_of_six_consensus_surface | consensus_vote | 17832.54 | 5.64 | 1.62 | 1.76 | 23691.63 | 5.97 | 2.51 | failed |
| cp321D_d_f_confirm_balance_surface | balanced_consensus | 17693.83 | 4.95 | 1.72 | 2.25 | 19340.81 | 5.20 | 2.32 | failed |
| cp321F_d_or_b_score50_hv80_curve_surface | curve_guard_not_stage320_controller | 17397.83 | 4.94 | 1.69 | 2.22 | 19016.06 | 5.13 | 2.33 | failed |

- next_action(다음 행동): `run321B_execute_post_controller_profit_curve_mt5_probe`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
