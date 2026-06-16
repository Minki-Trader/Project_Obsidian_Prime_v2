# Grok External Second Opinion — F67D Pre-MT5 Runtime Probe

**Review size:** medium review (중간 검토)
**Source:** bounded snapshot only — no local verification performed.

---

## 1. Critical risks (핵심 위험)

**A. Economics gap is real and systematic, not noise.**
F67A shows runtime DD (런타임 손실폭) median ~2.13× proxy DD (프록시 손실폭), with 22/64 rows where proxy DD < 10 but runtime DD > 10. F67D that only checks counts or cost fields without tying them to DD/PnL decomposition (손익/손실폭 분해) may confirm *what* differs but not *how much* each driver contributes to the gap.

**B. Cost identity missing everywhere (64/64).**
F67B shows spread/commission/slippage/swap (스프레드/수수료/슬리피지/스왑) absent from config identity. F67C still shows swap_nonzero on 54/64 rows and deal_swap_sum −515.95 with commission_nonzero 0/64. Risk: F67D records “cost fields” from tester output while config identity stays implicit — evidence will show *observed* costs but not *intended* costs, weakening parity claims.

**C. Order-intent-to-deal accounting is the dominant structural mismatch.**
F67C: order_fill = deal_count only 11/64; deal_count > order_fill on 53/64; deal_count = 2×trade on 64/64. The labeled gap cause (`lifecycle_trade_compression_plus_tester_side_exit_deals_plus_report_level_swap_cost_not_config_identity_drift`) bundles multiple hypotheses. If F67D does not isolate entry vs exit deals (진입 vs 청산 딜), partial fills, and tester-generated exits, one narrow run may mis-attribute the gap.

**D. Trade/signal compression masks intent.**
Overall trade/signal ratio 0.3468 (median 0.3248) with 70,032 signals vs 24,284 trades. Without per-stage or per-window breakdown, F67D may average away regime-specific compression and under-explain DD divergence.

**E. Overclaim drift despite stated boundary.**
Success criteria already list net/gross/PF/DD (순수익/총이익·손실/수익 팩터/손실폭). Recording these without explicit “observation only, not parity achieved” labels risks reading F67D as economics validation rather than diagnostic probe.

**F. Single tester/EA signature with 7 trade-shape signatures.**
F67B: one tester + one EA core signature, seven trade_shape signatures. A “narrow” probe that still spans multiple trade-shape variants may reproduce F67A–C breadth under a smaller row label — not actually narrow for deep inspection.

---

## 2. Required additions before MT5 (테스터 실행 전 필수 추가)

| Addition | Why (from snapshot) |
|----------|---------------------|
| **Explicit cost identity block** per run: spread, commission, slippage, swap — from `.set`/tester settings/manifest, or precise `unavailable_reason` with source (config vs report vs deal table). | Closes F67B 64/64 missing gap; separates config drift from report-level swap. |
| **Order intent receipt schema** with mandatory fields: `signal_count`, `order_attempt_count`, `order_fill_count`, `trade_count`, `deal_count`, plus **entry_deal_count**, **exit_deal_count**, **tester_side_exit_deal_count** (if distinguishable). | Addresses 53/64 deal≠fill and 64/64 deal=2×trade pattern. |
| **Accounting parity sheet** separate from count parity and economics parity: rows for signal→order→fill→trade→deal with delta columns and gap_class tag. | Success criteria ask for gap classification; needs operational definitions before run. |
| **Economics decomposition template**: proxy DD, runtime DD, delta_pp, attributed buckets (swap, commission, slippage, exit-deal inflation, lifecycle compression) — even if attribution is partial/`unknown`. | F67A DD gap is the core question; cost rows alone insufficient. |
| **Narrow selection rule** documented upfront: e.g. 1 tester signature × 1 EA core × **1** trade_shape signature × 1–3 time windows (not “small enough” post hoc). | Prevents faux-narrow probe across 7 trade shapes. |
| **Frozen comparison anchor**: which F67A/B/C row(s) F67D replays (row id, hashes if known, or `missing_material`). | Without anchor, F67D cannot explain *this* gap vs a new sample. |
| **Receipt-level swap/commission cross-check**: deal-table sums vs tester summary vs config — flag `commission_always_zero` and `swap_report_only` explicitly. | Matches F67C: 0/64 commission nonzero, 54/64 swap nonzero. |

