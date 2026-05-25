# run311A Post-Allocation Fresh Edge Materialization(311A 배분 이후 새 엣지 물질화)

- run_id(실행 ID): `run311A_design_post_allocation_fresh_edge_rebuild_packet_v1`
- source_run(원천 실행): `run310C_review_runtime_positive_fragment_allocation_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run311B_execute_post_allocation_fresh_edge_mt5_probe`

Effect(효과): Stage310(310단계)의 배분 실패를 좁게 수리하지 않고, adverse-hour mirror(불리 시간대 방향 반전)와 feature support(피처 지원)를 새 표면으로 만든다.

| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---|
| cp311E_conservative_17_18_20_router_hold3_surface | 2618.82 | 1712.32 | 7.23/5.34 | curve |
| cp311B_hour16_mirror_19_veto_hold4_surface | 2946.49 | 885.40 | 10.28/9.79 | density,curve |
| cp311A_hour16_19_direction_mirror_hold4_surface | 1215.92 | -991.09 | 11.62/11.34 | density,edge,curve |
| cp311D_oos_scale_preserve_16_19_mirror_hold5_surface | -158.03 | -1069.98 | 11.15/10.77 | density,edge,curve |
| cp311F_model_feature_adverse_hour_blend_hold4_surface | 516.36 | -1718.03 | 12.60/7.37 | density,edge,curve |
| cp311C_adverse_cluster_mirror_hold3_surface | -1018.54 | -532.49 | 12.43/11.54 | density,edge,curve |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
