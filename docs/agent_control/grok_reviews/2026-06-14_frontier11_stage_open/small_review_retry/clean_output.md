Frontier11 stage-open 검토 재시도입니다. Grok 협업 스킬과 현재 전선·F10 맥락을 먼저 확인한 뒤, 이 응답 안에서만 분류·이유·필수 기록·금지 주장을 정리하겠습니다.
## Grok Stage-Open Review Retry(그록 단계 개방 검토 재시도)

**Review size(검토 크기):** small review(소규모 검토)
**Claim boundary(주장 경계):** stage-open design only(단계 개방 설계만). completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

---

### 1. Classification(분류)

**accepted(수용)** — bounded conditions(조건부 경계) 포함

---

### 2. One-sentence reason(한 문장 이유)

Frontier11(전선11)은 F07~F10(전선07~10)의 라벨/목적/가중/브리지 수리 반복이 아니라 **후보를 고르는 검증 철학(validation philosophy, 검증 철학)** 을 바꾸며, F10 부정 기억인 validation DD 56~60%·strict rows 0·수리 후 OOS DD 악화를 **하위기간 안정성·최악 구간 손실폭** 으로 직접 시험하는 다음 가설 생명주기로 타당합니다.

**Plain meaning(쉬운 설명):** 지금까지는 “합계 PF/밀도가 좋으면 후보로 통과”였는데, F10은 합계가 괜찮아도 검증 구간 손실이 너무 컸습니다. Frontier11은 “월/분기마다 얼마나 흔들리는지, 최악 구간 손실이 얼마인지”를 먼저 보자는 **다른 질문**이라, 같은 수리 루프가 아닙니다.

---

### 3. Required records(필수 기록)

Codex(코덱스)가 과장 주장(overclaiming, 과장 주장)을 막으려면 아래를 **stage-open(단계 개방) 전** 명시 기록해야 합니다.

| Record(기록) | What to write(적을 내용) | Why(이유) |
|---|---|---|
| `frontier_thesis(전선 가설)` | fixed 3-class ONNX(고정 3분류 온엑스) 후보 선택 시 aggregate validation/OOS(검증/표본밖 합계)보다 subperiod stability(하위기간 안정성), worst-slice DD(최악 구간 손실폭), TUW proxy(회복 전 체류 시간 프록시), equity smoothness proxy(자산곡선 매끄러움 프록시)가 zoomed DD(확대 구간 손실폭)·curve chop(곡선 출렁임)을 줄이는가 | 무엇을 시험하는지 고정 |
| `novelty_delta(신규성 차이)` | F07~F10 = label/objective/weight/bridge(라벨/목적/가중/브리지); F11 = **selection surface only(선택 표면만)**. F10 subwindow consensus(하위구간 합의)는 **label-build phase(라벨 생성 단계)**; F11 subperiod metrics는 **post-fit candidate ranking(적합 후 후보 순위)** | 수리 반복 vs 새 전선 구분 |
| `prior_stage_scan(이전 단계 점검)` | F10 closeout path(마감 경로) + negative memory(부정 기억) 수치; archive overlap(보관소 겹침) — Stage171 segment stability(구간 안정성), Stage273 stability validation(안정성 검증), `subperiod_consistency` KPI — 각각 **difference_from_archive(보관소 대비 차이)** | archive amnesia(보관소 망각)와 이름만 같은 재시도 방지 |
| `do_not_repeat(반복 금지)` | side-weight ladder(방향 가중 사다리), density bridge(밀도 브리지), threshold micro-search(임계값 미세 탐색), F10-class capped repair(전선10급 상한 수리) | F10 negative memory(부정 기억) 잠금 |
| `frozen_surfaces(고정 표면)` | label family(라벨군), objective family(목적군), weight family(가중군) = **reference-only preserved clue(참조 전용 보존 단서)**; 변경 금지 | 숨은 라벨/목적 수리 차단 |
| `selection_metric_spec(선택 지표 명세)` | subperiod slice 정의(월/분기 경계), worst-slice DD 계산, TUW proxy, smoothness proxy, tie-break(동점 처리), **train-only fit boundary(학습 전용 적합 경계)** | 구현 시 누수·임의 정의 방지 |
| `control_arm(대조군)` | 동일 후보 풀에 **aggregate-only selector(합계 전용 선택기)** 병행 | 신규 철학 효과 분리 |
| `exit_rule(종료 규칙)` | strict rows(엄격 행) 0 + subperiod selector(하위기간 선택기)도 validation DD(검증 손실폭) 개선 없음 → close as negative memory(부정 기억 마감) | decision weight(결정 무게) 기준 |
| `claim_boundary(주장 경계)` | proxy scout only(프록시 탐색만); no model authority(모델 권위 없음); WFO/MT5 = strict clue(엄격 단서) 전 `out_of_scope_by_claim(주장 범위 밖)` | 권위 주장 차단 |
| `tier_records(티어 기록)` | Tier A separate(티어 A 분리) / Tier B separate(티어 B 분리) / Tier A+B combined(티어 A+B 합산) — 불가 시 `missing_required` 명시 | paired tier rule(티어 쌍 규칙) |
| `clue_row_definitions(단서 행 정의)` | strict vs preserved row(엄격 vs 보존 행) 게이트 수치 | scout clue(탐색 단서) 과장 방지 |
| `grok_receipt(그록 영수증)` | trigger, review_size, direction_before_grok, advice_classification, forbidden_claim_check | closeout gate(마감 게이트) 추적 |

