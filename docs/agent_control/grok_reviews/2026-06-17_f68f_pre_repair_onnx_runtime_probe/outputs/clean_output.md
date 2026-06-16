# Grok Review: F68F Pre-Repair ONNX Runtime Probe

**Review size:** medium (제한 스냅샷 + 집중 질문 3개)
**Role:** external second opinion only — no local verification performed.

---

## 1. Is F68F a reasonable next repair probe?

**Verdict: accepted — F68F is a reasonable next repair probe, with explicit scope limits.**

**Why it fits the evidence**

F68D showed **parity is not the blocker** (signal/feature diffs all `0`). The failure mode is **economic shape**: density axis has volume but bad PF/DD; PF axis has low DD but unusable sparsity. F68E’s attribution points repair at **feature set, trade spacing, risk, or exit shape** — not threshold-only retuning.

`f68b_0872ddc6192f` sits in a **plausible middle band** on proxy KPI:

| Axis | trades/day (proxy or F68D MT5) | PF / DD character |
|------|-------------------------------|-------------------|
| F68D density | ~6.8–8.5 | PF weak, DD ~71% val |
| F68D PF | ~0.005–0.007 | PF/DD strong, density dead |
| Repair candidate | ~3.2–4.0 (proxy) | PF ~1.23–1.29, proxy DD ~5–7% |

That is **not final-target density** (below ~5 trades/day), but it is a **credible DD/PF repair seed** to test whether MT5 can reproduce a **less extreme** tradeoff than either F68D axis. ExtraTrees also makes ONNX export **plausible**, unlike HGB low-DD paths called out as harder.

**Caveats (do not over-read proxy)**

- Proxy KPI is **not MT5 truth** until parity + tester run.
- Sub-5 trades/day may still be **operationally thin** even if PF/DD improve.
- F68F remains **probe**, not “we found the fix.”

---

## 2. Accept / Reject / Needs local verification

### Accept (수용)

| Item | Rationale |
|------|-----------|
| F68F labeled **repair probe**, not completion/baseline/promotion/runtime authority | Matches F68E diagnosis and Codex direction |
| Export **`f68b_0872ddc6192f`** as primary repair candidate | Targets economics, not parity rework |
| **ONNX probability/signal parity gate** before Strategy Tester | New candidate ≠ F68D parity receipt; parity must be re-established per artifact |
| **`f68b_0f012336cfaf` as duplicate/regime check only** unless feature hash differs | Keeps scope bounded; avoids dual-primary drift |
| Compare MT5 results against **both F68D axes** (density vs PF), not proxy alone | Separates “better than broken axis” from “meets research target” |

### Reject (거절)

| Item | Rationale |
|------|-----------|
| **Threshold-only retuning** as the main repair story | F68E explicitly ruled this out |
| Treating F68D zero-diff parity as **transferable to F68F** without re-proving | Different model/bundle = new parity obligation |
| Using proxy PF ~1.23–1.29 and DD ~5–7% as **MT5-achieved** before tester | Proxy ≠ runtime |
| Elevating **`f68b_0f012336cfaf`** to co-primary without hash-differentiated role | Regime check only, per Codex plan |
| Any claim of **selected baseline, promotion, runtime authority, live readiness, Goal Achieve** after one repair probe | Forbidden and unsupported by one candidate |

### Needs local verification (로컬 검증 필요)

Codex must verify locally **before** export/run and **after** run:

**Pre-export / pre-MT5**

1. **ONNX export success** for `f68b_0872ddc6192f` (ExtraTrees expected, not guaranteed).
2. **Feature manifest / hash identity** — candidate bundle matches intended `no_mega_top3`, threshold `0.3`, cooldown `6`, both sides, close-horizon exit.
3. **ONNX probability + signal parity** vs Python reference on validation/OOS windows (same standard as F68D).
4. **Feature hash diff** between `f68b_0872ddc6192f` and `f68b_0f012336cfaf` — if equal, regime check is redundant beyond sanity; if different, document what changed.
5. **EA/run manifest wiring** — cooldown, threshold quantile, exit horizon, both-side routing match candidate contract.

**Post-MT5 (if run completes)**

6. **MT5 validation/OOS KPIs** vs proxy: net, PF, DD, trades, trades/day.
7. **Parity receipts** for this candidate (signal_count_diff, feature_ready_diff) — expect zero again, but must be measured.
8. **Density sufficiency read** — does MT5 trades/day land near proxy ~3–4, or collapse toward PF-axis sparsity?
9. **Tier recording** if project lane requires Tier A/B separate + combined (not in snapshot; verify against operating rules).

---

## 3. Claim boundary after F68F (if it runs)

**Allowed claims (narrow)**

- F68F executed as **repair runtime probe** for candidate `f68b_0872ddc6192f`.
- ONNX export **attempted**; parity **measured** (pass/fail with diffs recorded).
- MT5 Strategy Tester **validation/OOS results recorded** with identity (settings, bundle hash, manifest).
- **Attribution-style read only**, e.g.:
  - “MT5 economics moved toward lower DD / better PF than F68D density axis” (only if tester shows it),
  - “Trade density remained below research target” (if trades/day &lt; ~5),
  - “Repair direction **plausible** / **inconclusive** / **negative**” — judgment from evidence, not aspiration.

**Forbidden claims (금지 주장)**

- completion, selected baseline, promotion, runtime authority, live readiness, Goal Achieve.
- “Parity problem solved for Frontier 68” — parity was already solved for F68D; F68F only adds **candidate-specific** parity.
- “Density target met” — proxy already below ~5 trades/day.
- “HGB/low-DD path closed” — only one ExtraTrees seed tested.
- “F68D axes obsolete” — they remain **diagnostic anchors** until a repair candidate beats both on agreed KPIs under MT5.

**Default label after F68F regardless of outcome**

`repair_probe_closed` with one of:

- **positive_signal** — MT5 improves PF/DD vs density axis *and* keeps usable density (&gt; PF axis, ideally ≥ proxy band),
- **inconclusive** — parity OK but economics mixed or density too sparse,
- **negative** — parity fail or MT5 repeats F68D-style failure mode.

None of those imply promotion or runtime authority.

---

## Summary for Codex

| Question | Grok classification |
|----------|---------------------|
| F68F as next step? | **Accepted** — aligned with F68E; right repair axis; bounded scope |
| Pre-export/run | **Accept** probe framing + parity gate + single primary candidate |
| | **Reject** threshold-only repair and F68D parity inheritance |
| | **Needs local verification** — export, hash, parity, MT5 KPIs, density read |
| Post-F68F boundary | **Repair probe evidence only** — no baseline/promotion/runtime authority/live/Goal Achieve |

**Single line for routing:** Proceed with F68F as a **narrow ONNX + MT5 repair probe** on `f68b_0872ddc6192f`; treat proxy KPI as **hypothesis**, F68D axes as **comparison baselines**, and any success as **directional clue** until density, PF, and DD are jointly acceptable under MT5 on the same parity standard as F68D.
