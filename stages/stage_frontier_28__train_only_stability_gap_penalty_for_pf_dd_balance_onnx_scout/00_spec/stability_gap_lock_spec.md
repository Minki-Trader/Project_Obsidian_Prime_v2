# Frontier28 Stability Gap Lock Spec(전선28 안정성 격차 잠금 명세)

Locks(잠금):
{
  "selection_split": "train_only",
  "forward_splits": "validation_oos_read_only",
  "changed_variable": "train_subperiod_pf_dd_balance_stability_gap_rank",
  "hypothesis_delta": "replace F27 global soft penalty rank with train-only chronological chunk stability gap rank",
  "source_surface": "f27b_234_soft_union_surface_reference_only_not_inherited_baseline",
  "f27_soft_penalty_role": "reference_clue_only_no_weight_retune_no_forward_selection_loop",
  "candidate_construction": "rebuild F27/F24 same-side OR-union machinery, then re-rank by F28 train chunks",
  "chunking_contract": {
    "split": "train",
    "chunk_count": 4,
    "method": "chronological_equal_row_count_chunks_locked_at_stage_open",
    "no_post_hoc_edits": true
  },
  "stability_gap_terms": [
    "chunk_profit_factor_floor_shortfall",
    "chunk_dd_risk_max_pressure",
    "chunk_density_imbalance",
    "net_positive_chunk_count_shortfall",
    "chunk_equity_trend_r2_floor_shortfall",
    "chunk_max_loss_streak_pressure",
    "global_vs_chunk_pf_gap",
    "global_vs_chunk_dd_concentration"
  ],
  "selection_boundary": "rank_by_train_chunks_only_validation_oos_read_only",
  "forbidden_primary_path": [
    "retune_f27_soft_penalty_weights",
    "select_by_validation_or_oos_metrics",
    "restore_seed_surface_pressure_as_hidden_target",
    "f26_hard_gate_numeric_threshold_relaxation",
    "f25_dd_headroom_first_bridge_archetype_preselection",
    "f24_density_first_bridge_score_as_primary_rank",
    "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok"
  ],
  "success_boundary": {
    "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
    "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
    "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
    "not_completion": "final_goal_gates_not_applicable_until_final_completion_review"
  },
  "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
  "reference_only_prior_artifacts": "Stage12-364 and F24-F27 are clues only, not winners/baselines/promotions/runtime authority/live readiness",
  "chunk_boundaries": [
    {
      "chunk_id": "train_chunk_01",
      "row_start_index": 0,
      "row_end_index": 7305,
      "row_count": 7306,
      "start_timestamp": "2022-09-01T16:40:00+00:00",
      "end_timestamp": "2023-03-09T20:20:00+00:00"
    },
    {
      "chunk_id": "train_chunk_02",
      "row_start_index": 7306,
      "row_end_index": 14610,
      "row_count": 7305,
      "start_timestamp": "2023-03-09T20:25:00+00:00",
      "end_timestamp": "2023-09-28T19:25:00+00:00"
    },
    {
      "chunk_id": "train_chunk_03",
      "row_start_index": 14611,
      "row_end_index": 21915,
      "row_count": 7305,
      "start_timestamp": "2023-09-28T19:30:00+00:00",
      "end_timestamp": "2024-05-31T18:00:00+00:00"
    },
    {
      "chunk_id": "train_chunk_04",
      "row_start_index": 21916,
      "row_end_index": 29221,
      "row_count": 7306,
      "start_timestamp": "2024-05-31T18:05:00+00:00",
      "end_timestamp": "2024-12-31T22:00:00+00:00"
    }
  ]
}
