# run286A Trade Density Curve Quality Materialization(286A 거래 밀도/곡선 품질 물질화)

- stage_id(단계 ID): `286_onnx_candidate_campaign__trade_density_curve_quality_rebuild`
- run_id(실행 ID): `run286A_design_materialize_trade_density_curve_quality_candidates_v1`
- status(상태): `completed_trade_density_curve_quality_candidate_inputs_materialized_no_selection`
- judgment(판정): `high_scale_signal_density_candidates_materialized_no_candidate_selection`
- branch_count(분기 수): `5`
- supply_rows(공급 행): `20`
- target_band_rows(목표 범위 행): `8`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run286B_execute_trade_density_curve_quality_mt5_probe`

## Fresh Thesis(새 논제)

Stage286(286단계)는 cp282D(282D 후보)의 ONNX(온엑스) 기술 성공을 보존하지 않는다.
Effect(효과): 새 후보는 먼저 4-10 trades/day(일 4-10거래), 순수익 규모, 확대 구간 곡선 품질을 만족해야 한다.

## Candidate Queue(후보 대기열)

- `cp286A_entry_dense_direct_surface`: validation approx(검증 근사) `3.44` trades/day(일 거래), OOS approx(표본외 근사) `3.67` trades/day(일 거래).
- `cp286B_trend_density_thr58_surface`: validation approx(검증 근사) `4.68` trades/day(일 거래), OOS approx(표본외 근사) `5.00` trades/day(일 거래).
- `cp286C_trend_density_thr52_surface`: validation approx(검증 근사) `6.70` trades/day(일 거래), OOS approx(표본외 근사) `6.95` trades/day(일 거래).
- `cp286D_trend_density_thr48_surface`: validation approx(검증 근사) `8.19` trades/day(일 거래), OOS approx(표본외 근사) `8.46` trades/day(일 거래).
- `cp286E_macro_blend_density_surface`: validation approx(검증 근사) `7.86` trades/day(일 거래), OOS approx(표본외 근사) `8.18` trades/day(일 거래).

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`

Effect(효과): 이 실행은 MT5(메타트레이더5) 압박 입력을 만든 것이며 후보 선택, Adapter(어댑터), ONNX(온엑스) 진행은 주장하지 않는다.
