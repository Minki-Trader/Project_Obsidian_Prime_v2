# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier53_pre_mt5_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
Grok 외부 2차 의견으로 Frontier 53 pre-MT5 후보를 검토합니다. 먼저 협업 스킬과 로컬 근거를 확인합니다.
# Grok Pre-MT5 Review — Frontier 53

**Review size:** small
**Role:** external second opinion only — no authority, no promotion, no completion claim
**Local verification performed:** `source_truth_snapshot.json`, `selected_proxy_candidate.json`, `proxy_surface_summary.csv`, `expected_signal_summary.csv`, `runtime_policy_manifest.json`, `.set` handoff, `run_frontier53_runtime_probe.py`. No `final_decision.json` — MT5 not run yet. Consistent with pre-MT5 scope.

---

## Receipt

| Field | Value |
|---|---|
| trigger_reason | User-requested Grok pre-MT5 critique |
| review_size | small |
| direction_before_grok | Send one Tier A runtime probe for `f53b_logreg_l2_c05_short_q25_q70_s90` |
| bounded_evidence | Candidate identity, proxy KPIs, ONNX parity, runtime policy, expected signals |
| advice_classification | **Q1: accepted** · **Q2: accepted** · **Q3: needs_local_verification at execution time only** |
| forbidden_claim_check | No completion / baseline / promotion / runtime authority / live readiness / Goal Achieve claimed |

---

## Q1. Valid to send to one MT5 runtime probe?

### Classification: **accepted**

**Yes — as one observation-only runtime probe, not as a strong-edge bet.**

Local files line up end-to-end:

- **Candidate identity** matches: `f53b_logreg_l2_c05_short_q25_q70_s90`, threshold `0.5617501169006113`, 58 features, hash `fa06973c...`
- **Model** is `logreg_l2_c05_balanced` with `class_weight="balanced"` in the F53 script
- **ONNX parity** passed: 4096 rows, max abs diff `8.30e-07`
- **Runtime policy** in manifest, override manifest, and `.set` files match the stated F52 DD envelope + suppression removal
- **Expected signals** density (7.26 validation_is, 10.24 OOS per day) matches proxy trade counts
- **Stress q=0.93** correctly excluded (`runtime_probe_candidate_flag=false`, lower density)

**Why this is acceptable for a probe**

F53’s question is whether a **new PF source** (path-quality classifier) survives MT5 order path — not whether it already wins. Proxy PF is only barely above 1.0 (validation 1.002, train 1.046). That weakness does **not** block a probe; it sets the expected outcome band.

**Runtime policy is coherent with the ONNX contract**

- `p_short = binary_event_score`, `p_flat = 0`, `p_long = 0`
- `threshold_margin` with `InpShortThreshold=0.56175`, `InpMinMargin=0`, `InpLongThreshold=1.0` → short when score ≥ threshold; long never fires
- Matches Python: `score >= threshold → short (-1)`

**Scope is correctly bounded**

- Tier A only: `validation_is` + `oos`
- Claim boundary: `runtime_probe_observation_no_authority`
- Tier B / combined: `missing_required` in gate audit — documented, not a blocker for this single probe

**Caveat (not a rejection):** Proxy uses train-quantile MFE/MAE path exits; MT5 uses ATR SL/TP + maxhold=6 + close-on-flat. Large proxy→MT5 PF gap is **expected by design**. The probe measures that gap — it does not promise parity.

---

## Q2. First local failure mode Codex should watch?

### Classification: **accepted**

### 1. **Signal / feature parity failure** — watch this first

Before trusting any PF number, confirm:

| Metric | Pass condition | Why first |
|---|---|---|
| `feature_ready_diff` | `== 0` on both splits | If features don’t match, the probe is invalid |
| `signal_count_diff` | near `0` vs `expected_signal_summary.csv` | If EA fires different signals than Python, PF is uninterpretable |

F53’s own `stage_judgment()` checks `feature_ready_ok` before PF. Parity failure → **blocked / invalid probe**, not “weak alpha.”

**Codex action at MT5 time:** Compare telemetry short-count vs expected 1328 (validation_is) and 1341 (oos).

### 2. **Proxy→runtime economics collapse on `validation_is`** — watch second

Validation proxy PF is **1.001867** — essentially zero edge before spread, commission, and exit-path mismatch.

Most likely post-parity outcome:

- MT5 PF **below 1.0** on validation_is
- Trade count in band but net economics negative
- OOS may look slightly better (proxy 1.096) but still fragile

This is a **valid negative observation**, not a handoff failure — if parity passed.

### 3. **Density / churn drift from lifecycle policy** — watch third

With `InpCloseOnFlatSignal=true`, `InpEntryTransitionOnly=false`, cooldowns=0:

- More round-trips than static proxy mask evaluation
- `runtime_trades_per_day` may diverge from proxy even when `signal_count_diff` is small

Track via `proxy_runtime_gap.csv` density column after the run.

---

## Q3. Overall bounded verdict

| Item | Classification |
|---|---|
| Send one MT5 runtime probe with this candidate + policy | **accepted** |
| First failure mode to watch | **accepted** — parity first, then validation_is PF collapse |
| Post-MT5 execution checks | **needs_local_verification** — Common Files ONNX/feature deploy, EA compile, `feature_ready_diff` / `signal_count_diff` after tester output |

### Rejected (forbidden claims)

- Completion, baseline, promotion, runtime authority, live readiness, Goal Achieve — **not claimed, not granted by this review**

### Not rejected

- Weak proxy edge — probe is still valid as observation
- Exit-model mismatch — intentional; measured by the probe
- Tier B missing — ledger note only for this probe scope

---

## Final Codex direction

**Proceed with one MT5 runtime probe** for `frontier53Z_runtime_probe_backfill_v1` / `f53b_logreg_l2_c05_short_q25_q70_s90`.

**Stop / downgrade conditions after MT5:**

1. `feature_ready_diff != 0` or large `signal_count_diff` → **invalid probe**, fix handoff before any PF read
2. Parity OK but validation_is MT5 PF ≪ proxy (~1.002) → record as **negative memory / preserved clue**, not promotion path
3. Do not send stress q=0.93 as first probe — already correctly excluded

**Claim boundary after probe:** `runtime_probe_observation_no_authority` only. A negative MT5 result closes F53’s PF-source question honestly; it does not kill broader frontier exploration.
