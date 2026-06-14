# Frontier41 Stage Open — Grok External Review(외부 2차 의견)

**Role boundary(역할 경계):** This is advisory only. No operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).

---

## 1. `verdict`

**`needs_local_verification`**

The direction is logically sound and better bounded than another raw-feature pass, but Codex should not open F41 as “trusted proxy” until local checks confirm (a) F40 scout lineage is split-clean and (b) exit comparison is attribution-clean vs density-matched A and F40 fixed-exit.

---

## 2. `novelty_ok`

**`yes` — with one condition**

**Why yes:**
- F40 closed as `preserved_clue_negative_memory` with usable short-pocket density (~7–8/day) but mediocre PF (~1.15) and high DD (~12–14%). That pattern fits “entry signal exists, exit shape may be wrong” better than “no signal.”
- F41 changes the **hypothesis lever(가설 레버)**: freeze entry source(진입 원천) from F40 scouts, vary only executable exit shapes(실행 가능한 청산 형태). That is a real pivot, not a rename of F40 threshold mining.
- The pre-registered exit family is finite: fixed holds `{4,6,8,12,18}`, train-only stop/take quantiles, conservative first-hit tie-break, optional time-stop. That is exploration-bounded.

**Condition:**
- Novelty holds only if entry pockets stay **immutable** from F40 top rows. Any new raw-feature threshold search, regime re-gate, or pocket re-ranking on validation/OOS collapses F41 back into F40-style mining.

---

## 3. `leakage_guard_ok`

**`needs_local_verification`**

**Protocol looks right on paper:**
- Entry frozen from prior stage scouts.
- Exit thresholds estimated on train entries only.
- Validation/OOS read-only.
- Conservative stop-first tie-break reduces optimistic path bias.

**What must be verified locally before trust:**
1. **F40 inheritance leak:** Were `f40b_0001` and sibling scouts selected without validation/OOS peek? If not, frozen entry is already contaminated.
2. **Exit quantile leak:** Stop/take quantiles must be computed only from train-split entries **after** the same split mask used for selection—not from pooled train+val pockets.
3. **Comparison leak:** Density-matched A must share the **same entry timestamps**; only exit logic may differ. Otherwise “lift vs A” mixes entry and exit effects.
4. **Replay timing leak:** Entry at bar close must not use same-bar OHLC path information unavailable at decision time.

If those four pass, leakage guard is acceptable. Until then: `needs_local_verification`.

---

## 4. `runtime_claim_boundary_ok`

**`yes`**

The tiered success boundary is appropriately strict and separated:

| Tier | PF | Density | DD | Claim level |
|------|-----|---------|-----|-------------|
| Scout clue | ≥1.03 | 4–12/day | ≤18% | Exploration clue only |
| Seed surface | ≥1.20 | 5–10/day | ≤12% | Still not runtime |
| Runtime candidate | ≥1.50 | 5–10/day | ≤10% | Pause before WFO/MT5 |

Explicit `proxy-only` until seed/runtime rows exist, plus “stop and ask Grok before expensive WFO/MT5” if runtime candidate appears—this is disciplined. F40 already showed `0/0` seed-runtime rows and `runtime_probe_ineligible`; F41 should inherit that humility.

---

## 5. `mandatory_guardrail`

Codex must implement **both** before trusting the proxy:

**Guardrail A — Entry freeze manifest(진입 고정 목록)**
Write an immutable manifest: exact F40 scout IDs/rules (starting with `f40b_0001`), row counts per split, and a hash. Reject any run that mutates raw-feature thresholds, re-opens quantile mining on `vix_zscore_20` / `ppo_hist_12_26_9`, or adds pockets not in the manifest.
*Effect:* Prevents silent slide back into F40.

**Guardrail B — Same-entry attribution lock(동일 진입 귀속 잠금)**
For every comparison (density-matched A, F40 fixed-exit reference, each exit variant), enforce identical entry timestamps and sizing; only exit path may change. Log per-split entry hash across arms.
*Effect:* PF/DD lift is attributable to exit shape, not hidden entry drift or density mismatch.

---

## 6. `do_not_repeat`

F41 becomes a repeat—not a new hypothesis—if any of these happen:

| Failure mode | Repeats |
|--------------|---------|
| New raw-feature or regime-gate threshold search because exits underperform | **F40** |
| Exit grid explodes beyond the pre-registered family (extra holds, adaptive re-fit per split, validation-driven exit picking) | **F31/F32/F33-style** overfit sweeps |
| “Improvement” comes only from train-best exit with no stable val/OOS lift | Generic mining loop, not exit-shape science |
| Density-matched A uses different entries or different replay engine than F41 arms | False novelty; compares apples to oranges |
| Interpreting PF ~1.15 + DD ~12–14% as seed/runtime progress without crossing stated tiers | F40 negative memory replay with new labels |

**Positive novelty signal for F41:** val and OOS both improve PF and/or cut DD vs **same-entry** F40 fixed-exit reference, with density still in band, **without** touching entry rules.

---

## Summary for Codex

| Item | Grok view |
|------|-----------|
| Open F41 conceptually? | **Yes** — logical post-F40 decomposition |
| Trust proxy results yet? | **No** — verify F40 lineage + same-entry comparisons first |
| Strongest risk | Entry contamination from F40 selection + confounded A/B comparison |
| Strongest virtue | Clear single-lever hypothesis with finite exit family and explicit proxy-only claims |

**Claim boundary preserved:** This review accepts the *direction as worth attempting* under guardrails; it does **not** accept any performance, seed, runtime, or promotion claim for F41.
