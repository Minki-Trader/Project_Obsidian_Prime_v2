# F71 Pre-MT5 Runtime Probe Review (F71 MT5 런타임 탐침 전 검토)

## 1. Advice classification (조언 분류)

**accepted** — with boundary (경계 조건 있음)

Codex’s proposed primary target is **reasonable for a mandatory transfer check (필수 전이 확인)**, not for discovery (탐색). The snapshot shows **0 meaningful candidates (의미 후보 0)** in both F71B and F71C, so the probe should answer one narrow question: *does the best fracture-pass scout surface (균열 통과 탐색 표면) survive proxy→MT5 handoff?* It should **not** be read as seed promotion (씨앗 승격) or hypothesis confirmation (가설 확정).

**Rejected (거절):** “repair once more before MT5 (MT5 전 한 번 더 수리)” as the default path. F71C already was repair/recombine (수리/재조합); another repair pass is **discovery (탐색)**, while stage rule says runtime probe is **transfer check (전이 확인)** before closeout (단계 마감). With 0 meaningful candidates everywhere, more proxy repair mostly risks **selection churn (선택 흔들림)** without fixing the core gap: **nothing cleared the meaningful bar in proxy (프록시에서 의미 후보 기준 미통과)**.

**needs_local_verification (로컬 검증 필요)** — execution only, not target choice:
- materialization identity (물질화 정체성): label / feature_set / model / selection / gap bars
- MT5 tester parity (테스터 동등성): spread, commission, slippage, modeling mode
- whether `density_lift_fracture_pass` (밀도 상승 균열 통과) maps to the same runtime gates Codex will observe

I cannot verify those from this prompt alone.

---

## 2. Recommended probe target (권장 탐침 대상) and fallback (대체 대상)

| Role | Candidate | Why |
|------|-----------|-----|
| **Primary (1차)** | **`f71b_1e511d3db9c3`** | Best joint scout signal in the bounded table: **scout_clue=True**, **density_lift_fracture_pass=True**, highest **validation/OOS PF (~1.23 / ~1.25)**, lowest **DD among strong rows (~2.6% / ~3.5%)**. Closest to F71’s “density + PF + DD together (밀도·PF·DD 동시 보존)” test at ~**1.3 trades/day (일 거래 약 1.3)**. |
| **Fallback (2차)** | **`f71c_d269d8fe1b47`** | Best **density leg (밀도 축)** in F71C (~**1.83 trades/day**), still **scout_clue=True**, but **fracture fail** and **weaker PF (~1.14 / ~1.15)**. Use only if you run a **two-lane probe (두 갈래 탐침)** or need a deliberate **density-vs-PF tradeoff transfer test (밀도 대 PF 전이 대조)**. |

**Single-slot probe (탐침 1슬롯만):** probe **F71B primary only**. Do **not** spend the first MT5 slot on F71C top unless the explicit question is “did repair density transfer despite fracture failure? (수리 밀도가 균열 실패에도 전이됐는가?)”

**Optional within-lane fallback (같은 레인 내 대체):** `f71b_edaf9fba5281` — also fracture-pass, similar stack, but **worse OOS PF (~1.15)** than `f71b_1e511d3db9c3`. Prefer only if primary materialization is blocked.

**Two-lane probe (두 갈래 탐침):** **accepted as stretch, not required.** If budget allows exactly two runs: **F71B `f71b_1e511d3db9c3` + F71C `f71c_d269d8fe1b47`**. That separates **PF/DD/fracture transfer (PF·DD·균열 전이)** from **density-first repair transfer (밀도 우선 수리 전이)** without pretending either is a meaningful winner.

---

## 3. Key risks (핵심 위험)

**Proxy/runtime gap (프록시/런타임 간극)** — **Highest.** Entire surface has **0 meaningful candidates**. Proxy PF ~1.25 and positive OOS profit are **thin margins**; spread, commission, slippage, fill timing, and `vol_expansion_q45` threshold behavior can erase edge in MT5 even when Python proxy looked “scout-positive.”

**Density collapse (밀도 붕괴)** — **High for F71B primary.** ~1.3 trades/day is already modest; vol-expansion gating often **compresses entries further** at runtime. F71C’s ~1.83/day is the density stress test, but it **failed fracture** — so high proxy density may **not** mean healthy joint surface.

**PF fragility (수익 팩터 취약성)** — **High.** PF ~1.23–1.25 (F71B) and ~1.14–1.15 (F71C) are **not robust buffers**. Small execution drag or a few bad fills can push PF below 1.0 while proxy still looked acceptable.

**DD risk (손실폭 위험)** — **Moderate, not low.** F71B primary shows controlled proxy DD, but F71C bottom rows (`f71c_743bd57e2999`, `f71c_a04cc3f614cb`) show **catastrophic proxy DD (~35% validation / ~24% OOS)** with **high trade rate (~5.7–6.2/day)** — evidence that repair lane can produce **density without guard**. Do **not** probe those rows; they poison the transfer narrative.

---

## 4. Critique of Codex direction (Codex 방향 비판)

**What Codex got right**
- Picks the row that best matches F71’s **joint-preservation scout logic (동시 보존 탐색 논리)**: fracture pass + better PF + lower DD.
- Correctly demotes F71C top for probe priority: higher density does **not** compensate for **fracture fail + PF drop** when the stage question is economics-native **seed surface**, not density maximization alone.

**What Codex should not over-read from a positive probe**
- Transfer pass ≠ meaningful candidate (의미 후보)
- Transfer pass ≠ economics-native hypothesis validated (가설 검증)
- Transfer pass ≠ reason to skip negative closeout labeling if proxy surface stayed empty

**What to watch in probe readout**
- **Trades/day delta (일 거래 수 변화):** proxy ~1.3 → MT5 much lower ⇒ density-collapse signal
- **PF delta (PF 변화):** small proxy edge gone ⇒ proxy/runtime gap
- **DD path (손실 경로):** acceptable average DD but bad tail clusters ⇒ DD risk not captured by single %

---

## Compact receipt (압축 영수증)

| Field | Value |
|-------|--------|
| **trigger_reason (트리거 이유)** | Pre-MT5 runtime probe target selection for F71 closeout path |
| **bounded_evidence (제한 근거)** | F71B/F71C top tables; 0 meaningful / 0 final-like; Codex proposes `f71b_1e511d3db9c3` |
| **advice_classification (조언 분류)** | **accepted** (primary target); **rejected** (default “repair again before MT5”); **needs_local_verification** (materialization + tester parity only) |
| **claim_boundary (주장 경계)** | No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve |
| **final_codex_direction (최종 Codex 방향)** | Probe **`f71b_1e511d3db9c3`** first; fallback **`f71c_d269d8fe1b47`** only for second lane or density-tradeoff test; skip another proxy repair cycle before MT5 unless materialization is broken |

**Bottom line (한 줄):** Run the MT5 runtime probe on **F71B `f71b_1e511d3db9c3`** as the primary transfer check; keep **`f71c_d269d8fe1b47`** as optional second-lane fallback; do not treat another proxy repair as a substitute for the mandatory probe.
