Grok 협업 규칙과 제한 근거 문서를 먼저 확인한 뒤, Frontier05 개방 제안을 검토하겠습니다.
## 1. Recommendation(권고)

**`open_frontier05(전선05 개방)`** — 단, **좁힌 Frontier05B scout(전선05B 탐색)** 조건을 붙여서 개방합니다.

`revise_direction(방향 수정)`이나 `do_not_open(개방 금지)`까지는 가지 않습니다. 가설 생명주기(hypothesis lifecycle, 가설 생명주기)는 분리돼 있고, Frontier04 repair(전선04 수리)로 보이지 않게 경계를 잡을 수 있습니다.

---

## 2. Reasoning(근거)

**Frontier04가 이미 닫혔고, 실패 원인이 “피처 표면”으로 좁혀져 있기 때문입니다.**

- Frontier04 closeout(전선04 마감)은 **negative memory + preserved clue(부정 기억 + 보존 단서)**입니다. proxy oracle(프록시 오라클)은 살아 있고, **trainable transfer collapse(학습 전달 붕괴)**만 부정 기억으로 남겼습니다.
- Frontier05가 바꾸는 변수는 **label threshold(라벨 임계값)**가 아니라 **feature surface(피처 표면)**입니다. `frontier_governance.md`의 repair escalation(수리 격상) 기준에서, **source/representation change(원천/표현 변경)**에 해당합니다.
- Frontier04D(전선04D)는 이미 “같은 라벨·분할·작은 모델”에서 `feature_set_v2` 한계를 확인했습니다. 다음으로 물을 질문은 자연스럽게 **“closed-bar precursors(확정봉 선행 단서)가 없어서 실패했는가?”**입니다.
- path label(경로 라벨)을 **fixed reference target(고정 참조 목표)**로만 쓰고, threshold sweep(임계값 반복 탐색)을 금지하면 Frontier04 repair loop(전선04 수리 반복)와 구분됩니다.

**다만 “전선04 수리와 너무 가깝다”는 우려도 일부 타당합니다.**

- 같은 locked variant `f04b_path_h12_t1p20_s0p80_trainp90`, 같은 dataset rows(데이터셋 행), 같은 small model grid(작은 모델 격자)를 쓰면 **표면상 F04D 후속 수리**처럼 보일 수 있습니다.
- F04D의 density blow-up(밀도 폭증) `~25–27/day` vs proxy `~6–8/day`는 “피처 부족”만으로 설명되지 않을 수 있습니다. class balance(클래스 균형), argmax policy(최대확률 정책), label-event sparsity(라벨 이벤트 희소성)도 같이 작용했을 수 있습니다.
- `feature_set_v2` 58개 피처 안에 이미 return/volatility/range 계열이 있어, 제안한 precursor families(선행 피처군) 일부와 **중복·상관(collinearity, 공선성)** 위험이 있습니다.

**그래도 개방이 맞는 이유:**

Frontier04 preserved clue(전선04 보존 단서)를 버리기 전에, **한 번의 통제 비교(controlled comparison, 통제 비교)**로 “closed-bar path precursors(확정봉 경로 선행 피처)가 learnability(학습 가능성)를 올리는가?”를 검증하는 것은 비용 대비 가치가 큽니다. 실패해도 **negative memory(부정 기억)**로 닫을 수 있고, 성공해도 scout clue(탐색 단서) 수준입니다.

**조언 분류(advice classification, 조언 분류) for Codex:**

| 항목 | 분류 |
|------|------|
| 별도 가설 생명주기로 Frontier05 개방 | **accepted(수용)** |
| Frontier04 path label을 fixed reference only로 유지 | **accepted(수용)** |
| 동일 행/분할에서 v2 vs v2+precursors 비교 | **accepted(수용)** |
| 첫 scout는 proxy/model-only, WFO/MT5 금지 | **accepted(수용)** |
| 7개 precursor family를 한 번에 전부 구현 | **rejected(거절)** — 좁혀야 함 |
| Frontier04 proxy를 baseline/winner로 상속 | **rejected(거절)** |
| closed-bar leakage-free 구현, OHLC alignment, identical splits | **needs_local_verification(로컬 검증 필요)** |

---

## 3. Required bounds for Frontier05B(전선05B 필수 경계)

**A. Hypothesis lock(가설 고정)**

- **Label(라벨):** Frontier04B locked variant 하나만. threshold/horizon/scale 재탐색 금지.
- **Rows/splits(행/분할):** `model_input_dataset.parquet`와 Frontier04D와 **동일 행·동일 train/validation/OOS**.
- **Models(모델):** Frontier04D와 **동일 model families/settings**. 모델 확장은 precursor A/B가 먼저 실패한 뒤에만.
- **Threshold policy(임계값 정책):** `argmax only(최대 확률만)`, searched threshold 금지.

**B. Feature-surface comparison(피처 표면 비교)**

- **Arm A:** `feature_set_v2` only (58 features).
- **Arm B:** `feature_set_v2` + stage-local closed-bar precursors only.
- **Precursor input(선행 피처 입력):** current and prior closed US100 M5 OHLC only. **No future bar access(미래 봉 접근 금지).**
- **Family budget(피처군 예산):** 7개 전부가 아니라 **2–3개 path-linked family(경로 연관 피처군)**부터:
  1. wick/body pressure + adverse-tail clustering
  2. recent excursion asymmetry
  3. volatility compression/expansion  
  나머지는 1차 scout 실패/부분 성공 후에만.
- **Overlap audit(중복 감사):** 새 precursor와 기존 v2 58개의 상관/중복을 보고서에 명시. “새 이름, 같은 정보” 방지.

