## Classification(분류)

**`accepted_with_conditions`(조건부 수용)**

F76을 `preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음)`로 닫는 것은 제한 근거와 맞습니다. 다만 Codex는 마감 문서에 **proxy–MT5 gap(프록시–MT5 간극) 수치**, **F76F repair failure(수리 실패)**, **forbidden claims(금지 주장) 경계**를 그대로 남겨야 합니다.

---

## 1. Accepted / Rejected Advice(수용/거절 조언)

**Accepted(수용)**

- **Closeout label(마감 라벨)**: `preserved_clue_negative_memory_no_authority` — 적절합니다. F76은 축 식별(axis identification, 축 식별)과 간극 원인 명명(gap-cause naming, 간극 원인 명명)에는 기여했지만, 운영 권위(operating authority, 운영 권위)를 줄 근거는 없습니다.
- **Claim boundary(주장 경계)**: completion, baseline, promotion, runtime authority, live readiness, Goal Achieve 금지 — 올바릅니다.
- **Next pivot(다음 전환)**: F76B independent-signal proxy(독립 신호 프록시) 수리 반복 중단 → runtime-lifecycle-native label/target/trade-shape design(런타임 생명주기 기본 라벨/목표/거래 형태 설계) — F76E/F76F가 같은 패러다임 안에서 실패했으므로 타당합니다.
- **Gap cause acceptance(간극 원인 수용)**: `same_direction_hold_compression_after_signal_parity(신호 동등성 이후 동방향 보유 압축)` — signal/order/trade funnel(신호/주문/거래 깔때기)과 tpd collapse(일거래 붕괴)와 정합합니다.

**Rejected(거절)**

- F76B `f76b_06637`를 **promotion candidate(승격 후보)** 또는 **repair success(수리 성공)** 근거로 쓰는 것 — F76D에서 proxy 대비 MT5 net/tpd가 크게 괴리합니다.
- F76F dual-positive rows(양수 수리 행)를 **“수리 경로 열림(repair path open)”** 또는 **F76 완료(completion)** 근거로 쓰는 것 — `repair meaningful signal count = 0`, best repair OOS net 음수, dual-positive는 PF≈1.0대·낮은 net으로 F76B·MT5 gap을 메우지 못합니다.
- “Signal parity achieved(신호 동등성 달성) → runtime economics mostly solved(런타임 경제성 대부분 해결)” — hold compression(보유 압축)이 경제성을 지배합니다.

**Conditions for Codex(코덱스 조건)**

- 마감 시 F76B proxy KPI와 F76D MT5 KPI를 **나란히** 기록하고, “proxy strong / MT5 weak”를 한 문장으로 고정하세요.
- F76F dual-positive 행은 **exploratory marginal(탐색적 미미)** 로만 라벨링하고, F76 성공 지표로 승격하지 마세요.

---

## 2. Preserved Clue(보존 단서)

| Clue(단서) | Why keep(보존 이유) |
|---|---|
| **Axis ablation can rank proxy axes(축 절제로 프록시 축 순위 가능)** | F76B `f76b_06637`는 validation/OOS 모두 양의 proxy economics(프록시 경제성)를 보여, “어떤 축 조합이 프록시에서 강한가”라는 질문에는 답이 있습니다. |
| **Primary runtime gap cause(주 런타임 간극 원인)**: `same_direction_hold_compression_after_signal_parity` | 신호 수는 맞는데 order/trade와 tpd가 무너지는 패턴이 명확합니다 (예: val 194/100/50, tpd 1.06→0.18). |
| **Hold-state dominates economics(보유 상태가 경제성 지배)** | `max hold_same_direction share ≈ 0.75` — 독립 신호 프록시만으로는 설명·수리가 부족합니다. |
| **Funnel loss is structural(깔때기 손실은 구조적)** | signal→order→trade 단계 손실이 반복되면, density/threshold repair(밀도/임계값 수리)만으로는 부족할 수 있습니다. |

---

## 3. Negative Memory(부정 기억)

