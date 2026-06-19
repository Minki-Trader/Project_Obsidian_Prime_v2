Grok 역할로 Frontier06 개방 제안을 검토합니다. 먼저 관련 스킬·마감 보고서·Stage364 유사 작업을 확인합니다.
## 1. Recommendation(권고)

**`open_frontier06`(전선06 개방)** — 단, **Stage364(364단계) negative memory(부정 기억)를 명시적으로 반입 금지 목록에 넣은 채** 개방합니다.

`revise_direction`(방향 수정)이나 `do_not_open`(개방 금지)까지는 필요 없습니다. 표면(surface, 표면)은 Stage364 probability-bin/veto repair(확률 구간/차단 수리)와 비슷하지만, **문제 설정(problem setup, 문제 설정)**과 **실패 모드(failure mode, 실패 모드)**가 충분히 달라서, Frontier05(전선05) 마감이 요구한 “signal contract or validation philosophy(신호 계약 또는 검증 철학) 전환”에 가장 직접적인 다음 가설입니다.

---

## 2. Reasoning(근거)

### Frontier05(전선05) 마감 논리와 정합(alignment, 정합)

Frontier05C(전선05C)는 feature micro-expansion(피처 미세 확장)을 `negative_memory`(부정 기억)로 닫았고, 다음 전선은 **신호 계약 또는 검증 철학**을 바꾸라고 명시했습니다. Frontier06(전선06)은 라벨·피처·모델군을 고정하고 **output-to-trade contract(출력→거래 계약)**만 바꾸므로, Frontier05(전선05)가 끊으려던 repair loop(수리 반복)와 정면으로 맞습니다.

### Frontier04(전선04) 실패 모드와의 연결

Frontier04(전선04) negative memory(부정 기억)의 핵심은 “oracle surface(오라클 표면)는 깨끗한데 argmax trainable transfer(최대 확률 학습 전달)가 과다거래(overtrading, 과다거래)로 망가진다”는 점입니다.

- argmax validation(검증): PF `0.98`, density `~25/day`, DD `~75%`
- argmax OOS(표본밖): PF `0.97`, density `~27/day`, DD `~40%`

즉 이번 전선이 겨냥하는 건 **저밀도 cherry-pick(선별)**이 아니라 **과다거래를 줄이는 abstention contract(기권 계약)**입니다. Stage364(364단계)가 주로 남긴 실패는 반대 방향 — density `~2.1/day`의 저밀도 함정 — 이라서, **같은 수리 축(repair axis, 수리 축)이지만 다른 failure vector(실패 벡터)**를 시험합니다.

### Stage364(364단계)와의 유사성 — 반복 위험은 있지만 개방을 막을 정도는 아님

Stage364(364단계)는 probability-bin veto(확률 구간 차단), margin threshold(마진 임계값), p_flat veto(플랫 확률 차단), density repair(밀도 수리)로 긴 repair chain(수리 연쇄)을 탔고, 마감 시 `strict_joint_pass_count = 0`이었습니다. 표면적으로 Frontier06(전선06) 후보 규칙군과 겹칩니다.

하지만 `reference, not inheritance(참조이지 상속 아님)` 규칙 하에서는 **같은 메커니즘 이름**이 반복을 자동으로 금지하지 않습니다. 달라야 하는 것은:

| 축(axis, 축) | Stage364(364단계) | Frontier06(전선06) 제안 |
|---|---|---|
| Label/feature stack(라벨/피처 스택) | h17/oos108/pf125 repair chain(수리 연쇄) | path-label + `feature_set_v2` 고정 스택 |
| Primary failure(주 실패) | 저밀도 + PF/DD joint pass 실패 | argmax 과다거래 + DD 붕괴 |
| Scope(범위) | MT5 runtime repair spiral(런타임 수리 나선) | train-only scout, no WFO/MT5 |
| Baseline(기준) | Stage364 preserved clue(보존 단서) 상속 금지 | Frontier04/05 argmax를 reference-only comparator(참조 전용 비교자)로 사용 |

Frontier governance(전선 운영 규칙)의 `novelty_delta`(신규성 차이) 조건도 충족합니다: **validation philosophy(검증 철학)**의 일부로 “고정 모델 스택에서 신호 계약만 바꿔 oracle-transfer gap(오라클 전달 격차)을 재측정”하는 것은 새 전선 가설로 타당합니다.

### 왜 다른 가설로 바꾸지 않나

`validation philosophy only`(검증 철학만 변경) — 예: split 재설계, cost-aware evaluation only(비용 인식 평가만) — 는 보조 축으로는 좋지만, Frontier04(전선04)의 즉각 blocker(차단 요인)는 “argmax가 너무 많이 거래한다”이므로 **signal contract(신호 계약)**가 먼저 시험할 1순위 가설입니다.

