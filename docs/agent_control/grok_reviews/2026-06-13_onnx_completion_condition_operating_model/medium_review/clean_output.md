Grok 중간 검토 요청이므로, 먼저 협업 스킬과 현재 프로젝트 진실(frontier governance, workspace state)을 읽고 그 위에서 비판 컨설팅 답을 쓰겠습니다.
# Grok Medium Review — ONNX 최종 완성 조건과 Frontier 운영 방식

**Review size:** medium review (중간 검토)
**Role:** external second opinion (외부 2차 의견) only — Codex가 최종 방향, 로컬 검증, 주장 경계를 유지
**Claim boundary:** consulting only — no training, MT5 execution, baseline, promotion, runtime authority, live readiness, Goal Achieve

---

## 한 줄 결론

Codex가 제안한 **proof ladder(증명 사다리)** 방향은 **수용(accepted)**한다.
다만 사용자가 말한 최종 완성 조건은 **scout(탐색) 단계의 hard gate(강제 게이트)가 아니라, 마지막 `final completion review(최종 완료 검토)`에서만 hard gate가 되어야** 한다.
중간 단계마다 **claim ceiling(주장 상한)**을 박아 두지 않으면, 예전처럼 “PF는 좋은데 DD가 깨짐” 같은 **repair loop(수리 반복)**가 다시 숨어든다.

---

## 1. Proof ladder — 탐색을 막지 않으면서 최종 조건을 지키는가?

**판정: accepted, with 4 changes**

Codex 사다리:

`scout clue → seed surface → WFO serious survivor → MT5 runtime probe → runtime parity → final completion review`

이 구조는 맞다. 각 층이 **다른 비용·다른 주장 상한**을 가지므로, 탐색은 넓게 열고 최종 조건은 끝까지 보존할 수 있다.

### 유지할 점

- scout(탐색)에는 gate(게이트)가 없다는 원칙은 그대로 둔다.
- 비싼 WFO/MT5 전에 **campaign map(캠페인 지도) + scoreboard(점수판)**를 먼저 두는 순서도 맞다.
- `frontier01B`를 학습 전 설계 packet(작업 묶음)으로 두는 것도 맞다.

### 바꿔야 할 4가지

**Change A — curve quality(곡선 품질)를 끝이 아니라 중간 층에 넣기**

과거 실패는 profit/density를 먼저 보고 curve를 나중에 봐서 repair loop가 커졌다.
`WFO serious survivor` 층부터 **curve pocket metric(구간 곡선 지표)**를 필수로 기록해야 한다.
Ulcer index, consecutive-loss weeks, equity flat/down pocket 같은 지표를 scout에서는 flag만, serious에서는 ranking에 넣는다.

**Change B — DD <10%는 “확장 구간 검사”를 별도 rung(단계)으로 분리**

사용자 조건은 “어떤 구간을 펼쳐도 DD <10%”다.
WFO fold 통과만으로는 부족하다. `runtime parity`와 `final completion review` 사이에
**interval expansion stress(구간 확장 스트레스)** rung을 넣어야 한다.

- rolling month / quarter
- worst regime segment
- extended OOS window

각 구간마다 DD를 다시 본다.

**Change C — proxy→MT5 gap(프록시-런타임 간극)을 ladder마다 anti-degradation rule(악화 방지 규칙)으로**

각 승격 rung마다 “Python 대비 MT5가 얼마나 나빠지면 승격 중단인가”를 미리 적는다.
예: density -30% 이상, PF -0.15 이상, trades -40% 이상이면 `runtime_probe`에서 멈춘다.

**Change D — final completion review는 일반 closeout이 아니라 전용 adversarial packet(비판 검토 전용 묶음)**

Grok 검토, full evidence stack(전체 근거 층), 사용자 목표 4축 동시 충족 여부를 한 번에 본다.
이 packet 없이는 ONNX completion(온엑스 완성)을 말하면 안 된다.

### 수정된 사다리

```text
scout clue
  → axis survivor (invalid filter 통과)
  → seed surface (WFO joint_pass_count ≥ 1)
  → wfo serious survivor (+ curve pocket audit)
  → MT5 runtime probe (+ anti-degradation)
  → runtime parity
  → interval expansion stress
  → final completion review (adversarial, full stack)
```

---

## 2. Intermediate claim labels — 최종 조건을 가장하지 않게

핵심 원칙: **라벨은 “지금 무엇이 증명됐는가”만 말하고, “사용자 목표를 달성했는가”는 말하지 않는다.**

