Frontier25 stage open review — gathering Frontier24 closeout evidence and frontier governance rules to judge the proposal.
## Frontier25 Stage Open Review

Local check against F24 closeout artifacts (`negative_memory.md`, `preserved_clue.md`, `density_bridge_lock_spec.md`, F24B `bridge_score`) matches your bounded evidence. F24 is closed; F24D already routes to `frontier25A_stage_open_bridge_archetype_preselection_hypothesis_design_v1`.

---

**1. verdict:** `accepted`

**2. novelty_check:** `acceptable_new_hypothesis`

F24B already built pair/triple OR-union bridges with overlap/diversity guards on train-only data. F25 is still valid because the **decision order** changes: F24 was `density_first` (density in the score numerator, DD repair deferred to F24C); F25 tests whether **DD-headroom-first archetype preselection** can reach seed/handoff without making capped repair the primary path. That matches F24’s explicit reopen condition in `negative_memory.md`.

Not `repeat` — if F25 only reweights F24B’s `bridge_score`, it becomes a repair loop. Not `invalid_setup` — testable with existing F24 micro-pocket artifacts and unchanged scout/seed/handoff gates.

---

**3. must_lock:**

- **Reference-only F24 inputs:** reuse F24B micro-pocket assembly + OR-union semantics; `f24c_0105/0106/0163` and `f24b_0174` are clues, not baselines/winners.
- **Validation philosophy flip:** write `density_first` as forbidden; lock `dd_headroom_first_preselection` as the changed variable.
- **Train-only selection:** rank archetypes on train only; validation/OOS are read-only flag columns — no validation/OOS in ranking (F24 closeout Grok note mentioned “validation DD headroom”; do **not** import that into F25 locks).
- **Explicit archetype score contract:** F25A must document a formula **distinct from F24B `bridge_score`** — must include per-pocket train DD cap, bridge train DD headroom to seed gate (18%), equity-trend R², overlap, min unique contribution, family diversity, density 5–10/day.
- **No repair in F25B primary path:** forbid F24C-style capped DD normalization as the first proxy; repair only as optional F25C if F25B produces zero seed-surface rows.
- **Unchanged gate thresholds:** carry F24 scout/seed/handoff PF-density-DD caps unchanged.
- **Runtime boundaries:** Tier A proxy only; Tier B `missing_required`; no ONNX/MT5/lifecycle until `handoff_candidate_rows > 0`.
- **Non-repeat proof:** F25A must require top-10 F25 vs F25B ID comparison against F24B top-10; overlap without metric lift = repeat.

---

**4. stop_conditions:**

- **Invalid setup:** zero pair/triple archetypes pass per-pocket train DD cap + 5–10/day density after headroom-first filter.
- **Repeat:** top F25B rows are substantially the same `micro_ids`/bridge keys as F24B leaders (e.g. `f24b_0174` lineage) with no train DD-headroom lift.
- **Negative memory confirmed:** seed/handoff appears only after adding F24C-like repair → close as “preselection insufficient; repair-only path repeats F24 failure.”
- **Preserved-clue-only exit:** preselected archetypes show train headroom but validation/OOS PF &lt; 1.10 or forward DD still blocks seed on all top-K.
- **Blocked open:** F25A ships without written archetype score formula + explicit F24B diff → do not materialize F25B.

---

**5. smallest_proxy:**

**F25B only** — no repair pass:

1. Reload F24B `micro_pockets` table.
2. Rebuild same-side pair/triple OR-unions.
3. Hard-filter: per-pocket `train_dd ≤ 16%`, bridge `train_dd ≤ 18%`, density 5–10/day, `train_pf ≥ 1.06`, overlap/unique-contribution/diversity guards.
4. Rank survivors by headroom-first score, e.g.
   `(18 - bridge_train_dd) × min_unique_contrib × family_diversity / (1 + overlap_ratio)`
   with equity-trend R² as tie-breaker.
5. Emit `train_ranked_archetype_table.csv` + read-only validation/OOS scout/seed/handoff flags.
6. Compare top-10 vs F24B top-10 to prove non-repeat.

Defer ONNX/MT5 entirely until a handoff-worthy row exists.

---

### Plain read

F24 showed that “build density first, fix DD later” can reach scout clues but not seed/handoff. Frontier25 is a fair next stage if it genuinely flips that order: pick safer bridge shapes on train **before** any repair. Accept F25A open, but lock the scoring formula so F25B is not F24B with a new label. The smallest first test is a headroom-first re-rank of existing F24 pockets with no repair — that directly tests the new hypothesis at minimum cost.
