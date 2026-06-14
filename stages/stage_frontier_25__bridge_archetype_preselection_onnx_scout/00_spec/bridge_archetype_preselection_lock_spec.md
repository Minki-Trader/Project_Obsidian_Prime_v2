# Frontier25 Bridge Archetype Preselection Lock Spec(전선25 연결 원형 사전 선택 잠금 명세)

Locks(잠금):
- selection_split: train_only
- forward_splits: validation_oos_read_only
- changed_variable: dd_headroom_first_bridge_archetype_preselection
- forbidden_primary_path: density_first_bridge_score_or_posthoc_dd_repair_as_primary_proxy
- structural_unit: same_side_pair_or_triple_entry_time_or_union
- duplicate_trade_rule: one_trade_per_timestamp_when_multiple_pockets_fire
- opposite_side_rule: do_not_mix_long_and_short_inside_one_archetype
- archetype_score_contract: train-only score includes per-pocket train DD cap, bridge train DD headroom to 18%, equity_trend_r2, overlap ratio, min unique contribution, family diversity, and 5-10/day density
- non_repeat_proof: compare top10 micro_id keys against Frontier24B top10 and require DD-headroom lift if overlap exists
- no_repair_in_frontier25b: F25B must test preselection only; capped repair is not allowed in the primary proxy path
- no_lifecycle_until_seed: no lifecycle repair until a seed or handoff worthy proxy exists
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
