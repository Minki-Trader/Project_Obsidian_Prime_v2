## advice_classification(조언 분류)

**needs_local_verification(로컬 검증 필요)** — 방향은 **accepted(수용)** 가능하지만, F76B 실행 전에 게이트 계층·축 정의·F71–F75 대비 차별이 로컬에서 한 번 더 맞는지 확인해야 한다.

---

## accepted(수용)

1. **F76 신규성(versus F71–F75)**  
   F71–F75가 “parity without runtime economics(동등성은 맞췄지만 런타임 경제성 없음)”이었다면, F76의 **source-axis falsification before fine-tuning(미세 조정 전 원천 축 반증)** 은 질문 자체가 다르다. parity 반복이 아니라 **6축 제거/교체/재조합 행렬**로 “어디가 망치거나 살리는지”를 먼저 보는 설계는 F76 개방으로 충분히 새롭다.

2. **가설 프레이밍**  
   “edge source(우위 원천)를 찾거나 반증한다”는 탐색 라벨에 맞고, operating promotion(운영 승격)·baseline(기준선)·runtime authority(런타임 권위) 주장과 분리되어 있다.

3. **런타임 규칙**  
   meaningful signal(의미 신호) → pre-MT5 Grok + MT5 probe(탐침); nonzero but sub-threshold(비영·미달) → bounded negative-control MT5; zero signal(영 신호) → logic impossibility(논리상 불가능) 기록 후 가짜 비교 없이 closeout — 탐색 단계에서 과장을 막는 순서로 적절하다.

4. **regime/session fragility gate(장세·세션 취약성 게이트)**  
   “한 micro slice(미세 구간)가 전체를 끌고 가면 fragility(취약성) 기록” — F71–F75의 반복 실패 패턴(좁은 표면·밀도 부족)을 직접 겨냥한다.

---

## rejected(거절)

1. **F76B를 또 다른 parity sweep(동등성 스윕)으로 돌리는 것** — 축 반증 없이 하이퍼파라미터·미세 조정만 반복하면 F71–F75 재현이다.

2. **단일 축 variant 하나가 meaningful gate(의미 게이트)를 넘었다고 source axis(원천 축) 확정** — 한 셀 통과는 clue(단서)일 뿐, 축 확정은 아니다.

3. **validation-only(검증만) 또는 single-side sparse cluster(단방향 희소 군집)를 “의미 신호”로 승격** — trade_shape·regime 게이트와 충돌한다.

4. **zero / sub-threshold에서 MT5 생략** — 프롬프트의 negative-control(부정 대조)·logic impossibility 규칙을 우회하는 closeout.

5. **6축 full Cartesian product(전 조합)를 한 번에 F76B에 넣는 것** — 탐색 폭발; scout pass(탐색 회차) 단위 bounded matrix(제한 행렬)가 아니면 반복 금지 대상이다.

---

## needs_local_verification(로컬 검증 필요)

Codex가 F76B 전에 로컬에서 확인할 것:

| 항목 | 확인 내용 |
|------|-----------|
| 게이트 계층 | `meaningful_gate`와 lighter **scout clue gate(탐색 단서 게이트)** 가 파이프라인에 분리돼 있는지 (model_family 행은 이미 암시) |
| 피처 variant 정의 | `full58`, `price_action_core`, `trend_momentum` 등이 **재현 가능한 feature family map(피처군 맵)** 으로 고정돼 있는지 |
| 라벨 variant | 5종 label_target이 구현·밀도 추정 가능한지 (`label density >= 1.0 trades/day proxy`) |
| model_family | EBM 가용 여부, NN “small” 스펙, 최소 2 family scout 생존 규칙의 operational definition(운영 정의) |
| F71–F75 아카이브 | parity 달성 방식·실패한 runtime economics KPI를 F76 **negative memory(부정 기억)** 로 1페이지 이상 연결 가능한지 |
| Tier A/B | Stage 10+ 규칙상 Tier A separate / Tier B separate / combined 기록 슬롯이 F76B 스카우트에 배선돼 있는지 |
| 데이터 identity | 46650 rows, split counts, 58 features가 **현재 materialization(현재 물질화)** 과 hash 일치하는지 |

---

## F76 opening boundary(F76 개방 경계)