| Label | Plain meaning | May claim | Must NOT claim |
|---|---|---|---|
| `scout_clue(탐색 단서)` | 한 축에서 흥미로운 신호가 보임 | proxy/single-window observation | seed surface, WFO survival, runtime truth |
| `axis_survivor(축 생존자)` | invalid rule을 통과한 scout 후보 | lane ranking, axis profile | joint multi-axis pass |
| `seed_surface(씨앗 표면)` | WFO에서 최소 1 fold joint pass | 다음 serious/MT5 입력 자격 | promotion, runtime authority, completion |
| `wfo_serious_survivor(WFO 진지 생존 후보)` | serious WFO에서 다축 생존 | Tier A/B/combined record | excellent ONNX, Goal Achieve |
| `runtime_probe_observation(런타임 탐침 관찰)` | MT5에서 실제 실행해 봤음 | tester output, KPI observation | runtime authority, live readiness |
| `runtime_parity_candidate(런타임 동등성 후보)` | Python ONNX와 MT5 의미가 맞음 | parity evidence | operating handoff |
| `interval_stress_survivor(구간 스트레스 생존자)` | 확장 구간 DD 검사 통과 | stress-window evidence | final completion |
| `onnx_completion_candidate(온엑스 완성 후보)` | 4축이 serious+MT5+stress에서 동시에 aspiration zone | “거의 다 왔다” 수준의 bounded claim | Goal Achieve |
| `onnx_completion(온엑스 완성)` | 사용자 최종 조건 충족 | Goal Achieve 가능 | — |

### 금지되는 upward drift(상향 드리프트)

- `scout_clue`를 `seed_surface`라고 부르지 않기
- `runtime_probe_observation`을 `runtime_authority`로 올리지 않기
- `joint_pass_count = 1`을 “excellent ONNX”로 말하지 않기
- `hold4_margin_0.01`을 baseline(기준선)이나 시작점으로 부르지 않기 — **preserved clue(보존 단서)**만

### aspiration envelope(목표 거리 점수) vs hard gate

- **scout / axis_survivor:** aspiration distance only — “목표에서 얼마나 먼가”
- **seed_surface / wfo_serious:** serious aspiration zone — 아직 최종 조건 아님
- **final completion review only:** 사용자 4축이 **hard gate**가 됨
  - density 5–10/day
  - PF 2–3x
  - DD <10% on any inspected interval
  - smooth rising equity curve

scout에서 PF 2를 못 맞춰도 탐색 실패가 아니다.
**최종 주장에서만** 못 맞추면 completion 실패다.

---

## 3. ONNX completion을 claim하려면 필요한 exact evidence layers(정확한 근거 층)

아래 **11 layers(층)**가 모두 있어야 `onnx_completion`을 말할 수 있다.

| Layer | What must exist | Why it matters |
|---|---|---|
| **L0 Identity** | model hash, ONNX hash, feature manifest, EA module hash, run manifest | “무엇을 검증했는지”가 고정돼야 함 |
| **L1 Data integrity** | Tier A sep, Tier B sep, A+B combined, split/leakage audit | 표본과 시간축이 깨지면 KPI 무효 |
| **L2 Training reproducibility** | training config, seed, export path, parity pre-check | ONNX 자체가 재현 가능해야 함 |
| **L3 WFO serious record** | 4–6+ folds, fold-level KPI on all 4 axes | single-window 착시 차단 |
| **L4 Joint multi-axis pass** | density, PF, DD, curve **동시** 기록 per fold | Stage364 `strict_joint_pass_count = 0` 반복 방지 |
| **L5 Curve quality audit** | ulcer, consecutive-loss weeks, pocket bleed flags | “돈은 벌었는데 곡선이 못생김” 차단 |
| **L6 Distinguishability** | score separation, not on/off filter behavior | filter-like surface 재발 방지 |
| **L7 MT5 runtime reproduction** | Strategy Tester output, same packet as shortlist | proxy-only completion 금지 |
| **L8 Runtime parity** | Python ONNX vs MT5 probability/trade meaning | handoff 의미 일치 |
| **L9 Interval expansion stress** | month/quarter/worst-segment DD all <10% | 사용자 “어떤 구간을 펼쳐도” 조건 |
| **L10 Adversarial closeout** | Grok review + Codex local verification receipt | 외부 비판 + 로컬 재검증 |

### 최종 hard gate 수치 (final layer only)

| Axis | Completion threshold |
|---|---|
| Density | 5–10 trades/day on routed total |
| PF | ≥ 2.0 (3.0은 strong bonus, not substitute for DD/curve) |
| Max DD | < 10% on every inspected interval |
| Curve | no 3+ week bleed pocket; visually smooth rising equity on Tier A and routed total |

