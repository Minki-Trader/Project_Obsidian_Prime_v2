Bounded evidence를 먼저 확인한 뒤, 마감 제안에 대한 외부 2차 의견을 정리하겠습니다.
## Grok External Review — Frontier04 Stage Closeout

**Review size:** medium review (제한 스냅샷 + 집중 질문)  
**Local verification note:** Bounded reports, `top.csv`, and `retention.csv` were read. Cited KPIs, `validation_oos_joint_pass`, `partial_transfer_pass=False`, and ONNX parity match the provided evidence. SHA256 re-check was not re-run in this turn.

---

### 1. Recommendation(권고)

**`close_negative_memory_with_preserved_clue` (부정 기억 + 보존 단서 마감)**

Do **not** `require_repair`, `blocked`, or `completion_candidate`.

---

### 2. Reasoning(근거)

**The stage hypothesis was tested in the right order and is now falsified on the trainable axis.**

Frontier04B answered its narrow question: path-aware event labels can jointly satisfy density/PF/DD on validation and OOS for one locked variant (`f04b_path_h12_t1p20_s0p80_trainp90`). That is a real **preserved clue(보존 단서)** — especially because the controlled `close_return_baseline` fails `validation_oos_joint_pass` while the path label passes. The clue is about **label-axis oracle semantics(라벨 축 오라클 의미)**, not tradable edge.

Frontier04C correctly authorized exactly one bounded falsification step: Frontier04D with a single label lock, fixed `feature_set_v2`, small fixed model grid, argmax-only, no WFO/MT5. That probe ran. Result is unambiguous **collapse(붕괴)**:

| Axis | Oracle proxy (F04B) | Best model `rf_depth5_leaf80_balanced_argmax` (F04D) |
|------|----------------------|-----------------------------------------------------|
| Val PF | 18.65 | 0.977 |
| Val density | 7.86/day | 25.15/day |
| Val DD | 6.53% | 74.74% |
| OOS PF | 214.98 | 0.965 |
| OOS density | 5.92/day | 26.68/day |
| OOS DD | 1.15% | 40.19% |
| `partial_transfer_pass` | n/a | **False** (all 3 models) |

This is not a borderline miss. PF is at or below 1.0, DD is catastrophically worse than proxy, and models **overtrade** rather than retain oracle selectivity. ONNX parity passing only confirms export correctness — it does not rescue the economic read.

**`require_repair` is not justified under the bounds Codex already accepted.**

F04C stop rules said collapse routes to proxy repair **or** stage closeout, with **no threshold-only broad sweeps**. Proxy integrity already passed in F04B; the failure mode is **oracle → feature_set_v2 → model transfer**, not label construction corruption. Repairing the proxy first would optimize label semantics before the learnability question was even asked — that was correctly rejected at F04C and should not be reopened now.

A second in-stage model sweep would be implicit repair by grid expansion, which violates the spirit of the agreed bounds and risks turning a clean falsification into an unfalsifiable tuning loop.

**`blocked` is wrong.**

Runs completed with `usable_with_boundary` integrity. Tier B is `missing_required`, not execution failure. This is a **negative result(부정 결과)**, not a blocked pipeline.

**`completion_candidate` is wrong.**

No trainable surface survived. No WFO, no MT5, no partial transfer, no promotion path. F04D report already labels `negative_memory_candidate`. Completion would overstate closure.

**Codex closeout framing is directionally correct.**

- **Preserved clue:** path-aware labels can form a clean oracle seed surface.
- **Negative memory:** under `feature_set_v2` + small fixed trainable grid, that oracle did not transfer into a usable ONNX decision surface.
- **Next frontier:** new hypothesis lifecycle, not Frontier04 continuation repair.

---

### 3. Required closeout bounds(마감 필수 경계)

Codex should close with these explicit locks:

1. **Dual ledger entry(이중 장부 기록):** one `preserved_clue` row for F04B variant `f04b_path_h12_t1p20_s0p80_trainp90`; one `negative_memory` row for F04D transfer collapse under locked inputs.
2. **Failure mode precision(실패 모드 정밀화):** negative memory must say *transfer failure under feature_set_v2 + small fixed grid*, not “path labeling is dead.”
3. **Repair prohibition(수리 금지):** no threshold-only broad sweeps, no proxy variant re-sweep, no extra model-grid rescue inside Frontier04.
4. **Tier honesty(티어 정직성):** Tier B = `missing_required`; no Tier A+B combined claim; no paired-tier alpha read.
5. **Time honesty(시간 정직성):** timezone remains unresolved; no UTC/session authority claims.
6. **Artifact retention(산출물 보존):** keep F04B oracle contract (`event_first`, t+1 path start, cost semantics) as reusable reference artifact, not as runtime authority.
7. **Next frontier rule(다음 전선 규칙):** next work must open a **new hypothesis lifecycle(새 가설 생명주기)** — e.g. different feature surface, different label-to-signal contract, or different model family — and must not inherit Frontier04 as an open repair queue.
8. **Frontier governance(전선 거버넌스):** close as `reference, not inheritance`; carry clue and negative memory only, not winner/baseline/promotion history.

---

### 4. Risks(위험)

**If Codex closes without the bounds above:**
- F04B oracle PF (18 / 214) may be misread as expected model performance.
- Preserved clue may be mistaken for a `promotion_candidate`.
- Future work may repeat the same transfer test under a renamed run ID.

**If Codex refuses closeout and repairs anyway:**
- Threshold or model-grid sweeps may chase overtrading density while PF stays ≤ 1.
- Stage lifecycle drifts into unfalsifiable tuning.
- Frontier04 becomes a hidden continuation campaign instead of a clean negative memory.

**Structural risks carried forward even after correct closeout:**
- Single-variant island (1/6 joint-pass in F04B) may be locally fragile.
- OOS proxy PF is almost certainly inflationary on horizon-close PnL semantics.
- `feature_set_v2` may be the bottleneck, but that is **next-hypothesis scope**, not proof that path labels are universally unlearnable.
- Missing Tier B limits cross-tier interpretation.

---

### 5. Do-not-claim boundary(주장 금지 경계)

Codex must **not** claim:

- `completion`, `selected baseline`, `operating promotion`, `runtime authority`, `live readiness`, `Goal Achieve`
- that F04B scout PF/density/DD forecast model or ONNX runtime performance
- that ONNX parity implies runtime readiness
- that path-aware labeling is universally dead — only that **this transfer contract failed**
- that Tier A-only evidence is full alpha truth without Tier B / combined records
- any repair, second probe, or threshold sweep as still-required work **inside Frontier04**
- `completion_candidate` based on oracle proxy alone

Codex **may** claim:

- Frontier04B found a bounded oracle seed surface with controlled baseline contrast
- Frontier04D falsified trainable transfer under agreed bounds
- Frontier04 should close as `negative_memory + preserved_clue`
- the next frontier should start a new hypothesis lifecycle with explicit new transfer contract

---

**Classification for Codex:** `accepted` — proceed with closeout as proposed, subject to the required bounds above.
