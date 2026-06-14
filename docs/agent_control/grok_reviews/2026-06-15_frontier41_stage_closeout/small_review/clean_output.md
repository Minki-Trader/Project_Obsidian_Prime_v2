## Grok closeout review (Frontier41)

1. **verdict:** `accepted`

2. **closeout_boundary_ok:** `yes`

3. **one risk:** Top-ranked exit-shape leader (`f40b_0013`) has **train PF &lt; 1.0** (0.958) while **PF lift vs same-entry is only ~1.1%** — preserving 94 scout clues is fine, but later work may over-weight DD-compression / `f41_exit_shape_score` and under-weight train–forward coherence.

4. **one next-stage clue:** Run the proposed **`capped_one_pass_tighter_tail_exit_family`** on high DD-reduction scouts (e.g. `f40b_0013`), and **in parallel** keep a train-positive, same-entry-locked track (e.g. `f40b_0011`) so the next pivot is not driven by exit-shape score alone.
