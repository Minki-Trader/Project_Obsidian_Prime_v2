# Grok Post-MT5 Review — F66 `frontier66C_proxy_signal_mt5_backfill_v1`

**Review size:** medium (제한 스냅샷 + 집중 질문 1개)
**Role:** external second opinion only — no local verification performed

---

## Verdict on Codex conclusion

**Classification: `needs_local_verification` (수용 방향은 맞으나, 커밋/푸시 전 로컬 재검증 필요)**

Codex의 핵심 판독 — *signal handoff gap(신호 인계 간극) is not the main issue; the gap is execution semantics(실행 의미론)* — 은 제공된 수치와 **방향적으로 일치(sound in direction)**합니다.
`feature_ready_diff = 0` (64/64), `signal_count_diff = 0` (64/64)이면 **신호·피처 인계 계층(signal/feature handoff layer)** 은 이번 백필에서 **닫혔다(closed)**고 말할 근거가 있습니다.

다만 **“main issue(주요 원인)”** 라는 표현은 아직 **과주장(overclaim) 위험**이 있습니다. 런타임 KPI가 나쁜 것(60/64 DD>10%, 1/64 PF≥2)은 사실이지만, 그것만으로 execution semantics가 **유일·1순위 원인**이라고 단정하려면 decomposition(분해) 가중치와 설정 동등성(setting parity) 확인이 더 필요합니다.

---

## What is properly bounded (잘 묶인 부분)

| Claim | Assessment |
|-------|------------|
| Observation only, no completion/baseline/promotion/runtime authority | **Accepted** — 스냅샷 범위와 일치 |
| 64/64 tester/runtime/report complete | **Accepted** — 단, F26/F34는 “no MT5 attempt”와 별도로 명시 유지 |
| Signal/feature parity at count level | **Accepted** — 0/0 diff는 강한 근거 |
| Runtime economics look poor (DD/PF) | **Accepted** — 수치가 그렇게 말함 |
| F11 OOS PF 2.18 as single bright spot | **Accepted if framed as anecdote** — 전체 패턴 대표로 쓰면 안 됨 |

---

## Overclaims / soft spots (과주장·약점)

### 1. “Signal handoff is **not the main issue**”
- **Risk:** `signal_count_diff` / `feature_ready_diff`는 **개수·준비 상태**만 닫습니다. 아래는 아직 열려 있을 수 있습니다:
  - bar/timestamp alignment(봉·시각 정렬)
  - signal ordering / duplicate suppression(순서·중복 억제)
  - proxy path vs ONNX/runtime path identity(프록시 vs 실제 런타임 경로 동일성)
- **Safer wording:** *“Count-level signal handoff parity holds; remaining gaps appear downstream of signal emission.”*

### 2. Execution semantics as **the** gap
- 나열하신 항목(fixed lot, one-position cap, max hold, SL/TP, spread/cost, broker DD basis)은 **가설 목록으로 타당**합니다.
- 하지만 스냅샷에 **어느 항목이 얼마나 기여했는지** 없습니다. `frontier66_proxy_runtime_gap_decomposition_report.md` 내용이 없어 **인과 순위(causal ranking)** 는 검증 불가.
- **Risk:** decomposition 없이 “main issue = execution semantics”는 **내러티브 주장(narrative claim)** 에 가깝습니다.

### 3. Stage scope vs split count
- Audit scope: F02–F64
- Actually backfilled: F11, F15, F18–F49
- Logic-zero: F26, F34 (no MT5 attempt)
- 64 splits, 32 executable stages, 31/32 max DD > 10%

이 조합은 **내부적으로 설명 가능**하지만, 커밋 메시지/요약에 **“F02–F64 전체 소급 완료”** 같은 문구가 있으면 **과주장**입니다.
정확한 표현: *“proxy-signal MT5 backfill completed for the routed executable split set; F02–F64 audit frame with partial stage execution.”*

### 4. F11 PF 2.18
- 1/64만 PF≥2 → **탐색적 이상치(exploratory outlier)** 로만 써야 합니다.
- “runtime can work”나 “promising stage”로 확장하면 **승격·기준선 뉘앙스**가 섞입니다.

---

## Missing local verification (Codex가 커밋 전 해야 할 것)

스냅샷만으로는 아래를 **확인했다고 말할 수 없습니다.** Codex 로컬 검증 필수:

1. **Config parity ledger** — proxy scout vs MT5 backfill: lot, max positions, hold, SL/TP, spread, commission, modeling mode가 split별로 **동일 문서화**됐는지
2. **DD basis crosswalk** — `frontier66_proxy_runtime_gap_by_split.csv`의 DD가 balance/equity/floating 중 무엇인지, proxy 쪽과 **같은 정의**인지
3. **Decomposition ↔ raw row reconcile** — decomposition report 수치가 `frontier66_proxy_signal_runtime_rows.csv`와 **행 단위 합산 일치**
4. **64-split registry mapping** — 64가 tier/split/OOS 라벨과 1:1인지, 누락·중복 split 없는지
5. **F26/F34 logic-zero** — “no MT5 attempt”가 **의도적 제외(blocked_by_design)** 인지, 실패인지 manifest에 명시
6. **Artifact hashes** — `run_manifest.json` / ledger에 run id `frontier66C_proxy_signal_mt5_backfill_v1`와 CSV 4종 **경로·해시 연결**
7. **Negative control** — signal parity 0/0인데 PF/DD가 크게 나쁜 split 1–2개를 **수동 trace** (진입은 맞는데 청산이 다른지 등)

---

## Suggested gap taxonomy (더 나은 분류)

Codex 결론을 커밋하기 전에, 아래 **6층 taxonomy** 로 바꾸면 주장 경계가 더 깨끗해집니다:

```text
L0 Scope / executability     — logic-zero, blocked tier, no bundle
L1 Feature readiness parity  — feature_ready_diff  (F66: 0/64 ✓)
L2 Signal emission parity    — signal_count_diff   (F66: 0/64 ✓)
L3 Order intent parity       — entry/exit/reject rules, hold, cap
L4 Fill & cost model         — spread, slippage, commission, lot
L5 KPI measurement basis     — DD definition, PF window, OOS label
L6 Stage-level rollup        — gap_by_stage aggregates + decomposition weights
```

**Codex 현재 결론의 재표현 (bounded):**

> L1–L2 parity holds for the backfilled split set. Residual runtime PF/DD dispersion is **consistent with** L3–L5 mismatch; decomposition weights **pending local verification**.

이렇게 쓰면 “signal은 괜찮다”와 “실행 의미론이 문제다” 사이의 **인과 단정**을 피하면서 같은 인사이트를 유지합니다.

---

## Commit / push readiness

| Item | Grok judgment |
|------|----------------|
| Direction of conclusion | **Accept** |
| Wording “not the main issue” | **Downgrade** → “not supported at L1–L2; downstream L3–L5 suspected” |
| Execution semantics list | **Keep as hypothesis taxonomy**, not ranked root cause |
| Observation-only boundary | **Keep** — 잘 지킴 |
| Push without local checks 1–7 | **Reject** — `needs_local_verification` |

---

## One-line summary for Codex

**F66 post-MT5 read is directionally sound and mostly bounded, but “main issue = execution semantics” should be downgraded to a layered hypothesis until decomposition CSVs, config parity, and DD-basis crosswalk are locally reconciled; use the L0–L6 taxonomy in the commit narrative.**
