# Frontier30 Density Preserving Preselector Lock Spec(전선30 밀도 보존 사전 선택기 잠금 명세)

Locks(잠금):
{
  "selection_split": "train_only",
  "forward_splits": "validation_oos_read_only",
  "active_changed_variable": "train_density_preserving_preselector_before_loss_veto",
  "hypothesis_delta": "move density preservation before loss veto instead of relaxing F29 veto thresholds",
  "source_surface": "f28_f29_reference_surface_only_not_inherited_baseline",
  "exit_shape_pivot_role": "reference_fallback_only_not_active_changed_variable",
  "pipeline_order": [
    "F28_reference_union_surface",
    "train_only_density_preserving_preselector",
    "same_family_train_only_loss_veto",
    "read_only_validation_oos_diagnostics"
  ],
  "preselector_contract": {
    "score_grain": "source_union_level_train_only",
    "required_train_inputs": [
      "train_trades_per_day",
      "train_profit_factor",
      "train_dd_risk",
      "train_loss_count",
      "train_loss_capture_sensitivity",
      "removed_train_trade_fraction_sensitivity"
    ],
    "density_target_center": 7.5,
    "density_soft_band": [
      5.0,
      10.0
    ],
    "density_preservation_floor": 5.0,
    "source_keep_cap": 160,
    "source_keep_rule": "top_160_by_train_only_preselector_score",
    "candidate_branches": [
      "source_no_veto_density_preservation_branch",
      "top_density_preserving_loss_veto_variant_per_source"
    ],
    "max_removed_train_trade_fraction_after_veto": 0.28,
    "rank_formula": "train_density_margin + train_pf_balance + train_dd_containment + loss_capture_per_removed_trade - density_thinning_penalty",
    "no_validation_oos_rank_inputs": true,
    "no_post_hoc_edits": true,
    "all_variants_recorded": true
  },
  "forbidden_primary_path": [
    "retune_f29_loss_veto_thresholds_to_rescue_near_scout_rows",
    "select_by_validation_or_oos_pf_dd_density",
    "use_f29b_0274_forward_metrics_to_set_preselector_cutoffs",
    "activate_exit_shape_pivot_in_f30b_proxy",
    "inherit_f28_or_f29_winner_baseline_promotion_runtime_authority",
    "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok"
  ],
  "success_boundary": {
    "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
    "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
    "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
    "not_completion": "final_goal_gates_not_applicable_until_final_completion_review"
  },
  "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
  "tier_pair_boundary": "Tier B and Tier A+B are missing_required until explicitly materialized in this frontier"
}
