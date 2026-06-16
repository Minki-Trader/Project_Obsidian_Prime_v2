# F70 Stage Open Review — Grok Second Opinion

**Review size:** medium (제한 스냅샷 + 집중 질문 3개)  
**Advice classification:** mixed — **accepted** on novelty framing and scout priority; **needs_local_verification** on whether F70 execution stays off the F69 repair rail  
**Claim boundary:** scout clue / seed surface only. No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

## 1. Genuinely new after F69, or disguised trade-shape-only repair?

**Verdict: conditionally new — not automatically a repeat, but high disguise risk if exit shape leads.**

F69’s negative memory is narrow: **event-first ExtraTrees + trade-shape-only repair** could not jointly satisfy density, PF, and DD. F69’s preserved clue is different: **ONNX/probability/signal/feature parity was exact**, and RuntimeVetoTape worked as an observation bridge. The runtime split (sparse PF 2.94 at ~0.04 trades/day vs dense PF 1.19 at ~1.34 trades/day) reads less like “bad trees” and more like **label/selection mismatch across density regimes**.

F70 is **genuinely new** if the primary move is upstream:

| F70 element | New vs F69? | Why |
|---|---|---|
| Regime/session-conditioned **asymmetric value + exit-survival labels** | **Yes** | Moves cause before threshold/cooldown/quota tuning |
| **Density embedded in label/selection** | **Yes** | Attacks F69E’s “650 rows, 0 final-like, 0 joint-soft” at the objective, not post-hoc |
| Model-family rotation (linear / EBM-like / small NN; ExtraTrees-light reference only) | **Yes** | Breaks F69’s ExtraTrees-centric repair path |
| Exit shape (fixed-hold vs exit-triggered, long/short routing) | **Partial overlap** | Same surface family as F69 if it becomes the lead variable |
| Explicit ban on F69 threshold/cooldown/daily-quota loop | **Good guard** | Necessary but not sufficient |

**Disguise pattern to watch:** F70 can look new on paper while still being trade-shape repair if scouts mostly vary hold/exit routing and then “fix density” with selection knobs. That would recreate F69 with regime labels pasted on top.

**Codex direction (accepted with guard):** Treat F70 as **label-and-regime hypothesis**, not **exit-shape hypothesis**. Exit shape belongs in **ablation**, not as the first scout axis.

---

## 2. First proxy scout priority

**Recommended order:**

```text
1) label/target  (+ coupled regime/session conditioning)
2) regime/session split  (as label strata, not standalone slicing)
3) model family  (only after 1–2 show a movable proxy signal)
4) exit shape  (reference/ablation only; never lead)
```

**Why label/target first**

- F69 already showed **PF can exist** (sparse OOS) while **density destroys PF** (dense OOS). That is classic misaligned objective / selection, not proof that the model family is exhausted.
- “Density-aware labels” and “asymmetric value labels” directly test whether one training objective can speak to both regimes — the core F70 hypothesis.
- F69E’s zero final-like and zero joint-soft rows argue the old repair surface was **empty**; a new scout should start where the empty set was defined (objective/label), not where F69 already spent its budget (trade-shape knobs).

**Why regime/session is second, coupled**

- The sparse/dense split is strong **scout clue** that conditioning may matter.
- Regime/session alone, without label redesign, risks becoming **sliced F69** (same repair, smaller buckets).
- Best F70 scout unit: **regime-specific asymmetric value / exit-survival label**, not “same label, filter by session.”

**Why model family third**

- Rotation is justified because F69’s ExtraTrees path failed jointly — but family change without label change often preserves the same PF/density tradeoff under a new name.
- ExtraTrees-light as **reference only** is correct; leading with trees again would inherit F69’s failure mode.

**Why exit shape last**

- F69 negative memory explicitly condemns trade-shape-only repair.
- Exit-triggered hold and asymmetric routing are valid **seed surface**, but leading here is the highest-probability path back to F69.

**First concrete scout (one packet, not four parallel fronts):**  
One regime/session stratum × one asymmetric value label × one density-aware selection rule × one interpretable model (linear or EBM-like). Shallow ExtraTrees only as a **parity/reference** row, not as the hypothesis carrier.

---

## 3. Failure condition → close F70 as negative memory (not keep repairing)

Close F70 as **negative memory** when **any** of these hold after a bounded scout pass (not one bad run):

### A. Same structural split, no new PF source
Proxy evidence still shows **high PF only at near-sparse density** and **PF collapses at target-density band** (~1+ trades/day scout band), with no stratum where PF and density move together.  
→ F70 hypothesis false: regime labels did not unify the sparse/dense fracture.

### B. Label-led scouts do not beat the empty repair surface
Across the planned label/regime scout grid, **no row** clears a pre-declared **joint-soft floor** (density band + PF floor + DD ceiling) and **no trend** toward a final-like row.  
Echo of F69E (many rows, zero viable joint rows) after **label-first** work → close; more threshold/cooldown/quota repair is repeat, not F70.

### C. Disguised F69 repair detected
Most iterations vary **exit shape, threshold, cooldown, or daily quota** while labels/regime stay cosmetic.  
→ Negative memory: “regime-specific trade-shape repair.”

### D. Model rotation without frontier movement
Linear / EBM-like / small NN / ExtraTrees-light all reproduce the **same Pareto knee** (PF vs density) with only noise-level differences.  
→ Negative memory: “model family is not the binding constraint; label/selection is.”

### E. Runtime probe contradicts proxy (if probe is run)
Meaningful proxy signal appears in research, but mandatory MT5 Runtime Probe shows **density or PF collapses** while parity stack stays exact (F69 preserved clue pattern).  
→ Negative memory: “proxy does not materialize under runtime-compatible envelope.”

**Do-not-repair rule after failure:**  
Do **not** open “F70B threshold sweep” or “F70C exit-shape rescue.” Either pivot to a **new hypothesis stage** (different label ontology or different feature contract) or archive. Per F69, post-hoc envelope rescue is out of scope.

---

## Summary for Codex

| Question | Grok answer |
|---|---|
| 1. New enough? | **Conditionally yes** — if label/regime/density-in-selection leads; **no** if exit-shape + quota tuning leads |
| 2. First scout priority | **label/target first**, regime/session **coupled second**, model family third, exit shape **ablation only** |
| 3. Close as negative memory when | Same sparse/dense fracture; zero joint-soft rows after label-first scouts; F69-style repair in disguise; model rotation moves nothing; runtime probe fails to materialize |

**Final Codex direction (accepted):** Open F70, but bind the stage contract to **one label-regime scout packet first**. Treat the sparse/dense OOS split as the **success/failure ruler**, not as motivation for another trade-shape repair loop.

**needs_local_verification (Codex-owned, not Grok):** Whether the repo’s F70 packet schema actually enforces label-first ordering and blocks F69 repair knobs by default — that cannot be judged from this snapshot alone.
