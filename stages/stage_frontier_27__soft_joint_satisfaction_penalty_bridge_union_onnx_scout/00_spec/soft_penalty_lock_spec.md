# Frontier27 Soft Penalty Lock Spec(전선27 연성 페널티 잠금 명세)

Locks(잠금):
{
  "selection_split": "train_only",
  "forward_splits": "validation_oos_read_only",
  "changed_variable": "soft_joint_satisfaction_penalty_rank",
  "hypothesis_delta": "replace F26 hard joint micro eligibility gate with train-only soft penalty rank before same-side OR-union",
  "source_micro_pool": "full_f24_80_micro_pocket_surface_reference_only_not_f26_three_passer_surface",
  "structural_unit": "same_side_pair_or_triple_entry_time_or_union",
  "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
  "opposite_side_rule": "do_not_mix_long_and_short_inside_one_union",
  "soft_penalty_contract": {
    "score_direction": "higher_is_better_after_penalty",
    "terms": [
      "train_profit_factor_shortfall_to_1_18",
      "train_dd_pressure_above_14",
      "train_density_distance_from_4_0_to_6_0_micro_band",
      "train_equity_trend_r2_shortfall_to_0_70",
      "train_max_loss_streak_pressure_above_18",
      "train_adverse_loss_p10_abs_pressure_above_source_median",
      "train_union_density_distance_from_7_5",
      "train_union_dd_pressure_above_16",
      "train_overlap_ratio_penalty",
      "min_unique_density_contribution_reward"
    ],
    "not_allowed": "using F26 micro_gate_contract or union_gate_contract pass/fail as the primary selector"
  },
  "broad_scout_envelope": {
    "purpose": "diagnostic_admission_after_penalty_rank_not_final_gate",
    "train_net_profit": "> 0",
    "train_profit_factor_min": 1.06,
    "train_trades_per_day_min": 4.0,
    "train_trades_per_day_max": 11.5,
    "train_dd_risk_max": 22.0,
    "overlap_ratio_max": 0.55,
    "min_unique_density_contribution_min": 0.35
  },
  "forbidden_primary_path": [
    "f26_hard_gate_numeric_threshold_relaxation",
    "f25_dd_headroom_first_bridge_archetype_preselection",
    "f24_density_first_bridge_score_as_primary_rank",
    "validation_oos_targeted_repair_or_selection",
    "onnx_mt5_runtime_probe_before_handoff_candidate"
  ],
  "invalid_setup_tripwire": "if F27B creates rows only by widening F26 caps without the written soft penalty mechanism, close invalid_setup",
  "no_repair_in_frontier27b": "F27B tests the locked penalty mechanism only; no capped repair or validation/OOS-targeted filter",
  "no_lifecycle_until_seed": "no lifecycle repair until a seed or handoff worthy proxy exists",
  "no_onnx_until_handoff": "no ONNX, MT5, or runtime probe execution until handoff_candidate_rows > 0",
  "non_repeat_proof": "compare F27B top10 keys against F24B, F25B, and F26B; overlap without seed-gap lift is repeat",
  "reference_only_prior_artifacts": "F24/F25/F26 artifacts are clues only, not baselines, winners, promotions, or runtime authority"
}

Criteria(기준):
{
  "scout_clue": {
    "pf": 1.1,
    "density_low": 5.0,
    "density_high": 10.0,
    "dd_cap": 25.0
  },
  "seed_surface": {
    "pf": 1.2,
    "density_low": 5.0,
    "density_high": 10.0,
    "dd_cap": 18.0
  },
  "handoff_candidate": {
    "pf": 1.5,
    "density_low": 5.0,
    "density_high": 10.0,
    "dd_cap": 12.0,
    "equity_trend_r2": 0.35
  }
}
