Pre-MT5 Grok review 요청이므로 협업 스킬과 단계 근거를 먼저 확인한 뒤, bounded evidence만으로 판단하겠습니다.
# Frontier61 Pre-MT5 Review — External Second Opinion(외부 2차 의견)

**Verdict(판정): `accepted`**

Codex should **proceed with the one pre-registered MT5 runtime probe** as **exploration-only `runtime_probe_observation`(탐색 전용 런타임 탐침 관찰)**. It should **not** close before MT5 as `negative` / `invalid` / `blocked` from this snapshot alone.

---

## Classification(분류)

| Item(항목) | Grok classification(그록 분류) |
|---|---|
| **Proceed with mandatory MT5 probe(필수 MT5 탐침 진행)** | **`accepted`** |
| **Close before MT5 as negative/invalid/blocked(MT5 전 부정/무효/차단 마감)** | **`rejected`** |
| **Additional local checks before probe(탐침 전 추가 로컬 검증)** | **`needs_local_verification` not required** for this go/no-go — snapshot says Codex already completed pre-materialization checks; **post-probe** MT5 rows still need local verification |

---

## Why `accepted` — proceed(진행 수용)

1. **Pre-registered contract(사전 등록 계약)** says exactly **one** MT5 runtime probe runs **before** repair or closeout. Skipping MT5 now breaks that contract, not fulfills it.
2. **Selection rule(선택 규칙)** is **train-first**(학습 우선): `train density → train PF → train DD → read-only forward balance`. The frozen candidate already records `forward_dual_positive_flag=false` and `forward_density_target_flag=false`. Those are **known forward weaknesses**, not surprise disqualifiers at probe time.
3. **Stop criteria(중단 기준)** in the snapshot apply **after** MT5 (`runtime PF<1`, `DD≥10`, `density outside 5–10/day`). They are **closeout judgment**, not a pre-MT5 skip gate.
4. **Failure-mode read(실패 모드 판독)** treats F53–F59 as **alpha/economics failure** with mostly `signal_diff=0`. F61’s discriminating evidence is **MT5 PF under the new 3-class target**, not proxy polish. Closing pre-MT5 leaves that question unanswered.
5. **Claim boundary(주장 경계)** is already tight: `runtime_probe_observation` only — no promotion, authority, baseline, or Goal Achieve. Weak proxy forward metrics do not make the probe **invalid**; they define what is being observed.
6. **ONNX parity passed(온엑스 동등성 통과)** — handoff preflight for this candidate is done; the remaining unknown is runtime economics, which is exactly what the probe is for.

---

## Why `rejected` — close before MT5(사전 마감 거절)

| Proposed early close(조기 마감 제안) | Why rejected(거절 이유) |
|---|---|
| `negative` because validation PF=0.9798 | Borderline proxy weakness under a **train-first** selection rule is not the registered pre-MT5 stop trigger |
| `invalid` because density 4.78/day &lt; 5 | Close to band edge (~0.22/day short); proxy density ≠ MT5 density until measured |
| `blocked` because forward flags are false | Flags document risk; they were **expected** at freeze time per selection_rule |

Early close would **substitute proxy forward weakness for the mandatory runtime observation** and forfeit the stage’s one allowed discriminating test.

---

## Concrete risks only(구체적 리스크만)

| Risk(리스크) | Why it matters(왜 중요한지) |
|---|---|
| **Validation PF already &lt; 1** | `forward_min_pf=0.9798`; MT5 may track validation, not OOS (`1.1169`) |
| **Density below target band(밀도 목표 밴드 미달)** | `forward_min_density=4.78/day` vs `5–10/day`; MT5 spread/fill/admission may compress further |
| **Train–forward divergence(학습–전진 괴리)** | Train PF `1.30` vs validation `0.98` — threshold/grid luck or overfit may not survive runtime |
| **Relabeling, same features(재라벨링, 동일 피처)** | Same 58-feature contract failed on short-only and long-only targets; 3-class head may repackage weak signal |
| **High entry suppression(높은 진입 억제)** | Validation `entry_suppression_count=1392` on `2269` signals — density/PF sensitive to runtime admission |
| **Proxy envelope optimism(프록시 봉투 낙관)** | ATR SL/TP + `max_hold=4` offline may diverge under MT5 friction even with `signal_diff≈0` history |
| **Single-shot probe(단일 탐침)** | One candidate, no repair before first MT5 — negative runtime likely ends as `negative_memory`, not a second chance |
| **Tier B gap(티어 B 공백)** | `missing_required` — no partial-context read on this packet; Tier A-only observation |

---

## Bottom line(요약)

**Proceed with MT5** as `runtime_probe_observation`. Treat weak forward proxy metrics as **risk flags inside the observation**, not as permission to skip the probe. **Judge closeout only after MT5** against the pre-registered stop criteria. No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve is implied.
