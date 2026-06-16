## F68J Pre-Probe Review (F68J 탐침 전 검토)

**Claim boundary (주장 경계):** runtime probe observation only (런타임 탐침 관찰 전용). No authority (권위 없음).

---

### Q1. Is F68J a reasonable repair probe after F68H/F68I?

**accepted** — F68J is a **repair probe (수리 탐침)**, not a repeat of capped ATR tuning (상한 평균진폭 조정 반복).

- F68H failed because variants **collapsed** to one effective shape: `open_sl=180`, `open_tp=260` via `InpAtrMaxStopPoints` / `InpAtrMaxTakeProfitPoints` caps.
- F68I correctly labeled that as **invalid variant differentiation (변형 구분 무효)** and preserved the clue: telemetry ATR is in **point-scale (포인트 단위)** (~904–35019 validation, ~1171–12734 OOS).
- F68J changes the **failure mode (실패 모드)**: min/max caps `0` + three distinct multiplier ladders (0.3/0.5, 0.6/1.0, 1.0/1.6). That targets the documented gap cause (간극 원인), not another sweep on 40/180 or 60/260 style caps.
- **needs_local_verification** — “uncapped” must mean **no cap path re-applies 180/260** in EA logic, `.set` defaults, or post-multiplier clamping. Snapshot alone cannot prove that.

**rejected** — Treating F68J as “more F68H tuning” without first proving telemetry differentiation.

---

### Q2. What must Codex verify locally before and after MT5?

**needs_local_verification — before run (실행 전)**

| Check | Why |
|--------|-----|
| `.set` / manifest per variant | Multipliers and **caps explicitly 0**; no hidden F52-style 40/180 or 60/260 |
| `InpAtrMaxStopPoints` / `InpAtrMaxTakeProfitPoints` | Not silently reintroducing 180/260 |
| Unit semantics | Multipliers × observed ATR points → expected SL/TP ranges, not re-clamped to one signature |
| Same F68F ONNX/feature/signal path | `f68b_0872ddc6192f` lineage unchanged |
| Parity baseline | Signal/feature diff targets remain `0` |

**needs_local_verification — after run (실행 후)**

| Check | Why |
|--------|-----|
| **Effective SL/TP telemetry (실효 손절/익절 기록)** | Per-variant distributions differ; **no collapse** to one fixed cap signature |
| Signal diff `0`, feature diff `0` | Parity preserved across all three variants |
| Validation + OOS for **all** variants | Per success criteria |
| KPI vs F68F | DD direction (lower preferred), trades/day not exploding (~4 vs F68H ~15–24), PF not destroyed vs F68F (~1.01 / 1.18) |
| Negative memory guard | Do not repeat F68H capped observation as if it were new evidence |

**accepted** — Primary pass/fail for this probe is **telemetry differentiation first**, then KPI vs F68F. KPI alone without proven variant separation repeats F68H’s mistake.

---

### Q3. What should Codex reject as out of boundary for F68J?

**rejected — for F68J scope**

- Completion, selected baseline, promotion, runtime authority, live readiness, Goal Achieve
- “F68J fixes economics” or “ATR envelope solved” from one probe
- Re-running F68H-style capped grids (40/180, 60/260) on the same ONNX path
- Judging success on PF/net alone while telemetry shows identical `open_sl`/`open_tp` across variants
- Using F68H negative KPIs as the comparison baseline (F68F is the stated reference)
- Expanding scope (new ONNX, feature path, signal logic) under the F68J repair label
- Promoting any variant to operating default from validation/OOS on this snapshot alone

**accepted — in boundary**

- Observation: variants **did or did not** differentiate in effective SL/TP telemetry
- Observation: KPI direction vs F68F on DD, trades/day, PF under parity constraints
- Recording negative memory if caps or unit error recur
- Preserved clue: point-scale ATR telemetry exists; next step depends on **unit-corrected** semantics, not cap repetition

---

### Summary (요약)

| Item | Classification |
|------|----------------|
| F68J as repair after F68I | **accepted** (conceptually sound) |
| “Uncapped” without code/set proof | **needs_local_verification** |
| Telemetry-first success gate | **accepted** |
| Strong closure / promotion claims | **rejected** |
| F68H-style capped retune | **rejected** |

**Codex direction (코덱스 방향):** Run F68J only after preflight confirms caps are off and unit math matches telemetry; after MT5, **fail fast** if effective SL/TP collapse repeats—regardless of headline KPI. Compare economically to **F68F**, not F68H.
