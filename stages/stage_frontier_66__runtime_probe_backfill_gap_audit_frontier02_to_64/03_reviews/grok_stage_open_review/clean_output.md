# Grok External Review: F66 Scope & Claim Boundary

**Classification:** `accepted` with `needs_local_verification` on inventory completeness and gap-taxonomy consistency.

---

## Is the F66 scope sound?

**Yes — directionally sound and appropriately bounded.**

F66 as `runtime_probe_backfill_gap_audit` (not a new model hypothesis) matches the stated intent: audit F02–F64 for **actual runtime probe KPI** presence, separate **missing probe** from **missing runtime material**, and analyze **proxy–runtime gap** in the F65 style. That keeps exploration open while refusing promotion, baseline, runtime authority, or closeout claims.

The claim boundary is the strongest part of the proposal:

| Boundary | Assessment |
|----------|------------|
| No MT5 backtest pretense when ONNX/joblib/pkl = 0 | Correct — avoids fake runtime evidence |
| `invalid_setup_no_runtime_material` vs missing probe | Correct separation |
| Existing runtime KPI kept as KPI; proxy-only ≠ runtime | Correct — prevents KPI inflation |
| Report without stage closeout unless explicitly closed | Correct — audit ≠ closure |

**Verdict:** Scope and claim boundary are **sound for an audit stage**. F66 should be labeled **evidence/inventory + gap taxonomy**, not alpha exploration or operating promotion.

---

## Main risks before writing reports and per-stage status files

### 1. Inventory false negatives / false positives (highest risk)

The dry-run buckets (present: F02–F10, F12–F14, etc.; missing: F11, F15, F18–F49, F51) are **classification outcomes**, not ground truth until locally re-verified.

**Risk:** A stage may have runtime KPI under a non-standard path, ledger view, or naming convention → wrongly tagged `invalid_setup_no_runtime_material`. Conversely, a row labeled “runtime KPI” may be **synthetic, partial, or mis-tiered** → gap analysis built on bad rows.

**Mitigation before writing files:** Per stage, record **discovery method** (path, ledger row id, hash/manifest if any) and **KPI definition used** (what counts as “actual runtime probe KPI”). Without that, status files become opinion, not audit.

### 2. Conflating three different “missing” states

The proposal correctly names two buckets; a third often hides in the data:

- **A.** No runtime material (ONNX/joblib/pkl absent)
- **B.** Material exists but probe never run / KPI not recorded
- **C.** Probe ran but KPI not linked in ledger or stage artifact layout

Dry-run says zero material for **all** missing stages — if that holds everywhere, B and C are less likely for those stages. **Risk:** One exception (material in external path, old bundle layout, or non-`.pkl` artifact) collapses the whole missing group into a single `invalid_setup` label.

**Mitigation:** Status file schema should force **mutually exclusive primary cause** plus optional secondary tags; never single-checkbox “missing.”

### 3. Gap analysis on “KPI present, gap report missing” stages (F02–F10, F12–F14, F16–F17)

These are **not** the same problem as F11/F15/F18–F49. Mixing them in one narrative invites overclaim (“frontier runtime validated”) when the real issue is **documentation / gap-report absence** or **unexamined proxy–runtime divergence**.

**Risk:** Backfilling gap reports from stale proxy metrics without re-checking SL/TP unit semantics (F65 clue) → **false parity** or **wrong gap cause** (e.g. attributing to PF transfer when the driver is points vs price units).

**Mitigation:** Split deliverables:

- **Tier 1:** stages with runtime KPI → extract + tag gaps (may include `gap_report_absence` only).
- **Tier 2:** stages without runtime KPI → materialization status only (no fabricated gap metrics).

### 4. F65 preserved clue not yet operationalized in F66 taxonomy

F65 clue: `sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points`.

**Risk:** F66 gap tagging lists SL/TP unit semantics as one cause among many but does not require **per-stage check** when both proxy and runtime KPI exist. Gaps may be mis-labeled as PF transfer failure or signal parity when the dominant issue is unit semantics.

**Mitigation:** For any stage with **both** proxy and runtime numbers, require explicit field: `sltp_unit_semantics_risk: assessed | not_assessed | n/a`. Default `not_assessed` until reviewed — do not imply F65 lesson was applied everywhere.

