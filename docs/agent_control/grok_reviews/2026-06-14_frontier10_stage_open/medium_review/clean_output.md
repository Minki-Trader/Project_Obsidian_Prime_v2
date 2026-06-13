Frontier10 stage-open 검토를 위해 Grok 협업 스킬과 프로젝트 현재 상태, Frontier07–09 맥락을 먼저 확인합니다.
## Grok Stage-Open Review(그록 단계 개방 검토)

**Review size(검토 크기):** medium review(중간 검토)
**Primary classification(주 분류):** **accepted(수용)** — bounded conditions(조건부 경계) 포함
**Claim boundary(주장 경계):** stage-open design only(단계 개방 설계만). completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

---

### Conclusion(결론)

Frontier10(전선10) `stage_frontier_10__split_consistent_utility_distillation` 개방을 **수용**합니다.

**Plain meaning(쉬운 설명):** Frontier07~09(전선07~09)는 “어떤 행을 long/short/flat(매수/매도/관망)으로 라벨링할지” 표현을 바꿨지만, 검증 손실폭(validation DD)은 56~64%에 머물렀고 엄격 탐색 단서(strict scout clue)는 0이었습니다. Frontier10은 **모델 학습 전에** “학습 구간 여러 하위창(subwindow)에서 효용(utility)이 안정적으로 합의된 행만 거래 라벨로 남긴다”는 **감독 철학**을 바꿉니다. 이는 Frontier09의 density bridge repair(밀도 브리지 수리) 반복이 아니라, 다음 가설 생명주기(hypothesis lifecycle)로 타당합니다.

로컬 확인: `workspace_state.yaml`은 Frontier09 마감·`frontier10A` 다음 실행을 가리키고, Frontier09 closeout(마감)은 validation DD 56~64%, strict rows 0, bridge repair 반복 금지를 기록합니다.

---

### 1. Novelty delta(신규성 차이)

| Axis(축) | F07 | F08 | F09 | F10 (proposed) |
|---|---|---|---|---|
| Changed variable(바뀐 변수) | risk-shaped labels(위험 형성 라벨) | sample weights(표본 가중) | clean-path label contract(깨끗한 경로 라벨 계약) | **subwindow-stable utility distillation(하위구간 안정 효용 증류)** |
| When constraints apply(제약 시점) | label build(라벨 생성) | train loss(학습 손실) | label build + bridge repair(라벨 + 브리지 수리) | **before model fit(모델 적합 전)** |
| DD intent(손실폭 의도) | adverse excursion scoring | reweight bad rows | bad-path → flat | **unstable/conflicted/DD-heavy → flat via consensus(불안정/충돌/고DD → 합의로 관망)** |

**vs Frontier09 bridge repair(전선09 브리지 수리):** F09C는 class-prior bridge(클래스 사전분포 브리지)로 밀도를 맞췄지만 validation DD는 개선되지 않았습니다. F10의 핵심은 **추론 후 브리지가 아니라 라벨 생성 시 분할 일관성**입니다. → novelty failure(신규성 실패) 회피에 충분합니다.

**vs Stage295 archive(295단계 보관소) — acknowledged overlap(겹침 인정), not blocking(차단 아님):**

`NEG-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION`은 MT5 route-signal distillation(MT5 경로 신호 증류) + validation damage veto(검증 손상 거부)였고, ONNX-worthy candidate(온엑스 가치 후보)로 닫히지 않았습니다.

F10은 다른 레인(lane)입니다:
- Python Tier A oracle-label scout(F07~F09 패턴)
- train subwindow consensus(학습 하위구간 합의) — S295에 없는 명시 메커니즘
- argmax-only, no threshold search(최대확률 전용, 임계값 탐색 없음)
- WFO/MT5는 strict clue(엄격 단서) + Grok pre-expensive review(비싼 검증 전 그록 검토) 전까지 금지

**Effect(효과):** archive reference(보관소 참조)는 필수이지만, S295 실패가 F10 개방을 막지는 않습니다. `prior_stage_scan(이전 단계 점검)`에 `difference_from_stage295(295단계 대비 차이)`를 적어야 “이름만 같은 재시도” 논쟁을 막을 수 있습니다.

