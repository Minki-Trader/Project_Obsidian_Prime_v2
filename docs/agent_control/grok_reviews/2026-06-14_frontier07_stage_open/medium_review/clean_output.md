Grok 역할로 Frontier07 제안을 검토합니다. 먼저 협업 스킬과 제한 근거 문서를 읽겠습니다.
Frontier07 제안과 기존 라벨·전선 거버넌스를 대조해 novelty delta(신규성 차이)를 확인합니다.
## 1. Recommendation(권고)

**`open_frontier07` (전선07 개방)** — 단, Frontier07A 스펙에 아래 §3 경계를 넣은 뒤 Frontier07B를 실행하라.

`revise_direction`(방향 수정)이나 `do_not_open`(개방 금지)은 아니다. 가설 축(label utility, 라벨 효용)은 맞고, F06 마감 후 자연스러운 다음 단계다. 다만 F04(전선04)와 겹치지 않게 **실행 경계**를 먼저 박아야 한다.

---

## 2. Reasoning(근거)

**가설 축 전환은 타당하다.**
F06(전선06)은 같은 모델·같은 `label_v1_fwd12` 위에서 출력 임계값·기권만 바꿨다. 최상위 규칙이 OOS 밀도/PF/DD를 개선했지만, validation PF는 탐색 하한 아래이고 OOS DD는 여전히 ~21%다. 즉 “예측 뒤에 거르기”만으로는 학습 목표 자체의 한계를 넘기 어렵다.

**진단도 설득력 있다.**
현재 학습 타깃은 확정봉 12봉 선행 수익률 기반 3-class다. 경로상 MAE(최대 불리 이동)가 크게 나온 진입과, MAE가 작은 진입을 분리하지 않는다. DD-heavy entry(손실폭 큰 진입)를 피하려면 training-time label(학습 시점 라벨) 쪽을 건드리는 시도는 논리적으로 맞다.

**탐색 순서도 frontier chain(전선 연쇄)과 맞다.**
F04 → path label oracle(경로 라벨 오라클) / transfer 실패
F05 → feature repair(피처 수리) 실패
F06 → signal contract(신호 계약) / strict clue 없음, DD 잔존
다음으로 label utility를 여는 것은 F06C가 제안한 “exit/risk/validation new axis(청산/위험/검증 새 축)”와도 일치한다.

**다만 novelty delta(신규성 차이)는 약하다 — 그래서 개방 조건부다.**
F04는 이미 raw OHLC 경로에서 favorable/adverse excursion(유리/불리 이동)과 target-before-stop(목표 선행·손절) 이벤트 라벨을 썼다. F07이 “MAE cap + MFE target + recovery window”만 추가하면, 겉포장만 바뀐 F04 재시도로 보일 수 있다. F04 negative memory(부정 기억) — oracle-looking but unlearnable(오라클처럼 보이나 학습 불가) — 가 그대로 반복될 위험이 가장 크다.

**그래도 완전히 다른 가설로 갈 이유는 없다.**
F07의 핵심 차이는 “이벤트 승/패 라벨”이 아니라 **risk-shaped utility(위험 형성 효용)** — 즉 “유리 이동은 MAE가 bounded(상한 이내)일 때만 긍정”이라는 **손실 분포 형성**이다. F04가 닫지 않은 질문이기도 하다: *path 정보를 다른 label semantics(라벨 의미)로 주면 feature_set_v2 + small ONNX model(작은 온엑스 모델)이 전달할 수 있는가?*

**결론:** 방향은 열되, F04 oracle trap(오라클 함정)을 막는 learnability-first gate(학습 가능성 우선 게이트)와 variant differentiation(변형 차별화) 없이는 열지 마라.

---

## 3. Required bounds for Frontier07B(전선07B 필수 경계)

1. **Fixed comparison surface(고정 비교 표면)**
   - 입력: `feature_set_v2` + 동일 small ONNX-exportable model family(작은 온엑스보내기 가능 모델군) — F04/F06과 동일 계열
   - 신호: **argmax only(최대확률만)** — F06식 train-only abstention/threshold micro-search(학습 전용 기권·임계값 미세탐색) 금지
   - 비교 기준 3종 필수:
     - `label_v1_fwd12` argmax baseline
     - F04 locked proxy `f04b_path_h12_t1p20_s0p80_trainp90` trainable reference
     - F06 best selective reference (`rf_depth5_leaf80_balanced_argmax__directional_margin__...`) — **참조용**, F07B에서 재적합 금지

2. **Variant design must not be F04 grid replay(F04 격자 재시도 금지)**
   - 금지: horizon × target_mult × stop_mult만 바꾼 이벤트 라벨 재탐색
   - 허용: MAE-bounded positive utility, graded/score labels, recovery-conditioned labels, time-to-adverse penalty, side-asymmetric caps
   - 각 family마다 “F04 event-label과 다른 semantics(의미)”를 스펙에 한 줄로 명시

