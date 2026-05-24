# run295C Split-Consistent Outcome Distillation Review(295C 분할 일관 결과 증류 검토)

- status(상태): `completed_split_consistent_outcome_distillation_review_no_candidate_stage296_opened`
- judgment(판정): `split_consistent_outcome_distillation_runtime_probe_negative_density_profit_curve_gate_failed`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- next_action(다음 행동): `run296A_design_density_floor_profit_expansion_rebuild_packet`
- next_stage(다음 단계): `296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild`

Effect(효과): Stage295(295단계)는 Stage294(294단계)의 OOS-positive/validation-negative(표본외 양수/검증 음수) 단서를 split-consistent outcome distillation(분할 일관 결과 증류)로 시험했지만, 후보 게이트를 넘지 못했다. 수익 단서는 보존하되 Adapter/ONNX(어댑터/온엑스)로 넘기지 않고 Stage296(296단계) 새 논제로 연다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | label(라벨) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp295A_cp294D_split_veto_distill_hold5_surface | -76.84 | 0.90 | 2.07 | 47.36 | 1.10 | 2.10 | oos_positive_validation_negative |
| cp295B_cp294C_oos_preserve_validation_veto_hold5_surface | -66.15 | 0.93 | 2.85 | 83.81 | 1.12 | 3.32 | oos_positive_validation_negative |
| cp295C_cp294B_cost_curve_distill_hold5_surface | -0.59 | 1.00 | 0.48 | 5.01 | 1.07 | 0.48 | oos_positive_validation_negative |
| cp295D_cp294E_smooth_state_hold4_surface | 60.04 | 1.25 | 0.88 | 51.47 | 1.33 | 0.81 | profit_positive_density_failed |
| cp295E_union_oos_band_rescale_hold5_surface | -63.66 | 0.93 | 2.99 | 98.58 | 1.14 | 3.47 | oos_positive_validation_negative |
| cp295F_defensive_damage_flat_router_hold3_surface | -48.08 | 0.53 | 0.26 | 19.02 | 1.39 | 0.29 | oos_positive_validation_negative |

## Judgment(판정)

- cp295D(295D 후보)는 validation/OOS(검증/표본외) 모두 순수익과 PF(수익 팩터)가 양수지만 일 거래수가 0.8대라 목표 4-10에 못 미친다.
- cp295B/cp295E(295B/295E 후보)는 OOS(표본외) 순수익 단서를 키웠지만 validation(검증)이 음수이고 일 거래수도 4 미만이다.
- 따라서 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.

## Stage296 Thesis(296단계 논제)

Stage296(296단계)는 seed(씨앗) `3`개로 density-floor profit expansion(거래 밀도 하한 수익 확장)을 연다. 효과는 cp295D의 수익 단서와 cp295B/E의 OOS 규모 단서를 후보로 보존하지 않고, 4-10 trades/day(일 4-10거래)를 먼저 만족하는 새 decision/risk surface(판단/위험 표면)로 재구성하는 것이다.

Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
