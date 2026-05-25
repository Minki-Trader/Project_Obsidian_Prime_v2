# run322A cp321B Curve Stability Pressure Materialization(322A cp321B 곡선 안정성 압박 물질화)

- run_id(실행 ID): `run322A_design_cp321b_curve_stability_pressure_packet_v1`
- candidates(후보): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): cp321B(321B 씨앗)를 exact replay(정확 재생), defensive threshold(방어 임계값), aggressive density(공격 밀도), source consensus/source swap(원천 합의/교체), volatility guard(변동성 방어)로 압박한다.

| package(패키지) | lane(레인) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| cp322A_cp321b_exact_replay_control_surface | replay_control | 21460.07 | 4.64 | 2.04 | 25267.59 | 4.66 | 3.17 | passed |
| cp322F_score57_hv90_curve_guard_surface | balanced_upside_guard | 21312.32 | 4.58 | 2.10 | 24513.98 | 4.73 | 3.09 | passed |
| cp322B_score65_tight_curve_surface | defensive_threshold | 20543.40 | 4.20 | 2.21 | 23739.05 | 4.18 | 3.34 | passed |
| cp322C_score55_density_upside_surface | aggressive_density | 18842.40 | 5.10 | 1.80 | 25406.48 | 5.20 | 2.94 | passed |
| cp322E_b_only_score60_dependency_surface | source_dependency | 21204.60 | 4.21 | 2.14 | 21643.44 | 4.27 | 2.98 | passed |
| cp322D_d_b_agree55_consensus_surface | source_consensus | 18582.93 | 4.63 | 1.85 | 20876.93 | 4.78 | 2.68 | passed |

- next_action(다음 행동): `run322B_execute_cp321b_curve_stability_pressure_mt5_probe`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