**Family overlap risk(가족 겹침 위험) — medium(중간):**

- `drawdown_veto_distillation` ≈ F09 underwater/clean-path + F07 adverse burden
- `utility_margin` ≈ F07 payoff/adverse ratio

**Accepted if(수용 조건):** stage brief(단계 개요)에 family별 `difference_from_f07(전선07 대비)` / `difference_from_f09(전선09 대비)`를 적고, F10B scout(탐색)에서 **class-prior density bridge 금지**를 명시합니다.

---

### 2. Leakage boundary(누수 경계)

**Accepted design elements(수용 설계 요소):**

- features = current/past closed bars only(피처 = 현재/과거 확정봉만)
- future path utility = label construction only(미래 경로 효용 = 라벨 생성 전용)
- thresholds/scales fit on train split only(임계값/스케일 = 학습 분할만 적합)
- oracle labels ≠ runtime signals(오라클 라벨 ≠ 런타임 신호) — claim boundary 적절

**Needs local verification at implementation(구현 시 로컬 검증 필요):**

1. **Subwindow containment(하위구간 포함):** 모든 subwindow(하위구간)가 train split(학습 분할) 안에만 있어야 합니다. validation/OOS 경계를 걸치면 consensus(합의)가 누수(leakage)입니다.
2. **Consensus statistics(합의 통계):** margin/threshold(마진/임계값)는 train subwindow rows(학습 하위구간 행)에서만 fit(적합)되어야 합니다.
3. **drawdown_veto “historically”(역사적 손실폭 거부):** underwater burden(수중 부담) 통계가 전체 샘플·검증 구간을 쓰지 않는지 확인합니다. F07 `base_scale = train quantile`(학습 분위수) 패턴을 따르면 안전합니다.
4. **Evaluation-only val/OOS(평가 전용 검증/표본밖):** val/OOS는 라벨 파라미터 적합에 쓰이지 않아야 합니다.

F07 `path_arrays` + label build 패턴과 동일한 경계를 유지하면 scout lane(탐색 레인)에서는 허용됩니다.

---

### 3. Controls(대조군)

**Strong enough(충분함):**

- `label_v1` reference — 절대 기준선이 아닌 비교 축
- **Frontier07 risk label** — 가장 중요한 대조군 (라벨 기하만 vs 합의 증류)
- **Frontier09 payoff/adverse ratio preserved clue** — 참조 전용, F09 대비 개선 측정
- matched sklearn specs + ONNX parity + 동일 scout gates(밀도 5–10/day, PF≥1.2, DD≤15%)

**Recommended addition(권장 추가):**

- **Frontier08 best sample-weight row(전선08 최상 가중 행)** — “가중만으로는 DD가 안 고쳐짐”을 같은 표에서 재확인
- **Explicit no-bridge control(명시적 무브리지 대조):** F10B에서 class-prior/density bridge 없이 argmax-only만 — F09C 실패 반복 방지

**Effect(효과):** winner/baseline(승자/기준선) 상속 없이도 F07/F08/F09 대비 paired axis(짝 축) 판정이 가능합니다.

---

### 4. Better next move than label/weight/bridge repair?(라벨/가중/브리지 수리보다 나은 다음 행동?)

| Alternative(대안) | Verdict(판정) |
|---|---|
| F09-style clean-path density bridge repair | **Reject(거절)** — negative memory(부정 기억) 명시 금지 |
| F08-style more sample weighting | **Reject(거절)** — validation DD 58~60% 미해결 |
| F07-family rename without subwindow consensus | **Reject(거절)** — novelty failure |
| **F10 split-consistent utility distillation** | **Accept(수용)** — supervision philosophy shift(감독 철학 전환) |

**Plain meaning:** F07~09는 “정답지/공부 비중/경로 표현”을 바꿨지만, **어떤 행이 ‘진짜 배울 가치가 있는지’를 먼저 거르지는 않았습니다**. F10은 그 필터를 라벨 단계로 올립니다. validation DD가 고정된 패턴(0 strict, high val DD)에 대한 합리적 다음 축입니다.

