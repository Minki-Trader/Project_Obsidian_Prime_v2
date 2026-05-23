# run281A Report(281A 보고서): Drawdown-Normalized Candidate Input Materialization(손실폭 정규화 후보 입력 물질화)

- run_id(실행 ID): `run281A_design_materialize_drawdown_normalized_directional_candidate_rebuild_v1`
- status(상태): `completed_drawdown_normalized_candidate_rebuild_inputs_materialized_no_candidate_selection`
- judgment(판정): `fresh_drawdown_normalized_candidate_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `4`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run281B_execute_drawdown_normalized_directional_mt5_probe`

| branch(분기) | val signals(검증 신호) | OOS signals(표본외 신호) | package(패키지) |
| `run281A_cp281A_concordant_breakout` | `218` | `198` | `cp281A_drawdown_normalized_concordant_breakout_surface` |
| `run281A_cp281B_macro_trend_concordance` | `166` | `141` | `cp281B_macro_trend_concordance_surface` |
| `run281A_cp281C_signal_pressure_hysteresis` | `231` | `211` | `cp281C_signal_pressure_hysteresis_surface` |
| `run281A_cp281D_low_supply_controlled_breakout` | `229` | `204` | `cp281D_low_supply_controlled_breakout_surface` |

Effect(효과): Stage281(281단계)는 Stage280(280단계)의 실패 기억을 새 route_signal_value(경로 신호 값) 표면으로 바꿨고, 다음 실행에서 MT5(MetaTrader 5, 메타트레이더5)로 검증한다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