---

## 3. Required bounds for Frontier06B(전선06B 필수 경계)

Codex(코덱스)는 Frontier06B(전선06B)를 아래 경계 안에서만 실행해야 합니다.

1. **Frozen controls(고정 통제)**
   - 동일 dataset / feature order / split / locked path target / Frontier04D·F05 model families
   - 라벨·피처·모델 재학습·재튜닝 금지

2. **Mandatory comparator(필수 비교자)**
   - 같은 모델·같은 split에서 **argmax baseline(최대 확률 기준선)** 필수
   - Stage364 `hold4_margin_0.01` 또는 probability-bin veto package(패키지)를 baseline(기준선)으로 쓰지 말 것

3. **Train-only rule fitting(학습 분할 전용 규칙 적합)**
   - threshold / margin / flat veto / density target calibration(밀도 목표 보정)은 **train split(학습 분할)**에서만 적합
   - validation/OOS(검증/표본밖) 라벨·PnL·density로 규칙을 고르거나 재적합하면 **invalid(무효)**

4. **Broad-first, capped grid(넓은 탐색 우선, 상한 있는 그리드)**
   - rule family(규칙군)별 coarse grid(거친 그리드)만 허용
   - combination count(조합 수) 상한 명시; Stage364식 micro-search escalation(미세탐색 격상) 금지

5. **Dual density floor(이중 밀도 하한)**
   - scout clue(탐색 단서)는 validation **and** OOS 모두에서 density가 argmax보다 낮아지면서 PF만 오르는 패턴이면 **low-density cherry-pick(저밀도 선별)**로 즉시 실패 처리
   - 실무 하한 예: 양 split 모두 `>= 4 trades/day` 미만이면 clue rejected(단서 거절)
   - 목표 밴드 `5-10/day`는 **success aspiration(성공 지향)**이지 scout pass(탐색 통과)의 유일 조건이 되면 안 됨

6. **Four-axis joint read(네 축 동시 판독)**
   - density, PF, DD, 그리고 net/expectancy(순수익/기대값)를 split별로 함께 기록
   - 한 축만 개선되면 preserved clue(보존 단서)도, negative memory(부정 기억)도 아님 — `inconclusive_partial_axis_gain`(불충분 부분 축 개선)

7. **Probability meaning boundary(확률 의미 경계)**
   - path-label model softmax(소프트맥스)는 **calibrated probability truth(보정된 확률 진실)**가 아니라 **ranking/score surface(순위/점수 표면)**로 취급
   - “calibration succeeded(보정 성공)” 주장 금지; “abstention contract changed trade density/PF/DD(기권 계약이 거래 밀도/PF/DD를 바꿨다)”만 허용

8. **Tier paired record(티어 쌍 기록)**
   - Tier A separate / Tier B separate / Tier A+B combined 기록
   - 불가 시 `missing_required`(필수 누락)로 명시 — 생략 금지

9. **No MT5 / no WFO on first scout(첫 탐색에 MT5·WFO 없음)**
   - validation+OOS Python replay(파이썬 재현)에서 cross-split clue(교차 분할 단서)가 나오기 전까지 runtime escalation(런타임 격상) 금지

10. **Fast close rule(빠른 마감 규칙)**
    - broad grid(넓은 그리드) 후에도
      - argmax 대비 density↓ + PF↑만 나오거나
      - OOS PF `< 1.0` 또는 DD가 argmax보다 악화
    - 이면 **negative memory(부정 기억)**로 닫고 threshold micro-search(임계값 미세탐색)로 넘어가지 말 것

11. **Explicit prior-stage scan entry(명시적 이전 단계 점검 항목)**
    - `do_not_repeat`: Stage364 probability-bin veto repair chain(확률 구간 차단 수리 연쇄), Stage364 package inheritance(패키지 상속), density-only rescue(밀도만 구제)
    - `reference only`: Stage364 preserved clue(보존 단서)는 “저밀도 고PF 단서가 가능했으나 joint pass는 실패”라는 **경고 메모**로만 사용

---

## 4. Risks(위험)

1. **Mechanism reuse disguised as novelty(신규성으로 위장한 메커니즘 재사용)**  
   이름만 “signal contract(신호 계약)”이고 실질은 Stage364 veto grid(차단 그리드) 재실행일 수 있습니다. 상한 있는 broad grid + dual density floor 없으면 반복됩니다.

2. **Train-density calibration leakage(학습 밀도 보정 누수)**  
   “train-target density calibration(학습 목표 밀도 보정)”은 train에서 density를 맞추는 과정이 validation 성능을 간접 최적화할 수 있습니다. train-only fitting(학습 전용 적합)과 rule family cap(규칙군 상한)으로 제한해야 합니다.

