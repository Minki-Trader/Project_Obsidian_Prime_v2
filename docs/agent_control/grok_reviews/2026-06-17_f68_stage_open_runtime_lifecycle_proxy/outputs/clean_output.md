# F68 Stage Open Review — Grok External Second Opinion

**Review size:** medium review (제한 스냅샷 + 집중 질문 4개)
**Evidence source:** prompt snapshot only — no local verification performed.

---

## Executive Classification

| Item | Classification |
|------|----------------|
| Open F68 as new frontier (not F67 repair) | **accepted** |
| Stage id / title narrowness | **accepted** |
| Frontier thesis novelty after F67 | **accepted** (with one scope guard) |
| Five-step sequence (68A→68E) | **accepted** |
| Success criteria framing | **accepted** |
| Artifact write readiness | **needs_local_verification** (3 items below) |

---

## Q1. Is F68 stage id/title and frontier thesis narrow enough and novel enough after F67?

**accepted** — with one tightening note.

**Narrow enough:**
`stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout` names four separable surfaces: runtime-native lifecycle, economics, proxy scout, ONNX. That is narrower than F67’s count-parity crosswalk and does not reopen signal-count repair.

**Novel enough after F67:**
F67 closed with preserved clue (row-grain isolation) and negative memory (count parity ≠ economics parity). F68 shifts the optimization target from count/feature parity to lifecycle economics labels/scores — a genuine **target/source surface change**, not a relabel of the same repair loop.

**Scope guard (not rejection):**
“ONNX scout” in the title is broad. Codex should treat ONNX as the **scoring vehicle**, not the stage subject. Stage subject = lifecycle economics proxy surface. If 68B drifts into model-family comparison without economics-label discipline, novelty erodes.

---

## Q2. Should F68 open as new frontier rather than F67 repair?

**accepted — open as new frontier, not F67 repair.**

Reasoning from snapshot only:

- F67 gap cause is already diagnosed: `lifecycle_trade_compression + tester_side_exit_deals + report_level_swap_cost`, not config identity drift.
- F67 claim boundary is observation-only; no authority to inherit.
- F67 `do_not_repeat` explicitly forbids another signal-count parity repair.
- F68 thesis addresses the **next hypothesis** (economics-aware proxy), not a missing F67 gate.

Treating F68 as F67 repair would violate F67 closeout direction and repeat a closed negative memory.

---

## Q3. Accept / Reject / Needs Local Verification before F68 artifacts

### Accepted (safe to write now)

| Element | Rationale |
|---------|-----------|
| Stage open direction | Logical successor to F67 negative memory |
| Frontier thesis statement | Clear pivot from count parity → lifecycle economics |
| `do_not_repeat` list | Aligned with F67 closeout |
| Exit rule (seed / clue / negative memory / invalid / blocked) | Matches exploration lane, no strong claims |
| 68A label design before 68B scout | Correct dependency order |
| 68C pre-MT5 Grok review gate | Appropriate if proxy signal is meaningful |
| 68D MT5 probe as conditional mandatory | Matches external-verification anti-deferral spirit |
| Tier A / Tier B labeling requirement in 68A | Required by paired-tier discipline |
| Success criteria as exploration evidence, not four-axis hard gate | Claim boundary consistent |

### Rejected (do not bake into open artifacts yet)

| Element | Rationale |
|---------|-----------|
| Any wording implying F67 “failed because proxy was wrong” without lifecycle label definition | Overstates diagnosis; F67 already isolated economics gap |
| PF-alone or DD-alone as single optimization objective | Explicitly in `do_not_repeat`; risks repeating F67C read (PF≥2 in 1/64, DD>10 in 60/64) under a new name |
| F31 OOS slice as fleet-wide calibration anchor | Explicit `do_not_repeat`; F67D is one probe slice only |
| “Runtime-native” without row-grain contract | Would smuggle authority; needs 68A definition first |
| Opening 68B before 68A Tier availability is recorded | Violates paired-tier and label-design-first sequence |

