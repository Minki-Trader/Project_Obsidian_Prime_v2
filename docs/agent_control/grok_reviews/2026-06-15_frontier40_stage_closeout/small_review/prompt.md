# Grok small review - Frontier40 closeout

You are giving a bounded second opinion for Project Obsidian Prime v2.

Do not browse the web. Do not inspect files. Use only the evidence in this prompt.

Return a compact verdict with these fields:

- verdict: accepted / rejected / needs_local_verification
- closeout_ok: yes / no
- runtime_boundary_ok: yes / no
- guardrail_followed: yes / no
- biggest_risk
- must_not_repeat
- next_stage_hint

## Current stage

- stage_id: `stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative`
- hypothesis: a train-only raw feature state pocket can create a short-side path-native PF edge without using model score, score quantile, or score-conditioned regime gates.
- claim boundary: exploration closeout only. No completion, no baseline, no promotion, no runtime authority, no live readiness.

## Prior reference, not inheritance

- F39 closeout class: `preserved_clue_negative_memory`
- F39 preserved clue: `f39_regime_gate_can_reduce_density_dd_and_keep_scout_pf_but_not_matched_seed_edge`
- F39 negative memory: `f39_regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density`
- F39 seed/runtime rows: `0 / 0`
- F39 runtime status: `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation_guardrail_fail`

## Stage-open Grok guardrail

Stage-open Grok accepted the direction and required local guardrails:

- train-only selection freeze
- search budget cap: single feature, two-feature AND, and one capped OR repair only
- density-matched A comparison
- no WFO/MT5/runtime packaging without seed/runtime rows
- entry-known closed-bar feature audit

Codex locally implemented:

- thresholds and stop/take levels from train only
- validation/OOS read-only
- density-matched A as a deterministic periodic baseline using train coverage
- candidate inputs limited to 58 closed-bar feature contract fields
- one capped OR-union repair selected only from train-ranked pockets

## Official result

- condition rows: `30`
- candidate rows: `521`
- scout rows: `181`
- seed rows: `0`
- runtime rows: `0`
- closeout class: `preserved_clue_negative_memory`

Best candidate:

- candidate_id: `f40b_0001`
- candidate kind: `pair_and`
- rule: `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25`
- validation PF-density-DD: `1.154 / 7.262 / 11.867`
- OOS PF-density-DD: `1.158 / 7.985 / 13.517`
- minimum PF lift vs density-matched A: `0.187`
- scout flag: true
- seed flag: false
- runtime flag: false

Interpretation:

- Raw feature pockets created density-matched scout clues.
- No seed surface appeared because forward PF stayed below 1.20 and/or DD stayed above seed limits.
- No runtime candidate appeared.
- Capped OR repair did not create seed/runtime candidate.

## Proposed runtime boundary

`runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f40_proxy_repair`

No MT5 Strategy Tester run is proposed for this closeout because there is no seed/runtime candidate to hand off.

## Proposed closeout

- closeout_class: `preserved_clue_negative_memory`
- preserved clue: `f40_raw_feature_pair_pockets_create_density_matched_short_scout_edge_reference_only`
- negative memory: `f40_raw_feature_state_pockets_did_not_create_seed_or_runtime_candidate`
- next stage: `stage_frontier_41__short_pf_edge_exit_shape_source_pivot_after_f40_raw_pocket_scout`
- next run: `frontier41A_stage_open_short_pf_edge_exit_shape_source_hypothesis_design_v1`

## Review question

Is this an honest Frontier40 closeout without MT5 runtime execution, given scout rows exist but seed/runtime rows are zero?
