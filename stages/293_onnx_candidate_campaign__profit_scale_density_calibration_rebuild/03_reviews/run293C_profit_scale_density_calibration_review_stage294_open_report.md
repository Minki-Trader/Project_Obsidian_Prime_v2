# run293C Profit-Scale Density Calibration Review(293C 순수익 규모/거래 밀도 보정 검토)

- status(상태): `completed_profit_scale_density_calibration_review_no_candidate_stage294_opened`
- judgment(판정): `profit_scale_density_calibration_runtime_probe_negative_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- next_action(다음 행동): `run294A_design_mt5_outcome_relabel_directional_flip_rebuild_packet`
- next_stage(다음 단계): `294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild`

Effect(효과): Stage293(293단계)는 trade density(거래 밀도)는 일부 맞췄지만 net profit(순수익), PF(수익 팩터), recovery(회복), expectancy(기대값), curve pocket(곡선 포켓)을 함께 통과한 package(패키지)가 없어 Adapter/ONNX(어댑터/온엑스)를 진행하지 않는다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp293A_runtime_calibrated_histgb_hold5_surface | -33.95 | 0.99 | 9.52 | -230.72 | 0.90 | 11.84 | valid_negative_no_candidate |
| cp293B_profit_scale_lgbm_hold7_surface | -429.74 | 0.84 | 6.25 | -379.57 | 0.82 | 6.77 | valid_negative_no_candidate |
| cp293C_smooth_curve_extratrees_hold4_surface | -81.20 | 0.94 | 3.67 | -144.17 | 0.88 | 4.48 | valid_negative_no_candidate |
| cp293D_density_band_xgb_hold6_surface | -495.99 | 0.74 | 3.89 | -494.98 | 0.81 | 8.82 | valid_negative_no_candidate |
| cp293E_hybrid_meta_lgbm_hold8_surface | -187.34 | 0.91 | 6.17 | -268.18 | 0.85 | 6.53 | valid_negative_no_candidate |
| cp293F_asymmetric_tail_control_xgb_hold5_surface | -91.64 | 0.95 | 6.17 | -86.62 | 0.94 | 7.27 | valid_negative_no_candidate |

## Stage294 Thesis(294단계 논제)

Stage294(294단계)는 Stage293(293단계)의 좁은 repair(수리)가 아니다. 실제 MT5 outcome relabeling(MT5 결과 재라벨), direction flip(방향 반전), cost-aware acceptance(비용 인식 수락), curve smoother(곡선 완화)를 새 decision surface(판단 표면)로 만든다.

Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
