# run321C Post Controller Profit Curve Review(321C 제어기 이후 수익 곡선 검토)

- run_id(실행 ID): `run321C_review_post_controller_profit_curve_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- survivor_seed(생존 씨앗): `cp321B_d_or_b_score60_scale_curve_surface`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): actual MT5(실제 메타트레이더5) 수익과 trade-frame shape(거래 프레임 형태)를 함께 읽어, ONNX(온엑스)로 바로 가지 않고 Stage322(322단계) 안정성 압박으로 넘길 씨앗만 분리한다.

| package(패키지) | net val/oos(검증/표본외 순익) | t/day val/oos(일거래) | PF val/oos | DD% val/oos | worst chunk val/oos(최악 확대 구간) | survivor(생존) |
|---|---:|---:|---:|---:|---:|---|
| cp321B_d_or_b_score60_scale_curve_surface | 472738/237628 | 5.02/4.86 | 1.64/1.51 | 19.11/15.51 | -1035/32 | passed |
| cp321C_d_or_b_score50_aggressive_scale_surface | 545653/323509 | 6.02/6.00 | 1.59/1.54 | 18.29/10.68 | -1528/-6659 | failed |
| cp321E_three_of_six_consensus_surface | 355562/189654 | 6.10/6.25 | 1.38/1.34 | 30.18/17.14 | -6877/-4877 | failed |
| cp321F_d_or_b_score50_hv80_curve_surface | 322319/136731 | 5.40/5.40 | 1.41/1.32 | 25.73/22.00 | -991/-10585 | failed |
| cp321D_d_f_confirm_balance_surface | 188826/78007 | 4.97/5.22 | 1.26/1.23 | 42.19/36.25 | -1944/-13631 | failed |
| cp321A_d_a_confirm_efficiency_surface | 119396/40875 | 4.18/4.28 | 1.21/1.31 | 52.60/34.60 | -1650/-26742 | failed |

- opened_stage(열린 단계): `322_onnx_candidate_campaign__cp321b_curve_stability_pressure`
- next_action(다음 행동): `run322A_design_cp321b_curve_stability_pressure_packet`

Boundary(경계): survivor seed(생존 씨앗)는 선택 후보나 Adapter(어댑터) 시작이 아니다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
