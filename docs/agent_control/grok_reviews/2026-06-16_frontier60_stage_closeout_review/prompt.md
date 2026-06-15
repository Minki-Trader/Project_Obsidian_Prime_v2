Project Obsidian Prime v2 - Frontier60 stage closeout review request

Required answer format:
1. verdict: accepted / rejected / needs_local_verification
2. closeout_label: negative_memory / preserved_clue / invalid_setup / blocked / completion_candidate
3. must_record: concise bullets
4. forbidden_claims_check: pass/fail with reason

Current stage:
- stage: stage_frontier_60__long_axis_friction_escape_or_negative_memory.
- hypothesis: fixed F59 long-quality score plus entry-transition/close-on-flat/cooldown admission cadence may escape repeated-entry MT5 friction, or close long-axis friction escape as negative memory.
- changed variable: runtime representation/admission cadence only. No relabel, no retrain, no validation-guided threshold tuning.
- Grok stage-open: accepted with locks.
- Grok pre-MT5: accepted as yes_but_negative_boundary under user-mandated per-stage MT5 probe rule.

Proxy selected candidate:
- candidate: f60b_fixed_f59_long_entry_cadence_q80_cd2_same3_h4.
- train proxy: PF 1.3579, DD 2.3035%, density 2.4747/day.
- validation proxy: PF 1.0182, DD 5.6620%, density 2.7158/day.
- OOS proxy: PF 0.9961, DD 2.0824%, density 2.8321/day.
- Proxy already missed 5-10/day density and OOS PF was slightly below 1.

MT5 runtime probe:
- validation_is: completed/completed, PF 0.41, DD 14.89%, trades 661, trades/day 3.6120, feature_ready_diff 0, signal_diff -1501, entry_policy_suppression_count 1501.
- OOS: completed/completed, PF 0.51, DD 8.48%, trades 494, trades/day 3.7710, feature_ready_diff 0, signal_diff -1159, entry_policy_suppression_count 1159.
- Signal diff is expected entry-transition suppression, not feature mismatch. Feature_ready_diff is 0.
- No blocker; tester completed.

Codex proposed closeout:
- close as negative_memory_long_axis_friction_escape_failed_pf.
- Preserve only a narrow observation: admission cadence reduced repeated entries and improved DD relative to F59 raw OOS, but it did not restore PF or 5-10/day density; validation DD still exceeded 10%.
- Do not run repair ladder inside F60. Next frontier should pivot away from long-axis friction rescue toward a new PF source.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.

Question:
Accept or adjust this closeout? Name mandatory failure memory and do-not-repeat note.
