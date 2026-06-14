Frontier16 개방 검토를 위해 Grok 협업 스킬과 F12–F15 맥락을 먼저 확인합니다.
# Classification(분류)

**`accepted`(수용)**

---

## Review Answers(검토 답변)

### 1. Novelty delta(신규성 차이) vs F12–F15(프론티어12~15)

**Sufficient(충분), but bounded(제한적).** F16(프론티어16)은 F12–F14(프론티어12~14)의 **label-family(라벨 계열) 재시도**가 아니라, F15(프론티어15) **decision-contract(결정 계약) 실패**에 대한 **구조화된 상류(上游) 응답**입니다.

| Stage(단계) | Mechanism tested(시험 메커니즘) | F16 relation(F16 관계) |
|---|---|---|
| F12 | trade-shape / path / adverse excursion label(거래 형상·경로·역행폭 라벨) | **Overlap(겹침)** — path+adverse(경로+역행폭) 표면은 F07/F12(프론티어07/12)와 유사 |
| F13 | regime-normalized label(국면 정규화 라벨) | **Not repeated(반복 없음)** |
| F14 | opportunity-quota label(기회 할당 라벨) | **Explicit pivot(명시 전환)** — F16은 quota(할당)를 버리고 risk-quality path(위험 품질 경로)로 바꿈 |
| F15 | 9-cell score-threshold grid(9칸 점수 임계값 격자) | **Inverted(반전)** — F16은 label upstream(라벨 상류)으로 가고 decision(결정)은 고정 |

핵심 차이는 이겁니다. F15(프론티어15)가 증명한 것은 **density transfer(빈도 전이)는 calibration clue(보정 단서)**이지 **edge quality(엣지 품질)**이 아니라는 점입니다. F16(프론티어16)은 그 단서를 **입력으로만** 쓰고, **고정된 `edge_margin__target8` train-only policy(학습 전용 정책)** 아래에서 **새 label meaning(라벨 의미)**이 PF/DD(수익 팩터/손실폭)를 만드는지 묻습니다. 이 질문은 F12–F15(프론티어12~15) 중 어느 단계에서도 직접 시험되지 않았습니다.

**Risk flag(위험 표시):** `f16b_edge_h8_t0p30_cap0p45_early0p25` 같은 knob naming(파라미터 이름)은 F12(프론티어12) `h/cap/early` 패턴과 겉모습이 비슷합니다. 그래서 F16(프론티어16)은 **“새 메커니즘”**이 아니라 **“F15 실패 이후의 제한된 label-contract repair(라벨 계약 수리)”**로 열어야 합니다. 그렇게 라벨링하지 않으면 F12(프론티어12) 반복으로 읽힙니다.

---

### 2. Single `edge_margin__target8` train-only policy(학습 전용 정책) — F15 grid repetition(격자 탐색 반복) 회피?

**Yes(예), 조건부로.** 한 개의 score contract(점수 계약) + 한 개의 train-only density target(학습 전용 빈도 목표)는 F15(프론티어15)의 **9-cell expansion(9칸 확장)**을 직접 반복하지 않습니다.

- F15(프론티어15): post-fit decision surface(적합 후 결정 표면) — 9 score cells(9개 점수 칸)
- F16(프론티어16): pre-fit label variants × 1 fixed decision policy(적합 전 라벨 변형 × 고정 결정 정책) — 3 label rows(3개 라벨 행), 1 decision cell(1개 결정 칸)

3개의 pre-registered label variants(사전 등록 라벨 변형)는 **label-contract exploration(라벨 계약 탐색)**이지 score-grid search(점수 격자 탐색)가 아닙니다. F12B(프론티어12B) scout pattern(탐색 패턴)과 같은 계열입니다.

**Hard requirement(필수 조건):** `edge_margin__target8` 외 score cell(점수 칸), validation/OOS threshold retune(검증/표본밖 임계값 재조정), F15-style grid repair(프론티어15식 격자 수리)는 **materialization(물질화) 전에 금지**로 박아야 합니다. 그렇지 않으면 “single policy(단일 정책)” 주장이 약해집니다.

---

### 3. Minimum guards(최소 가드) before Frontier16A/B materialization(프론티어16A/B 물질화)

Codex(코덱스)가 물질화 전에 넣어야 할 **필수 가드(필수 가드)**:

