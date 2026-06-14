# Frontier26 Joint Micro Satisfaction Lock Spec(전선26 미세 구간 합동 충족 잠금 명세)

Locks(잠금):
{
  "selection_split": "train_only",
  "forward_splits": "validation_oos_read_only",
  "changed_variable": "joint_micro_satisfaction_before_bridge_union",
  "forbidden_primary_path": [
    "dd_headroom_first_bridge_archetype_preselection",
    "density_first_bridge_score_or_posthoc_dd_repair_as_primary_proxy",
    "validation_oos_targeted_capped_filter_repair"
  ],
  "structural_unit": "same_side_pair_or_triple_entry_time_or_union",
  "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
  "opposite_side_rule": "do_not_mix_long_and_short_inside_one_union",
  "micro_gate_contract": {
    "train_profit_factor_min": 1.18,
    "train_dd_risk_max": 14.0,
    "train_trades_per_day_min": 2.0,
    "train_trades_per_day_max": 6.0,
    "train_equity_trend_r2_min": 0.7,
    "train_max_loss_streak_max": 18,
    "train_adverse_loss_p10_abs_max": "source_median_train_adverse_loss_p10_abs",
    "direction_note": "lower_or_equal_is_better_for_loss_magnitude; local verification corrected Grok sign(손실 크기는 작거나 같을수록 좋으므로 Grok 부등호 방향을 로컬 검증에서 보정)"
  },
  "union_gate_contract": {
    "union_size": "same_side_pair_or_triple",
    "train_profit_factor_min": 1.1,
    "train_dd_risk_max": 16.0,
    "train_trades_per_day_min": 5.0,
    "train_trades_per_day_max": 10.0,
    "overlap_ratio_max": 0.4,
    "min_unique_density_contribution_min": 0.4
  },
  "scoring_contract": "joint_micro_satisfaction_score is train-only and combines micro PF floor, micro DD margin, micro R2 floor, adverse-loss margin, union PF, overlap penalty, unique contribution, and density fit; DD headroom is not the primary rank term",
  "no_repair_in_frontier26b": "F26B must test pre-union joint micro eligibility only; no capped repair or val/OOS-targeted filter",
  "no_lifecycle_until_seed": "no lifecycle repair until a seed or handoff worthy proxy exists",
  "no_onnx_until_handoff": "no ONNX, MT5, or runtime probe execution until handoff_candidate_rows > 0",
  "non_repeat_proof": "compare F26B top10 micro_id keys against both F25B and F24B top10; overlap without seed-gap lift is repeat",
  "reference_only_prior_artifacts": "F24/F25 artifacts are clues only, not baselines, winners, promotions, or runtime authority"
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
