Frontier15 개방 검토를 위해 Grok 협업 스킬과 F14·F15 관련 근거를 먼저 확인합니다.
## Classification(분류)

**`accepted` (수용)** — bounded conditions(조건부 경계) 포함

---

## Review Answers(검토 답변)

### 1. Novelty delta(신규성 차이): F14(프론티어14)와 충분히 다름 — disguised micro-search(위장 미세 탐색)는 아님

**판정:** 신규성 차이는 충분합니다. F14 do-not-repeat(반복 금지) 위반으로 보이지 않습니다.

| 축(axis, 축) | F14(프론티어14) | F15(프론티어15) |
|---|---|---|
| Changed variable(변경 변수) | label-side opportunity budget(라벨 쪽 기회 예산) | runtime decision contract(런타임 결정 계약): argmax → score threshold |
| Failure mode(실패 양상) | label ~8/day, model ~0.07–0.10/day via argmax | same cliff(같은 절벽)을 **decision layer(결정 계층)** 에서 시험 |
| Banned repeat(금지 반복) | quota/flat repair, class-weight forcing, **threshold micro-search on this label family** | label family(라벨 계열) 미세 탐색이 아니라 **representation swap(표현 교체)** |

**쉬운 설명:** F14는 “라벨이 기회를 8회/일로 만들면 모델도 그만큼 거래할까?”를 봤고, argmax(최대확률)만으로는 밀도가 안 올라왔습니다. F15는 같은 라벨을 **통제(control, 통제)** 로 두고, “확률을 점수로 바꿔 임계값으로 밀도를 맞출 수 있나?”를 봅니다. `frontier_governance.md`의 opening condition(개방 조건)인 **runtime representation change(런타임 표현 변경)** 에 해당합니다.

**경계(boundary, 경계):** train-only density threshold fit(학습 전용 밀도 임계값 적합)은 threshold work(임계값 작업)입니다. 다만 3 score contracts × 3 density targets = **9개 사전 등록 셀**로 묶이면 micro-search(미세 탐색)가 아니라 **bounded grid(경계 있는 격자)** 입니다. val/OOS(검증/표본밖)에서 best contract(최고 계약)를 고르거나 grid(격자)를 늘리면 그때 disguised micro-search(위장 미세 탐색)가 됩니다.

---

### 2. Controls(통제): 누수 방지에 **거의 충분** — stage-open spec(단계 개방 명세)에 3가지 보강 필요

**현재 통제의 강점:**
- train-only threshold fit(학습 전용 임계값 적합), no val/OOS calibration(검증/표본밖 보정 없음)
- same Tier A / feature order / initial F14 labels(같은 티어 A·피처 순서·초기 F14 라벨)
- no quota/horizon retuning(할당량·보유기간 재조정 없음)
- failure if train thresholds do not transfer density(학습 임계값이 밀도를 전달 못 하면 실패) — honest falsifier(정직한 반증)

**남은 누수·선택 편향(selection bias, 선택 편향) 구멍:**

| Gap(구멍) | Required guard(필수 방어) |
|---|---|
| 9-cell implicit selection(9칸 암묵 선택) | **all 9 reported(9개 전부 보고)**; strict scout(엄격 탐색 단서)는 **pre-declared primary cell(사전 선언 1순위 셀)** 1개만 통과 기준으로 쓰거나, 9개 전부 pass(통과) 요구 |
| PnL-guided threshold pick(손익 기반 임계값 선택) | threshold fit(임계값 적합)은 **train probability scores + train calendar only(학습 확률 점수 + 학습 달력만)**; PF/net/DD로 threshold reorder(임계값 재정렬) 금지 |
| No argmax baseline(최대확률 기준선 없음) | every variant(모든 변형)에 **F14-matched argmax row(프론티어14 동일 최대확률 행)** 필수 — density cliff(밀도 절벽) 비교 없이는 novelty claim(신규성 주장)이 약함 |

이 3가지가 `00_spec/`에 들어가면 val/OOS leakage(검증/표본밖 누수) 방어는 F14 open precedent(프론티어14 개방 선례) 수준으로 충분합니다.

---

### 3. Proceed(진행) vs change hypothesis(가설 변경): **이 score contracts(점수 계약)로 진행** — 가설 변경 불필요

**판정:** Frontier15(프론티어15)는 **지금 가설로 materialize(물질화)** 해도 됩니다. 가설 자체를 바꿀 필요는 없습니다.

이유:
- F14 closeout(마감)이 `frontier15A_stage_open_new_hypothesis_design_v1`를 다음 행동으로 명시
- negative memory(부정 기억)가 가리키는 미해결 면(unresolved face, 미해결 면)이 **argmax density cliff(최대확률 밀도 절벽)** — F15가 직접 겨냥
- `edge_margin`, `side_gap`, `utility_tilt`는 서로 다른 trade-gating semantics(거래 게이팅 의미)를 가진 합리적 starter grid(시작 격자)

**Codex가 stage-open 전에 고정할 것(가설 변경 아님, 경계 강화):**
1. `novelty_delta`에 “F14 do-not-repeat의 label-family threshold micro-search(라벨 계열 임계값 미세 탐색)가 아님 — runtime representation change(런타임 표현 변경)” 명시
2. 9-cell grid freeze(9칸 격자 고정) + primary cell(1순위 셀) 또는 all-cells rule(전체 셀 규칙)
3. argmax baseline row(최대확률 기준선 행) + label/model density split(라벨/모델 밀도 분리) per split(분할별)
4. F12–F14 do-not-repeat carry(반복 금지 이월): quota retuning, flat-subset ladder, class-weight forcing, val/OOS threshold calibration

---

## One-sentence reason(한 문장 이유)

F14(프론티어14)가 “라벨 밀도 ≠ argmax 거래 밀도”로 닫힌 뒤, F15(프론티어15)는 **같은 라벨을 통제로 두고 decision contract(결정 계약)만 바꿔** density cliff(밀도 절벽)를 시험하므로 새 frontier hypothesis(새 전선 가설)로 열 가치가 있고, 9-cell pre-registration(9칸 사전 등록)과 train-only fit(학습 전용 적합)이 지켜지면 banned micro-search(금지 미세 탐색)가 아닙니다.

---

## Forbidden claims check(금지 주장 확인)

| Forbidden claim(금지 주장) | Status(상태) |
|---|---|
| completion(완성) | not_claimed(주장 없음) |
| baseline(기준선) | not_claimed |
| promotion(승격) | not_claimed |
| runtime authority(런타임 권위) | not_claimed |
| live readiness(실거래 준비) | not_claimed |
| Goal Achieve(목표 달성) | not_claimed |

**pass(통과)**

---

## Summary for Codex(코덱스용 요약)

**Classification: `accepted`**

Materialize(물질화) `stage_frontier_15__score_threshold_density_controlled_onnx_scout` after fixing the three leakage/selection guards(누수·선택 방어 3가지) and argmax baseline(최대확률 기준선) in `00_spec/`. Keep score contracts as proposed(제안한 점수 계약 유지). Do not retune labels/quota/horizon(라벨·할당량·보유기간 재조정 금지). Scout boundary only(탐색 경계만) — no authority claims(권위 주장 없음).
