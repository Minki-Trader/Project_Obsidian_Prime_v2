## F72D Runtime Bridge Review (F72D 런타임 연결 검토)

**Claim boundary (주장 경계):** This is a pre-MT5 bridge critique only. No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

### 1. Accepted (수용) — proceed as proposed

| Item | Why valid |
|------|-----------|
| **Mandatory MT5 Runtime Probe (필수 MT5 런타임 탐침)** with observation-only framing | Frontier stage rule requires the probe unless system limit or logic impossibility. F72C failed the meaningful-candidate gate (의미 후보 게이트); proxy alone does not excuse skipping MT5. |
| **Narrow compatibility bridge (좁은 호환 연결)** instead of direct binary handoff | F72C best proxy is binary small NN; EA expects ONNX 3-class `[p_short, p_flat, p_long]`. A dedicated bridge model is the right shape—not forcing the binary ONNX into a 3-class slot. |
| **Explicit blocked/invalid setup (차단/무효 설정)** if signal meaning cannot be preserved | Matches progressive hardening: record failure with repair action rather than silently skipping the probe (F69/F70/F71-style “proxy-only closure” avoidance). |
| **Probe scope limited to parity + gap observation (동등성 + 간극 관찰)** | Signal parity (신호 동등성), feature readiness parity (피처 준비 동등성), net/PF/DD/trades/day, and proxy/runtime gap are the correct observables—not promotion KPIs. |
| **Regenerate selected-entry tape (선택 진입 테이프 재생성)** from bridge signal under F72C shape/label contract | Keeps trade-shape and label contract anchored to F72C repair (`short_h24_sl1.2_tp1.8 / early_survival_045`) while separating runtime signal generation from proxy training artifact. |
| **Export bundle triad (보내기 묶음)** ONNX + feature matrix + RuntimeVetoTape | Minimum materialization set for a real probe, not a stub run. |

**Effect (효과):** F72D can satisfy the mandatory probe obligation without pretending F72C already passed exploration gates.

---

### 2. Rejected (거절) — do not proceed this way

| Item | Why reject |
|------|------------|
| **Treating F72C OOS as runtime success criteria** (`4933 / 1.34 / 12.8% / 3.01`) | Meaningful candidate = 0; DD > 10%, PF < 2. These numbers are proxy context only—not MT5 pass/fail thresholds or baseline targets. |
| **Implicit promotion of `f72c_0098` as “the” runtime candidate** | Best repair candidate ≠ meaningful candidate. Bridge must not re-label it as selected baseline or promotion candidate. |
| **Synthetic 3-class semantics without parity proof** | Mapping binary short-positive → `p_short`, invented long counterpart → `p_long`, remainder → `p_flat` can distort F72C meaning if long is not independently defined under the same label contract. That risks repeating F69/F70/F71: runtime-compatible packaging that no longer measures the same decision rule. |
| **Using bridge MT5 KPIs to overturn F72C negative gate** | A positive runtime probe cannot retroactively create meaningful-candidate status or imply alpha confirmation. |
| **Threshold or veto tuning inside F72D to “make probe look good”** | Observation-only probe must not become a hidden optimization pass on the same OOS window. |
| **Skipping probe because proxy “already improved” after F72C repair** | Repair expanded scout clues (16) but did not clear gates. Improvement ≠ exemption. |
| **Claiming runtime authority or live readiness from a bridge built only for compatibility** | Bridge is a transport layer, not evidence that the underlying idea is operationally ready. |

**Effect (효과):** Blocks the common failure mode: packaging for MT5 that changes what is being tested, then reading tester output as exploration success.

---

### 3. Needs local verification (로컬 검증 필요) — Codex must verify before MT5

| Verification | What Codex must establish |
|--------------|---------------------------|
| **Binary → 3-class mapping contract** | Exact rule for `p_short`, `p_flat`, `p_long` from bridge training/inference; whether long counterpart label is real paired label or derived/synthetic. Mismatch here = invalid setup, not a weak probe. |
| **Signal parity vs F72C binary selected-entry tape** | Same bars, same entries, same veto outcomes on a fixed replay slice before MT5. Without this, bridge distorts proxy meaning. |
| **Feature matrix identity** | Column order, scaling, warmup, and Tier routing (Tier A/B if applicable) match between Python materialization and EA consumption. |
| **Shape/label contract lock** | `short_h24_sl1.2_tp1.8`, `early_survival_045`, `small_nn_16`, `all58` hashes/manifests unchanged except the intentional bridge model swap. |
| **ONNX ↔ EA contract** | Input tensor shape, output layout `[p_short, p_flat, p_long]`, and RuntimeVetoTape hook behavior match existing EA expectations without undeclared EA logic changes. |
| **Selected-entry tape regeneration lineage** | New tape is traceable to bridge output + F72C contract, not hand-edited or threshold-tuned post hoc. |
| **Materialization feasibility** | Export, bundle, and tape generation complete without silent fallback. If not → `blocked` with repair action, per proposal step 5. |
| **Probe success/failure definition for F72D** | Pre-declare: parity failure = invalid/blocked; parity pass + KPI gap = observational record only. No automatic stage closeout from tester numbers. |
| **System-limit vs logic-impossibility branch** | If bridge cannot preserve meaning, document which condition applies so mandatory-probe rule is satisfied by explicit blocked record, not omission. |

**Effect (효과):** Codex owns the gate between “compatible packaging” and “same idea under test.” Grok cannot verify these from the snapshot.

---

## Summary classification (요약 분류)

| Verdict | One-line |
|---------|----------|
| **Accepted** | Proceed with narrow 3-class bridge + regenerated tape + observation-only MT5 probe + explicit blocked path if meaning cannot be preserved. |
| **Rejected** | Do not use F72C proxy KPIs, `f72c_0098`, or bridge tester results to imply meaningful candidate, baseline, promotion, or runtime authority; do not invent 3-class semantics without parity proof. |
| **Needs local verification** | Binary→3-class mapping fidelity, signal/feature parity, artifact lineage, ONNX/EA contract match, and materialization feasibility must pass before MT5 execution. |

**Final Codex direction (최종 Codex 방향):** Execute F72D as a **parity-first runtime observation packet (동등성 우선 런타임 관찰 묶음)**. MT5 is mandatory; bridge is the minimum compatibility layer. If parity fails, record **blocked/invalid** and repair—do not skip, do not promote, do not treat tester KPIs as overturning F72C’s meaningful-candidate failure.