**중요:** PF 2–3 + DD <10% + 5–10/day + smooth curve를 **동시에** 맞추기 어렵다.
그래서 중간 라벨은 Pareto(트레이드오프)로 보고, **completion claim은 동시 충족만** 인정한다.

---

## 4. Stage balance — packet vs new frontier stage

### 같은 frontier stage 안의 packet(작업 묶음)

- campaign map, DNR, scoreboard spec
- 같은 thesis(가설) 안의 lane scout
- 같은 lane의 repair (novelty 없음)
- 같은 serious shortlist의 WFO refinement
- governance/doc closeout

**효과:** 작은 수리마다 새 단계를 열지 않는다.

### 새 frontier stage를 열 조건

`frontier_governance.md` 기준에 더해 ONNX 맥락에서는:

| Trigger | Example |
|---|---|
| source / label / runtime / validation philosophy change | label regime 바꿈, ONNX output shape 바꿈, WFO 철학 변경 |
| prior frontier exit rule fired | scout 전 lane blocked, 또는 serious 0 survivor |
| repair chain without novelty | 같은 lane 3회 repair 후에도 joint_pass 0 |
| decision weight shift | “지도 짓기” → “wild scout” → “MT5 parity”처럼 질문 자체가 바뀜 |

### 권장 stage split

| Stage | Role | Close with |
|---|---|---|
| `stage_frontier_01` (current) | archive synthesis, axis lock, campaign map | reference surface + next frontier proposal |
| `stage_frontier_02` | ONNX multi-axis scout + WFO shortlist | seed surfaces or lane blocked memories |
| `stage_frontier_03` | MT5 runtime probe + parity + interval stress | runtime_probe_observation or parity candidate |
| `stage_frontier_04` or dedicated completion packet | final completion review | onnx_completion or explicit fail memory |

**rejected:** frontier_02에 scout + WFO + MT5 + parity + completion을 전부 넣기 — 거대 비초점 단계가 된다.

**accepted:** Codex의 frontier01B → frontier02 scout/WFO 순서.

---

## 5. Prior evidence library — inheritance 없이 consult하기

### 허용되는 consult mode(참조 방식)

| Class | Use as | Never use as |
|---|---|---|
| `preserved clue(보존 단서)` | hypothesis seed, axis profile hint | baseline, starting config, winner |
| `negative memory(부정 기억)` | invalid rule, DNR entry | reason to skip exploration |
| `reusable artifact(재사용 산출물)` | feature logic, export utility, report template | proof of current performance |
| `do-not-repeat note(반복 금지 메모)` | scout invalid filter | permanent ban on whole lane |
| `blocked retry condition(차단 재시도 조건)` | same-packet repair limit | “never try again” |

### Do-not-repeat classes(반복 금지 부류)

1. **Repair loop without novelty** — density↑ → cost↓ → DD↑ 반복
2. **Sparse PF999** — PF 매우 높음 + trades 너무 적음
3. **Proxy-only promotion** — Python만 좋고 MT5 미검증
4. **Filter-like surface** — score가 on/off 스위치
5. **Single-axis win** — 한 축만 aspiration zone
6. **Density-profit-cost triangle break** — 셋 중 둘만 OK
7. **Curve-last validation** — profit 먼저, curve 나중
8. **hold4 inheritance** — `hold4_margin_0.01`을 baseline으로 승격
9. **Strict joint pass illusion** — 한 fold 한 축만 통과를 survival로 착각
10. **Tier B omission** — combined record 없이 전체 알파 주장

### Prior library interface(접점) 형식

`frontier01B` deliverable은 **index + citation path + limit note**만:

```text
clue_id | source_stage/run | axis | numbers | limit | allowed_use | forbidden_use
```

config를 복사해 inherit(상속)하지 않는다.

---

## 6. Consulting pass 이후 첫 3 work packets

### Packet 1: `frontier01B_build_stage12_364_campaign_map_v1`

- **Family:** design / archive synthesis
- **Deliverables:** campaign map, DNR consolidated, prior evidence library interface, aspiration envelope spec, proof ladder + claim label spec
- **Gate:** 문서만, zero training
- **Close claim:** `reference surface` only

### Packet 2: `frontier02A_lane_parallel_onnx_scout_v1`

- **Family:** exploration
- **Input:** Packet 1 map + 7 lanes
- **Execution:** lane당 20–50 wild variants, proxy/single-window, scout invalid rules 적용
- **Output:** per-lane top 5 `axis_survivor` + axis profile
- **Close claim:** `scout_clue` / `axis_survivor` only