### Needs Local Verification (Codex must check before / during artifact write)

1. **Runtime row inventory for 68A** — Do existing runtime rows + proxy rows support lifecycle label candidates (entry-to-exit deal accounting, swap/cost, DD repricing, trade/signal conversion) at **row grain** F67 preserved? Snapshot asserts method exists but not row coverage, schema, or Tier B partial-context feasibility.

2. **Bridge feasibility for 68D** — “At least one materialized signal if proxy nonzero and bridge is possible” needs a concrete bridge checklist (artifact path, ONNX export surface, EA handoff identity). Snapshot does not confirm bridge is possible for economics labels vs count-parity labels.

3. **Frontier governance / retrospective gate** — Whether five-stage retrospective or register state blocks frontier open is not in snapshot. **needs_local_verification** on `docs/registers/five_stage_retrospective_register.yaml` and frontier open policy before canonical stage open claims.

Until (1)–(3) are checked locally, write **draft/open-direction** artifacts only — not “F68 opened and active” as operational truth.

---

## Q4. Forbidden Claim Risks Codex Must Guard in F68

| Risk | Why it’s dangerous | Guard |
|------|-------------------|--------|
| **Runtime authority** | F67 showed signal/feature diff 0 yet PF 1.0, DD 30.58, long-only 259/0 | Every 68D probe = observation only; no “validated for deployment” |
| **Economics parity = count parity** | F67 negative memory | Separate proxy KPI axes; never collapse to signal diff |
| **Proxy KPI “closer” without metric contract** | Success criterion is comparative | Pre-register comparison baseline (F67 proxy vs F68 proxy vs runtime) in 68A |
| **PF≥2 or DD<10 as scout success** | F67C fleet stats undermine single-metric wins | Multi-axis economics score; PF-only optimization forbidden |
| **F31 slice → fleet truth** | F67D is one OOS window | Label per-probe; no baseline selection |
| **Selected baseline / promotion candidate** | Exploration stage | Close as seed surface or clue only |
| **Tier A-only alpha read** | Paired-tier rule | 68A must record Tier A separate, Tier B separate, combined or `missing_required` |
| **ONNX export = runtime parity** | New surface, untested bridge | Export identity ≠ economics equivalence |
| **Repair loop disguised as scout** | If 68B chases count alignment | Stop and close as negative memory |
| **Goal Achieve / live readiness** | Frontier exploration | No language in closeout templates |

Highest-leverage guard: **define the economics comparison contract in 68A before any 68B run** — otherwise “closer to MT5 runtime economics” becomes unfalsifiable narrative.

---

## Recommended Codex Direction (final)

**Proceed with F68 open as new frontier stage** with claim boundary held at stage-open direction + scout planning only.

**Before canonical open artifacts:**

1. Locally verify runtime/proxy row availability for lifecycle labels (68A preflight).
2. Locally verify frontier open gates (retrospective register if applicable).
3. Lock 68A comparison metric contract vs F67 proxy baseline.

**Do not:** reopen F67 count-parity repair, inherit F67/F31 as baseline, or advance 68B until 68A Tier labeling and label candidates are documented.

---

## Compact Receipt

| Field | Value |
|-------|--------|
| **trigger_reason** | Stage-open Grok review after F67 closeout (`preserved_clue_negative_memory_no_authority`) |
| **bounded_evidence** | F67 KPI snapshot, gap cause, proposed F68 thesis/sequence/success criteria from prompt |
| **advice_classification** | **accepted** (open new frontier); **needs_local_verification** (row inventory, bridge checklist, frontier gate register) |
| **claim_boundary** | Stage-open direction and scout framing only; no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve |
| **final_codex_direction** | Open `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout` as F67 successor; execute 68A→68E; guard economics-metric contract and paired-tier records before 68B/68D |