- **허용:** F76 = **axis-ablation / source-discovery matrix(축 제거·원천 탐색 행렬)** 탐색 단계; 축별 bounded variant runs; proxy KPI; fragility·density 기록; 조건부 MT5 probe.
- **불허:** selected baseline(선택 기준선), promotion_candidate(승격 후보) 운영 주장, runtime authority(런타임 권위), live readiness(실거래 준비), “F76 winner(승자)”.
- **성공 정의(탐색 한정):** (a) 한 축 이상의 **falsified(반증됨)** 또는 **surviving clue cluster(생존 단서 군집)** 가 validation+OOS+regime에서 기록됨; (b) MT5 규칙에 따른 probe 또는 documented impossibility(기록된 불가능).
- **실패 정의(유효):** 전 축 scout에서 meaningful gate 0건 + fragility만 반복 → **negative result closure(부정 결과 마감)** (아이디어 사망 아님).

---

## F76B proxy-scout cautions(F76B 프록시 탐색 주의)

**Q2 — meaningful signal gates(의미 신호 게이트) 적절성**

- **의미 게이트(`meaningful_gate`)**: 초기 탐색의 “최종 통과선”으로는 **다소 엄격(strict)** — validation **및** OOS 동시 `net>0`, `PF>=1.30`, `DD<=10%`, `trades/day>=1.0`, `trade_count>=100`는 scout 단계에서 통과율이 낮을 수 있다. **의도적 엄격함**은 맞다(가짜 의미 신호 억제).
- **권장 계층**:  
  - **Scout clue**: 예) 한 split에서 `net>0` OR `PF>=1.15`, `trade_count>=50`, density proxy 통과 → “다음 축/재조합 후보”만.  
  - **Meaningful**: 현재 joint gate → pre-MT5 Grok + MT5 probe 트리거만.
- **적절한 느슨함**: regime “no single micro slice(단일 미세 구간 금지)”·trade_shape “no isolated sparse cluster(고립 희소 군집 금지)” — 느슨하지 않고 **필수**.
- **너무 느슨하면 안 되는 것**: validation-only 승리, long-only 또는 한 세션만 밀도 충족.

**F76B 실행 순서 제안(조언)**  
1) feature_set + label_target scout → 2) 생존 clue에만 model_family → 3) trade_shape + risk_logic proxy 압박 → 4) regime fragility audit → 5) gate tier에 따라 MT5.

---

## forbidden_claim_check(금지 주장 확인)

| 금지 주장 | 본 프롬프트 기준 |
|-----------|------------------|
| Completion / Goal Achieve | **금지** — Grok·F76 open이 만들 수 없음 |
| Baseline / operating promotion | **금지** — 축 scout는 promotion_candidate도 자동 생성 안 함 |
| Runtime authority / live readiness | **금지** — MT5 probe는 관찰일 뿐 권위 닫힘 아님 |
| “F76 found alpha(알파 발견)” | **금지** — source axis identified **or falsified(확정 또는 반증)** 만 허용 |
| “Gates prove tradeable live edge(게이트가 실거래 우위 증명)” | **금지** — proxy; MT5는 probe 라벨 |

---

## F76 do-not-repeat(반복 금지) — 기록 권고

> **F76-DNR-01:** F71–F75에서 parity(동등성)만 달성한 채 feature/label/model/trade-shape/risk/regime 축을 구조적으로 제거·교체·재조합하지 않은 채 fine-tuning(미세 조정)·threshold sweep(임계값 스윕)·단일 variant 최적화를 반복하지 않는다.  
> **F76-DNR-02:** validation-only, single-session, 또는 single-side sparse cluster를 meaningful signal(의미 신호)로 기록하지 않는다.  
> **F76-DNR-03:** nonzero·sub-threshold 결과에서 negative-control MT5(부정 대조 탐침) 없이 closeout하지 않는다 (logic impossibility(논리상 불가능) 문서화 시 예외).  
> **F76-DNR-04:** 6축 full combinatorial explosion(전 조합 폭발) 없이, 축별 bounded scout pass(제한 탐색 회차) 없이 F76B를 확장하지 않는다.

---

**요약 답변(4문항)**  
1. **신규성:** 예, 질문이 F71–F75와 다름 — **충분히 새 단계**.  
2. **게이트:** meaningful = 탐색 최종선으로 **적절히 엄격**; scout에는 **한 단계 낮은 clue gate(단서 게이트)** 로컬 분리 권고.  
3. **F76B 전:** 위 `needs_local_verification` 표 + scout/meangingful 계층·Tier 기록·F71–F75 negative memory 링크.  
4. **DNR:** parity-without-ablation 반복 금지 + 단일 표면/검증-only 승리 금지 + MT5 생략 금지 + 무제한 조합 확장 금지.