**Primary failure mode(주요 실패 모드):** triple filter(utility_consensus + utility_margin + drawdown_veto)가 과하게 flat(관망)을 만들어 density < 2/day(일 2회 미만)로 붕괴할 수 있습니다. 제안된 stop criteria(중단 기준)는 적절합니다. F10B scout는 **한 family씩** 또는 **완화 ladder(완화 사다리)** 로 시작해 “전부 flat” 원인을 분리하는 것이 좋습니다.

---

### Advice classification detail(조언 분류 상세)

| Item(항목) | Classification(분류) |
|---|---|
| Open Frontier10 stage(전선10 단계 개방) | **accepted(수용)** |
| Hypothesis lifecycle direction(가설 생명주기 방향) | **accepted(수용)** |
| Novelty vs F07–F09(전선07–09 대비 신규성) | **accepted(수용)** |
| Novelty vs Stage295(295단계 대비 신규성) | **needs_local_verification(로컬 검증 필요)** — brief에 archive delta(보관소 차이) 기록 필요 |
| Leakage boundary at design(설계 단계 누수 경계) | **accepted(수용)** |
| Leakage at implementation(구현 단계 누수) | **needs_local_verification(로컬 검증 필요)** |
| Controls(대조군) | **accepted(수용)** — F08 row 추가 권장 |
| WFO/MT5 deferral(WFO/MT5 연기) | **accepted(수용)** |

**Forbidden claim check(금지 주장 확인):** operating promotion, runtime authority, live readiness, selected baseline, Goal Achieve — **none claimed(주장 없음)** ✓

---

### Required bounds for Frontier10A/B(전선10A/B 필수 경계)

Codex가 materialize(물질화) 전에 stage brief(단계 개요)에 넣을 항목:

1. `prior_stage_scan`: Frontier09 negative memory + `NEG-ST295` + reopen rationale(재개 근거: Python subwindow consensus scout, not MT5 route replay)
2. `do_not_repeat`: F09 clean-path density bridge; F08 weight-only repair; F07-family rename without consensus
3. `difference_from_f07` / `difference_from_f09` / `difference_from_stage295` per target family
4. F10B: **no class-prior bridge**, argmax-only, train-only subwindow definitions documented in report
5. Stop if consensus collapses density or val DD stays >>15% with no paired improvement — already in proposal ✓

---

### Grok receipt(그록 영수증)

| Field(필드) | Value(값) |
|---|---|
| trigger_reason(트리거 이유) | user-requested Frontier10 stage-open adversarial review(사용자 요청 전선10 단계 개방 비판 검토) |
| review_size(검토 크기) | medium review(중간 검토) |
| direction_before_grok(그록 전 방향) | open `stage_frontier_10__split_consistent_utility_distillation` |
| bounded_evidence(제한 근거) | `workspace_state.yaml`, Frontier09D closeout, F07–F09 patterns, `NEG-ST295`, frontier governance |
| prompt_identity(프롬프트 정체성) | conversation + `docs/agent_control/grok_reviews/2026-06-14_frontier10_stage_open/medium_review/prompt.md` |
| grok_output_identity(그록 출력 정체성) | this conversation turn(본 대화 턴) |
| advice_classification(조언 분류) | **accepted(수용)** with implementation/archive documentation conditions(구현·보관소 문서화 조건) |
| local_verification(로컬 검증) | Codex must verify subwindow leakage guards + archive delta in brief before `frontier10B`(전선10B 전) |
| forbidden_claim_check(금지 주장 확인) | pass(통과) |
| final_codex_direction(최종 Codex 방향) | **Proceed to open Frontier10A(전선10A 개방 진행)**; materialize stage scaffold + brief with archive deltas; then `frontier10B_utility_distillation_proxy_scout_v1` |

---

### Next action for Codex(코덱스 다음 행동)

1. `frontier10A_stage_open_split_consistent_utility_distillation_v1` materialize — stage folder, brief, `do_not_repeat`, archive scan
2. Update `workspace_state.yaml` active stage only after materialize + local receipt(물질화 + 로컬 영수증 후)
3. Do **not** run WFO/MT5 until strict scout clue appears

**Not yet true(아직 사실 아님):** Frontier10이 validation DD를 고칠 것, strict clue가 나올 것, 어떤 promotion/runtime readiness(승격/런타임 준비) — 모두 scout 결과 전까지 주장 불가.