1. **Locked decision contract(고정 결정 계약)** — `edge_margin = max(p_short,p_long)-p_flat` 하나만, train-only `target8` 하나만; validation/OOS calibration(검증/표본밖 보정) 금지.
2. **Pre-registered label spec(사전 등록 라벨 명세)** — 3 variants(변형)의 path-return(경로 수익) + adverse-excursion veto(역행폭 배제) 정의, train-only quantile cut points(학습 전용 분위수 절단점), F16B metrics(지표) 전에 manifest(실행 목록)에 고정.
3. **Density transfer audit table(빈도 전이 감사 표)** — label density(라벨 빈도) / model argmax density(모델 최대확률 빈도) / `edge_margin__target8` density(점수 칸 빈도)를 train·validation·OOS(학습·검증·표본밖)별로 분리 기록. F14(프론티어14) label–model gap(라벨–모델 격차) 재발 방지용입니다.
4. **Do-not-repeat registry(반복 금지 등록)** — F15C(프론티어15C) 항목을 그대로 이식: 9-cell grid(9칸 격자), validation-guided filtering(검증 유도 필터링), density-transfer-as-edge claim(빈도 전이를 엣지로 주장).
5. **Variant cap(변형 상한)** — 3 pre-registered labels(사전 등록 라벨)만; post-hoc knob addition(사후 파라미터 추가) 금지.
6. **No repair ladder(수리 사다리 금지)** — F14 flat/class-weight/density-bridge repair(프론티어14 평면/클래스가중/빈도브리지 수리) 금지; F16B(프론티어16B) 0 strict + 0 preserved(엄격 0 + 보존 0)이면 바로 closeout(마감) 경로.
7. **Prior-stage overlap disclosure(이전 단계 겹침 공개)** — F07/F12(프론티어07/12) adverse-excursion label history(역행폭 라벨 이력)를 `prior_stage_scan`(이전 단계 스캔)에 명시하고, F16(프론티어16)이 **무엇이 다른지**(F15 locked decision + density-transfer-as-input-only)를 한 문단으로 적기.
8. **Tier paired records(티어 쌍 기록)** — Tier A separate(티어 A 분리) / Tier B separate(티어 B 분리) / combined(합산); Tier B(티어 B) 없으면 `missing_required`(필수 누락)로 기록.
9. **ONNX parity gate(온엑스 동등성 게이트)** — model row(모델 행)마다 parity pass(동등성 통과) 없으면 strict/preserved(엄격/보존) 판정 불가.
10. **Claim boundary lock(주장 경계 고정)** — proxy scout only(프록시 탐색만); completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 전부 `not_claimed`(주장 없음).

---

## Rationale for `accepted`(수용 근거)

- F15 closeout(마감)의 prescribed next action(규정 다음 행동) — “density transfer(빈도 전이)를 edge(엣지)로 과장하지 말고, edge quality/risk(엣지 품질/위험)를 새 가설로 설계” — 과 **정합(정합)**합니다.
- Changed variable(변경 변수)가 명확합니다: **quota label → risk-quality path label(할당 라벨 → 위험 품질 경로 라벨)**, decision surface(결정 표면)는 **고정**입니다.
- F15 grid-search repetition(격자 탐색 반복)은 **의도적으로 차단**됩니다. 위 10개 가드가 들어가면 실질적으로 막힙니다.
- Claim boundary(주장 경계)가 올바르게 낮습니다 — proxy scout only(프록시 탐색만).

**Not `rejected`(거절 아님):** 방향이 F15 negative memory(부정 기억)를 직접 겨냥하고, 탐색 discipline(탐색 규율)을 유지합니다.

**Not `needs_local_verification`(로컬 검증 필요 아님):** F15 closeout evidence(마감 근거)와 F12–F15 arc(연속선)가 prompt(프롬프트) 안에서 이미 bounded(제한)되어 있고, stage-open(단계 개방) 시점에는 label contract implementation(라벨 계약 구현)이 아직 없는 것이 **정상**입니다. 구현 검증은 Frontier16A materialization(프론티어16A 물질화) 단계의 로컬 게이트입니다.

---

## Codex Action(코덱스 행동)

`accepted`로 Frontier16A(프론티어16A) stage open(단계 개방)을 진행하되, 위 **10 guards(가드)**를 `00_spec` / `experiment_design` / `do_not_repeat`에 **먼저** 박은 뒤 Frontier16B(프론티어16B) scout(탐색)로 넘기세요. 효과(effect, 효과)는 F12/F07(프론티어12/07) 표면 반복과 F15(프론티어15) 격자 재탐색을 동시에 막는 것입니다.
