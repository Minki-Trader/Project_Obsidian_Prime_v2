Bounded evidence와 Grok 협업 규칙을 먼저 확인한 뒤, Frontier04 개방 제안을 검토하겠습니다.
## 1. Recommendation(권고)

**`open_frontier04(전선04 개방)`**

Frontier04(전선04)는 Frontier03(전선03)의 threshold/decision-surface repair loop(임계값/결정 표면 수리 반복)와는 다른 축이다. 라벨 outcome definition(라벨 결과 정의)을 close-return(종가 수익률)에서 path event(경로 이벤트)로 바꾸는 것은 Frontier03 negative memory(부정 기억) — “close-only profitable-looking labels with validation DD(종가만 보면 수익처럼 보이지만 검증 손실폭이 큰 라벨)” — 에 직접 대응한다.

다만 `revise_direction(방향 수정)` 수준의 한 가지 보완은 필요하다: prior-stage scan(이전 단계 점검)에 archive barrier/path labeling(보관소 장벽/경로 라벨링), 예를 들어 `stage355`의 `first_barrier_labels`, 를 **reusable artifact(재사용 산출물)** 로 명시해 novelty claim(신규성 주장)을 과장하지 말 것.

---

## 2. Reasoning(근거)

**Frontier03과의 거리**

Frontier03B(전선03B)는 `future_log_return_12`(12봉 미래 로그 수익률) 위에 regime-conditioned asymmetric threshold(체제 조건부 비대칭 임계값)만 바꿨다. PnL(손익)도 같은 close return(종가 수익률)이다. 이후 03C–03G 수리는 ONNX(온엑스)와 decision surface(결정 표면: threshold/margin/cooldown) 쪽이었다.

Frontier04(전선04)는 **라벨 철학(label philosophy, 라벨 철학)** 을 먼저 바꾼다: next-bar high/low path(다음 봉 고가/저가 경로), target/stop hit(목표/손절 도달), timeout(시간 만료), event-first rule(이벤트 우선 규칙). 이는 “같은 교사에 또 sweep(같은 교사에 또 스윕)”이 아니라 **broken artifact(고장 산출물)의 원인 축** 을 건드린다.

**Frontier03 preserved clue(보존 단서)와의 관계**

`f03e_repair` OOS PF/DD(표본밖 수익 팩터/손실폭)는 좋지만 validation DD 15.5%(검증 손실폭)는 close-path mismatch(종가 경로 불일치) 가설을 뒷받침한다. Frontier04(전선04)는 그 단서를 **reference only(참조 전용)** 로 두고, “path-aware labels가 validation DD를 줄이는가?”를 먼저 proxy(프록시)로 시험하는 순서가 맞다.

**Bounded enough(경계 충분)**

- 첫 실행은 Frontier04B proxy-only(프록시 전용) — ONNX/WFO/MT5 없음  
- 후보군 3개 target/stop(목표/손절) 배수 — broad sweep(넓은 스윕) 아님  
- stop condition(중지 조건)이 joint density/PF/DD(밀도/수익 팩터/손실폭 동시성) 실패 시 negative memory(부정 기억) — Frontier03 “do not repeat broad sweeps(넓은 스윕 반복 금지)”와 정합

**왜 `do_not_open(개방 금지)`가 아닌가**

Frontier03 closeout(마감)이 이미 “new hypothesis lifecycle(새 가설 생명주기)”를 다음 행동으로 적었다. path-aware labeling(경로 인식 라벨링)은 그 지시와 일치한다. 개방 금지는 “또 같은 수리”일 때만 타당한데, 이번 제안은 수리가 아니라 **label source change(라벨 원천 변경)** 이다.

**왜 완전한 `revise_direction`이 아닌가**

방향 자체는 타당하다. 수정은 방향 교체가 아니라 **경계 강화** 와 **archive honesty(보관소 정직성)** — stage355 barrier precedent(선례) 인용 — 수준이다.

---

## 3. Required bounds for Frontier04B(전선04B 필수 경계)

1. **Proxy-only gate(프록시 전용 게이트)**  
   Frontier04B(전선04B) 끝까지 ONNX training/export, WFO, MT5 금지. 효과(effect, 효과): Frontier03 “oracle ≠ trainable ONNX(오라클 ≠ 학습 가능 온엑스)” 반복을 막는다.

2. **OHLC alignment preflight(원천 OHLC 정렬 사전 점검)**  
   `bars_us100_m5_mt5api_raw.csv`를 model input timestamps(모델 입력 타임스탬프)에 join하기 **전에** row-level alignment manifest(행 단위 정렬 목록)를 만든다. `timezone_status: UNRESOLVED_REQUIRES_MANUAL_BINDING`(시간대 미해결)이면 KPI 주장 금지.

3. **Controlled comparison(통제 비교)**  
   각 path label variant(경로 라벨 변형)마다 **같은 행·같은 split(분할)** 에서 close-return proxy baseline(종가 수익률 프록시 기준선), 예: Frontier03-style `future_log_return_12` threshold proxy, 와 나란히 기록한다. 효과: “path가 DD를 줄였는가”를 orphan metric(고립 지표)이 아니라 paired delta(쌍 비교)로 본다.

4. **Fixed variant grid(고정 변형 격자)**  
   제안된 3 target/stop × 2 horizon(12/18)만. 추가 multiplier sweep(배수 스윕), regime overlay(체제 오버레이), margin/cooldown repair(마진/쿨다운 수리) 금지 — Frontier03 do-not-repeat(반복 금지)와 동일 선상.

