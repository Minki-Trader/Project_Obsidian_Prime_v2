Reviewing the Grok collaboration skill and bounded Frontier04B evidence to form a structured recommendation.
## Grok External Review — Frontier04C Pre-Trainable Transfer Gate

**Review size:** medium review (제한 스냅샷 + 집중 질문)  
**Local verification note:** Bounded evidence files were read; cited KPIs, joint pass, and integrity fields match `run_manifest.json`, `top.csv`, `summary.csv`, and `integrity.json`. Hash re-check was not re-run in this turn.

---

### 1. Recommendation(권고)

**`proceed_to_trainable_probe` (학습 가능 탐침 진행)**

Do **not** revise the proxy first. Do **not** close as negative memory. Do **not** block.

---

### 2. Reasoning(근거)

**Frontier04B did the job it was designed for.**

This run was a **proxy-only scout(프록시 전용 탐색)** — no ONNX, no WFO, no MT5. Its question was narrow: *can the path-label axis(경로 라벨 축) jointly satisfy density / PF / DD on validation and OOS?* One variant (`f04b_path_h12_t1p20_s0p80_trainp90`) passes with `validation_oos_joint_pass=True`. That is a legitimate **seed surface(씨앗 표면)**, not runtime authority.

**Integrity is good enough to spend one cheap falsification step.**

- Alignment clean: `missing_raw_matches=0`, `raw_duplicate_close_keys=0`, `missing_future_paths h12/h18=0`
- Label boundary respected: future OHLC from t+1 only; no `feature_set_v2` in label construction
- Split boundary respected: train supplies p90 scale only; val/OOS are eval-only
- Judgment: `usable_with_boundary` — not `blocked`

**Path semantics matter versus the controlled baseline.**

For the same variant, `close_return_baseline` fails `validation_oos_joint_pass` (val density ~4.48/day, OOS ~3.04/day) while the path label passes (~7.86 / ~5.92 per day). So this is not “any oracle label looks good” — the **path event semantics(경로 이벤트 의미)** are doing real work on the aspiration axes. That justifies asking whether `feature_set_v2` can learn them.

**This gate is pre-trainable, not post-collapse.**

Frontier03D correctly said **repair first** because ONNX had already been run and showed severe oracle→model collapse (density ~58% loss, PF near 1.0). Frontier04 has **not** run trainable transfer yet. The next falsification is: *do features carry any of this label signal?* Skipping the probe and repairing the proxy first would optimize label semantics before knowing learnability — premature at this stage.

**Known weaknesses are real but already bounded.**

- OOS PF `214.98` with 98.6% win rate is almost certainly **proxy inflation(프록시 과장)** on a horizon-close PnL basis, not tradable edge
- Path labels remain **oracle proxy(오라클 프록시)** — scout KPIs are an upper bound, not a model forecast
- Only **1 / 6** path variants joint-pass → thin island, not a broad surface
- Timezone unresolved; Tier B `missing_required`

Those weaknesses define **claim bounds(주장 경계)** and **probe stop rules(탐침 중단 규칙)**. They do not justify blocking a narrow, cheap ONNX transfer probe.

**Reject the other routes at this point.**

| Route | Why not now |
|-------|-------------|
| `revise_proxy` | Integrity and alignment pass; 1 joint-pass row exists. Repair without learnability test is premature. |
| `close_negative_memory` | A positive scout clue with controlled baseline contrast exists; the stage question is not falsified yet. |
| `blocked` | No corruption, no alignment failure, no leakage in label construction. |

---

### 3. Required bounds for the next run(다음 실행 필수 경계)

**Run ID:** `frontier04D_trainable_path_label_onnx_probe_v1`

1. **Single label lock(단일 라벨 고정):** train only on `f04b_path_h12_t1p20_s0p80_trainp90`. No new threshold / horizon / multiplier sweep.
2. **Fixed inputs(고정 입력):** same `model_input_dataset`, raw US100, splits, and `feature_set_v2` column order; record dataset hashes from `integrity.json`.
3. **Small fixed model grid(소형 고정 모델 격자):** e.g. 1–2 model families × micro hypergrid (logistic / small tree or equivalent). No WFO, no MT5, no threshold-only broad sweeps.
4. **Proxy comparison table(프록시 대비표) — mandatory outputs:**
   - Oracle proxy clue: val/OOS density, PF, DD, trade count
   - Model decision surface: same KPI basis and cost semantics
   - **Retention metrics(유지율 지표):** density retention %, PF retention %, DD delta
5. **Evaluation semantics parity(평가 의미 동등):** reuse Frontier04B label semantics contract (`event_first`, `t+1` path start, same-bar ambiguity → flat, timeout → flat, one cost deduction per trade, horizon close-return proxy PnL).
6. **Stop / route rules(중단·분기 규칙):**
   - **Partial transfer(부분 전달):** density retention ≥ ~50% and val/OOS PF materially above 1.0 with DD not worse than proxy by a large margin → one more narrow probe allowed; still no WFO/MT5.
   - **Collapse(붕괴):** balanced accuracy ~coin-flip and density retention < ~50% with PF ≤ ~1.2 → route to `frontier04D_path_label_proxy_repair_v1` or `frontier04D_stage_closeout_negative_memory_v1`; no threshold-only sweeps.
7. **Tier / time honesty(티어·시간 정직성):** Tier B = `missing_required`; timezone = unresolved; no UTC/session claims.
8. **ONNX:** export only with parity check; parity ≠ runtime authority.

---

### 4. Risks(위험)

**If Codex proceeds without bounds:**
- Proxy PF 18 / 214 treated as expected model performance → over-claim
- Threshold / cooldown sweeps chase density while PF collapses
- Multiple label variants dilute the single scout winner

**If the probe succeeds weakly:**
- Partial transfer may look “alive” but still be far from promotion
- High proxy win rates may not survive feature noise

**If the probe fails:**
- May mean label axis is not learnable from current features, not that path labeling is universally dead
- Single-variant island may be a local optimum

**Structural risks carried forward:**
- Oracle proxy ≠ runtime signal
- Unresolved timezone weakens session-level claims
- Missing Tier B limits paired-tier interpretation

---

### 5. Do-not-claim boundary(주장 금지 경계)

Codex must **not** claim:

- completion, selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve
- that scout PF (18 / 214) forecasts model PF
- that path labels are tradable edge or runtime signals
- direct UTC / market-session correctness
- Tier A-only alpha read (Tier B missing)
- ONNX parity as proof of economic edge
- that one joint-pass row closes the stage topic

**Allowed after a bounded probe (only):**
- `trainable_transfer_probe_result(학습 가능 전달 탐침 결과)` with explicit oracle→model retention
- `promotion-ineligible clue(승격 부적격 단서)` or `negative_memory_candidate(부정 기억 후보)` with evidence
- `proxy_semantics_possibly_learnable(프록시 의미가 부분 학습 가능)` — only if retention thresholds are met

---

**Classification for Codex:** `accepted` — proceed to `frontier04D_trainable_path_label_onnx_probe_v1` under the bounds above.  
**Forbidden-claim check:** no operating promotion, runtime authority, live readiness, baseline, or Goal Achieve implied by this advice.
