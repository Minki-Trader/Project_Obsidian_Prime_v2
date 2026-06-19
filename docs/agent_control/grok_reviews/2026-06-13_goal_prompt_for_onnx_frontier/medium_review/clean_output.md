Grok 검토 요청이므로 협업 스킬과 ONNX·프론티어 관련 맥락을 먼저 확인한 뒤, 직관적인 목표 프롬프트 초안을 제안하겠습니다.
# Grok Review — Intuitive ONNX Frontier Goal Prompt

**Review size:** small review (소규모 검토)
**Role:** external second opinion (외부 2차 의견) only — Codex owns direction, verification, claim boundary
**Claim boundary:** consulting only — no training, MT5, baseline, promotion, runtime authority, live readiness, Goal Achieve

---

## 한 줄 결론

Codex 5-part draft(5부분 초안)는 **accepted(수용)**.
사용자용 목표 프롬프트는 **“북극성 + 계속 밀기 + 가짜 완료 금지”** 세 덩어리만 기억하면 된다.
proof ladder(증명 사다리)와 claim label(주장 라벨)은 프롬프트 **안에 짧게** 넣되, 절차 이름은 빼는 편이 낫다.

---

## 1. Recommended user-facing goal prompt (권장 사용자용 목표 프롬프트)

```text
# ONNX Frontier North Star (ONNX 프론티어 북극성)

목표는 US100 M5에서 진짜 좋은 ONNX 하나다.
완성 기준은 네 가지다: 하루 5–10회 거래, PF 2–3배, 확대·검사한 모든 구간에서 손실폭 10% 미만, 매끄럽게 우상향하는 잔고/자산 곡선.
이 네 가지는 최종 완성 검토에서만 강제 게이트다. 탐색 초반에는 “목표에서 얼마나 가까운가”만 본다.

# How We Work (운영 방식)

하나의 frontier stage = 하나의 가설 생명주기다.
가설 → 프록시 탐색 → WFO/스트레스 → 런타임 검증 → 수리(상한 있음) → 마감.
한 가설이 닫히기 전까지 Codex는 실험을 멈추지 않는다. 닫힐 때는 완성, 보존 단서, 또는 부정 기억 중 하나로 정직하게 닫는다.
다음 frontier stage는 새 가설로 시작한다.

Stage12–364는 참조만 한다. reference, not inheritance(참조이지 상속 아님).
승자, 기준선, 승격, 런타임 권위, 실거래 준비는 가져오지 않는다.

# Grok Collaboration (그록 협업)

Codex가 실행한다. Grok는 2차 의견이다.
Grok 검토 시점: stage open(단계 개방), 비싼 WFO/MT5 전, stage closeout(단계 마감).
Grok 조언은 자동 실행되지 않는다. Codex가 로컬 검증 후 반영한다.

# Claim Boundary (주장 경계)

중간에는 scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), completion candidate(완성 후보)까지만 말한다.
“완성”, “기준선”, “승격”, “런타임 권위”, “실거래 준비”, Goal Achieve(목표 달성)는
전체 근거 층 + 구간 확장 스트레스 + MT5/parity + adversarial closeout(비판 마감)이 끝난 뒤에만 말한다.

# Keep Pushing (계속 밀기)

한 축만 좋으면 끝이 아니다. 네 축을 동시에 맞추는 후보만 앞으로 보낸다.
같은 수리를 반복하면 blocked(차단)로 닫고 다음 가설로 넘긴다.
목표에 도달할 때까지, 또는 더 이상 이 가설에 신규성이 없을 때까지 멈추지 않는다.
```

**왜 이 형태인가:** Codex 5-part를 그대로 유지하면서, 사용자가 외울 수 있는 **한 문장 북극성**과 **“언제 멈추는가”**가 바로 보인다.

---

## 2. Shorter variants (짧은 변형)

### One-line (한 줄)

```text
US100 M5용 진짜 좋은 ONNX(5–10회/일, PF 2–3x, 모든 검사 구간 DD<10%, 매끄러운 우상향)를 만든다 — 가설당 frontier stage 하나, archive는 참조만, 완성 주장은 전체 근거가 닫힐 때만.
```

### Slightly more operational (조금 더 운영형)

```text
# ONNX Frontier Operating Goal

NORTH STAR: excellent ONNX on US100 M5 — 5–10 trades/day, PF 2–3x, DD <10% on every inspected interval, smooth rising equity. Hard gate only at final completion review.

LOOP: one frontier stage = one hypothesis lifecycle (scout → WFO → MT5 → interval stress → capped repair → closeout). Then next hypothesis. Do not stop early on single-axis wins.

ARCHIVE: Stage12–364 = reference only. No winner, baseline, promotion, or runtime authority inheritance.

GROK: second opinion at stage open, before expensive WFO/MT5, and at closeout. Codex executes and verifies locally.

CLAIMS: mid labels only (scout clue / seed surface / runtime probe / completion candidate). Say “ONNX complete” or Goal Achieve only after full evidence stack + adversarial review.

PUSH RULE: keep experimenting within the same hypothesis until completion, preserved clue, negative memory, or blocked retry — never fake closure.
```