### 5. “Materialize/backfill where possible” scope creep

Wording is fine if **“where possible”** is strictly:

- Document what is missing
- Run materialization **only** where material chain is valid and scoped (not full re-train across F18–F49)

**Risk:** Audit stage becomes silent **re-execution campaign** → new runs without experiment design, tier pairing (A/B/combined), or run evidence gates → new proxy/runtime rows that confuse the audit.

**Mitigation:** F66 report should state **backfill attempted: yes/no per stage** and **blocked reason**; no aggregate “backfill completed” without per-stage receipts.

### 6. Frontier governance and reference-not-inheritance

F02–F64 are **reference, not inheritance**.

**Risk:** Audit report ranks stages, implies winners, or suggests “promotion candidate” from highest runtime PF — that violates frontier rules and your own success criteria.

**Mitigation:** Outputs are **inventory + gap causes + preserved clues/negative memory**, not leaderboard or baseline selection.

### 7. Tier A / Tier B / combined record ambiguity

If historical stages mixed Tier A only, Tier B fallback, or combined views, a single “runtime KPI present” flag may hide **which tier** was probed.

**Risk:** Gap analysis compares proxy (full-context) to runtime (partial or fallback) without labeling → false “parity gap.”

**Mitigation:** Each extracted KPI row needs **tier label** and whether row is **separate vs combined vs routed total**; else mark `needs_local_verification`.

### 8. User-facing report tone vs per-stage status files

**Risk:** Summary report says “N stages invalid” while per-stage files show edge cases → user trusts the summary and skips files.

**Mitigation:** Summary counts only **after** all per-stage files exist; summary uses language like “classified as of audit date” not “frontier runtime coverage = X%.”

---

## Specific answers to the review question

**Is F66 scope and claim boundary sound?**
**Yes**, provided F66 remains audit-only: classify, extract, tag gaps, report problems — no closeout, baseline, or runtime authority unless a **separate** explicit packet says so.

**Main risks before writing reports and status files?**

1. Unverified inventory (wrong present/missing buckets).
2. Collapsing material absence, probe absence, and ledger/linkage absence into one label.
3. Building gap reports for F02–F17 without SL/TP semantics pass (F65).
4. Scope creep from audit into backtest/materialization without per-stage receipts.
5. Tier/view ambiguity on existing KPI rows.
6. Accidental promotion narrative from ranked or aggregated KPIs.

---

## Recommended pre-write checklist (for Codex local verification)

Before any F66 report or `missing-material` status file:

1. **One row per stage F02–F64:** `runtime_kpi_present` (y/n), `discovery_evidence`, `runtime_material_present` (y/n + artifact types found), `primary_classification`.
2. **If material absent:** `invalid_setup_no_runtime_material` — **no** proxy-as-runtime, **no** implied MT5 run.
3. **If KPI present, gap report absent:** queue gap extraction; flag `gap_report_absence`; do not claim “runtime validated.”
4. **If both proxy and runtime metrics exist:** mandatory gap cause tags from your list + `sltp_unit_semantics_risk` field.
5. **Explicit non-goals** in F66 header: no baseline, no promotion, no Goal Achieve, no stage closeout in this packet.

---

## `needs_local_verification` (Codex must confirm locally)

- Full F02–F64 stage list matches repo canonical ids (no off-by-one or skipped frontier numbers).
- “Actual runtime probe KPI” definition matches `docs/policies/kpi_measurement_standard.md` / stage ledger conventions.
- Zero ONNX/joblib/pkl for missing group holds under long-path / `io_path` scan, not only shallow glob.
- Whether any “present KPI” stages are proxy mislabeled as runtime in ledger.
- Tier A/B/combined labeling on present-KPI stages.

Until those are verified, F66 can **open** and **plan** status files; aggregate conclusions in the user report should stay **provisional**.

---

**Bottom line:** Proceed with F66 as proposed. The main failure mode is not overclaim in rhetoric but **misclassification in the inventory** and **gap reports that ignore F65 SL/TP semantics**. Write per-stage evidence-first status files before any summary narrative.
