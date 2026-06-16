# Grok Second Opinion — F70E Selected-Entry Tape Repair

## Verdict

**Primary classification: `accepted`**

F70E is a **legitimate next repair** under the F70 hypothesis lifecycle, not scope creep. F70D already named a **single, testable mechanism** (`trade_lifecycle_gap_after_signal_parity`) after ONNX/signal parity passed. F70E changes **only entry lifecycle semantics** on the same two axes — that is a standard **mechanism isolation** step, not a new alpha search.

**Secondary classification: `needs_local_verification`** for **tape materialization fidelity** only: whether “proxy selected non-overlap entry bars” can be encoded in RuntimeVetoTape **without** changing models, labels, features, thresholds, or decision mode, and without silently altering exits or regime masks.

---

## Why `accepted` (not close yet)

| Factor | Effect |
|--------|--------|
| F70D gap is **diagnosed**, not vague | Lifecycle inflation (e.g. validation 254 selected → 960 runtime) has a named cause |
| Repair is **narrow** | Same artifacts; only tape allow-list semantics |
| Two outcomes are **pre-registered** | Count aligns → lifecycle was the blocker; PF/DD still weak → edge weak under MT5 economics |
| Stays inside claim boundary | Runtime probe **observation** only — no completion, baseline, promotion, runtime authority, live readiness, Goal Achieve |

**Closing F70 now** would leave an unresolved fork:

- Weak runtime KPI because **entry lifecycle** diverged from proxy, or  
- Weak KPI because **label/model edge** does not survive MT5 economics even on the intended entry set.

Proxy KPIs are already much stronger; F70E asks whether **forcing runtime onto proxy-selected bars** closes that fork. That is worth one bounded MT5 pass.

---

## When closing as preserved clue / negative memory would be right

Prefer **close without F70E** only if Codex locally confirms one of these:

1. **Prior frontier negative memory** already ran this exact tape repair and recorded the result.  
2. **Proxy entry bars cannot be reproduced** in tape without hidden semantic drift (overlap rules, bar indexing, regime mask interaction).  
3. **F70 core question** was model-rotation alpha under correct lifecycle — and lifecycle was already fixed upstream; F70D then becomes confirmation, not a new repair lane.

From the bounded snapshot alone, none of these are established — so **do not close on evidence given here**.

---

## Guardrails Codex must enforce

1. **Frozen comparison set** — Identical models, labels, feature sets, thresholds, decision mode, splits (validation/OOS), and the same two axes. No threshold sweep, tuning, or post-hoc candidate search.  
2. **Single-variable change** — Only RuntimeVetoTape: F70D = regime-mask-active bars; F70E = proxy selected non-overlap entry bars only; veto all else. Document the bar-selection rule in the repair receipt.  
3. **Pre-registered success/failure read**  
   - **Lifecycle confirmed:** `runtime_trades ≈ selected_trades` (same order of magnitude; not merely “lower than F70D”).  
   - **Edge weakness confirmed:** counts align but PF/DD still far below proxy → stop lifecycle chasing; record negative memory on MT5 economics.  
   - **Residual gap:** counts align but KPI still below proxy → next fork is exits/fills/slippage/exit semantics, **not** another open-ended probe in F70.  
4. **Claim ceiling** — Receipt language: `repair_observation` / `runtime_probe_observation` only. No promotion candidate, operating promotion, runtime authority, or live readiness from F70E.  
5. **Tier discipline** — If Tier A/B/combined records exist for this stage family, keep the same tier labeling; do not let Tier A-only runtime read stand in for full alpha read.  
6. **Stop rule after F70E** — Regardless of outcome: **no F70F threshold/model sweep**. Outcomes map to (a) preserved clue — lifecycle fixable, (b) negative memory — edge too weak after MT5 economics, or (c) bounded follow-up **outside** F70 if a **new** non-lifecycle hypothesis is opened explicitly.  
7. **Parity receipt minimum** — Log for both axes × validation/OOS: `selected_trades`, `runtime_trades`, tape veto/allow counts, and ONNX/signal parity **re-check** post-tape change (tape must not break signal bridge).

---

## Claim boundary (unchanged)

F70E remains **runtime probe observation**. It may strengthen **mechanism evidence** (lifecycle vs edge). It does **not** justify completion, baseline selection, promotion, runtime authority, live readiness, or Goal Achieve.

---

## Compact receipt

| Field | Value |
|-------|--------|
| `trigger_reason` | F70D lifecycle gap after signal parity; propose selected-entry tape repair |
| `bounded_evidence` | F70D parity pass + runtime/proxy KPI table + `trade_lifecycle_gap_after_signal_parity` |
| `advice_classification` | **`accepted`** (run F70E); **`needs_local_verification`** (tape bar materialization fidelity) |
| `claim_boundary` | Repair observation only; no promotion/runtime authority |
| `final_codex_direction` | Proceed with F70E under guardrails above; close F70 after F70E to preserved clue or negative memory — no further MT5 probes in F70 without a new explicit hypothesis |
