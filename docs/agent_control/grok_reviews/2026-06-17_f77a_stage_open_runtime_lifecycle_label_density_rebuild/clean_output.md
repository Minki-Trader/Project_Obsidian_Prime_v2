**Classification(분류): `accepted_with_conditions` (조건부 수용)**

---

## 1. Is F77 sufficiently novel versus F76?

**Yes — substantively, not cosmetically.**

F76 closed as `preserved_clue_negative_memory` with **5120 candidates and 0 meaningful / 0 density / 0 near**, while proxy KPIs wildly overshoot runtime (e.g. validation proxy_net **1760** vs runtime_net **153**; proxy_tpd **~1.06** vs runtime_tpd **~0.18**). That pattern points to a **target/object mismatch**: independent future-return signals counted at proxy density do not survive single-position runtime compression.

F77’s core pivot — **independent future-return signals → runtime lifecycle event outcomes** — changes *what is being learned*, not just thresholds or model knobs. The six-axis contract (especially `label_target`, `trade_shape`, `risk_logic`) is aligned with that pivot. This is more than “tune F76”; it is a **research-object redesign** with a plausible causal link to F76’s failure mode.

**Condition:** novelty is accepted at **stage-open / hypothesis level** only. It is not evidence that lifecycle labels will produce meaningful signal.

---

## 2. Which axis is most likely to reduce proxy/runtime gap?

**Primary: `label_target` + `trade_shape` (paired, not either alone).**

| Axis | Why it targets the gap |
|------|------------------------|
| **`label_target`** | Proxy trained on independent forward returns; runtime realizes path-dependent TP/SL, MAE, hold, and occupancy. Path-outcome labels (first-hit, MFE/MAE, time-to-exit, lifecycle utility) force the model to predict what a **single concurrent position** can actually earn. |
| **`trade_shape`** | Directly converts “signal count” into **lifecycle density** — event entry, first-touch exit, max_hold grids, single-position occupancy. This is the mechanical explanation for proxy_tpd ≫ runtime_tpd. |
| **Secondary: `risk_logic`** | DD/MAE/daily-loss in the **target/proxy**, not post-hoc MT5 explanation — may shrink proxy/runtime DD gap (validation proxy_dd **6.4** vs runtime **6.6** is closer than net/tpd, but OOS widens). |

**Less likely first-pass gap reducers:** `feature_set` (F76 clue survival test, not gap mechanism), `model_family` (bias separation, not density), `regime_session_split` (localization, not compression).

**Codex should treat `label_target` × `trade_shape` as the mandatory coupling** in F77B design; sweeping them independently risks repeating F76’s “dense proxy, sparse runtime” illusion.

---

## 3. What must Codex locally verify before F77B?

1. **Lifecycle label materialization** — path-outcome labels (TP/SL first-hit, MFE/MAE, hold limits) can be built on the stated dataset (**46650 rows**, splits train/val/oos) without leakage across the 2025-01-02..2026-04-14 evaluation windows.
2. **Compression accounting** — explicit metrics for **single-position occupancy** and **proxy-signal → lifecycle-trade** conversion; F76 had density=0 but never closed the loop with recorded compression.
3. **Apples-to-oranges guard** — proxy KPI definitions in F77 use the **same trade_shape and risk_logic** as lifecycle scoring; no independent-return proxy compared to lifecycle runtime.
4. **Feature lineage** — `all58` vs reduced families (mega-cap removed, raw-price-only, etc.) preserve row alignment and **58→N** changes are logged per axis arm.
5. **Gate operability** — `lifecycle trades/day>=1.0` (scout) and `>=2.0` (meaningful) are computable from simulated lifecycle trades, not raw bar signals.
6. **MT5 bridge feasibility** — entry/exit rules for at least one F77B arm map to EA/tester parameters without “logic impossibility”; runtime rule requires probe unless truly impossible.
7. **F76 negative memory linkage** — which F76 “preserved clue” (if any) is being tested under lifecycle labels vs explicitly dropped; avoid orphan sweeps.

Until (1)–(3) are verified locally, F77B should stay **plan-only** for gap claims.

---

## 4. What do-not-repeat rule should be recorded?

> **Do not repeat F76-style broad independent future-return candidate sweeps (e.g. thousands of proxy-positive arms) without lifecycle trade_shape simulation, single-position compression recording, and aligned proxy/runtime trade definitions.** Proxy net/PF/tpd without lifecycle density is **non-admissible** for scout/meaningful gates and must not justify stage closeout or MT5 skip.

Optional addendum: **Do not interpret F76 runtime closeout net>0 (val **153**, OOS **66**) as clue validation** — it coexists with meaningful=0 and extreme proxy/runtime divergence; it is runtime residue, not research success.

---

## 5. Forbidden claim risks

| Risk | Why |
|------|-----|
| **Baseline / promotion / runtime authority** | F76 already shows proxy can look strong while runtime throttles; F77 open does not repair that. |
| **“F77 fixes the gap” from proxy-only F77B** | Gap reduction must be shown on **lifecycle-aligned** proxy vs later MT5 probe — not val/OOS proxy alone. |
| **Meaningful signal from scout-tier only** | Gates explicitly require compression recorded for meaningful tier; scout is exploration only. |
| **Final-like reference (PF≥2, 5–10 tpd) as target** | Marked “reference only”; using it as success criterion violates claim boundary. |
| **Skipping MT5** | Required unless documented impossibility; F76 had runtime_net>0 — bridge is not obviously impossible. |
| **Tier-wide alpha read from one regime slice** | `regime_session_split` broad sweep must not collapse to one session/regime as “the idea.” |

---

## Summary for Codex

**Direction accepted with conditions:** open F77 as lifecycle label/density rebuild; prioritize **`label_target` + `trade_shape`** for gap work; verify label pipeline, compression metrics, and proxy/runtime definition parity **before** F77B execution and any pre-MT5 Grok review.

**Claim boundary unchanged:** no completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve from this review.
