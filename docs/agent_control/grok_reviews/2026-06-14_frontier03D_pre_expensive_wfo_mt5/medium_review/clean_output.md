Grok review request — I'll read the collaboration skill and the bounded evidence files you cited before answering.
Verifying cited hashes and checking stage aspiration thresholds for density/PF.
## Grok External Review — Frontier03 Pre-Expensive Decision

**Review size:** medium review (제한 스냅샷 + 집중 질문)
**Local verification note:** Bounded evidence files were read; cited KPIs and `onnx_parity: true` match the Frontier03C report and manifest. Hash re-check was not re-run in this turn.

---

### 1. Recommendation(권고)

**`repair_first` (수리 우선)**

Do **not** proceed to narrow WFO/stress/MT5 precheck yet. Do **not** closeout as negative memory yet.

---

### 2. Reasoning(근거)

**Density below 5/day is a soft stop for exploration, but a hard stop for expensive precheck.**

Frontier03C’s own `onnx_seed_observation_flag` only requires parity, non-sparse val/OOS, positive val/OOS net, and aspiration distance below loose ceilings. It does **not** require `density_pass` or `pf_pass`. So 3.34/day and PF 1.17 are enough to call this a **seed observation(씨앗 관찰)** — not enough to justify **expensive verification(비싼 검증)**.

**The main problem is oracle→model collapse, not missing WFO.**

| Split | Frontier03B oracle proxy | Frontier03C best ONNX |
|-------|--------------------------|------------------------|
| OOS density | 8.02/day | 3.34/day |
| OOS PF | 999 (oracle-bound) | 1.17 |
| OOS net | 7.85 | 0.125 |

Roughly **58% density loss** and **near-total edge loss** after distillation. WFO/MT5/stress mostly test what is already on the table; they do not fix a teacher-student gap this large.

**Best surface fails aspiration on multiple axes.**

For `f03c_logreg_f03b_v08__p46__m3__cd6`:
- `density_pass`: false on train / val / OOS
- `pf_pass`: false on train / val / OOS (aspiration PF floor = 2.0)
- `joint_pass_count`: train 0, val 1, oos 1 (mostly DD only)
- Val PF **1.12** is weaker than OOS PF **1.17** → ranking is fragile

**Classifier metrics support “barely learnable,” not “runtime-ready.”**
- Balanced accuracy ~0.48–0.49 across splits
- Heavy flat-teacher vs over-active short predictions
- 23 observation rows out of 192 decision rows = thin positive island, not a stable surface

**ONNX parity is necessary but not sufficient.**
Parity proves export/runtime feasibility. It does not prove the decision surface is worth WFO/MT5 cost.

**Exploration mandate alignment.**
Exploration has no gates, but this gate is **pre-expensive**, not “stop exploring.” Cheap Python repair should run before expensive falsification.

---

### 3. Risks(위험)

**If Codex proceeds to precheck now:**
- WFO/MT5 spend likely confirms weak PF and low density — high cost, low information gain
- Marginal positive net (0.12–0.14) may look “alive” under stress while PF collapses below 1.0
- Single-teacher lock-in (`f03b_v08` only) may miss better distill targets among Frontier03B’s 12 go-rule rows
- Threshold-only density repair may lift trades/day while destroying PF/DD — needs joint guardrails

**If Codex repairs without bounds:**
- Endless threshold sweeps on a weak teacher
- Chasing density toward 5/day with PF falling toward 1.0
- Treating oracle PF=999 as if the ONNX model inherited that edge

**If Codex closes out too early:**
- Valid stage question (“can regime-asymmetric labels distill to ONNX?”) is not fully tested — only one teacher + one micro-grid pass

---

### 4. Narrow next experiment(좁은 다음 실험)

**Proposed run:** `frontier03D_regime_asymmetric_label_model_repair_v1`
(already named in the Frontier03C pipeline as the repair path)

**Scope (bounded, cheap):**
1. **Decision-surface repair first** on existing ONNX — no new training yet
   - Bias grid toward density: lower `probability_threshold`, shorter `cooldown_bars`, test `side_mode` variants if cheap
   - Hold `hold_bars=12` fixed initially to limit degrees of freedom

2. **If step 1 fails**, train **1–2 additional teachers** from other Frontier03B go-rule variants (e.g. `f03b_v11_trend_density_restore`, `f03b_v04_trend_easy_chop_strict`) — not all 12

3. **Do not open WFO/MT5** in this repair pass

**Repair success criteria (to unlock precheck):**
- OOS density ≥ **4.5/day** (interim; full aspiration band remains 5–10/day)
- Val **and** OOS PF ≥ **1.20**
- Val **and** OOS net > 0
- DD not worse than current best (~9.6% val / ~7.2% OOS)
- ONNX parity remains `True`

**Repair stop criteria (then reconsider closeout negative memory):**
- No row reaches OOS density ≥ 4.0 with PF ≥ 1.15 after bounded repair + ≤2 extra teachers
- Or density rises but PF drops below 1.10 on either val or OOS

---

### 5. Do-not-claim boundary(주장 금지 경계)

Codex must **not** claim:
- completion / selected baseline / promotion / runtime authority / live readiness / Goal Achieve
- “precheck passed” or “WFO-ready”
- “tradable signal confirmed” — Frontier03B remains oracle-bound; Frontier03C remains seed observation
- that positive val/OOS net alone justifies MT5 runtime probe
- that density 3.34/day is “close enough” for expensive verification
- that Frontier03B scout clue transfers to ONNX without repair evidence

**Allowed claims after repair pass only:**
- `onnx_seed_observation_no_authority` continued, or
- `repair_failed_bounded_negative_memory` if stop criteria hit, or
- `precheck_eligible_no_authority` if repair success criteria are met — still not promotion/runtime

---

### Codex receipt hint (for local closeout)

| Grok advice | Classification |
|-------------|----------------|
| `repair_first` | **accepted** |
| Density < 5 is soft stop at exploration, hard stop at pre-expensive gate | **accepted** |
| `proceed_to_precheck` now | **rejected** |
| `closeout_negative_memory` now | **rejected** |
| Forbidden promotion/runtime claims | **accepted** (guard) |

**Bottom line:** Frontier03C proved **trainable ONNX with seed-level positive net**. It did **not** prove a surface shape worth WFO/MT5. Repair the decision surface (and possibly the teacher set) first; revisit narrow precheck only if repair clears the bounded success criteria above.