| Memory(기억) | Evidence(근거) |
|---|---|
| **Proxy–MT5 economics gap is order-of-magnitude(프록시–MT5 경제성 간극은 자릿수급)** | Val: proxy net 1760 vs MT5 152.99; OOS: 1471 vs 66.09. tpd도 ~5–6배 차이. |
| **Signal parity ≠ runtime parity(신호 동등성 ≠ 런타임 동등성)** | 신호 수는 맞지만 거래·수익 경제성은 크게 다릅니다. |
| **F76F lifecycle-aware density repair failed(생명주기 인식 밀도 수리 실패)** | 5120 rows, meaningful signal 0, density scout 0, completion-axis nearness 0; best repair OOS net -924, PF 0.88. |
| **Dual-positive repair is not a win(양수 수리가 승리 아님)** | PF≈1.0–1.04, 낮은 net, 높은 tpd(≈3+) — F76B·MT5 목표와 거리가 큽니다. |
| **Do not reopen F76 as “one more proxy sweep”(F76을 “프록시 스윕 한 번 더”로 재개하지 말 것)** | 같은 패러다임에서 수리 신호가 0입니다. |

---

## 4. Next-Stage Direction(다음 단계 방향)

**Primary(주 방향)**: runtime-lifecycle-native label/target/trade-shape design(런타임 생명주기 기본 라벨/목표/거래 형태 설계)

구체적으로:

1. **Label/target(라벨/목표)** — hold duration, re-entry, same-direction stacking(동방향 누적)을 반영한 목표 정의.
2. **Trade-shape(거래 형태)** — signal count가 아니라 **filled trade economics(체결 거래 경제성)** 기준 설계.
3. **Evaluation(평가)** — signal parity 다음 단계로 **order fill path(주문 체결 경로)**, **hold-state distribution(보유 상태 분포)**, **tpd under MT5 constraints(MT5 제약 하 일거래)** 를 1차 KPI로 둠.
4. **Explicit non-goal(명시적 비목표)** — F76B axis grid(축 그리드)나 F76F density repair(밀도 수리) 재개.

**Secondary carry-forward(보조 이관)**: F76B 축 조합은 “proxy-only reference(프록시 전용 참조)”로만 보관. MT5 probe(탐침) 전제 설계 입력으로 쓰지 않음.

---

## 5. Forbidden Claim Risk(금지 주장 위험)

| Risk(위험) | Why dangerous(위험 이유) | Guard(보호) |
|---|---|---|
| **Runtime authority / live readiness(런타임 권위/실거래 준비)** | MT5 OOS net 66, PF 1.47, tpd 0.19 — 실거래·권위 주장 불가. | “runtime probe only, no authority(런타임 탐침만, 권위 없음)” |
| **Baseline / promotion candidate(기준선/승격 후보)** | F76B proxy 강함 ≠ MT5 재현. F76F 수리 실패. | “proxy reference only(프록시 참조만)” |
| **Goal Achieve / completion(목표 달성/완성)** | 가설은 부분 답(간극 원인)만, 수리·경제성은 미해결. | “stage closed as clue/memory, not solved(단서/기억으로 마감, 미해결 아님)” |
| **“F76F dual-positive = repair path(양수 수리 = 수리 경로)”** | PF≈1, 낮은 net — 승격·기준선으로 오해 가능. | “marginal exploratory only(탐색적 미미만)” |
| **“Signal parity closes F76(신호 동등성으로 F76 종료)”** | hold compression이 경제성을 깨뜨림. | gap cause를 마감 요약 첫 줄에 둠 |

---

## Summary for Codex(코덱스 요약)

F76 마감은 **수용**합니다. 이 단계의 가치는 “runtime economics를 만드는 축을 찾았다”가 아니라 **“프록시가 강해도 MT5 경제성은 hold/lifecycle에서 깨진다”** 를 기록한 것입니다. 다음 단계는 프록시 수리가 아니라 **lifecycle-native 설계**로 피벗하는 것이 증거와 일치합니다.
