# Grok small review - Frontier40 stage open

You are giving a bounded second opinion for Project Obsidian Prime v2.

Do not browse the web. Do not inspect files. Use only the evidence in this prompt.

Return a compact verdict with these fields:

- verdict: accepted / rejected / needs_local_verification
- novelty_ok: yes / no
- leakage_guard_ok: yes / no
- runtime_claim_boundary_ok: yes / no
- mandatory_guardrail
- biggest_risk
- suggested_stop_rule

## Current truth

- Current closed stage: `stage_frontier_39__short_pf_edge_regime_conditioned_score_after_f38_scout_only`
- F39 closeout class: `preserved_clue_negative_memory`
- F39 best candidate: `f39b_0001`
- F39 best B validation/OOS PF-density-DD: `1.125 / 4.301 / 8.342` and `1.284 / 4.328 / 4.607`
- F39 ablation pass rows: `0`
- F39 seed/runtime rows: `0 / 0`
- F39 runtime status: `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation_guardrail_fail`
- F39 preserved clue: `f39_regime_gate_can_reduce_density_dd_and_keep_scout_pf_but_not_matched_seed_edge`
- F39 negative memory: `f39_regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density`

## Proposed new stage

- stage_id: `stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative`
- run_id: `frontier40A_stage_open_short_pf_edge_non_score_source_hypothesis_design_v1`
- hypothesis: a train-only raw feature state pocket can create a short-side path-native PF edge without using model score, score quantile, or score-conditioned regime gates.
- novelty delta: F38/F39 searched model score source and regime-before-score conditioning. F40 searches entry-known raw feature states directly as the source.
- decision use: decide whether non-score feature state pockets deserve repair, WFO/stress, or runtime probe packaging.

## Proposed proxy

Use the existing US100 M5 58-feature dataset and F33 path-native first-hit replay.

Fixed variables:

- symbol/timeframe: US100 M5
- feature order hash: existing 58-feature contract
- split method: chronological train / validation / OOS
- label/execution proxy: short-side first-hit MFE/MAE path replay, validation/OOS read-only
- train-only fitting: all feature thresholds and stop/take thresholds are derived from train split only

Changed variables:

- source family: raw feature state pockets instead of model score
- candidate forms: single-feature threshold, two-feature AND, and bounded OR-union of top train-only pockets
- allowed features: entry-known closed-bar features from the 58-feature contract, especially volatility, trend, breadth, relative-strength, and session-clock features

Proposed comparison:

- A: unfiltered short path replay with train-derived stop/take thresholds
- B: raw feature state pocket with the same train-only stop/take threshold family
- F39 best is reference only, not inherited baseline

Proposed scout/seed/runtime thresholds:

- scout clue: validation and OOS PF >= 1.03, density 4-12 trades/day, DD <= 18
- seed surface: validation and OOS PF >= 1.20, density 5-10 trades/day, DD <= 12
- runtime candidate: validation and OOS PF >= 1.50, density 5-10 trades/day, DD <= 10

Proposed repair rule:

- If broad raw-feature pockets create scout but no seed, allow one capped repair that tests bounded OR-union of train-only selected pockets.
- If no scout or no lift versus unfiltered A, close negative memory.
- If seed/runtime candidate appears, stop before expensive WFO/MT5 and run a pre-expensive Grok review.

## Claim boundary

Exploration only. No completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve.

## Review question

Is this a valid Frontier40 stage-open direction after F39, and what mandatory local guardrail should Codex enforce before any WFO/MT5/runtime work?
