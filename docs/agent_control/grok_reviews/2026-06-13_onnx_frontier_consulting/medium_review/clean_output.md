Grok 협업 스킬과 현재 프로젝트 상태를 먼저 확인한 뒤, ONNX frontier 구조에 대한 bounded consulting 답을 정리하겠습니다.
# Grok Medium Review — ONNX Frontier 구조 제안

**Review size:** medium review (중간 검토)
**Claim boundary:** consulting only — no training, MT5, baseline, promotion, runtime authority
**Receipt trigger:** ONNX frontier structure after foundation complete

---

## 한 줄 결론

Codex가 제안한 방향은 **accepted(수용)**.
다만 사용자 목표(5–10 trades/day, PF 2–3x, DD <10%, 매끈한 equity)는 **동시 달성 가능성이 낮다** — Pareto 탐색 표면으로 두고, scout(정찰)와 serious(WFO) 두 층으로 나눠야 repair loop(수리 반복)를 막을 수 있다.

---

## 1. 목표 현실성 — adversarial check

| 축 | 사용자 목표 | Stage364 preserved clue | 판정 |
|---|---|---|---|
| Density | 5–10/day | 1.7–3.0/day (probe 기준) | **needs_local_verification** — M5 US100에서 5–10/day는 비용·슬리피지 부담 큼 |
| PF | 2–3x | 1.05–1.39 | **rejected as joint default** — 단일 윈도우 scout에서 PF 2+는 흔히 sparse sample(표본 부족) 착시 |
| DD | <10% | curve quality 반복 실패 | **aspirational only** — WFO fold마다 10% 미만은 매우 까다로움 |
| Curve | smooth rising | repeated failure | **valid axis** — 별도 curve metric 필요 |

**그래도 탐색하는 법:** 목표를 **hard gate(하드 게이트)**가 아니라 **aspiration envelope(목표 거리 점수)**로 쓴다.
scout 단계에서는 “PF 2 달성”이 아니라 “PF·density·DD·curve 4축 중 몇 축이 동시에 aspiration zone에 들어왔는가”로 순위를 매긴다.

---

## 2. Wild exploration vs evidence — 두 층 분리

```
┌─────────────────────────────────────────────────┐
│  SCOUT LAYER (정찰층) — gate 없음, 비용 낮음      │
│  • single-window OK, proxy OK, wild variants OK  │
│  • invalid = 즉시 폐기 (아래 §4)                  │
│  • output = lane survivor list + axis profile   │
└────────────────────┬────────────────────────────┘
                     │ top N per lane only
┌────────────────────▼────────────────────────────┐
│  SERIOUS LAYER (진지층) — WFO default             │
│  • Tier A sep / Tier B sep / A+B combined 필수  │
│  • joint multi-axis pass 필요                     │
│  • MT5 claim은 같은 packet에서 external verify   │
└─────────────────────────────────────────────────┘
```

효과: Stage12–364의 “한 축 고치면 다른 축 깨짐” 패턴을 scout에서 걸러내고, serious 층에서만 강한 주장을 허용한다.

---

## 3. Search lanes — 7개 노선

각 lane은 **독립 scout batch**로 돌리고, lane 간 winner inheritance(승자 상속)는 금지.

| Lane | 탐색 대상 | Stage364에서 배운 것 |
|---|---|---|
| **L1 Model/Label** | horizon, regime label, cost-aware label, multi-head | label pivot은 density는 올렸으나 joint pass 0 |
| **L2 Feature/Source** | feature set, source mix, distinguishability test | proxy signature collapse, filter-like surfaces |
| **L3 Decision surface** | threshold, probability-bin veto, calibration | bin veto는 net+지만 density/cost tradeoff 잔존 |
| **L4 Risk/Exit** | hold time, margin, SL/TP, trailing | hold4_margin_0.01은 clue만, authority 아님 |
| **L5 Routing** | Tier A primary + B fallback, throttle | weak-clock throttle instability |
| **L6 Calibration** | Platt/isotonic, score monotonicity | candidate distinguishability failure |
| **L7 Curve-shaping** | equity pocket quality, consecutive-loss weeks | density/profit seed without curve-pocket quality |

**accepted:** L7 curve-shaping lane을 별도로 둔다 — 과거 campaign에서 curve가 마지막에야 검증돼 repair loop를 키웠다.

---

## 4. Multi-axis scoreboard — exploration을 막지 않는 점수판

### Scout scoring (정찰 점수) — hard reject만

즉시 **invalid(무효)** 조건 (DNR에서 가져옴):

- `strict_sample_floor`: WFO fold당 trades < 30 → PF 무시
- `distinguishability_fail`: active/flat score separation < threshold
- `proxy_signature_collapse`: feature importance 단일 축 > 90%
- `pf999_sparse`: PF > 5 AND total trades < 200
- `one_axis_only`: 한 축만 aspiration zone, 나머지 3축 전부 fail

Survivor ranking (생존자 순위):

```
scout_score = w1·norm(density) + w2·norm(PF) + w3·(1-norm(DD)) + w4·norm(curve_quality)
            - penalty(one_axis_only) - penalty(cost_blind)
```

weights는 고정; scout 중 tuning 금지 (overfit 방지).

### Serious scoring (진지 점수) — WFO joint pass

WFO fold마다 4축 동시 기록:

| Axis | Scout flag | Serious aspiration | Serious hard fail |
|---|---|---|---|
| Density | 2–12/day band | 5–10/day zone | <1/day or >15/day |
| PF | >1.1 | ≥1.8 (2–3은 bonus) | <1.0 on ≥2 folds |
| Max DD | flag >15% | <12% per fold | >20% any fold |
| Curve | Ulcer / consec-loss weeks | Ulcer <5, no 3-week bleed | 4+ week equity flat/down |

