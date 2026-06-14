# Frontier24 Density Bridge Lock Spec(전선24 빈도 연결 잠금 명세)

Locks(잠금):
- selection_split: train_only
- forward_splits: validation_oos_read_only
- structural_unit: same_side_multi_pocket_entry_time_or_union
- duplicate_trade_rule: one_trade_per_timestamp_when_multiple_pockets_fire
- opposite_side_rule: do_not_mix_long_and_short_inside_one_bridge
- overlap_penalty: train_overlap_ratio_penalized_and_capped_before_forward_read
- diversity_guard: max_two_pockets_per_feature_family_and_min_two_families_for_bridge
- density_first: F24B optimizes density bridge first; DD normalization is only diagnostic or later repair
- no_lifecycle_until_seed: no lifecycle repair until density bridge seed surface exists
- no_onnx_until_handoff: no model training or ONNX branch until handoff candidate exists

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
