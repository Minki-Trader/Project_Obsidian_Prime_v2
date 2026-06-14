Frontier21 개방 검토를 위해 Grok 협업 스킬과 전선20·관련 전선 기록을 먼저 확인합니다.
F17·F18·F20 기록과 기존 Grok 검토 패킷을 대조해 독립 검토를 진행합니다.
# Grok Review — Frontier21 Stage Open(전선21 단계 개방 검토)

**Review size(검토 크기):** small review(소규모 검토), bounded snapshot only(제한 스냅샷만)

**Local cross-check(로컬 대조):** F20 `preserved_clue.md`, `negative_memory.md`, `run_registry.csv`의 수치·종료 라벨은 제안 스냅샷과 일치합니다. F20 negative memory의 reopen condition(재개 조건)은 “DD containment mechanism(손실폭 억제 메커니즘) 또는 runtime representation(런타임 표현)이 바뀌는 새 가설”입니다. F21은 그 조건에 맞습니다.

---

## Decision(결정): **adjust(조정)**

F21은 **유효한 새 전선 가설(valid new frontier hypothesis, 유효한 새 전선 가설)** 이고 F20 금지 반복(forbidden repetition, 금지 반복)은 **아닙니다**. 다만 F18 negative memory(부정 기억)와 겹치는 생명주기 축 때문에 **개방 전 계약 조정(mandatory opening-contract adjustment, 필수 개방 계약 조정)** 이 필요합니다. 그래서 bare accept(그대로 수용)가 아니라 adjust입니다.

**Why not reject(거절이 아닌 이유):**
- F20이 막은 것은 train-only depth-2 rule atlas rerank(학습 전용 깊이2 규칙 지도 재순위)입니다. F21은 진입 표면을 **고정 참조 단서(fixed reference clue, 고정 참조 단서)** 로 두고 변경 변수를 lifecycle/risk stack(생명주기/위험 규칙 묶음)으로 둡니다.
- F20 preserved clue(보존 단서)는 PF·density는 괜찮지만 DD가 큰 씨앗입니다. “rule-seed + bar-level lifecycle(규칙 씨앗 + 봉 단위 생명주기)”는 F20 negative memory가 허용한 **새 메커니즘 축**입니다.
- F17(loss-cluster firewall, 손실 군집 방화벽)과 F18(model/backbone lifecycle sweep, 모델/백본 생명주기 훑기)과는 질문 구조가 다릅니다.

**Why not bare accept(그대로 수용이 아닌 이유):**
- F18은 이미 ATR stop/take(손절/익절), max-hold(최대 보유), asymmetric exit(비대칭 청산) 등 bar-level lifecycle(봉 단위 생명주기)를 ONNX 진입 신호에 씌웠고 **negative memory(부정 기억)** 로 닫혔습니다(strict/seed/preserved 0/0/0).
- F21도 같은 도구 집합을 쓰므로, **F20 씨앗 진입이 계약상 고정(lock, 잠금)** 되지 않으면 F18 재시도로 읽힙니다.

---

## Main risk(주요 위험)

1. **F18 lifecycle prior(전선18 생명주기 선행 실패)**
   F18 best row는 density는 맞았지만 OOS PF ≈ 1.0, forward clue 0입니다. F21이 “lifecycle alone purifies DD(생명주기만으로 손실폭 정화)”를 증명하지 못하면 같은 negative memory(부정 기억)로 닫힐 가능성이 큽니다.

2. **Execution-assumption mismatch(실행 가정 불일치)**
   F20 seed metrics(씨앗 지표)는 proxy atlas(프록시 지도) 기준입니다. F21이 next-bar-open + stop/take/hold(다음 봉 시가 + 손절/익절/보유)를 넣으면 PF·density·DD가 같이 바뀝니다. **같은 실행 가정 없이 F20 대비 DD 개선을 주장하면 착시**가 납니다.

3. **DD–density–PF trilemma(손실폭–빈도–수익팩터 삼각 딜레마)**
   Hypothesis의 “DD toward under 10%(손실폭 10% 미만 지향)”는 scout 단계에서 density 5~10/day와 충돌하기 쉽습니다. F20은 PF는 괜찮지만 DD가 큰 씨앗이었습니다. DD만 줄이면 **invalid setup(무효 설정)** 으로 갈 수 있습니다.

4. **Hidden entry drift(숨은 진입 표면 드리프트)**
   Lifecycle sweep(생명주기 스윕) 안에서 quantile(분위수), side(방향), conjunction(결합)을 다시 건드리면 F20 train-only atlas rerank(학습 전용 규칙 지도 재순위) 반복이 됩니다. F20이 막은 수리 경로입니다.

5. **ONNX naming overclaim(ONNX 명칭 과주장)**
   Stage 이름에 `onnx_scout`이 있지만, scout 단계에서 ONNX encode(인코딩)를 성공처럼 읽으면 F19/F20 패턴의 authority creep(권위 상승) 위험이 있습니다.

---

## Required adjustment(필수 조정)

1. **Freeze F20 seed entry in opening contract(개방 계약에서 F20 씨앗 진입 고정)**
   - Single fixed rule(단일 고정 규칙): `vix_zscore_20 <= q30 & close_ema50_ratio >= q70`, long only(롱만)
   - F20 train quantiles(학습 분위수) 그대로, validation/OOS read-only(검증/표본외 읽기 전용)
   - **No new conjunction search(새 결합 탐색 금지)**, no atlas rerank(지도 재순위 금지), no side flip(방향 전환 금지)

