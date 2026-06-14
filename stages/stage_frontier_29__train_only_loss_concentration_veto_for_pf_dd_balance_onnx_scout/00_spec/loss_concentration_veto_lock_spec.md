# Frontier29 Loss Concentration Veto Lock Spec(전선29 손실 집중 차단 잠금 명세)

Locks(잠금):
{
  "selection_split": "train_only",
  "forward_splits": "validation_oos_read_only",
  "changed_variable": "train_loss_conditioned_veto_mask",
  "hypothesis_delta": "replace F28 train stability ranking with train-loss-conditioned veto masks",
  "source_surface": "f28b_234_stability_union_surface_reference_only_not_inherited_baseline",
  "f28_stability_rank_role": "reference_clue_only_no_weight_retune_no_forward_selection_loop",
  "candidate_construction": "reconstruct F28/F27 same-side OR-union masks, then apply train-loss veto variants",
  "veto_contract": {
    "pocket_definition": "candidate_train_trades_only_bottom_loss_region",
    "aggregation_grain": "trade_level_with_optional_session_chunk_diagnostics",
    "rule_family": "single_feature_loss_concentration_threshold_veto_and_capped_pair_veto",
    "max_variants_per_union": 8,
    "max_single_feature_variants_per_union": 4,
    "max_pair_variants_per_union": 4,
    "min_removed_train_trade_fraction": 0.03,
    "max_removed_train_trade_fraction": 0.35,
    "min_loss_capture_ratio": 0.12,
    "no_post_hoc_edits": true,
    "all_variants_recorded": true
  },
  "selection_boundary": "rank_by_train_loss_concentration_reduction_only_validation_oos_read_only",
  "forbidden_primary_path": [
    "retune_f28_stability_gap_weights",
    "select_by_validation_or_oos_metrics",
    "target_f28c_near_seed_or_pf_ready_rows_by_forward_metrics",
    "generic_f23_f24_feature_veto_replay_without_loss_concentration_key",
    "f26_hard_gate_numeric_threshold_relaxation",
    "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok"
  ],
  "success_boundary": {
    "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
    "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
    "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
    "not_completion": "final_goal_gates_not_applicable_until_final_completion_review"
  },
  "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
  "reference_only_prior_artifacts": "Stage12-364 and F24-F28 are clues only, not winners/baselines/promotions/runtime authority/live readiness"
}