**Bounded condition(조건부 경계):** archive stability work(보관소 안정성 작업)와 겹침은 인정하되, `prior_stage_scan`에 **lane difference(레인 차이)** — Python fixed-argmax ONNX scout(고정 최대확률 온엑스 탐색), no threshold search(임계값 탐색 없음), F10 failure linkage(전선10 실패 연결) — 가 없으면 novelty(신규성) 주장을 낮춰야 합니다.

---

### 4. Forbidden claims check(금지 주장 확인)

| Forbidden claim(금지 주장) | Status(상태) |
|---|---|
| completion(완성) | **not_claimed(주장 없음)** — stage-open design only |
| selected baseline(선택 기준선) | **not_claimed** — F10 winner/baseline 상속 없음 |
| promotion candidate / operating promotion(승격 후보/운영 승격) | **not_claimed** |
| runtime authority(런타임 권위) | **not_claimed** — proxy scout lane |
| live readiness(실거래 준비) | **not_claimed** |
| Goal Achieve(목표 달성) | **not_claimed** |
| “DD solved / alpha found”(손실폭 해결/알파 발견) | **not_claimed** — hypothesis test only(가설 시험만) |
| Grok-created authority(Grok 생성 권위) | **rejected by policy(정책상 거절)** — Codex local verification(로컬 검증) 후에만 반영 |

---

### Novelty vs repair-loop check(신규성 vs 수리 반복 점검)

| Question(질문) | Verdict(판정) |
|---|---|
| Another F10 repair?(또 다른 F10 수리?) | **No(아니오)** — label/objective/weight/bridge 미변경 |
| Genuine frontier open?(진짜 전선 개방?) | **Yes(예)** — `validation philosophy` change = governance-valid open trigger(거버넌스 유효 개방 조건) |
| Valid for four-axis goal?(네 축 목표에 유효?) | **Yes, as next hypothesis(예, 다음 가설로)** — F02~F10이 aggregate gate(합계 게이트)로 DD를 못 막았음; stability axis(안정성 축)를 selection-first(선택 우선)로 올리는 시도는 정당 |

**Effect(효과):** Codex는 Frontier11을 **열 수 있되**, 위 필수 기록과 대조군 없이는 scout 실행·긍정 판정·다음 단계 승격 주장을 하면 안 됩니다.
