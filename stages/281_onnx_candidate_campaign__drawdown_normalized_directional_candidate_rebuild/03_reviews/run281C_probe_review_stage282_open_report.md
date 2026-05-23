# run281C Report(281C 보고서): Drawdown-Normalized Directional Probe Review(손실폭 정규화 방향 탐침 검토)

- run_id(실행 ID): `run281C_review_drawdown_normalized_directional_mt5_probe_v1`
- source_run(원천 실행): `run281B_drawdown_normalized_directional_mt5_probe_v1`
- status(상태): `completed_drawdown_normalized_directional_probe_review_no_candidate_selection_stage282_opened`
- judgment(판정): `drawdown_normalized_directional_rebuild_failed_validation_stability_no_candidate_selection`
- branch_count(분기 수): `4`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run282A_design_validation_first_asymmetric_confirmation_candidate_packet`

## Scoreboard(점수판)

| branch(분기) | val net(검증 순수익) | val PF(검증 수익 팩터) | val recovery(검증 회복) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | label(라벨) |
| run281A_cp281A_concordant_breakout | -43.41 | 0.91 | -0.25 | 216.41 | 1.48 | failed_validation_stability_no_candidate |
| run281A_cp281B_macro_trend_concordance | 16.07 | 1.05 | 0.10 | 192.70 | 1.60 | failed_validation_stability_no_candidate |
| run281A_cp281C_signal_pressure_hysteresis | -85.57 | 0.84 | -0.42 | 320.08 | 1.73 | failed_validation_stability_no_candidate |
| run281A_cp281D_low_supply_controlled_breakout | -36.90 | 0.92 | -0.22 | 252.23 | 1.56 | failed_validation_stability_no_candidate |

## Stage282 Queue(282단계 대기열)

- `cp282A_validation_recovery_floor_direction_surface`: Validation-first recovery floor before OOS scale.
- `cp282B_session_loss_asymmetry_surface`: Session-specific loss asymmetry is a decision surface, not a post-hoc filter.
- `cp282C_concentration_penalty_confirmation_surface`: Top-month and top-trade concentration must be penalized inside construction.
- `cp282D_macro_trend_countercheck_surface`: Macro trend agreement needs a countercheck that protects validation, not only OOS upside.

## Meaning(의미)

Stage281(281단계)은 OOS(표본외) 상방을 다시 보였지만 validation(검증) 회복력이 후보 패키지 기준에 닿지 않았다.
Effect(효과): 이 분기는 선택 후보로 부르지 않고, Stage282(282단계)에서 validation-first(검증 우선) 후보 구성을 새 질문으로 연다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