**C. Success / stop metrics(성공·중지 지표)**

- **Primary(1차):** Frontier04D 대비 **learnability retention(학습 전달 유지율)** 개선 여부  
  - PF: validation/OOS 모두 `> 1.0` 방향
  - density: proxy `~5–10/day`에 **가까워지는 방향** (F04D `~25/day`에서 크게 줄어야 함)
  - DD: validation/OOS 모두 **`< 10%` exploratory target(탐색 목표)** 쪽
- **Partial-transfer pass(부분 전달 통과):** PF·density·DD **동시 개선**이 없으면 scout clue(탐색 단서) 주장 금지.
- **Stop(중지):** Arm B가 Arm A 대비 material retention gain(유의미한 유지율 개선) 없으면 **negative memory 또는 preserved clue**로 닫고, label sweep(라벨 반복 탐색)으로 넘어가지 않음.

**D. Data integrity(데이터 무결성)**

- Frontier04B와 같은 **OHLC alignment preflight(원천 OHLC 정렬 사전 점검)** 재실행.
- `timezone_status = UNRESOLVED_REQUIRES_MANUAL_BINDING`은 **usable_with_boundary(경계부 사용 가능)**로만 기록. UTC/session 주장 금지.
- Rolling/shift precursor에 대한 **leakage audit(누수 감사)** 필수.
- **Tier record(티어 기록):** Tier A separate / Tier B `missing_required` / combined — 명시적 라벨링.

**E. Architecture(구조)**

- 구현은 `stage_pipelines/stage_frontier_05/` stage-local only.
- `foundation/features` 승격 없음. foundation owner decision 전까지 truth(진실 원천) 아님.
- **No WFO, no MT5, no ONNX parity expansion** in Frontier05B first scout.

**F. Reporting(보고)**

- retention table(유지율 표)에 **3-way reference(3방향 참조)** 포함:
  1. Frontier04B proxy oracle
  2. Frontier04D trainable baseline
  3. Frontier05B Arm A vs Arm B

---

## 4. Risks(위험)

1. **Repair drift(수리 드리프트):** 같은 라벨·모델·행을 쓰면 Frontier04D “feature repair packet(피처 수리 묶음)”으로 오해될 수 있음. → novelty_delta와 stop rule을 문서에 반복 기록해야 함.
2. **Fundamental unlearnability(근본적 비학습성):** path-aware label은 미래 경로 품질을 직접 인코딩합니다. closed-bar precursors만으로는 **구조적으로 전달 한계**가 있을 수 있음.
3. **Density pathology(밀도 병리):** F04D density blow-up이 피처 부족이 아니라 **class frequency / argmax policy** 문제면 precursor 추가만으로는 안 고쳐질 수 있음.
4. **Feature redundancy(피처 중복):** v2 58개와 새 precursor가 겹치면 marginal gain(한계 이득)이 거의 없을 수 있음.
5. **Leakage via rolling windows(롤링 창 누수):** shift/alignment 실수 하나로 scout 전체가 invalid(무효)가 됨.
6. **Overfitting surface(과적합 표면):** precursor family를 많이 붙이면 train 쪽만 좋아지고 OOS는 그대로일 수 있음.
7. **Timezone unresolved(시간대 미해결):** bar alignment 오류가 precursor 품질을 더 흐릴 수 있음.
8. **False hope from preserved clue(보존 단서 과대 기대):** proxy PF `18.6 / 214.9`는 oracle upper bound(오라클 상한)에 가깝고, trainable target(학습 목표)으로 착각하면 안 됨.

---

## 5. Do-not-claim boundary(주장 금지 경계)

Frontier05 stage-open(전선05 단계 개방)과 Frontier05B scout(전선05B 탐색)에서 **절대 주장하면 안 되는 것:**

- `completion(완성)`, `selected baseline(선택 기준선)`, `promotion_candidate(승격 후보)` 이상의 운영 의미
- `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`, `live_readiness(실거래 준비)`, `Goal Achieve(목표 달성)`
- Frontier04 proxy oracle을 **inherited winner(상속 승자)** 또는 **trainable baseline(학습 기준선)**으로 취급
- “path-aware labels are learnable(경로 라벨은 학습 가능하다)” — Frontier05B retention evidence 전에는 불가
- “closed-bar precursors solve oracle transfer(확정봉 선행 피처가 오라클 전달을 해결한다)” — scout clue 전에는 불가
- stage-local features를 **foundation truth(파운데이션 진실 원천)** 또는 MT5 parity-ready(동등성 준비 완료)로 표기
- density `25/day`를 “알파 풍부”로 읽기 — F04D에서는 **failure signature(실패 징후)**임
- Tier B/combined 결과를 Tier A 전체 결론처럼 말하기
- `UNRESOLVED` timezone을 확정된 market-session truth(시장 세션 진실)로 말하기

**허용되는 주장 범위:**

- Frontier05는 **distinct hypothesis lifecycle(별도 가설 생명주기)**로 열렸다
- Frontier05B는 **exploratory learnability scout(탐색적 학습 가능성 탐색)**이다
- positive/negative/preserved clue 판정은 **retention comparison evidence(유지율 비교 근거)** 이후에만

---

**Bottom line(한 줄 요약):** Codex는 Frontier05를 열어도 됩니다. 다만 Frontier05B는 “7개 피처군 대량 추가”가 아니라, **Frontier04D와 동일한 통제 조건에서 2–3개 path-linked precursor family만 붙인 좁은 A/B scout**로 시작해야 Frontier04 repair(전선04 수리)가 아니라 **정당한 다음 가설(legitimate next hypothesis, 정당한 다음 가설)**로 남습니다.
