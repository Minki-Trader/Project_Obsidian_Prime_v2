Grok 외부 2차 의견으로 Frontier07 마감안을 검토합니다. 먼저 협업 스킬과 제한 근거 파일을 읽고 로컬로 대조하겠습니다.
해시와 strict/preserved 행 수를 로컬로 대조해 Codex 제안 마감안의 사실 근거를 확인합니다.
## 1. Recommendation(권고)

**`close_preserved_clue_negative_memory(보존 단서+부정 기억 마감)`**

Codex should close Frontier07(전선07) now. Do **not** run another repair(추가 수리) inside this stage, and do **not** mark invalid/blocked(무효/차단).

---

## 2. Reasoning(근거)

**Evidence chain is complete(근거 사슬이 닫혔음).**
F07A(전선07A) opened a bounded hypothesis(제한 가설). F07B(전선07B) ran the planned broad scout(넓은 탐색): 4 label families(라벨군) × 3 variants(변형), fixed `feature_set_v2`, argmax-only, ONNX-exportable models. F07C(전선07C) ran the planned capped repair(상한 수리): top 4 preserved variants × 4 directional class-prior weights. That is enough exploration for a frontier closeout(전선 마감), not a blocked run(차단 실행).

**Strict scout gate(엄격 탐색 게이트) stayed at zero by design, not by accident.**
From the scout logic, strict clue(엄격 단서) needs all of these at once on **both** validation(검증) and OOS(표본밖):

- density band(밀도 구간): 5.0–10.0 trades/day
- PF floor(수익 팩터 하한): ≥ 1.2 with positive net profit
- DD soft ceiling(손실폭 상한): ≤ 15%
- parity(동등성) + learnability(학습 가능성) + improvement vs `label_v1` on PF, DD, and aspiration score

F07B and F07C reports and CSV summaries both show `strict_scout_clue_rows = 0`. That matches the bounded numbers Codex gave.

**There is a real preserved clue(보존 단서), but it is DD-skewed(손실폭 쏠림).**
Best F07B: `time_to_adverse_penalty` variant `f07b_time_to_adverse_penalty_v2_lt1p05_st1p05_lc0p70_sc0p70_q90__v08_lr_plain`

- validation(검증): PF 1.06855, density 3.11/day, DD 53.13%
- OOS(표본밖): PF 1.70687, density 1.37/day, DD 13.09%
- ONNX parity(온엑스 동등성): true
- vs `label_v1`: OOS DD ~41.6% → ~13.1%, OOS PF ~1.08 → ~1.71

So adverse-excursion risk-shaped labels(불리한 이동 위험 형성 라벨), especially **time-to-adverse penalty(불리 이동까지 시간 벌점)** and **side-asymmetric caps(방향 비대칭 상한)**, do show material OOS DD reduction(표본밖 손실폭 실질 감소) and OOS PF lift(표본밖 수익 팩터 상승) under argmax-only.

**Negative memory(부정 기억) is also real and should be recorded.**
The clue never satisfied the four-axis scout contract(네 축 탐색 계약) at the same time:

| Axis(축) | F07B best | F07C best repair |
|---|---|---|
| Validation PF(검증 수익 팩터) | 1.07 (< 1.2 floor) | 1.04 (< 1.2) |
| Validation DD(검증 손실폭) | 53.1% (>> 15%) | 58.9% (>> 15%) |
| Density band(밀도 구간) | 3.11 / 1.37 (under 5) | 5.71 / 4.12 (validation closer; OOS still under 5) |

F07C did what it was meant to do: bridge density(밀도 브리지) without threshold search(임계값 탐색). It raised validation density for some repairs, but still produced **0 strict rows**, and the best repair **gave back OOS PF** versus F07B best (1.71 → 1.18) while validation DD stayed very high. That is a useful negative result(유용한 부정 결과), not a reason to keep repairing inside the same knob(같은 조절축).

**Why not `repair_once_more(한 번 더 수리)`?**
Another class-prior sweep(클래스 사전분포 추가 스윕) would repeat F07C’s capped repair lane(상한 수리 레인). Threshold or abstention repair(임계값/기권 수리) would drift back toward Frontier06(전선06), which F07A explicitly avoided. The stage already answered its core question(핵심 질문): *can risk-shaped labels improve DD utility under argmax-only without reopening threshold grids?* Answer: **partial yes on OOS DD/PF, no on strict scout readiness.**

