# F73F Pre-MT5 Grok Review — Advice Classification

## Summary verdict

**Proceed with F73F**, but only as a **capped repair probe(상한 있는 수리 탐침)**. The direction is **mostly accepted(대체로 수용)**; nothing in the snapshot warrants full **rejection(거절)**. Several steps are **needs_local_verification(로컬 검증 필요)** before MT5 and before any stronger claim.

---

## 1. Is F73F justified by F73E gap analysis?

**Accepted (수용)**

F73E points to **`proxy_bridge_selection_divergence(프록시-연결 선택 분기)`** as the primary gap cause, with validation/OOS selection overlap only **~0.18–0.19** despite F73D reporting **signal parity 0 / feature parity 0**. That pattern fits a **handoff-path distortion(인계 경로 왜곡)**: parity at one layer does not imply the same **entry set(진입 집합)** or **economic path(경제성 경로)** as the F73C binary proxy.

F73F targets that layer directly:

- Keeps the **F73C binary decision surface(이진 결정면)** instead of a **3-class bridge(3분류 연결)** that can re-rank or re-threshold entries.
- Avoids **EA module changes(EA 모듈 변경 없음)** while still matching **RuntimeProbeEA 3-column contract(3열 계약)** via graph patch.
- Does **not** claim to fix weak PF or low density; it only tests whether removing bridge distortion narrows the proxy/runtime gap.

**Claim boundary preserved (주장 경계 유지):** scoped as repair probe, explicit stop conditions, no completion/baseline/promotion/runtime authority/live readiness.

**Caveat (needs_local_verification):** F73E’s secondary cause — **`trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극)`** — may still dominate even if selection overlap improves. F73F success should be defined narrowly: **narrower selection overlap and/or improved runtime KPI vs F73D**, not “F73 closed” or “gap solved.”

---

## 2. Is this F72 repeat?

**Rejected as a concern (해당 우려는 거절)**

From the snapshot, F73F is **not** “change trade shape first(거래 형태 우선 변경).” It is **remove bridge-induced runtime handoff distortion(연결로 생긴 런타임 인계 왜곡 제거)** while staying on the F73 topic (feature/model/session-regime signal handoff). That is a distinct hypothesis from F72-style shape-first repair.

---

## 3. Risks Grok sees from the snapshot alone

| Risk | Classification | Note |
|------|----------------|------|
| Retrain drift vs `f73c_0002` | **needs_local_verification** | Same recipe ≠ same artifact; proxy reproduction must be explicit pass/fail |
| Patched ONNX `[0, p_flat, p_long]` threshold semantics | **needs_local_verification** | EA may use 3-class argmax or column-specific rules; `p_short=0` must not silently skew decisions |
| “Signal parity 0” under F73D vs 0.19 overlap | **needs_local_verification** | Codex must define **which parity definition** F73F will use (bar-level signal vs selected-entry set) |
| Lifecycle gap remains after parity | **accepted as boundary** | Passing local parity does not authorize strong runtime success claims |

---

## 4. Mandatory local checks before MT5 execution

**All needs_local_verification — Codex must complete before Strategy Tester:**

1. **Proxy reproduction gate (프록시 재현 게이트)**
   Retrained candidate vs `f73c_0002`: selected count, net/PF/DD/tpd, score threshold ~`0.4489733875`. Record material match or **documented delta(기록된 차이)**; no silent drift.

2. **Binary probability parity (이진 확률 동등성)**
   sklearn (or training-source) probabilities vs exported ONNX vs **patched** ONNX mapped probabilities. Tolerance and max-delta must be recorded.

3. **Signal parity on the same tape (동일 테이프 신호 동등성)**
   Same bars, same features, same threshold → same long/flat (or entry) decisions as reproduction proxy.

4. **Feature readiness parity (피처 준비 동등성)**
   Same readiness/null-bar behavior as F73D probe context; “0 feature diff” must be re-checked on the **binary** path, not assumed from F73D bridge.

5. **Graph-patch contract check (그래프 패치 계약 점검)**
   Confirm output schema is exactly `[p_short=0, p_flat, p_long]`, dtypes/shapes match EA expectation, and **decision rule equivalence(결정 규칙 동등성)** holds vs raw binary `[p_flat, p_long]`.

6. **Selection-overlap pre-MT5 metric (MT5 전 선택 중복 지표)**
   Compare F73F local selected-entry set vs F73C proxy on validation/OOS windows. Pre-register: overlap should materially exceed F73D’s **~0.19** or the repair is **inconclusive(불충분)**, not “blocked setup” alone.

7. **Artifact identity line (산출물 정체성 한 줄)**
   Model hash, ONNX hash, patched-graph hash, threshold, feature manifest — one traceable row before tester.

**If any of 1–5 fail → close as blocked or invalid setup (차단/무효 설정), not success.** That matches the proposed stop condition and is **accepted(수용)**.

---

## 5. What Codex may claim after MT5 (if receipts exist)

| Outcome | Allowed claim boundary |
|---------|------------------------|
| Parity pass + tester receipts + overlap ↑ vs F73D | **Repair probe informative(수리 탐침 유익)**; gap cause update (bridge vs lifecycle) |
| Parity pass + tester receipts + KPI still far from proxy | **Primary cause may be lifecycle(생명주기가 주원인일 수 있음)**; F73F does not close F73 |
| Parity fail or patch fail | **blocked/invalid**; no MT5 success narrative |
| Any path | **No** completion, baseline, promotion, runtime authority, live readiness, Goal Achieve |

---

## Final classification

| Advice | Classification |
|--------|----------------|
| Proceed with F73F before closing F73 | **Accepted (수용)** — as capped repair probe, not stage closeout |
| F73F justified by F73E `proxy_bridge_selection_divergence` | **Accepted (수용)** |
| Preserve claim boundary (repair probe only) | **Accepted (수용)** |
| Skip F73F and close F73 on F73D receipts alone | **Rejected (거절)** — snapshot shows large proxy/runtime economics gap with plausible bridge cause |
| Retrain + ONNX export + graph patch + parity + MT5 sequence | **Accepted (수용)** with strict gates |
| Proxy reproduction, patched-graph semantics, selection overlap, lifecycle residual | **Needs_local_verification (로컬 검증 필요)** |

**Bottom line:** Codex should proceed with F73F. Treat it as the **narrowest next experiment(가장 좁은 다음 실험)** implied by F73E, keep claims at **repair-probe(수리 탐침)** level, and do not close F73 until local gates and MT5 receipts show whether the gap shrank via **selection alignment(선택 정렬)** or persists via **trade lifecycle(거래 생명주기)**.
