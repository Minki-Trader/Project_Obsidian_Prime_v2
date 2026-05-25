# run322C cp321B Curve Stability Pressure Review(322C cp321B 곡선 안정성 압박 검토)

- run_id(실행 ID): `run322C_review_cp321b_curve_stability_pressure_mt5_probe_v1`
- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- next_stage(다음 단계): `323_onnx_candidate_campaign__selected_curve_adapter_package`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): actual MT5(실제 메타트레이더5) 수익, 거래 밀도, 위험, 확대 곡선 포켓을 함께 읽어 Adapter(어댑터)로 넘길지 또는 새 구조로 폐기/전환할지 정한다.

| package(패키지) | net val/oos(검증/표본외 순익) | t/day val/oos(일거래) | PF val/oos | DD% val/oos | worst chunk val/oos(최악 확대 구간) | gate(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp322A_cp321b_exact_replay_control_surface | 472738/237628 | 5.02/4.86 | 1.64/1.51 | 19.11/15.51 | -1035/32 | passed |
| cp322B_score65_tight_curve_surface | 459390/210975 | 4.54/4.36 | 1.71/1.55 | 18.20/13.14 | -638/-143 | passed |
| cp322C_score55_density_upside_surface | 513841/281552 | 5.55/5.47 | 1.61/1.52 | 19.17/12.22 | -1563/-5756 | failed |
| cp322F_score57_hv90_curve_guard_surface | 428841/192397 | 5.01/4.98 | 1.58/1.41 | 19.53/18.11 | -1390/29 | failed |
| cp322E_b_only_score60_dependency_surface | 346459/141560 | 4.60/4.47 | 1.52/1.39 | 23.27/22.91 | -1399/-8094 | failed |
| cp322D_d_b_agree55_consensus_surface | 256629/97944 | 4.68/4.82 | 1.38/1.27 | 32.38/32.33 | -6198/-16539 | failed |

- next_action(다음 행동): `run323A_build_selected_curve_adapter_package`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
