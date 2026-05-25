# run320A Validation Pocket Drawdown Controller Materialization(320A 검증 포켓 드로다운 제어기 물질화)

- run_id(실행 ID): `run320A_design_validation_pocket_drawdown_controller_packet_v1`
- candidates(후보): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): cp319D(319D 후보)의 수익 규모를 유지하면서 VIX/quality state(VIX/품질 상태)로 validation pocket(검증 포켓)을 줄이는 후보를 만들었다.

| package(패키지) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val DD/net(검증 DD/순익) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | design gate(설계 관문) |
|---|---:|---:|---:|---:|---:|---|
| cp320A_cp319D_vix30_pocket_controller_surface | 15456.59 | 4.21 | 0.31 | 23138.75 | 4.15 | passed |
| cp320D_cp319D_vix30_lowrisk_surface | 15456.59 | 4.21 | 0.31 | 23138.75 | 4.15 | passed |
| cp320B_cp319D_score10_vix25_scale_surface | 15618.29 | 4.08 | 0.34 | 22582.63 | 4.18 | passed |
| cp320E_cp319D_score10_vix25_lowrisk_surface | 15618.29 | 4.08 | 0.34 | 22582.63 | 4.18 | passed |
| cp320C_cp319D_score20_quality80_guard_surface | 15195.23 | 4.10 | 0.31 | 21583.62 | 4.05 | passed |
| cp320F_cp319D_score20_quality80_lowrisk_surface | 15195.23 | 4.10 | 0.31 | 21583.62 | 4.05 | passed |

- next_action(다음 행동): `run320B_execute_validation_pocket_drawdown_controller_mt5_probe`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
