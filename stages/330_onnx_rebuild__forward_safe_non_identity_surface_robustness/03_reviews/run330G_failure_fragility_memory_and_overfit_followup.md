# run330G Failure Fragility Memory and Overfit Follow-up(330G 실패 취약성 기억 및 과적합 후속)

- run_id(실행 ID): `run330G_raw_forward_failure_fragility_memory_and_overfit_followup_v1`
- parent_run_id(부모 실행 ID): `run330F_raw_forward_mt5_kpi_regime_cost_curve_review_v1`
- status(상태): `completed_failure_fragility_memory_stage330_closed_no_selection`
- judgment(판정): `negative_memory_and_preserved_clues_no_forward_pass_no_goal_achieve`
- decision(결정): `stage330_closed_no_selection_forward_safe_rebuild_clues_preserved_stage331_open`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Pressure Matrix(압력 표)

| attempt(시도) | level(수준) | score(점수) | PF(수익 팩터) | cost+1 PF(비용+1 수익 팩터) | worst pocket(최악 포켓) | flags(표시) |
|---|---|---:|---:|---:|---:|---|
| c56_bal_rf | high | 20 | 1.0 | 0.805598 | -66.07 | net_too_small_for_forward_robustness;pf_near_flat;dd_percent_high;trade_density_below_us100_review_band;fails_plus1_cost_stress;fails_plus2_cost_stress;deep_rolling_curve_pocket;long_underwater_stretch;short_side_drag;db_source_missing_for_cp322a_attribution;run330f_fragility_flag |
| u42_bal_rf | high | 20 | 1.01 | 0.682058 | -77.21 | net_too_small_for_forward_robustness;pf_near_flat;dd_percent_high;fails_plus1_cost_stress;fails_plus2_cost_stress;deep_rolling_curve_pocket;long_underwater_stretch;short_side_drag;long_side_concentration;db_source_missing_for_cp322a_attribution;run330f_fragility_flag |
| m48_bal_rf | high | 16 | 1.08 | 0.745648 | -79.99 | pf_low_margin;dd_percent_high;fails_plus1_cost_stress;fails_plus2_cost_stress;deep_rolling_curve_pocket;long_underwater_stretch;short_side_drag;db_source_missing_for_cp322a_attribution;run330f_fragility_flag |
| u42_plain_rf | high | 13 | 1.17 | 0.760391 | -72.06 | pf_low_margin;fails_plus1_cost_stress;fails_plus2_cost_stress;deep_rolling_curve_pocket;short_side_drag;long_side_concentration;db_source_missing_for_cp322a_attribution;run330f_fragility_flag |
| m48_plain_rf | medium | 5 | 1.49 | 1.001302 | -62.79 | fails_plus2_cost_stress;deep_rolling_curve_pocket;long_side_concentration;db_source_missing_for_cp322a_attribution;watchlist_not_selection |
| c56_plain_rf | low | 4 | 1.67 | 1.278846 | -34.86 | trade_density_below_us100_review_band;fails_plus2_cost_stress;short_side_drag;db_source_missing_for_cp322a_attribution;watchlist_not_selection |

## Failure Memory(실패 기억)

- memory_counts(기억 수): `{"negative_memory": 4, "preserved_clue_not_selection": 2}`
- preserved_clues_not_selection(선택 아닌 보존 단서): `c56_plain_rf, m48_plain_rf`
- high_pressure_attempts(높은 압력 시도): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- effect(효과): raw-forward(원본 전진) 양수 후보도 비용, 곡선 포켓, 방향, D/B source(D/B 원천) 압력이 남으면 선택 후보가 아니다.

## Follow-up Queue(후속 대기열)

| queue(대기열) | stage(단계) | purpose(목적) | status(상태) |
|---|---|---|---|
| run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1 | 331_overfit_guard__cross_horizon_cost_curve_parity_probe | cross-horizon/cost/curve/parity guard design(교차 기간/비용/곡선/동등성 방어 설계) | planned_next |
| run331B_materialize_no_retune_replay_and_resampling_controls_v1 | 331_overfit_guard__cross_horizon_cost_curve_parity_probe | materialize no-retune replay controls(무재튜닝 재생 대조군 물질화) | planned_after_stage331A |
| run331C_runtime_replay_or_block_cross_horizon_probe_v1 | 331_overfit_guard__cross_horizon_cost_curve_parity_probe | runtime replay or block(런타임 재생 또는 차단) | planned_after_stage331B |
