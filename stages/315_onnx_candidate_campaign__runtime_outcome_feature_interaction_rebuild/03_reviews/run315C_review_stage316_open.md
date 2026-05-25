# run315C Runtime Outcome Feature Interaction Review(315C 런타임 결과 피처 상호작용 검토)

- run_id(실행 ID): `run315C_review_runtime_outcome_feature_interaction_mt5_probe_v1`
- source_run(원천 실행): `run315B_execute_runtime_outcome_feature_interaction_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `-989.48`; source_package(원천 패키지): `cp315A_hour20_sell_lowvol_mirror19_21_hold3_surface`

Effect(효과): actual routed total(실제 라우팅 전체)의 trade list(거래 목록)를 읽어 최소 거래수, 4-10 trades/day(일 4-10거래), 순수익 규모, PF(수익 팩터), DD(손실폭), recovery(회복), expectancy(기대값), curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp315A_hour20_sell_lowvol_mirror19_21_hold3_surface | -499.11 | 0.84 | -490.37 | 0.91 | 7.49/16.21 | -989.48 | density,scale,eff,curve |
| cp315D_curve_guard_hour20_22_sell_mirror_release_hold2_surface | -498.87 | 0.84 | -492.03 | 0.86 | 8.64/13.33 | -990.90 | density,scale,eff,curve |
| cp315E_hour20_sell_23buy_asymmetric_release_hold3_surface | -499.10 | 0.87 | -495.16 | 0.89 | 8.15/17.47 | -994.26 | density,scale,eff,curve |
| cp315C_hour20_sell_21mirror_19guard_hold2_surface | -499.15 | 0.86 | -496.82 | 0.83 | 7.11/16.84 | -995.97 | density,scale,eff,curve |
| cp315B_hour20_22_sell_full_mirror_hold3_surface | -499.16 | 0.86 | -497.31 | 0.91 | 9.05/21.61 | -996.47 | density,scale,eff,curve |
| cp315F_aggressive_hour20_sell_inversion_convexity_hold4_surface | -499.19 | 0.87 | -498.90 | 0.90 | 6.86/13.15 | -998.09 | density,scale,eff,curve |

- next_stage(다음 단계): `316_onnx_candidate_campaign__post_interaction_profit_scale_curve_rebuild`
- next_action(다음 행동): `run316A_design_post_interaction_profit_scale_curve_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
