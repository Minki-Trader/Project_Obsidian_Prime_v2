Project Obsidian Prime v2 - Frontier60 pre-MT5 review request

Required answer format:
1. verdict: accepted / rejected / needs_local_verification
2. proceed_to_mt5: yes / no / yes_but_negative_boundary
3. interpretation_locks: concise bullets
4. failure_modes_to_record: concise bullets

Current truth:
- User goal rule requires one MT5 Runtime Probe for every frontier stage, even when proxy is weak; it must be recorded as runtime_probe_observation, not promotion.
- F60 stage-open Grok accepted the hypothesis only under strict locks: fixed F59 score source, finite grid, one selected proxy, one MT5 probe, no repair ladder.
- F60 changed variable: entry-transition/close-on-flat/cooldown admission cadence on fixed F59 long score. No relabel, no retrain, no validation-guided threshold tuning.
- Selected proxy candidate: f60b_fixed_f59_long_entry_cadence_q80_cd2_same3_h4.
- Proxy train: PF 1.3579, DD 2.3035%, trades/day 2.4747.
- Proxy validation: PF 1.0182, DD 5.6620%, trades/day 2.7158.
- Proxy OOS: PF 0.9961, DD 2.0824%, trades/day 2.8321.
- Raw signal density is high (~11.82/day validation, ~12.64/day OOS) but entry-transition/cooldown suppresses entries to ~2.7-2.8/day.
- This misses the final density target, but final hard gates only apply at final completion review. In this stage, the purpose is to observe whether runtime economics improve or the long-axis friction escape should close as negative memory.
- Claim boundary: runtime_probe_observation only; no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.

Codex proposed action:
- Proceed to exactly one MT5 Runtime Probe because the user mandated it for each stage.
- Before running, record the negative boundary: proxy already fails density and OOS PF is below 1 by a hair, so MT5 cannot be read upward unless it unexpectedly restores PF/density/DD.
- If MT5 PF < 1 or density remains below 5/day, close F60 as negative memory_long_axis_friction_escape_failed or lost_density.

Question:
Under the user-mandated per-stage MT5 rule, is this single MT5 probe valid as an observation, and what interpretation locks should Codex preserve?
