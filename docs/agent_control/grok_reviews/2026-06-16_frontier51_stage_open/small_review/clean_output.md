F51 개방 검토를 외부 2차 의견으로 답하려면, 먼저 관련 스킬과 F50·F51 근거를 확인합니다.
## Frontier51 Stage-Open Review — External Second Opinion(외부 2차 의견)

**Review size(검토 크기):** small review(소규모 검토)
**Verdict(판정):** **`accepted`** — stage open(단계 개방) with execution guardrails(실행 보호선)

---

### 1) Distinct stage hypothesis after F50(충분히 독립된 단계 가설)?

**`accepted`**

- F50 primary lever(주 레버) was **loss-floor regime transfer(손실 하한 체제 전이)**; F51 shifts to **outcome-memory recurrence(결과 기억 재발)** with different event families (`good_recurrence`, `bad_to_good_recovery`, `decay_memory` vs F50’s `loss_floor_transfer`).
- F51 adds what F50 negative memory(부정 기억) demanded: **single-position order-path compression proxy(단일 포지션 주문 경로 압축 프록시)** before MT5 handoff(인계). That is a real **validation philosophy(검증 철학)** change, not a rerun.
- Shared MFE/MAE decay scaffolding(공유 감쇠 골격) is reference reuse(참조 재사용), not winner/baseline inheritance(승자/기준선 상속).

**Caveat(주의):** same short-PF campaign lane(숏 PF 캠페인 축) — novelty(신규성) is narrow but sufficient for a new frontier stage(새 전선 단계).

---

### 2) Leakage / overfit / grid-drift risks(누수/과최적화/격자 쏠림)?

**`needs_local_verification`** (guardrails look right; execution must prove them)

| Risk(위험) | Flag(표시) | Reason(이유) |
|---|---|---|
| Outcome-memory leakage(결과 기억 누수) | verify at run(실행 시 확인) | `horizon+1` embargo(유예) on shifted known outcomes(시프트된 확정 결과) is declared; `past_outcome_embargo_join_audit` must pass in Run B/C. |
| Order-path proxy fidelity(주문 경로 프록시 충실도) | verify at MT5 probe(MT5 탐침 시 확인) | F50 showed clean signal parity(신호 동등성) but DD/trade collapse(손실폭/거래 붕괴). Python `single_position_order_path_mask` is better than first-hit, but **proxy≠MT5** until probe records gap(차이). |
| Grid drift(격자 쏠림) | moderate watch(중간 주의) | Repair cap(수리 상한) is scoped correctly, but repair expands to **90 candidates**, extra event variants(추가 이벤트 변형), and wider base-scorer quantiles(0.82–0.88). Keep repair inside stated boundary(명시 경계 내). |
| Train-only overfit(학습 전용 과최적화) | low if lock holds(잠금 유지 시 낮음) | Train-split-only thresholds(학습 분할 전용 임계값) + read-only val/OOS(읽기 전용 검증/표본외) are correct; scout/seed thresholds must not become hidden selection feedback(숨은 선택 피드백). |

**Accepted guardrails(수용된 보호선):** train-only construction lock(학습 전용 구성 잠금), capped repair scope(상한 수리 범위), mandatory MT5 runtime probe(필수 MT5 런타임 탐침).

---

### 3) Claim boundary(주장 경계)?

**`accepted`**

- Scope(범위) correctly limits to **scout clue(탐색 단서) / seed surface(씨앗 표면) / runtime probe observation(런타임 탐침 관찰)** only.
- No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) — aligned with F50 closeout(마감) and frontier governance(전선 운영 규칙).
- Mandatory MT5 probe(필수 MT5 탐침) framed as **proxy/runtime gap recording(프록시/런타임 차이 기록)**, not authority closure(권위 종료).

---

### Summary(요약)

| Criterion(기준) | Classification(분류) |
|---|---|
| Distinct hypothesis(독립 가설) | **`accepted`** |
| Leakage/overfit/grid-drift(누수/과최적화/격자 쏠림) | **`needs_local_verification`** |
| Claim boundary(주장 경계) | **`accepted`** |
| **Stage-open(단계 개방)** | **`accepted`** |

**Effect(효과):** F51 may open(개방 가능). Run B/C must verify embargo audit(유예 감사) and order-path keep-rate(유지율) before scout selection(탐색 선택); Run Z must record proxy/runtime gap(프록시/런타임 차이) regardless of scout positivity(탐색 양성 여부와 무관).