### Packet 3: `frontier02B_wfo_serious_shortlist_v1`

- **Family:** evidence
- **Input:** Packet 2 survivors only
- **Execution:** WFO 4–6 folds, Tier A/B/combined 필수, curve pocket audit, joint_pass_count primary
- **Output:** `seed_surface` or `negative memory`
- **Close claim:** `seed_surface` max — no MT5 authority

**순서 변경 rejected:** scout 전에 training 시작하기.

---

## 7. Codex advice classification — accept / reject / needs_local_verification

| Advice | Classification | Reason |
|---|---|---|
| 사용자 목표를 최종 완성 조건으로 유지 | **accepted** | 약화하면 프로젝트 의도가 깨짐 |
| 목표를 scout hard gate로 쓰지 않기 | **accepted** | 탐색 원칙과 일치 |
| proof ladder before expensive WFO/MT5 | **accepted** | repair loop 예방 |
| frontier01B campaign map 먼저 | **accepted** | 현재 next_run과 일치 |
| frontier02 = multi-axis scout + WFO shortlist | **accepted** | stage balance 적절 |
| Grok at stage open / scout shortlist / pre-WFO/MT5 / closeout | **accepted** | 비판 검토 시점 명확 |
| joint_pass_count를 primary metric | **accepted** | Stage364 교훈 반영 |
| curve quality를 WFO serious부터 강제 | **accepted** | curve-last failure 방지 |
| interval expansion stress를 별도 rung/stage로 | **accepted** | 사용자 DD 조건 충족에 필요 |
| hold4_margin_0.01을 시작점/baseline으로 | **rejected** | inheritance 위반 |
| PF 2–3를 scout default 기대치로 | **rejected** | sparse PF 착시 유발 |
| 사용자 목표를 중간 라벨에서 “달성”으로 말하기 | **rejected** | claim drift |
| 5–10 trades/day가 M5 US100에서 항상 feasible | **needs_local_verification** | cost/slippage/session 의존 |
| PF 2–3 + DD <10% + 5–10/day + smooth curve 동시 달성 가능성 | **needs_local_verification** | Pareto 현실성은 데이터로 봐야 함 |
| `stage_pipelines` ONNX orchestration naming/path | **needs_local_verification** | 첫 serious packet 전 filesystem 확인 |
| frontier_02에 MT5+parity+completion까지 포함 | **rejected** | giant unfocused stage |
| lane당 repair 3회 초과 시 blocked | **accepted** | repair loop 차단 |

**Forbidden claim check:** operating promotion, runtime authority, live readiness, selected baseline, Goal Achieve — **none proposed by this review.** ✓

---

## Codex가 가져갈 final direction(그록 종합)

1. **사용자 최종 조건은 약화하지 않는다.** 다만 scout까지는 aspiration distance(목표 거리)로만 쓰고, **final completion review에서만 hard gate**로 쓴다.
2. **frontier01B**에서 campaign map, DNR, claim labels, proof ladder, scoreboard를 먼저 고정한다.
3. **frontier02**는 scout + WFO shortlist까지만 — MT5/parity/stress는 frontier03으로 분리한다.
4. **Prior evidence는 citation-only(인용 전용)** — `hold4_margin_0.01`은 L4/L3 clue seed일 뿐, baseline 아님.
5. **Completion claim은 11 evidence layers + adversarial Grok + Codex local verification** 없이는 금지.
6. **4축 Pareto 현실성**은 인정하되, 그건 중간 탐색 순위용이지 최종 조건 완화용이 아니다.

---

## Plain meaning(쉬운 말)

지금 목표는 “대충 잘 되는 ONNX”가 아니라, **US100 M5에서 하루 5–10번 거래하면서 PF 2–3배, 손실폭 10% 미만, 곡선이 예쁘게 우상향**하는 모델이다.
그 목표는 **끝까지 유지**하되, 처음부터 그 기준으로 후보를 잘라내면 탐색이 막힌다.

그래서 **앞에서는 넓게 보고, 뒤에서 엄격하게 확인**하는 사다리가 맞다.
중간에는 “흥미롭다”, “씨앗이다”, “MT5에서 한번 봤다”까지만 말하고,
**“완성됐다”는 말은 MT5·parity·구간 확장 검사·최종 검토가 다 끝난 뒤에만** 한다.

다음 실제 행동은 **`frontier01B`로 Stage12–364 지도와 반복 금지 목록, 점수판 규칙을 먼저 고정**하는 것이다.
학습은 그 다음이다.

---

*Grok receipt note: this is conversation-based medium review. Codex should record advice classification and local verification in the work packet closeout. No operating authority created.*
