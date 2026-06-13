Acting as external second opinion — I'll read the Grok collaboration skill and the bounded Frontier06/07 evidence to review the Frontier08 proposal.
## Grok External Second Opinion — Frontier08 Stage-Open Review

**Review size:** medium review (제한 스냅샷 + 집중 질문)
**Advice classification:** `accepted` with bounded conditions (조건부 수용)

---

### 1. Recommendation(권고)

**`open_frontier08` (전선08 개방)**

Not `revise_direction` or `do_not_open`. The core hypothesis is the right next axis; what needs tightening is Frontier08B execution bounds, not the stage thesis.

---

### 2. Reasoning(근거)

**Why open, not close**

Frontier06–07 show a stable pattern: **partial axis gains, zero strict scout rows**.
- F06: runtime abstention improved OOS density/PF/DD (~5.31/day, 1.267, 21.11%) but validation PF stayed weak and strict rows = 0.
- F07: risk-shaped labels cut OOS DD (~13.09%) and class-prior bridge lifted density (~4.12/day), but validation DD stayed very high, PF weak, strict rows = 0.

That pattern points to a **training objective problem**, not just labels or inference rules. The model may still treat ambiguous, DD-heavy path rows as equally important during loss — even when labels encode risk.

Frontier08 shifts the changed variable to **per-row train loss geometry** while holding fixed:
- `feature_set_v2`
- chronological split
- `[p_short, p_flat, p_long]` ONNX contract
- no validation/OOS threshold fitting

That is a **genuine novelty delta** relative to F06 (runtime abstention) and F07 (label geometry + global class priors). F07D explicitly called for a new hypothesis axis without inheriting winners — this fits.

**Why not full `revise_direction`**

The hypothesis is coherent and falsifiable. F07C’s directional class-prior weights (1.25–2.00) are **global, class-level** weighting. Frontier08’s per-row path-utility weighting is a different mechanism. The risk is confounding, not conceptual duplication — solvable with bounds, not a new stage topic.

**Why not `do_not_open`**

You have not exhausted the train-side objective surface. Stopping now would leave an unexplained gap: F07 improved *what* the model predicts, but not *which rows* the loss prioritizes. Sample weighting is the natural next lever before expensive WFO/MT5.

**One local verification note for Codex**

Stage ID naming drifts between `sample_weighted_objective` and `multi_objective_sample_weighting`. Resolve to one canonical ID before materializing artifacts.

---

### 3. Required bounds for Frontier08B(전선08B 필수 경계)

| Bound | Requirement |
|---|---|
| **Paired controls** | Every weighted run must have a **matching unweighted control** on identical rows, split, model spec, seed, and label surface. Primary comparison is weighted vs its own control — not vs F06/F07 best rows. |
| **Train-only weight derivation** | Weights from **train split only**, using train-side target/path utility. No validation/OOS columns, no post-hoc KPI tuning, no weight fitting on eval splits. |
| **Isolation from F07 confound** | Frontier08B must **not** combine per-row utility weights with F07 class-prior bridge weights in the same candidate. Run them as separate families or forbid mixing in v1 scout. |
| **Minimum control ladder** | At least four baselines: (a) label_v1 unweighted, (b) one F07 risk-shaped label unweighted reference only, (c) train-only class-balance-only weighting, (d) per-row utility weighting families. This separates “any weighting helps” from “path-utility weighting helps.” |
| **Weight family cap** | Cap at **≤4 weight families × ≤3 variants each** for first scout. No open-ended sweep. Stop after one broad pass unless a preserved clue appears. |
| **Weight transparency** | Log per-family weight stats: mean, std, min, max, % clipped, % zeroed, train-row coverage. Flag degenerate weights (all ~1.0 or extreme concentration on <5% of rows). |
| **Four-axis paired improvement** | Scout clue requires weighted model to beat **its unweighted control** on validation **and** OOS for density, PF, DD, and smoothness together — same bar that blocked F06/F07. |
| **Density band** | Target band stays **5–10/day** on validation and OOS vs control, not vs F06/F07 reference surfaces. |
| **ONNX parity gate** | Every trained model: ONNX probability parity before KPI read. Fail = invalid row, not preserved clue. |
| **Reference surfaces only** | label_v1 and one F07 risk-shaped label are **read-only references**. They are not winners, baselines, or repair seeds. |
| **Tier honesty** | Tier B and Tier A+B: `missing_required` if unavailable — do not omit. |
| **Stop rule** | If weighting moves only density or only DD vs control → preserved clue or negative memory. **No WFO/MT5** without strict scout clue. |
| **No threshold escape hatch** | Argmax-only inference in scout. No abstention rules, no validation/OOS threshold grids — that would reopen F06. |

---

### 4. Risks(위험)

1. **Hidden F07 re-encoding** — Per-row utility weights derived from the same path features that shaped F07 labels may just re-apply label geometry inside the loss. The class-balance-only control is mandatory to detect this.

2. **Single-axis illusion again** — Utility downweighting of ambiguous/flat rows may lift density or cut DD without lifting PF or smoothness, repeating F06/F07.

3. **Validation DD blind spot** — F07’s best OOS DD sat beside validation DD ~53–59%. Weighting may overfit train-path cleanliness and fail validation stability.

4. **Weight degeneracy** — Extreme downweighting can collapse effective train size, producing sparse/overconfident models with pretty OOS DD and weak PF.

5. **Sweep creep** — “Broad sweep” language invites F06-style unbounded search. The cap above is non-negotiable for 08B v1.

6. **False progress via reference cherry-picking** — Comparing against F06 abstention or F07 best rows instead of paired controls would inflate scout reads.

7. **Conceptual overlap with Stage12 recency weighting** — Prior `sample_weight` work (recency policy) failed without promotion. Frontier08 must show **path-utility weighting** is different, not “sample_weight retry.”

---

### 5. Do-not-claim boundary(주장 금지 경계)

Grok does **not** authorize any of the following from stage-open or scout-only work:

| Forbidden claim | Boundary |
|---|---|
| completion / Goal Achieve | Not claimable |
| selected baseline / winner inheritance | Not claimable — F06/F07 rows are reference only |
| promotion_candidate → operating_promotion | Not claimable |
| runtime_authority / live readiness | Not claimable |
| strict scout clue | Not claimable until validation **and** OOS four-axis paired pass exists |
| WFO/MT5 justification | Not claimable without strict scout clue |
| “sample weighting solves DD” | Not claimable from OOS-only or density-only movement |
| ONNX parity as alpha evidence | Parity is validity gate only, not performance proof |

**Allowed after 08B (scout scope only):** preserved clue, negative memory, invalid/blocked rows, and “weighted vs control delta on named axes” — with explicit validation/OOS split honesty.

---

### Summary for Codex

**Open Frontier08.** The hypothesis closes a logical gap left by F06 (inference) and F07 (labels/priors): **train loss row prioritization**. Keep the thesis; enforce paired unweighted controls, train-only weight derivation, F07-confound isolation, weight-family cap, and the same strict four-axis bar that blocked prior frontiers. If 08B only moves one axis again, close as preserved clue or negative memory — do not escalate to WFO/MT5.
