# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier62_pre_mt5_review/small_review`
- classification(분류): `needs_local_verification`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), hashes(해시), ledgers(장부), MT5 output(MT5 출력)으로 다시 검증한다.
- effect(효과): Grok output(그록 출력)은 authority(권위)가 아니라 bounded critique(제한 비판)로만 쓰인다.

## Clean Output(정리 출력)
# Frontier62 Pre-MT5 Review — Bounded Second Opinion

**Claim boundary(주장 경계):** `runtime_probe_observation` only. No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

## Classification by option

| Option | Verdict | Rationale |
|--------|---------|-----------|
| **1. Run MT5 anyway** | **rejected** | Proxy validation density ~`0.366/day` vs target `5–10/day` is roughly **14–27×** below band. MT5 here mostly measures **sparse-runtime mechanics**, not whether event-compressed representation closes the F61 density gap while keeping side-allocation signal. Expensive run with weak hypothesis linkage. |
| **2. Bounded proxy repair, then MT5** | **accepted** | Matches stage-open Grok conditions: locked sequential proxy definition stays; **only** threshold/margin/cooldown grid expands; density-band penalty + retrain gate apply before any MT5 probe. Tests the actual stage question at a defensible density. |
| **3. Close as invalid setup** | **rejected** | Too strong for current evidence. ONNX parity passed; OOS PF/DD are not dead (`1.6075 / 0.5717`). This reads as **grid/protocol calibration miss**, not hypothesis falsification. Exploration rule: sparse ≠ idea-dead. |

**Overall recommendation:** **accepted → option 2**, with one **needs_local_verification** gate below.

---

## Smallest safe action (minimal sequence)

1. **Hold locked definition** — event-compressed sequential proxy, density-band penalty, retrain gate unchanged.
2. **One bounded repair pass** — expand **only** threshold / margin / cooldown grid toward `5–10 trades/day`; no new features, no runtime-policy unlock, no candidate cherry-pick outside the frozen grid rules.
3. **Retrain + reselect** — one candidate frozen from that pass; record train/val/OOS PF, DD, density.
4. **Density decision gate (local):**
   - If proxy val density lands **inside or near** `5–10/day` (e.g. ≥`~3/day` as a pragmatic lower bound) → **one narrow MT5 runtime probe** on the frozen candidate.
   - If still **≪ target** after bounded expansion → **do not run full MT5 yet**; close this pass as **`density_miss_after_bounded_repair`** (exploration negative), not `invalid_setup`. Optional **ultra-narrow MT5** only if you need a single density-gap datapoint—and label it **sparse-proxy observation only**.

5. **MT5 claim** — if run: “observed runtime density / handoff behavior vs proxy for candidate X”; not alpha quality, not promotion.

---

## needs_local_verification (before MT5)

Codex should verify locally:

- Whether the **locked grid rules** allow enough threshold/margin/cooldown expansion to reach `~3–10/day` without breaking stage-open locks.
- Whether **density-band penalty** forces full retrain on every grid point (cost/time bound for “one repair pass”).
- Whether **handoff/ONNX path** stays clean after grid expansion (parity re-check on the new frozen candidate only).

Until those three are checked, MT5 timing stays **needs_local_verification**; direction still favors **repair-first, not MT5-now**.

---

## Why not option 1 or 3

- **Option 1** satisfies “run something in MT5” but not “test density-gap hypothesis at meaningful trade rate.” Risk: costly **misleading sparse-runtime read**.
- **Option 3** conflates **calibration failure** with **hypothesis failure**. Stage question is unanswered until a **density-targeted** proxy candidate exists or bounded repair proves the band is unreachable under locked protocol.

---

## One-line co-pilot summary

**Do one bounded proxy grid repair toward 5–10/day, retrain, freeze one candidate, then run a single narrow MT5 probe only if density is no longer far below target; otherwise record density_miss and skip expensive MT5 for now.**
