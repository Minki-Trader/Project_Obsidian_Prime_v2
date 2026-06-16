## F68D MT5 Runtime Probe — Grok critique(비판 검토)

**Claim boundary(주장 경계):** `scout/runtime_probe_observation(탐색/런타임 탐침 관찰)` only. No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

### 1. Run both eligible axes(두 적격 축 모두 실행)?

**accepted(수용)** — run both `f68b_23f4d4607a78`(density) and `f68b_3481a04983ee`(PF), not one.

- F68 question is **proxy philosophy vs runtime economics gap(프록시 철학 대 런타임 경제성 간극)**, not winner pick(승자 선택).
- The two axes are **deliberately incomparable on one score(한 점수로 비교 불가)**: both-side high-density vs long-only low-frequency; ATR SLTP off vs on; 59 vs 49 features; different threshold/margin surfaces.
- Four bounded tester attempts(4회 한정 탐침) materialize **split-axis proxy/runtime KPI gap(분리 축 간극)** — the stated F68D effect.
- Picking one now would **collapse the experiment(실험 붕괴)** before measuring whether lifecycle/cost/DD-aware proxy aligns with MT5 on *each* economic profile.
- Axis 3 is already **out of scope(범위 밖)** (HGB failed); that is not a reason to drop either eligible axis.

---

### 2. Local verification(로컬 검증) before tester execution(테스터 실행 전)

**needs_local_verification(로컬 검증 필요)** — Codex must confirm locally; Grok cannot verify.

| Check | Why |
|--------|-----|
| ONNX SHA256(온엑스 해시) | `5fb01508…` / `167e99f1…` on disk match snapshot before Common Files copy |
| Feature count/hash(피처 수/해시) | `59/b33f5586…` and `49/14a037f1…` CSV identity matches materialization |
| Handoff paths(인계 경로) | ONNX + feature CSV land in **Common Files** paths the EA actually reads |
| Per-axis `.set`/`.ini`(축별 설정) | Thresholds, margins, hold bars, cooldown, long_only/both, ATR SLTP **exactly** match decision block above |
| EA identity( EA 정체성) | Reuse `ObsidianPrimeV2_RuntimeProbeEA.mq5` only — no clone, no drift |
| Compile(컴파일) | MetaEditor compile succeeds before any tester run |
| Date windows(기간) | validation `2025.01.02–2025.10.01`, OOS `2025.10.01–2026.04.14` align with proxy splits |
| Signal parity baseline(신호 동등성 기준) | Prior `0/0` ONNX signal diff is handoff input; record Python-side signal counts per window for runtime compare |
| Axis 3 exclusion(3번 축 제외) | `f68b_547ac8b4ead1` not in probe queue |
| Tester accounting settings(테스터 회계 설정) | Spread, commission, slippage, symbol contract documented per attempt — same across 4 runs unless axis-specific by design |

**accepted(수용):** block with **blocked reason + repair action(차단 사유 + 수리 행동)**, not “comparison impossible.”

---

### 3. Gap causes(간극 원인) to separate in F68D report(보고서)

**accepted(수용)** — report must **tag each gap(간극별 태그)**, not blend into one “MT5 bad/good” verdict.

- **Proxy saturation vs runtime PF(프록시 포화 vs 런타임 PF):** PF axis proxy `99` is ceiling(상한), not runtime expectation — separate from tester PF.
- **Trade density / cost sensitivity(거래 밀도/비용 민감도):** ~7–9 trades/day vs ~1/day — spread/commission/slippage impact differs by axis.
- **Lifecycle exit mechanics(생명주기 청산):** max_hold `2` vs `6`, cooldown `1` vs `0`, ATR SLTP disabled vs `1.0/1.5`.
- **Directionality(방향성):** both vs long_only — short-side economics and signal count parity.
- **Decision surface(의사결정면):** near-zero thresholds + tight margin vs high short_threshold + wide margin — signal count vs execution filter gap.
- **Feature readiness(피처 준비):** 59 vs 49 features — missing/stale feature parity in MT5 vs Python.
- **ONNX inference vs execution(추론 vs 실행):** signal parity `0/0` vs runtime signal/trade count — separate inference, gating, and fill layers.
- **Accounting / trade shape(회계/거래 형태):** gross P/L, avg win/loss, payoff, expectancy, long/short breakdown vs proxy net/PF/DD%.
- **DD methodology(손실폭 측정):** proxy DD% (~12% vs `0.0`) vs tester DD — don’t merge definitions.
- **Split isolation(분할 격리):** validation and OOS gaps reported **per axis per window**, not pooled “overall winner” KPI.

---

### 4. Advice Codex should reject as out of boundary(경계 밖 조언 거절)

**rejected(거절)** for this run:

- Picking a **winner(승자)** or **selected baseline(선택 기준선)** from 4 tester attempts.
- **Operating promotion(운영 승격)**, **runtime authority(런타임 권위)**, **live readiness(실거래 준비)**, or **Goal Achieve(목표 달성)** from probe output.
- Treating proxy PF=`99` or OOS uplift as **MT5 success criterion(성공 기준)**.
- **Threshold/parameter retuning(임계값 재조정)** from tester results inside F68D (changes the experiment).
- Skipping one eligible axis for “efficiency” or because axis 3 failed.
- Claiming F68 hypothesis **validated/rejected(가설 확정)** from probe alone.
- Equating prior **ONNX signal parity pass(신호 동등성 통과)** with runtime authority.
- Using F68D to **fix HGB export(3번 축 수리)** or merge axis 3 into the same completion claim.
- **Promotion-ineligible(승격 부적격)** or **idea-dead(아이디어 사망)** labels from a single scout probe.
- Any **“deploy / trade live / replace F67”** narrative from economics-gap observation only.

**accepted(수용)** within boundary: materialize both axes, record proxy/runtime/signal/feature/accounting gaps, preserve clues, label **blocked** with repair path if tester fails.

---

### Summary framing(요약)

| Item | Classification |
|------|----------------|
| Run both eligible axes, 4 tester attempts | **accepted** |
| Pre-tester identity/handoff/compile/window checks | **needs_local_verification** |
| Separate gap-cause taxonomy in report | **accepted** |
| Winner, baseline, promotion, runtime authority, live, Goal Achieve | **rejected** |

**Final Codex direction(최종 Codex 방향):** Proceed with **both-axis, four-window runtime probe(양축 4창 탐침)**; verify handoff identity locally first; report **labeled gaps only(라벨된 간극만)** — no elevation beyond scout observation.
