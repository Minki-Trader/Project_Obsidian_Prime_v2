# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier53_stage_open_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
Grok 외부 2차 의견 역할로 F53 단계 개방 검토를 진행합니다. 협업 스킬과 관련 맥락을 먼저 확인합니다.
# Grok External Review — Frontier 53 Stage-Open (소규모)

**Review size:** small
**Claim boundary:** critique only — no completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성)

---

## Receipt (영수증)

| Field | Value |
|---|---|
| Trigger | F53 stage-open direction critique |
| Bounded evidence | User-supplied scout proxy metrics + F52 close memory |
| Forbidden-claim check | No operating claims made below |

---

## Q1. Is F53 direction valid as new PF source search(수익 팩터 원천 탐색), not F52 lifecycle repair repeat(생명주기 수리 반복)?

### **Accepted (수용)**

F53 is **directionally valid** as a distinct PF-source search, not a repeat of F52 lifecycle-only repair.

**Why this holds:**

1. **Mechanism shift is real.** F52 negative memory(부정 기억) says post-entry lifecycle tightening(생명주기 조임) killed PF/economics. F53 moves the lever to **pre-entry selection(진입 전 선택)** — a short-only path-quality classifier(숏 전용 경로 품질 분류기) trained on train-only MFE/MAE/horizon labels. That is a new hypothesis axis, not another cooldown/entry-transition pass.

2. **Frontier discipline is correct.** Raw 58 contract features(계약 피처), no prior winner(승자)/baseline(기준선) import, train-only label construction, and score-quantile gating on train — these match `reference, not inheritance(참조이지 상속 아님)`.

3. **F52 clue is used as constraint, not as the search object.** Keeping ATR SL/TP + DD memory while dropping entry-transition-only suppression(진입 전환 전용 억제) unless locally justified is the right split: preserve risk envelope(리스크 봉투), stop trading economics for DD compression alone.

### **Needs_local_verification (로컬 검증 필요)**

1. **Scout PF is razor-thin.** Best dual-positive proxy(양쪽 전진 구간 PF 양수) is validation_is PF≈1.002 and OOS PF≈1.096. That is exploration-legal(탐색 허용) but **not yet evidence of a durable PF source(지속 PF 원천)** — it may be noise, spread-thin edge, or quantile overfit.

2. **Hidden lifecycle tightening risk.** `score_q=0.90–0.93` cuts density sharply (5–10 trades/day). If PF gain comes mostly from **fewer entries** rather than **better path quality per entry**, F53 could accidentally repeat F52’s economics failure in classifier clothing. Codex should decompose: PF lift from win-rate vs trade-count reduction.

3. **Label–eval mismatch.** Labels use horizon_pnl>0; evaluation uses path-native first-hit SL/TP proxy(경로 기반 선도달 손절/익절 프록시). Local verification must confirm the classifier is learning entry quality that survives the eval exit rule, not horizon-specific artifacts.

### **Rejected (거절)**

- **Reject** treating current scout numbers as “F53 already has PF edge.” They are **weak dual-positive proxy only**, not validated PF source closure.

---

## Q2. First MT5 runtime probe(런타임 탐침) candidate and main failure mode(주요 실패 양상)?

### **Accepted (수용) — first probe candidate**

Send **one** representative narrow candidate:

> **logreg_l2_c05 | short | stop_q=0.25 | take_q=0.70 | score_q=0.90**

**Why this one first:**

| Criterion | logreg 0.90 | logreg 0.93 | ExtraTrees 0.85 |
|---|---|---|---|
| Dual-positive proxy | Yes (val 1.002, OOS 1.096) | Yes, weaker val PF | Yes |
| DD vs F52 clue (<10%) | 7.96% / 7.35% | 5.93% / 7.79% | **10.85%** val — breaches clue |
| Runtime parity tractability | **High** (linear, exportable) | High | Lower (tree ensemble) |
| Density for signal observation | 7.26 / 10.24 per day | Thinner (5.09 / 7.84) | Moderate |
| Hypothesis representativeness | Core F53 design | More conservative filter variant | Different model family |