**joint_pass_count** = 4축 모두 serious aspiration 동시 충족 fold 수.
Stage364의 `strict_joint_pass_count = 0`을 반복하지 않으려면 이 숫자가 primary metric이다.

**accepted:** Codex의 “multi-axis scoreboard before expensive execution” — scout invalid 조건 + serious joint_pass_count 구조.

---

## 5. Project-specific failure modes — 반복 금지

| Failure mode | 증상 | Frontier 대응 |
|---|---|---|
| Repair loop | density↑ → cost↓ → density↓ | lane별 scout → serious 승격만 허용; 같은 lane 3회 repair면 blocked |
| Sparse PF999 | PF 9.99, trades 40 | `pf999_sparse` invalid rule |
| Proxy≠runtime | Python 좋음, MT5 나쁨 | serious 층 MT5는 같은 packet; scout는 proxy only claim |
| Filter surface | score가 on/off 스위치 | distinguishability test를 L2/L3 공통 gate |
| Density-profit-cost triangle | 셋 중 둘만 OK | joint_pass_count primary; single-axis promotion 금지 |
| hold4 inheritance | margin 0.01을 baseline으로 씀 | **rejected** — preserved clue로만 L4 seed |

---

## 6. Frontier stage 구조 제안

### stage_frontier_01 (현재) — 마감 조건

아직 남은 것: **ONNX campaign map + DNR consolidation + next frontier proposal** (`frontier01B`).

### stage_frontier_02 — 제안 canonical id

`stage_frontier_02__onnx_multi_axis_scout_and_wfo_shortlist`

- **frontier_thesis:** wild ONNX variant scout로 lane survivor를 찾고, WFO serious 층에서 joint multi-axis pass 후보를 좁힌다.
- **novelty_delta:** Stage12–364 repair chain이 아니라 lane-parallel scout + pre-defined invalid + joint_pass_count primary.
- **claim_boundary:** scout = exploration only; serious survivor = `promotion_candidate`도 아님, `seed surface`까지만.

**rejected:** frontier_02를 “hold4_margin_0.01 개선”으로 열기 — inheritance 위반.

**needs_local_verification:** `stage_pipelines` ONNX orchestration naming — 첫 serious packet 전에 확인.

---

## 7. 첫 1–3 concrete work packets

### Packet 1: `frontier01B_onnx_campaign_map_and_scoreboard_spec_v1`

**Lane:** design only, zero training
**Deliverables:**

- ONNX campaign map (82 stage → 7 lane 분류)
- DNR list (negative_result_register + Stage364 합침)
- scout invalid rules + serious joint_pass_count spec
- aspiration envelope 정의 (사용자 목표를 수치화)

**Gate:** 문서만; 실행 없음.

### Packet 2: `frontier02A_lane_parallel_scout_sweep_v1`

**Lane:** exploration
**Execution:**

- lane당 20–50 wild variants (brute-force OK)
- proxy only, single-window, Tier A sep 기록
- Tier B sep / combined: 만들 수 없으면 `missing_required` 명시
- output: lane별 top 5 survivor + axis profile

**Stop:** invalid rate > 80% lane은 “lane blocked” 기록 후 다음 lane.

### Packet 3: `frontier02B_wfo_serious_shortlist_v1`

**Lane:** evidence
**Input:** Packet 2 survivors only (cross-lane merge 금지)
**Execution:**

- WFO 4–6 folds minimum
- Tier A / B / combined 필수
- joint_pass_count ≥ 1인 것만 `seed surface` 기록
- MT5 probe: joint_pass ≥ 1 후보만, 같은 packet

**Claim:** `seed surface` or `preserved clue` only — no promotion candidate.

---

## 8. Advice classification summary

| Advice | Classification |
|---|---|
| Foundation 후 ONNX frontier 별도 개방 | **accepted** |
| Scout/serious 두 층 | **accepted** |
| 7 search lanes + curve-shaping | **accepted** |
| joint_pass_count를 primary metric | **accepted** |
| 사용자 목표를 hard gate로 쓰기 | **rejected** — aspiration envelope로 대체 |
| hold4_margin_0.01을 시작점으로 상속 | **rejected** |
| PF 2–3x를 scout default 기대치로 | **rejected** |
| 5–10 trades/day를 M5 US100에서 무조건 가능 | **needs_local_verification** |
| stage_pipelines naming | **needs_local_verification** |
| frontier01B campaign map 먼저 | **accepted** |
| lane당 repair 3회 초과 시 blocked | **accepted** |

**Forbidden claim check:** operating promotion, runtime authority, live readiness, selected baseline, Goal Achieve — **none proposed**. ✓

---

## 9. Codex final direction (Grok synthesis)

1. **frontier01B**로 ONNX campaign map + scoreboard spec + DNR를 먼저 고정한다 (비용 0).
2. **frontier02**를 `multi_axis_scout_and_wfo_shortlist`로 연다 — wild scout 허용, serious는 WFO + joint_pass_count.
3. 사용자 목표는 **“찾고 싶은 거리”**로만 쓰고, scout/serious hard gate로 쓰지 않는다.
4. Stage364 clue는 L4/L3 **참고 시드**일 뿐; winner/baseline으로 쓰지 않는다.
5. PF 2–3 + DD <10% + 5–10/day + smooth curve를 **동시에** 기대하면 실망 확률이 높다 — 대신 **4축 Pareto frontier**를 보고 “어느 축을 희생할지”를 각 seed surface마다 명시하게 한다.

이 구조면 aggressive exploration은 허용하면서, Stage12–364식 fragmented repair loop와 weak result overclaim을 같은 scoreboard로 막을 수 있다.