**Why not `invalid_or_blocked(무효/차단)`?**
Runs completed, learnability passed, ONNX parity passed, artifacts and reports exist. This is a **valid negative/partial-positive exploration closeout(유효한 부분 긍정 탐색 마감)**, not broken execution(실행 고장).

**No WFO/MT5 is correct here.**
With `strict_scout_clue_rows = 0`, expensive forward/runtime steps(비용 큰 전진/런타임 단계) should not open from this stage.

---

## 3. Required closeout wording(필수 마감 표현)

Codex should close Frontier07 as:

> **`closed_preserved_clue_with_negative_memory_no_authority`**
> **`judgment: preserved_clue_with_negative_memory(보존 단서+부정 기억)`**

**Preserved clue block(보존 단서 블록):**

- Adverse-excursion risk-shaped labels(불리한 이동 위험 형성 라벨), especially `time_to_adverse_penalty` and `side_asymmetric_caps`, produced **repeatable preserved-clue rows(반복 보존 단서 행)** under argmax-only with ONNX parity true.
- Relative to `label_v1` and prior frontier references, the strongest signal is **OOS DD reduction(표본밖 손실폭 감소)** with **OOS PF improvement(표본밖 수익 팩터 개선)** on the best F07B candidate.
- Label utility(라벨 효용) moved from event-first direction(이벤트 우선 방향) toward adverse-path survival grading(불리 경로 생존 점수화) with measurable OOS risk-shape benefit(측정 가능한 표본밖 위험 형상 이점).

**Negative memory block(부정 기억 블록):**

- `strict_scout_clue_rows = 0` after F07B scout and F07C capped class-prior repair.
- No candidate met simultaneous density band + PF floor + validation DD soft ceiling + full `label_v1` improvement contract.
- Validation DD(검증 손실폭) remained very high throughout; argmax-only plain/balanced models stayed validation-DD-toxic(검증 손실폭 유독 높음) even when OOS DD improved.
- F07C density-bridge repair(밀도 브리지 수리) did not upgrade the stage to strict clue; it mainly traded OOS PF(표본밖 수익 팩터) for density movement(밀도 이동).
- Tier B / Tier A+B paired records(티어 B / 티어 A+B 쌍 기록): `missing_required(필수 누락)`.

**Closeout action line(마감 행동 문장):**

- Close Frontier07 as **reference, not inheritance(참조이지 상속 아님)**.
- Next work opens as a **new frontier hypothesis(새 전선 가설)**; do not carry winner, baseline, promotion, runtime authority, or live readiness forward.

---

## 4. Do-not-claim boundary(주장 금지 경계)

Codex must **not** claim:

- `completion(완성)`, `baseline(기준선)`, `promotion(승격)`, `promotion_candidate(승격 후보)` as operating truth
- `runtime_authority(런타임 권위)`, `runtime_probe success(런타임 탐침 성공)`, `live_readiness(실거래 준비)`, `Goal Achieve(목표 달성)`
- `strict_scout_clue(엄격 탐색 단서)` or “scout passed(탐색 통과)”
- WFO readiness(워크포워드 준비) or MT5 tester/runtime parity closure(메타트레이더5 테스터/런타임 동등성 마감) from this stage
- That F07C best repair supersedes F07B best as stage winner(단계 승자) — it is a **repair tradeoff row(수리 트레이드오프 행)**, not a promoted selection
- That OOS DD improvement alone proves deployable alpha(배포 가능 알파)
- Tier A-only alpha read(티어 A 단독 알파 판독) while Tier B / combined records remain missing
- That adverse-excursion labeling is dead(사망) — it is **preserved clue + negative memory(보존 단서+부정 기억)**, not idea death

**Allowed bounded carry-forward(허용되는 제한 이월):**

- Future frontiers may **reference(참조)** `time_to_adverse_penalty` and `side_asymmetric_caps` as DD-shaped label clues.
- Future work should treat F07C as proof that **class-prior weighting alone(클래스 사전분포 가중치만으로는)** insufficient for strict scout under current scout floors.
- Any re-open needs a **new hypothesis packet(새 가설 묶음)** — e.g. different signal contract, model family, split/feature contract, or explicit threshold lane — not another F07C-weight sweep.

---

**Grok classification for Codex(코덱스용 그록 분류):** `accepted(수용)` on closeout direction; `needs_local_verification(로컬 검증 필요)` only for final hash/register write during F07D closeout execution, not on the judgment itself.