**Probe policy (accepted):**

- Keep **ATR SL/TP + maxhold DD envelope** from F52 preserved clue(보존 단서).
- **Remove F52 entry-transition-only suppression** for this first probe unless local pre-probe justification exists.
- F52 MT5 already showed massive `signal_diff` under entry-transition blocking; F53’s whole point is whether **better entries** can replace that suppression. Testing with suppression still on would confound the PF-source question.

### **Needs_local_verification (로컬 검증 필요)**

- Whether logreg 0.90 remains best after **full label-hash, feature-hash, split-boundary, and Tier A/B ledger** checks — scout table alone is not enough to freeze artifact identity.
- Whether 0.93 should be probe #2 **only if** probe #1 shows runtime over-churn (과다 회전), not as the opening representative.

### **Rejected (거절)**

- **Reject ExtraTrees depth6 score_q=0.85 as first probe** — validation_is DD=10.85% violates the F52 DD preservation clue you intend to carry forward.
- **Reject multi-candidate MT5 sweep at stage-open** — one narrow probe is correct; more would blur failure attribution.

### **Main failure mode to watch (accepted framing)**

**Primary:** **proxy-to-runtime economics collapse(프록시→런타임 경제성 붕괴)**

F52 precedent is stark: reference MT5 probe showed validation_is PF≈0.41 / OOS PF≈0.66 with large negative `signal_diff` under lifecycle policy. F53 scout proxy PF≈1.00–1.10 can easily fall below 1.0 in MT5 once spread, commission, bar-open timing, and ATR SL/TP path differ from Python first-hit proxy.

**Watch in this order:**

1. **PF evaporation** — proxy PF ~1.00 becomes MT5 PF <1.0 with same candidate identity.
2. **Entry-count divergence** — without entry-transition block, trade count may **exceed** proxy density; economics worsen via churn.
3. **Exit-path divergence** — first-hit proxy vs MT5 ATR SL/TP + maxhold changes win/loss mix even when entries match.
4. **Quantile transfer failure** — train score_q=0.90 gate selects well in-sample but passes marginal shorts OOS.
5. **False DD success** — DD stays <10% only because runtime trades too few to matter (density collapse disguised as risk control).

**Telemetry must separate:** `feature_ready_diff`, `signal_diff`, `entry_count`, `blocked_by_score_gate`, `blocked_by_runtime_policy` — otherwise you cannot tell PF failure from parity failure.

---

## Q3. Bounded guidance summary

| Item | Classification |
|---|---|
| F53 as new PF source search vs F52 lifecycle repeat | **Accepted** — valid stage-open direction |
| Scout proxy = PF edge found | **Rejected** — too weak; not closure evidence |
| Decompose PF lift (quality vs density) before stronger claims | **Needs_local_verification** |
| First MT5 probe: logreg_l2_c05, stop_q=0.25, take_q=0.70, score_q=0.90 | **Accepted** |
| Drop entry-transition-only suppression on first probe | **Accepted** |
| Keep ATR SL/TP + DD envelope from F52 clue | **Accepted** |
| ExtraTrees 0.85 as first probe | **Rejected** |
| Primary failure mode: proxy→runtime PF collapse + entry-count/exit-path divergence | **Accepted** |

---

## Adversarial note (비판 검토 한 줄)

F53 is **the right question** after F52, but the scout snapshot reads like **“barely positive after heavy gating.”** Stage-open is justified; **PF-source discovery is not.** Treat F53 as exploration until MT5 probe proves the classifier adds economics that lifecycle policy could not — not until proxy PF crosses an arbitrary 1.05 line.

**Codex next action (guidance only, not execution):** open F53 with hypothesis doc + ledger row, run local verification on label/proxy parity checklist, then one logreg 0.90 runtime probe with F52 DD policy minus entry-transition suppression, and judge with `runtime_probe_observation_no_authority` boundary intact.
