## Grok Classification(그록 조언 분류)

**`accepted_with_conditions` (조건부 수용)**

F78D를 **negative-control MT5 runtime probe(부정 대조 MT5 런타임 탐침)** 로 진행하는 방향은 스냅샷 기준으로 타당하다. F78B는 `meaningful signal count = 0`(의미 신호 0)이고 best proxy도 `scout clue only`(탐색 단서만)이므로, 이번 실행 목적은 “승격·기준선·런타임 권위”가 아니라 **proxy/runtime gap(프록시/런타임 간극) 측정**이어야 한다. 다만 **materialization(물질화)** 는 제안 그대로 실행하기 전에 아래 조건을 Codex가 로컬에서 먼저 닫아야 한다.

---

## Proceed Or Adjust?(진행 vs 조정)

**Proceed(진행):** F78D negative-control probe 자체는 진행 가능.
**Adjust before execution(실행 전 조정 필수):** “재학습 → ONNX → veto tape → 고정 TP/SL → val/OOS tester” 흐름은 유지하되, **P/L 해석 전**에 parity gate(동등성 게이트)를 넣어야 한다. P/L을 먼저 읽으면 gap measurement(간극 측정)가 calibration noise(보정 잡음)에 오염된다.

---

## Top Proxy/Runtime Gap Risks(상위 프록시/런타임 간극 위험)

1. **`CONTRACT_PNL_SCALE` proxy drift(프록시 보정 표류)**
   F77 gross-profit scale 평균 기반이라 broker contract P/L(브로커 계약 손익)과 직접 대응하지 않는다. proxy net/PF와 MT5 net/PF를 1:1 비교하면 false gap(가짜 간극) 또는 false parity(가짜 동등)가 난다.

2. **Entry semantics mismatch(진입 의미 불일치)**
   Proxy는 `next raw bar open after feature timestamp`(피처 시각 다음 원천 봉 시가). MT5는 bar open fill, spread, slippage, order type에 따라 달라진다. density/lifecycle(밀도/생명주기) 차이의 1순위 원인이다.

3. **Threshold / signal-selection drift(임계값·신호 선택 표류)**
   `q0.72` train quantile + `logistic_l2_balanced`는 proxy selected timestamps와 MT5 signal count가 어긋나기 쉽다. veto tape 비교 없이 trade KPI를 읽으면 probe가 무의미해진다.

4. **ONNX schema / feature-order parity(ONNX 스키마·피처 순서 동등성)**
   Export는 family smoke(`in_memory_skl2onnx_smoke_passed`) 수준이고, **selected candidate `f78b_02234` 전체 파이프라인 parity**는 아직 증명되지 않았다. `contract_core` feature order, scaling, short-only 3-column schema가 EA와 맞지 않으면 음성 대조가 아니라 구현 오류 probe가 된다.

5. **Fixed TP/SL point semantics(고정 TP/SL 포인트 의미)**
   TP `2600.0`, SL `1600.0`, point scale `100`은 preserved mechanic(보존 메커니즘)일 뿐 broker authority가 아니다. US100 M5에서 price/point 변환이 어긋나면 lifecycle occupancy(생명주기 점유)와 DD가 proxy와 완전히 달라진다.

6. **Weak proxy base + axis-sweep overfit(약한 프록시 기반 + 축 탐색 과적합)**
   상위 행 다수가 OOS trade 1~3, PF `999.0` 같은 sparse-artifact(희소 표본 인공물)를 보인다. `f78b_02234`도 PF·calendar_tpd가 final target 미달이라, runtime에서 “약한 양성”이 나와도 meaningful signal로 승격하면 안 된다.

---

## Required Local Verification(필수 로컬 검증)

Codex가 Grok 없이 로컬에서 먼저 닫아야 할 최소 목록:

| Priority | Verification(검증) | Pass criterion(통과 기준) |
|----------|-------------------|---------------------------|
| 1 | **Selected-candidate export parity** — `f78b_02234` full re-train → ONNX, not family smoke only | Same feature hash/order, threshold artifact, model bundle identity |
| 2 | **Signal-count parity** — proxy selected-entry set vs MT5 veto tape | Count + timestamp alignment within agreed bar tolerance; mismatch rate logged |
| 3 | **Entry-bar parity** — feature closed-bar key → next-bar open | First executable bar matches proxy rule on sample window |
| 4 | **TP/SL price conversion** on US100 FPMarkets | Broker points → price matches intended H18/TP26/SL16 mechanic |
| 5 | **Short-only inference** — `[p_short, p_flat, p_long=0]` | EA reads 3 columns correctly; no long-side leakage |
| 6 | **Split-window identity** | Validation/OOS tester windows match proxy split calendar boundaries |

**P/L comparison은 위 1–6 이후에만** 허용한다.

---

## Forbidden Claim Risk(금지 주장 위험)

claim boundary(`pre_mt5_review_only...`)를 넘기면 안 되는 주장:

- F78B `f78b_02234`를 **meaningful signal**, **promotion candidate**, **baseline**으로 말하기
- F78D negative-control 결과로 **runtime authority**, **live readiness**, **Goal Achieve** 주장
- `CONTRACT_PNL_SCALE` 또는 proxy net/PF를 **broker-authoritative P/L**처럼 말하기
- OOS PF `1.28`, calendar_tpd `1.25`를 “목표 근접”으로 읽고 **운영 승격**으로 연결하기
- veto tape / signal parity 없이 tester net/PF만으로 “execution-calibrated hypothesis validated”라고 말하기
- sparse top-row artifacts(PF `999`, trades `1`)를 대표 증거로 끌어오기

허용되는 주장 범위: **“proxy scout clue exists; runtime gap measured under negative control; parity pass/fail recorded.”**

---

## Smallest Useful MT5 Probe Scope(가장 작은 유용 MT5 탐침 범위)

**Single-candidate, signal-first, validation-only first pass:**

1. **One candidate only:** `f78b_02234`
2. **One direction/schema:** short-only ONNX 3-column
3. **One window first:** validation split only (OOS는 narrow parity gate 통과 후)
4. **One broker setup:** US100 M5, fixed TP/SL, `cd6`, session `all`, risk `none`
5. **Primary KPI order:**
   - signal count vs proxy selected count
   - entry timestamp alignment rate
   - then trades, calendar_tpd, PF, net (labeled **non-authoritative vs proxy**)
6. **Explicit negative-control label:** success = “gap documented with parity evidence,” not “strategy works”

OOS tester는 validation에서 **signal-count parity가 허용 범위**일 때만 추가한다. 그렇지 않으면 OOS는 gap 원인 분해에 도움이 안 되고 noise만 늘린다.

---

## Summary For Codex(코덱스 요약)

| Item | Grok advice |
|------|-------------|
| Classification | **`accepted_with_conditions`** |
| Direction | F78D negative-control probe **진행 가능** |
| Blocker | **Materialization parity gates** 미충족 시 실행 금지 |
| Read order | Signal parity → entry parity → lifecycle → P/L last |
| Claim ceiling | Gap measurement only; no promotion/runtime authority |

**한 줄 결론:** 제안된 F78D는 “약한 scout clue를 runtime에서 어떻게 깨지는지 보는 음성 대조”로는 맞다. 다만 **selected-candidate export parity와 veto-tape signal parity**를 먼저 닫지 않으면, tester 실행은 조기에 해도 **간극 측정이 아니라 구현 검증 실패**로만 끝날 위험이 크다.