3. **Weak-model ranking assumption(약한 모델 순위 가정)**  
   “ranking information exists(순위 정보가 있다)”는 가설은 plausible(그럴듯)하지만, Frontier04(전선04) ONNX metrics(지표)가 이미 weak(약함)이므로 abstention이 **노이즈 제거**가 아니라 **표본 축소(sample starvation, 표본 고갈)**만 할 수 있습니다.

4. **Asymmetric split behavior(분할 비대칭)**  
   validation에서만 좋아지고 OOS에서 붕괴하면 Stage364(364단계)와 같은 partial clue(부분 단서) 패턴이 반복됩니다. 양 split 동시 개선을 scout success(탐색 성공)의 최소 조건으로 둬야 합니다.

5. **Oracle gap misread(오라클 격차 오독)**  
   Frontier04(전선04) proxy oracle(프록시 오라클)은 매우 강합니다. abstention이 argmax를 조금만 나아지게 해도 “oracle transfer solved(오라클 전달 해결)”로 과장하기 쉽습니다. comparator는 **argmax trainable(최대 확률 학습 가능)**, oracle가 아님.

6. **Repair loop re-entry via density target(밀도 목표로 수리 루프 재진입)**  
   density `5-10/day`를 맞추려다 Stage364식 density repair(밀도 수리)로 새는 위험이 큽니다. 첫 scout(첫 탐색)에서는 density target(밀도 목표)을 **soft constraint(약한 제약)**로만 취급하세요.

---

## 5. Do-not-claim boundary(주장 금지 경계)

Frontier06(전선06) open/scout(개방/탐색) 단계에서 아래는 **모두 not_claimed(주장 없음)**:

| 금지 주장(forbidden claim, 금지 주장) | 허용 범위(allowed scope, 허용 범위) |
|---|---|
| completion / baseline / promotion(완성/기준선/승격) | exploration scout only(탐색 전용) |
| runtime authority / live readiness(런타임 권위/실거래 준비) | Python replay only(파이썬 재현만) |
| Goal Achieve(목표 달성) | four-axis distance improvement clue only(네 축 거리 개선 단서만) |
| calibrated probability truth(보정 확률 진실) | score-threshold contract only(점수 임계값 계약만) |
| oracle transfer success(오라클 전달 성공) | vs argmax trainable only(최대 확률 학습 가능 대비만) |
| Stage364 package reuse / inheritance(364단계 패키지 재사용/상속) | negative memory reference only(부정 기억 참조만) |
| ONNX parity ⇒ usable alpha(온엑스 동등성 ⇒ 쓸만한 알파) | parity is plumbing check(동등성은 배관 점검) |
| single-split PF>1.2 ⇒ promotion candidate(단일 분할 PF>1.2 ⇒ 승격 후보) | validation **and** OOS joint read required(검증과 표본밖 동시 판독 필요) |

---

### Classification note for Codex(코덱스 분류 메모)

| Grok advice item(그록 조언 항목) | Classification(분류) |
|---|---|
| Open Frontier06 as signal-contract hypothesis(신호 계약 가설로 전선06 개방) | **accepted(수용)** |
| Keep labels/features/models fixed(라벨/피처/모델 고정) | **accepted(수용)** |
| Train-only calibration + val/OOS evaluation(학습 전용 보정 + 검증/표본밖 평가) | **accepted(수용)** — bounds above required(위 경계 필수) |
| Inherit Stage364 probability-bin veto as baseline(364단계 확률 구간 차단을 기준선으로 상속) | **rejected(거절)** |
| Operating/runtime claim from proxy thresholds(프록시 임계값으로 운영/런타임 주장) | **rejected(거절)** |
| Unbounded threshold micro-search(무제한 임계값 미세탐색) | **rejected(거절)** |
| Thresholds fitted train-only(임계값 학습 전용 적합) | **needs_local_verification(로컬 검증 필요)** |
| Tier B/combined ledger rows(티어 B/합산 장부 행) | **needs_local_verification(로컬 검증 필요)** |
| Score thresholds ≠ calibrated probability truth(점수 임계값 ≠ 보정 확률 진실) | **needs_local_verification(로컬 검증 필요)** |

**Bottom line(요약):** Frontier06(전선06) 개방은 타당합니다. 다만 “새 전선”이 아니라 “Stage364 abstention 메커니즘을 path-label transfer 문제에 **통제 실험(controlled experiment, 통제 실험)**으로 재시험”이라고 문서에 정직하게 적고, Stage364(364단계) 저밀도 함정을 **명시적 stop condition(중지 조건)**으로 박아 두어야 repair loop(수리 반복)가 다시 열리지 않습니다.