3. **Learnability-first gate(학습 가능성 우선 게이트) — oracle celebration 전에 통과**
   Frontier07B scout는 proxy oracle metrics(프록시 오라클 지표)를 먼저 보고하지 말고, 아래를 먼저 기록:
   - train/validation class balance(클래스 균형)
   - train→validation score separability proxy(점수 분리도 대리 지표)
   - ONNX parity pass(온엑스 동등성 통과)
   - **transfer gap(전달 격차)**: proxy validation PF가 trainable model validation PF보다 X배 이상이면 `oracle_transfer_risk(오라클 전달 위험)`로 태그하고 strict clue 후보에서 제외

4. **Broad variants, capped count(넓은 변형, 상한 고정)**
   - 사전 등록 family ≤ 5, family당 variant ≤ 3~4
   - micro-search(미세탐색) 금지
   - train-only scale quantile(학습 전용 스케일 분위)만 허용; validation/OOS fitting(검증/표본밖 적합) 금지

5. **Scout success definition(탐색 성공 정의) — F06보다 엄격**
   validation **and** OOS 모두에서, argmax 기준:
   - density 5–10/day
   - PF 개선
   - DD 개선
   - smoothness proxy 개선
   - **그리고** validation PF ≥ F06 scout floor(탐색 하한, 대략 1.0 이상)
   threshold fitting 없이 달성해야 strict scout clue(엄격 탐색 단서) 후보

6. **Partial success rule(부분 성공 규칙)**
   - DD만 좋아지고 density/PF가 죽으면 → preserved clue only(보존 단서만)
   - oracle만 좋고 trainable transfer 없으면 → negative memory(부정 기억), F04 패턴으로 즉시 close path(마감 경로)

7. **Tier recording(티어 기록)**
   Tier A separate / Tier B / Tier A+B — 없으면 `missing_required`로 기록. 생략 금지.

8. **Runtime boundary(런타임 경계)**
   Frontier07B = `research_only_no_mt5`. strict scout clue 0이면 WFO/MT5 금지.

---

## 4. Risks(위험)

| Risk(위험) | Why it matters(왜 중요한가) |
|---|---|
| **F04 oracle-transfer replay(F04 오라클 전달 반복)** | MAE/MFE path labels가 proxy에서는 PF/DD가 극단적으로 좋아도, feature_set_v2로는 다시 전달 안 될 수 있음 |
| **Semantic overlap disguised as novelty(겉만 새로운 의미 중복)** | target/stop path event와 MAE-cap utility가 실질적으로 같은 positive set을 고를 수 있음 |
| **DD via sparsity, not quality(DD 개선이 품질이 아니라 희소성)** | 긍정 라벨이 너무 적으면 DD는 내려가지만 density/PF가 동시에 무너짐 |
| **feature_set_v2 information ceiling(피처 정보 한계)** | 라벨을 아무리 risk-shape 해도 입력이 path quality를 담지 못하면 transfer는 0 |
| **Overfitting recovery/time penalties(회복·시간 벌점 과적합)** | recovery window, time-to-adverse는 train split에서만 “예쁜” utility를 만들기 쉬움 |
| **False hope from F06 preserved clue(F06 보존 단서 과신)** | F06 OOS DD 21%는 “충분히 좋다”가 아니라 “post-hoc throttle 한계” 신호 |

---

## 5. Do-not-claim boundary(주장 금지 경계)

Frontier07A/B에서 **주장하면 안 되는 것**:

- completion / baseline / promotion / runtime authority / live readiness / Goal Achieve
- F06 selective rule을 F07 성공의 운영 기준선으로 승격
- proxy/oracle PF·DD를 trainable ONNX 성공으로 기록
- validation/OOS threshold fitting 없이도 “모델이 위험을 학습했다”는 인과 주장
- DD만 개선된 variant를 strict scout clue로 승격
- Tier B/A+B 없이 Tier A만으로 전체 알파 판독
- strict scout clue 0 상태에서 MT5/WFO/런타임 probe를 “다음 필수 단계”로 제시
- F04 preserved clue oracle metrics를 F07 재현 또는 상속 성공으로 표현

**말해도 되는 것(탐색 범위 내):**

- Frontier07을 label-utility hypothesis(라벨 효용 가설)로 개방
- risk-shaped labels가 trainable transfer를 개선하는지 **scout-negative / scout-partial / scout-positive** 판정
- F04/F06 대비 four-axis distance(네 축 거리) 비교 결과를 exploration evidence(탐색 근거)로 기록

---

### Codex classification hint(코덱스 분류 힌트)

| Advice(조언) | Classification(분류) |
|---|---|
| Open Frontier07 on label-utility axis | **accepted(수용)** |
| §3 learnability-first + anti-F04 variant bounds | **accepted(수용)** |
| Any promotion/runtime/live readiness | **rejected(거절)** |
| Hash/file presence before materialize | **needs_local_verification(로컬 검증 필요)** |

**한 줄 요약:** Frontier07은 **열어도 된다**. 다만 “불리한 이동 위험 형성 라벨링”은 말만 바꾼 F04가 되면 안 되고, **학습 전달 가능성을 먼저 검사하는 scout**로 시작해야 한다.