5. **Event semantics contract(이벤트 의미 계약)**  
   event-first(이벤트 우선), same-bar ambiguity(동일 봉 모호), timeout label(시간 만료 라벨), cost deduction point(비용 차감 시점)를 run manifest(실행 목록)에 고정한다. stage355 `first_barrier_labels`와 차이가 있으면 diff(차이)를 적는다.

6. **Leakage audit(누수 감사)**  
   라벨은 future OHLC만 사용, features(피처)는 closed-bar only(종료봉 전용). label construction(라벨 생성)에 `feature_set_v2` 컬럼을 넣지 말 것.

7. **Joint scout success(동시 탐색 성공 기준)**  
   validation **and** OOS(검증 **및** 표본밖) 모두에서 density ≥ ~4.5/day, PF > 1.2, DD < 10% — **동시 충족** 행이 ≥1개. OOS-only clue(표본밖 단서만)는 Frontier03과 같은 preserved clue(보존 단서)로만 취급.

8. **Sparse/PF999 guard(희소/PF999 방어)**  
   PF≥999 + sparse sample(희소 표본) 행은 success row(성공 행)에서 제외. Frontier03 oracle trap(오라클 함정) 반복 금지.

9. **Tier discipline(티어 규율)**  
   Tier A: model input rows + raw OHLC. Tier B: `missing_required(필수 누락)` — paired materialization(쌍 물질화) 전까지 합산 주장 금지.

10. **Hard stop(강제 중지)**  
    joint improvement row 0개면 negative memory close(부정 기억 마감). threshold-only retry(임계값만 재시도) 금지.

---

## 4. Risks(위험)

| Risk(위험) | Why it matters(왜 중요한가) |
|---|---|
| **Timezone/alignment failure(시간대/정렬 실패)** | `UNRESOLVED_REQUIRES_MANUAL_BINDING`이면 path labels(경로 라벨)가 잘못된 bar(봉)에 붙어 전체 scout(탐색)가 invalid(무효) |
| **False novelty(가짜 신규성)** | Barrier-style labeling(장벽형 라벨링)은 archive에 이미 있다. 실패 시 “새 가설”이 아니라 “archive replay without ONNX bridge(온엑스 연결 없는 보관소 재생)”로 닫힐 수 있음 |
| **Proxy-to-ONNX transfer gap(프록시→온엑스 전달 간극)** | Frontier03이 이미 보여줌: 좋은 label proxy(라벨 프록시) ≠ trainable joint KPI(학습 가능 동시 KPI) |
| **Density collapse(밀도 붕괴)** | Tighter stops(더 타이트한 손절)는 DD(손실폭)는 줄이지만 density(밀도)를 4.5/day 아래로 떨어뜨릴 수 있음 — F03 density/DD trade-off(밀도/손실폭 트레이드오프) 재현 위험 |
| **Ambiguous same-bar bias(동일 봉 모호 편향)** | US100 M5(5분봉)에서 TP/SL same-bar(동일 봉 동시 도달) 비율이 높으면 label noise(라벨 잡음)로 proxy가 흔들림 |
| **Cost model mismatch(비용 모델 불일치)** | rough cost(대략 비용)가 close-return scout(종가 수익률 탐색)과 path PnL(경로 손익)에서 다르게 적용되면 paired comparison(쌍 비교)이 왜곡됨 |

---

## 5. Do-not-claim boundary(주장 금지 경계)

Codex(코덱스)와 이후 단계에서 **주장하면 안 되는 것**:

- `winner(승자)`, `selected baseline(선택 기준선)`, `operating promotion(운영 승격)`, `runtime authority(런타임 권위)`, `live readiness(실거래 준비)`, `Goal Achieve(목표 달성)` — Frontier governance(전선 운영 규칙) 그대로
- Frontier04B proxy success(프록시 성공) → “trainable ONNX promise(학습 가능 온엑스 약속)”
- OOS-only positive(표본밖만 양호) → “validation DD problem solved(검증 손실폭 문제 해결)” — Frontier03 preserved clue(보존 단서)와 같은 trap(함정)
- PF999 / tiny sample(작은 표본) → positive scout row(양성 탐색 행)
- OHLC alignment 미검증 상태에서 Tier A alpha read(티어 A 알파 판독)
- “완전히 새로운 labeling paradigm(완전히 새로운 라벨링 패러다임)” — archive barrier work(보관소 장벽 작업) 무시 시 overclaim(과장 주장)
- Frontier03 surface `p40/m4/cd6`를 Frontier04(전선04) baseline(기준선)으로 inherit(상속)

**허용되는 주장 범위(개방 후):**  
“Frontier04 opened(전선04 개방됨) as label-philosophy pivot(라벨 철학 전환)”; “Frontier04B proxy completed with clue / negative memory / blocked(프록시 완료: 단서/부정 기억/차단)”; “path labels improved vs close-return proxy on joint validation+OOS KPI(경로 라벨이 종가 프록시 대비 검증+표본밖 동시 KPI 개선)” — **로컬 검증 후에만**.

---

**Grok classification hint for Codex(코덱스용 조언 분류 힌트):**  
- **Accepted(수용):** open Frontier04; Frontier04B proxy-first; keep F03 clue reference-only  
- **Needs local verification(로컬 검증 필요):** OHLC alignment, leakage audit, stage355 prior-artifact citation, paired close-vs-path comparison  
- **Rejected(거절):** inherit F03 surface as baseline; WFO/MT5 before proxy; broad threshold sweeps
