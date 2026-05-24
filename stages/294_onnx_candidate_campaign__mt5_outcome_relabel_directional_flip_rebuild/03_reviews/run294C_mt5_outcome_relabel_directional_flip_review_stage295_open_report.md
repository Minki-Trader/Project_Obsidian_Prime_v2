# run294C MT5 Outcome Relabel Directional Flip Review(294C MT5 결과 재라벨 방향 반전 검토)

- status(상태): `completed_mt5_outcome_relabel_directional_flip_review_no_candidate_stage295_opened`
- judgment(판정): `mt5_outcome_relabel_directional_flip_runtime_probe_negative_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- next_action(다음 행동): `run295A_design_split_consistent_outcome_distillation_rebuild_packet`
- next_stage(다음 단계): `295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild`

Effect(효과): Stage294(294단계)는 OOS(표본외) 일부 양수 단서를 만들었지만 validation(검증)이 전부 음수라서 ONNX(온엑스) 후보로 넘기지 않는다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp294A_cp293F_full_outcome_flip_hold5_surface | -193.02 | 0.90 | 6.17 | -74.62 | 0.95 | 7.27 | valid_negative_no_candidate |
| cp294B_cp293F_cost_aware_flip_skip_hold5_surface | -166.61 | 0.90 | 5.69 | 46.77 | 1.04 | 5.79 | valid_negative_no_candidate |
| cp294C_cp293A_density_trimmed_flip_hold5_surface | -366.61 | 0.86 | 9.22 | 104.89 | 1.06 | 9.18 | valid_negative_no_candidate |
| cp294D_cp293A_smooth_curve_flip_router_hold5_surface | -79.28 | 0.95 | 6.20 | 38.57 | 1.03 | 6.20 | valid_negative_no_candidate |
| cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface | -210.47 | 0.88 | 5.86 | 46.24 | 1.04 | 5.96 | valid_negative_no_candidate |
| cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface | -416.37 | 0.85 | 9.80 | 50.69 | 1.03 | 9.70 | valid_negative_no_candidate |

## Stage295 Thesis(295단계 논제)

Stage295(295단계)는 flip(반전) 자체를 반복하지 않는다. OOS(표본외) 양수 단서가 validation(검증)에서 왜 깨지는지 split-consistent outcome distillation(분할 일관 결과 증류)과 validation damage veto(검증 손상 거부)로 새 decision surface(판단 표면)를 만든다.

Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