---

## 3. Words to avoid (피해야 할 단어)

| Avoid (피할 것) | Why (이유) |
|---|---|
| `Goal Achieve`, `완성됨`, `done`, `finished` | 최종 검토 전 가짜 종료를 만든다 |
| `baseline`, `selected baseline`, `winner`, `starting point` | archive 상속처럼 보인다 |
| `promotion`, `operating promotion`, `승격` | 운영 권위가 생긴 것처럼 들린다 |
| `runtime authority`, `live ready`, `실거래 준비` | MT5 한 번 본 것과 혼동된다 |
| `excellent ONNX` (중간 단계에서) | PF 하나 좋은 후보를 과장한다 |
| `proxy-positive`, `parity OK` alone | Python만 좋거나 동등성만으로 완성 주장이 된다 |
| `joint pass`, `one fold pass` as survival | Stage364식 “한 축만 통과” 착시 |
| `inherit`, `continue Stage364`, `hold4 as baseline` | reference-only 원칙 위반 |
| `good enough`, `close for now`, `ship it` | Pareto 핑계로 최종 4축을 약화시킨다 |
| `repair until it works` (무한) | 수리 루프를 숨긴다 — `capped repair(상한 있는 수리)`로 바꿀 것 |

**대신 쓸 말:** `aspiration distance(목표 거리)`, `scout clue`, `seed surface`, `completion candidate`, `negative memory(부정 기억)`, `reference only(참조 전용)`.

---

## 4. Minimal rules that must stay in the prompt (프롬프트에 남겨야 할 최소 규칙)

아래 **7개**만 있으면 혼란도, 과도한 절차화도 피할 수 있다.

1. **Fixed north star (고정 북극성):** 4 performance axes(성과 4축)는 약화하지 않는다.
2. **Late hard gate (늦은 강제 게이트):** 그 4축은 **final completion review(최종 완성 검토)**에서만 강제한다.
3. **Hypothesis unit (가설 단위):** one frontier stage = one hypothesis lifecycle.
4. **Honest close (정직한 마감):** 각 stage는 completion / preserved clue / negative memory / blocked 중 하나로 닫는다 — “그냥 다음으로” 금지.
5. **Reference-only archive (참조 전용 보관소):** prior stages는 clue와 DNR(반복 금지)만; authority(권위)는 가져오지 않는다.
6. **Claim ceiling (주장 상한):** 중간 라벨은 증거 수준만 말하고, 완성·승격·권위는 말하지 않는다.
7. **Push + Grok hook (밀기 + 그록 훅):** Codex는 끝까지 실험한다; Grok는 open / expensive gate / closeout에서만 비판한다.

**프롬프트에 넣지 말 것:** work packet 이름, gate audit 절차, register 경로, skill 이름 — 이건 Codex 운영 레이어에 두고, 목표 프롬프트는 **의도와 경계**만 담는다.

---

## 5. Advice classification (조언 분류)

| Item | Classification |
|---|---|
| Codex 5-part structure (target / loop / evidence / Grok / boundary) | **accepted** |
| Final 4-axis as completion-only hard gate | **accepted** (prior ONNX completion review와 일치) |
| One frontier stage = one hypothesis lifecycle | **accepted** (frontier stage scope review와 일치) |
| Grok at open / pre-WFO-MT5 / closeout only | **accepted** |
| Mid labels without completion language | **accepted** |
| “Keep pushing until excellent ONNX or honest negative close” | **accepted** |
| Putting full 11-layer evidence list inside user goal prompt | **rejected** — 너무 관료적; 운영 문서로 분리 |
| Putting PF 2–3 as scout cutoff in the prompt | **rejected** — sparse-PF 착시 유발 |
| Claiming 4-axis simultaneous hit is always feasible on US100 M5 | **needs_local_verification** — Pareto는 데이터로 봐야 함 |
| Exact prompt wording after user edits | **needs_local_verification** — 사용자 톤 선호에 맞게 한 번 다듬기 |

**Forbidden claim check:** operating promotion, runtime authority, live readiness, selected baseline, Goal Achieve — **not proposed by this review.** ✓

---

## Plain meaning (쉬운 말)

원하시는 건 **도구 목표 설정**이 아니라, 세션마다 붙여 넣을 **짧은 지휘 문장**이다.
그 문장은 “무엇을 최종적으로 원하는지”와 “중간에 무엇을 말하면 안 되는지”를 같이 잡아야 Codex가 실험을 끝까지 밀 수 있다.

가장 기억하기 쉬운 핵심은 이것이다.

> **앞에서는 넓게 탐색하고, 뒤에서 네 축을 동시에 확인한 뒤에만 “완성”이라고 말한다. 가설 하나가 닫힐 때까지 멈추지 않되, 가짜 완료는 하지 않는다.**

권장 본문(섹션 1)을 그대로 쓰거나, 한 줄 버전을 sticky note(메모)로 두고 본문은 운영형(섹션 2)으로 두면 된다.

---

*Grok consulting only. Codex should record classification in closeout if this feeds a work packet. No authority created.*
