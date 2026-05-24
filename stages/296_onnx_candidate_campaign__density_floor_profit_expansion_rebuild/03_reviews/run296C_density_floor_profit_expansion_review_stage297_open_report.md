# run296C Density-Floor Profit Expansion Review(296C 거래 밀도 하한 수익 확장 검토)

- status(상태): `completed_density_floor_profit_expansion_review_no_candidate_stage297_opened`
- judgment(판정): `density_floor_profit_expansion_runtime_probe_negative_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- next_action(다음 행동): `run297A_design_bilevel_curve_monotonic_profit_rebuild_packet`
- next_stage(다음 단계): `297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild`

Effect(효과): Stage296(296단계)는 proxy(대리) 상방을 그대로 믿지 않고 MT5 actual routed total(MT5 실제 라우팅 전체)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 월/세션/롤링 포켓을 같이 판정한다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp296A_cp294C_validation_counter_density8_hold4_surface | -99.63 | 0.91 | 5.10 | 51.80 | 1.06 | 5.72 | valid_negative_no_candidate |
| cp296B_cp294F_union_counter_density9_hold4_surface | -139.98 | 0.88 | 5.66 | 19.18 | 1.02 | 6.31 | valid_negative_no_candidate |
| cp296C_cp294D_profit_expand_density7_hold4_surface | -103.35 | 0.87 | 3.33 | 11.75 | 1.02 | 3.75 | valid_negative_no_candidate |
| cp296D_cp294D_session_quota_density9_hold3_surface | -30.34 | 0.97 | 4.28 | -13.67 | 0.98 | 4.18 | valid_negative_no_candidate |
| cp296E_cp294C_payoff_tail_density10_hold4_surface | -72.87 | 0.94 | 5.30 | 63.60 | 1.07 | 5.95 | valid_negative_no_candidate |
| cp296F_cp294E_lowdensity_profit_expand_density8_hold4_surface | -126.96 | 0.82 | 3.18 | -2.67 | 1.00 | 3.39 | valid_negative_no_candidate |

## Stage297 Thesis(297단계 논제)

조건을 통과한 패키지가 있으면 Stage297(297단계)은 Adapter package(어댑터 패키지)로 넘어간다. 없으면 Stage297(297단계)은 좁은 repair(수리)가 아니라 bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성)로 entry creation(진입 생성), profit scale(순수익 규모), curve veto(곡선 거부)를 한 번에 다시 설계한다.

Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