---

## 3. Items to reject or defer (거절 또는 보류 항목)

**Reject for F67D primary scope**

- PF/DD optimization or parameter sweeps — diagnostic only per drift risks.
- Treating compile success or Python report regeneration as MT5 Runtime Probe evidence.
- Using trade/signal ratio as **primary** success criterion — keep secondary observation only.
- Closing F67 or implying repair direction from F67D alone — observation boundary only.
- Inheriting winner/baseline/promotion/runtime authority from Stage12~364.
- Claiming “cost parity achieved” because tester output lists spread/swap — config identity was missing on 64/64; observation ≠ parity.

**Defer**

- Full 64-row replay — defer; F67D should be deliberately small and deep.
- Economics parity as a pass/fail gate — defer until accounting parity hypotheses are tested on narrow set.
- Unified fix for lifecycle compression + tester exits + swap — defer; F67D classifies, does not repair.
- Live readiness or runtime authority uplift — explicitly forbidden.

---

## 4. Tight F67D run design (좁은 F67D 실행 설계)

**Purpose:** Explain proxy/runtime **economics** gap (especially DD) via cost identity + order-intent-to-deal accounting — not to improve KPIs.

**Recommended shape (from snapshot logic):**

1. **Select 1 canonical slice**
   - One trade_shape signature (pick the median trade/signal ratio row or the worst DD-delta row from F67A — Codex must name the row in manifest; Grok cannot verify which).
   - Same tester_signature and ea_core_signature as F67B (already uniform).

2. **Single tester run + explicit handoff**
   - Strategy Tester output required: report HTML/CSV, deal table, order history if available, settings snapshot.
   - Manifest records cost identity fields or `unavailable_reason` per field.

3. **Order intent receipt (one row per probe)**

   ```
   signal_count → order_attempt_count → order_fill_count → trade_count → deal_count
                 ↳ entry_deal_count, exit_deal_count, tester_attributed_exit_deals
   ```

4. **Three-way gap table (one row per metric)**

   | Layer | Metrics | F67D action |
   |-------|---------|-------------|
   | Count parity | signals, orders, fills, trades, deals | Reconcile vs F67C patterns (2× deal, fill mismatch) |
   | Accounting parity | fill vs deal, entry+exit vs trade | Tag dominant mismatch |
   | Economics parity | net, gross, PF, DD (proxy vs runtime) | Report delta_pp; no pass/fail |

5. **Hypothesis tags (mutually non-exclusive)**
   Assign each observed delta: `lifecycle_compression`, `tester_side_exit_deals`, `swap_cost_report_level`, `config_cost_identity_missing`, `unclassified`.
   Aligns with F67C `runtime_gap_cause_read` but forces per-metric attribution discipline.

6. **Secondary observations only**
   trade/signal ratio, swap sum, commission nonzero flags — recorded, not optimized.

7. **Stop condition**
   Probe complete when tester output exists, cost identity block filled, order intent receipt complete, and gap classification row exists — **not** when PF/DD improves.

---

## 5. Claim boundary reminder (주장 경계 재확인)

F67D may claim only **`runtime_probe_observation` (런타임 탐침 관찰)**:

- Allowed: “On this narrow slice, runtime DD exceeded proxy DD by X pp; Y% of deal inflation aligns with exit-deal pattern; swap observed in deals but not in config identity; cost fields recorded or marked unavailable with reason.”
- Not allowed: completion, selected baseline, promotion, runtime authority, live readiness, Goal Achieve, economics parity achieved, or F67 closeout readiness.

Mandatory gate remains: **F67 closeout requires MT5 Runtime Probe** — F67D is one probe tranche, not the gate pass itself unless Codex locally verifies full gate coverage.

---

**Classification for Codex:** **accepted with required additions** — direction is sound; F67D will fail to explain the economics gap unless cost identity is config-anchored, order-intent receipt splits entry/exit deals, narrow selection is pre-specified (1 trade shape), and gap classification is operationalized before MT5 runs. **needs_local_verification** for row selection, manifest paths, and actual tester settings — Grok does not own those.
