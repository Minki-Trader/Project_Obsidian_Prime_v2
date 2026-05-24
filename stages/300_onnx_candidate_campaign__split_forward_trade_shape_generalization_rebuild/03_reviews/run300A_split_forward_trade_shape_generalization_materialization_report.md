# run300A Split-Forward Trade Shape Generalization Materialization(300A 분할 전진 거래 형태 일반화 물질화)

- status(상태): `completed_split_forward_trade_shape_generalization_candidates_materialized_no_selection`
- judgment(판정): `split_forward_trade_shape_generalization_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run300B_execute_split_forward_trade_shape_generalization_mt5_probe`

Effect(효과): Stage299(299단계)의 실제 MT5(메타트레이더5) validation(검증) 거래를 시간 순서 fold(분할)로 나눠 후보 6개를 만들었다. OOS(표본외)는 후보 구성에 쓰지 않았다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp300A_fold_consensus_shape_density50_surface | -4233.4 | 4.99 | -1375.2 | 4.99 | passed | failed | failed |
| cp300B_late_validation_veto_density55_surface | 0.0 | 0.00 | 0.0 | 0.00 | failed | failed | failed |
| cp300C_stable_session_directional_density60_surface | -5697.4 | 5.58 | -1606.3 | 5.78 | passed | failed | failed |
| cp300D_low_dd_microburst_density45_surface | -3147.2 | 4.48 | -1290.7 | 4.50 | passed | failed | failed |
| cp300E_regime_consensus_density70_surface | -4646.5 | 5.92 | -1220.5 | 6.37 | passed | failed | failed |
| cp300F_aggressive_forward_reexpand_density80_surface | -5017.5 | 8.13 | -3514.5 | 8.09 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
