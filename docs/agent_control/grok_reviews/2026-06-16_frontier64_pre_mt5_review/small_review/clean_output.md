# Frontier64 Pre-MT5 Review — Grok Classification

**Classification(분류): `needs_local_verification(로컬 검증 필요)`**

Proxy-only evidence(프록시 전용 근거) is materially better than F63 reference proxy(참조 프록시) and answers the stage-open thinning warning(단순 축소 경고), but F63 negative memory(부정 기억) shows proxy strength(프록시 강도) does not transfer to MT5 without verified handoff(검증된 인계). This packet does not justify MT5 execution yet; it justifies **local handoff verification first(인계 로컬 검증 우선)**, then **one narrow MT5 probe(좁은 MT5 탐침 1회)** if that verification passes.

---

## 1. Is proxy strong enough for one narrow MT5 probe after local handoff verification?

**Conditional yes(조건부 예)** — not on proxy alone(프록시만으로는 아님).

**For(근거):**
- Best candidate(최선 후보) beats F63 proxy on PF, DD, density, smoothness(수익 팩터·손실폭·빈도·매끄러움) on validation and OOS(검증·표본외).
- `hazard_gate_proxy_clue_not_only_thinning(위험 게이트가 단순 축소만은 아님)` — density(빈도) rose vs F63 proxy, so F55-style sparse admission(희소 진입) is not the dominant read yet.
- ONNX parity(온엑스 동등성) passed at `1.98e-7` — necessary but not sufficient(필요조건, 충분조건 아님).
- 48 four-axis beat rows(네 축 동시 개선 행) and 80 preserved clue rows(보존 단서 행) support exploration continuation(탐색 지속), not closure(마감).

**Against(반대 근거):**
- F63 proxy was decent; MT5 collapsed anyway(PF ~0.35/0.44, large `signal_diff(신호 차이)`).
- `seed surface rows = 0(씨앗 표면 행 0)` weakens surface-confidence(표면 신뢰).
- No WFO/stress/MT5 yet — claim boundary(주장 경계) stays proxy-only(프록시 전용).

**Verdict:** Strong enough to **earn** one narrow probe **after** handoff verification; not strong enough to skip it.

---

## 2. Main proxy-to-runtime risk(프록시-런타임 주요 위험)

**Composed handoff divergence(합성 인계 불일치)** — not ONNX tensor drift(텐서 드리프트) alone.

F64 splits logic into:
1. **Binary hazard gate(이진 위험 게이트)** — admit/block only(허용/차단만)
2. **Simple symmetric direction rule(단순 대칭 방향 규칙)** — supplies direction(방향 제공)

F63 already showed `feature_ready_diff = 0` yet `signal_diff` was large. That pattern points to **bar-level admission composition(바 단위 허용 합성)**, timing/order(시점/순서), or threshold application(임계값 적용) — not missing features(피처 누락).

Main risk: MT5 reproduces hazard ONNX correctly but **composes it differently with direction rule**, changing the trade set(거래 집합) even when raw hazard scores match.

Secondary risk: hazard gate becomes **effective thinning(실질적 축소)** in runtime — fewer admits, distorted PF/DD vs proxy.

---

## 3. What Codex must verify locally before MT5

| Priority | Verification(검증) | Why(이유) |
|----------|-------------------|-----------|
| P0 | **End-to-end bar-level parity(종단 바 단위 동등성)** on fixed narrow window: hazard decision + direction + final admit/trade intent vs proxy | ONNX parity alone did not save F63 |
| P0 | **Composition order(합성 순서)**: same bar index, same lookback, same threshold semantics (`hz65`, `h2`, `cd0`, `w36`, `h6`, `q75`, `eq55`) | Split handoff is the failure surface |
| P0 | **Admission rate / density check(허용률·빈도 점검)** vs proxy for selected candidate | Confirms not runtime thinning |
| P1 | Artifact identity(산출물 정체성): ONNX hash/path, EA/module wiring, manifest for selected candidate | Prevents wrong-model probe |
| P1 | **Signal/count reconciliation(신호·건수 대조)**: admitted bars, blocked bars, directional entries on same slice | Direct F63 `signal_diff` guard |
| P1 | `io_path(입출력 경로)` / long-path access to `02_runs` artifacts | Avoid false “missing” before probe |
| P2 | Documented narrow probe scope(좁은 탐침 범위): one candidate, one routed tier policy(라우팅 티어 정책), F63-comparable KPI slice | Keeps probe bounded |

**Pass criterion(통과 기준):** local composed parity(로컬 합성 동등성) within agreed tolerance(합의 허용오차) on admission count and bar-level decisions — not just ONNX `max_abs_diff`.

---

## 4. Proceed, adjust handoff first, or close/block?

**Recommendation: adjust handoff first(인계 먼저 조정) → then one narrow MT5 probe(그다음 좁은 MT5 탐침 1회).**

| Option | Verdict |
|--------|---------|
| **Close/block(마감/차단)** | **Rejected(거절)** — proxy improvement and non-thinning hazard read are real exploration signals(탐색 신호). |
| **Proceed to MT5 now(지금 MT5 진행)** | **Rejected(거절)** — F63 negative memory forbids skipping local verification. |
| **Local handoff verify → narrow MT5 probe(로컬 인계 검증 → 좁은 MT5 탐침)** | **Accepted path(수용 경로)** — matches stage intent and external-verification anti-deferral(외부 검증 지연 방지). |

**Stop/close triggers after probe(탐침 후 중단 조건):**
- F63-like collapse: PF and DD diverge sharply with large `signal_diff` despite clean hazard ONNX.
- Hazard gate reduces admits but does not change loss-cluster structure(손실 군집 구조 미변경) — thinning repeat per stage-open warning.
- Handoff parity fails on fixed slice — fix handoff, do not rerun MT5 blindly.

---

## Summary for Codex

| Item | Grok read |
|------|-----------|
| Overall | `needs_local_verification(로컬 검증 필요)` |
| Proxy quality | Sufficient for **next step = verification**, not for MT5 claim |
| MT5 justification | **After** composed handoff parity passes |
| Biggest risk | Hazard × direction **composition mismatch**, not model export |
| Direction | **Do not block F64**; **do not open MT5 yet**; verify handoff locally first |

Forbidden claims(금지 주장) remain **not_claimed(주장 없음)**. This review authorizes verification work and a **conditional** narrow probe — not promotion, baseline, runtime authority, or live readiness.
