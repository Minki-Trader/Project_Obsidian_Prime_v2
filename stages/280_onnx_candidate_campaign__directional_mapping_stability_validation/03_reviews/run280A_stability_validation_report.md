# run280A Report(280A 보고서): Directional Mapping Stability Validation(방향 매핑 안정성 검증)

- run_id(실행 ID): `run280A_directional_mapping_stability_validation_v1`
- source_run(원천 실행): `run279C_directional_runtime_mapping_mt5_signal_replay_v1`
- status(상태): `completed_directional_mapping_stability_validation_no_candidate_selection`
- judgment(판정): `directional_mapping_seeds_failed_stability_no_candidate_selection_stage281_opened`
- seed_count(씨앗 수): `3`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run281A_design_drawdown_normalized_directional_candidate_rebuild_packet`

## Stability Read(안정성 판독)

| seed(씨앗) | val net(검증 순손익) | val PF(검증 PF) | val recovery(검증 회복) | OOS net(표본외 순손익) | OOS PF(표본외 PF) | label(라벨) |
| run279B_cp277C_consensus_q01 | 52.27 | 1.04 | 0.15 | 140.85 | 1.12 | failed_stability_no_selected_candidate |
| run279B_cp277D_breakout_q02 | 29.48 | 1.06 | 0.14 | 241.98 | 1.59 | failed_stability_no_selected_candidate |
| run279B_cp277D_breakout_q03 | 41.36 | 1.26 | 0.51 | 9.07 | 1.04 | failed_stability_no_selected_candidate |

## Failure Memory(실패 기억)

- `run279B_cp277C_consensus_q01`: validation_pf_below_1_05(검증 PF 1.05 미만);validation_recovery_below_0_25(검증 회복 0.25 미만);validation_drawdown_over_4x_net(검증 손실폭이 순손익의 4배 초과);tier_b_validation_negative(Tier B 검증 음수);validation_worst_month_below_minus_100(검증 최악 월 -100 미만);oos_worst_month_below_minus_100(표본외 최악 월 -100 미만);validation_losing_streak_ge_7(검증 연속 손실 7 이상);validation_top_month_contribution_over_80pct(검증 상위 월 기여 80% 초과);oos_top_month_contribution_over_80pct(표본외 상위 월 기여 80% 초과)
- `run279B_cp277D_breakout_q02`: validation_recovery_below_0_25(검증 회복 0.25 미만);validation_drawdown_over_4x_net(검증 손실폭이 순손익의 4배 초과);validation_losing_streak_ge_7(검증 연속 손실 7 이상);validation_top_month_contribution_over_80pct(검증 상위 월 기여 80% 초과)
- `run279B_cp277D_breakout_q03`: oos_pf_below_1_05(표본외 PF 1.05 미만);thin_trade_count_under_80(거래 수 80 미만);oos_recovery_below_0_50(표본외 회복 0.50 미만);validation_losing_streak_ge_7(검증 연속 손실 7 이상);oos_top_month_contribution_over_80pct(표본외 상위 월 기여 80% 초과)

## Meaning(의미)

Stage280(280단계)는 Stage279(279단계)의 생존 씨앗을 거래 목록, 월별 손익, 세션 손익, 잔액 곡선, 거래 품질로 압박했다.
Effect(효과): 표본외 숫자가 좋아 보여도 검증 회복, 손실폭 대비 순손익, 월/세션 취약성이 약하면 후보 패키지로 부르지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