2. **Tier DD success criteria(손실폭 성공 기준 계층화)** — hypothesis aspiration(가설 지향)과 judgment tiers(판정 계층) 분리
   - **Scout clue(탐색 단서):** validation+OOS 양수, density 5~10/day 근처, **DD가 F20보다 분명히 낮음**
   - **Seed surface(씨앗 표면):** PF ≥ ~1.2, density 5~10/day, DD **materially below F20**(예: validation <25%, OOS <18%), single-split collapse 없음
   - **Handoff observation(인계 관찰):** PF ≥ 1.5, DD ≤ 15%, smoothness 개선 — **DD <10%는 handoff 필수 조건이 아님**
   - Hypothesis의 “under 10%”는 **exploration aspiration(탐색 지향)** 으로만 두고 scout/seed 판정에 넣지 마세요.

3. **Explicit F18 differentiation lock(전선18 차별화 잠금 명시)**
   - Entry source(진입 원천): F20 rule-seed only(규칙 씨앗만), **not** F18 model/backbone ONNX entry(모델/백본 ONNX 진입 아님)
   - Changed variable(변경 변수): lifecycle/risk profile stack(생명주기/위험 프로필 묶음) only
   - Pre-register capped lifecycle grid(사전 등록·상한 생명주기 격자): next-bar-open, ATR SL/TP, max-hold, cooldown, optional early-adverse-exit — **profile count cap(프로필 수 상한)** 필수

4. **Parity baseline row(동등성 기준 행)**
   F20 seed를 **동일 bar simulator(동일 봉 시뮬레이터)** 로 재실행한 baseline row(기준 행) 하나를 F21A에 넣으세요. 효과: lifecycle 효과와 execution-model change(실행 모델 변화)를 분리합니다. *(이 row는 비교용이지 selected baseline(선택 기준선)이 아닙니다.)*

5. **F20 negative-memory carry-forward(전선20 부정 기억 이월)**
   `do_not_repeat`: train-only depth-2 atlas rerank, capped train-risk rerank that collapses OOS PF(표본외 PF 붕괴 유발 학습 위험 재순위)

6. **Runtime probe gate unchanged(런타임 탐침 게이트 유지)**
   Handoff candidate(인계 후보)가 보여도 **pre-expensive Grok review(비싼 실행 전 그록 검토)** + local verification(로컬 검증) 전에는 MT5 work(런타임 작업) 금지

7. **F20A-style locks in `00_spec`(00_spec에 F20A식 잠금)**
   no boosted backbone(부스팅 백본 없음), no probability thresholds(확률 임계값 없음), no WFO(워크포워드 없음), no new feature engineering(새 피처 설계 없음), ONNX encode는 surviving surface 이후 후행 단계만

---

## Stop condition(중단 조건)

| Trigger(트리거) | Closeout label(마감 라벨) |
|---|---|
| Capped lifecycle sweep 후 **어떤 프로필도** F20 seed 대비 DD를 materially 낮추지 못함 | `negative_memory`: rule-seed + bar-level lifecycle alone does not purify DD-heavy seed |
| Density가 5~10/day에서 벗어나고 PF만 개선 | `invalid_setup` — frequency target missed |
| OOS PF < 1.0 또는 single-split collapse | `negative_memory` |
| Entry rule/quantile/side가 sweep 중 변경됨 | `blocked` — F20 atlas repetition |
| Density/PF만 개선, DD는 F20과 비슷 | `preserved_clue` only, handoff 없음 |
| Handoff-like row가 나와도 pre-expensive Grok + parity 미완료 | `runtime_probe_ineligible` 유지 |

F21은 **한 번의 capped scout + optional single repair pass(상한 정찰 + 선택적 단일 수리 회차)** 로 닫는 것이 맞습니다. Atlas-style rerank loop(지도식 재순위 루프)로 늘리지 마세요.

---

## Claim boundary reminder(주장 경계 알림)

- F20 preserved clue(보존 단서)는 **reference clue(참조 단서)** 일 뿐, baseline(기준선)·promotion(승격)·runtime authority(런타임 권위)가 **아닙니다**.
- F21에서 PF·DD가 좋아져도 **completion(완성)**, **live readiness(실거래 준비)**, **Goal Achieve(목표 달성)** 로 올리지 마세요.
- Handoff candidate(인계 후보)는 **observation label(관찰 라벨)** 이며, MT5 전 그록 검토와 로컬 검증 없이는 다음 단계로 넘기지 마세요.
- `onnx_scout`은 encode/distill 가능성 탐색 이름이지, ONNX 성공·런타임 권위 주장이 **아닙니다**.

---

## Advice classification for Codex(코덱스용 조언 분류)

| Item(항목) | Classification(분류) |
|---|---|
| Valid new frontier, not F20 repetition | **accepted(수용)** |
| Open after contractual locks + tiered DD criteria | **accepted(수용)** |
| Bare accept without F18/entry locks | **rejected(거절)** |
| F20 metrics as stated | **needs_local_verification(로컬 검증 필요)** — 이미 ledger와 일치 확인됨 |
| Forbidden claims (baseline/promotion/runtime authority/live/Goal Achieve) | **rejected(거절)** if proposed |

**Final Codex direction(최종 Codex 방향):** `adjust` 수용 후 `stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout` 개방. F18 negative memory와 F20 entry lock을 opening contract에 넣고, tiered DD criteria로 scout/seed/handoff를 분리하세요.
