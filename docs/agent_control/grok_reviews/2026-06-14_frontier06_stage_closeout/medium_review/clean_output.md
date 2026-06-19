Grok 외부 2차 의견으로 Frontier06 마감안을 검토합니다. 협업 스킬과 제한 근거 파일을 먼저 확인합니다.
## 1. Recommendation(권고)

**`close_negative_memory_preserved_clue`(부정 기억+보존 단서 마감)**

Codex(Codex, 코덱스) 제안대로 Frontier06(전선06)을 닫는 것이 맞습니다. `repair_once`, `invalid_setup`, `blocked`는 권하지 않습니다.

---

## 2. Reasoning(근거)

**실험은 정상적으로 끝났습니다.** 405개 capped signal grid(상한 신호 격자), mandatory argmax comparator(필수 최대확률 비교), train-only threshold calibration(학습 전용 임계값 보정), ONNX parity 3/3 pass(온엑스 동등성 3/3 통과) — 설정 오류나 실행 차단이 아닙니다.

**엄격 실패 원인이 분명합니다.** best rule(최상위 규칙) `rf_depth5_leaf80_balanced_argmax__directional_margin__flat1p01__margin0p00__d4p0` 기준:

| Gate(게이트) | Validation(검증) | OOS(표본밖) | Scout floor(탐색 하한) |
|---|---|---|---|
| PF floor | 1.05864 **FAIL** | 1.26664 PASS | ≥ 1.2 |
| DD soft ceiling | 30.9057% **FAIL** | 21.1091% **FAIL** | ≤ 15% |
| Density floor | 6.38 PASS | 5.31 PASS | ≥ 4.0 |
| Score improvement vs argmax | +7.09 PASS | +5.13 PASS | both > 0 |
| `strict_scout_clue_pass` | — | — | **False** |

`scout_clue_rows = 0`, `partial_axis_gain_rows = 376` — 부분 개선은 많지만, PF/DD를 동시에 통과한 규칙은 없습니다. 이건 “아직 안 봤다”가 아니라 **“이 축만으로는 scout clue(탐색 단서) 기준을 못 넘는다”**는 결과입니다.

**임계값 미세탐색을 더 해도 답이 안 바뀝니다.** 상위 규칙들이 `flat1p01`/`flat0p65` × `margin0p00`/`0p03`/`0p06`에서 **동일 KPI**를 보입니다. `d4p0`에서 flat/margin이 실질 거래 집합을 바꾸지 못합니다. Frontier06 내부 threshold micro-search(임계값 미세탐색)는 탐색 반복이지 새 가설이 아닙니다.

**preserved clue(보존 단서)는 좁게만 유효합니다.** directional-margin abstention(방향 마진 기권)은 argmax 대비 OOS density(표본밖 밀도) `26.68 → 5.31/day`(target band 5–10), OOS PF `0.965 → 1.267`, OOS DD `40.2% → 21.1%`를 개선했습니다. 하지만 validation PF(검증 수익 팩터)는 floor(1.2) 미달, DD는 validation/OOS 모두 soft ceiling(15%) 초과입니다. **completion candidate(완성 후보)가 아닙니다.**

**다른 옵션을 거절하는 이유:**

- **`repair_once`**: ONNX·격자·비교기준선이 정상입니다. 실패는 측정/환경 오류가 아니라 **가설 한계**입니다.
- **`invalid_setup`**: 실험 설계가 질문에 답했습니다. scout clue 0은 무효가 아니라 **음성 결과(negative result)**입니다.
- **`blocked`**: 실행·패리티·산출물 체인이 완료됐습니다. 외부 검증(MT5/WFO) 부재는 이 단계 claim boundary(주장 경계) 안의 `research_only`입니다.

**다음 전선 방향** — exit/risk/validation hypothesis(청산/위험/검증 가설) 같은 **새 축** — 은 타당합니다. 병목은 “신호 게이팅 mechanics(기계)”보다 **PF/DD 품질**에 가깝습니다.

---

## 3. Accepted / rejected / needs_local_verification(수용/거절/로컬 검증 필요)

**Accepted(수용)**

- Frontier06을 **negative_memory + preserved_clue**로 마감
- **WFO/MT5 실행 금지**, Frontier06 내부 **threshold micro-search 금지**
- best read(최상위 판독), scout_clue_rows=0, partial_axis_gain_rows=376, strict=False
- 다음 전선은 **signal-contract threshold tuning(신호계약 임계값 조정)이 아닌 새 축**으로 개방

**Rejected(거절)**

- `repair_once` — 근거 불충분; 파라미터 포화가 이미 보임
- `invalid_setup` / `blocked` — 증거와 불일치
- preserved clue를 **promotion candidate / completion candidate / baseline**으로 승격
- OOS 개선만으로 “가설 성공” 주장 — validation PF·양쪽 DD miss(미달) 무시

**Needs local verification(로컬 검증 필요)** — Codex가 마감 기록 전 확인

- bounded evidence sha256(제한 근거 해시) 5건 재계산
- Tier B / Tier A+B가 `missing_required`로 장부에 기록됐는지
- negative_result_register / idea_registry에 preserved clue 문구가 **좁은 범위**로만 들어갔는지

---

## 4. Closeout wording(마감 문구)

> **Frontier06 closed(전선06 마감): negative_memory + preserved_clue.**
>
> Train-only selective probability abstention(학습 전용 선택적 확률 기권) on fixed labels/features/models(고정 라벨/피처/모델) did not produce any strict scout clue(엄격 탐색 단서) across 405 capped rules(405 상한 규칙) (`scout_clue_rows=0`). Best partial read(최상위 부분 판독): `rf_depth5_leaf80_balanced_argmax__directional_margin__flat1p01__margin0p00__d4p0` improved argmax overtrading and OOS PF/DD/density(표본밖 수익팩터/손실폭/밀도) vs argmax, but failed validation PF floor(검증 수익팩터 하한) and validation+OOS DD soft ceiling(검증+표본밖 손실폭 상한). Preserved clue(보존 단서): directional-margin + train-density calibration(방향마진+학습밀도 보정) can throttle trade density(거래 밀도 억제); not a completion, baseline, promotion, or runtime path(완성/기준선/승격/런타임 경로 아님). No further threshold micro-search inside Frontier06(전선06 내부 임계값 미세탐색 금지). Next work(다음 작업): new frontier axis(새 전선 축) such as exit/risk/validation(청산/위험/검증).

---

## 5. Do-not-claim boundary(주장 금지 경계)

다음은 **주장 금지**입니다.

- **completion / Goal Achieve / selected baseline / operating promotion / runtime authority / live readiness**
- **“selective abstention solves overtrading”** — OOS는 개선됐지만 validation PF·양쪽 DD가 scout floor를 못 넘김
- **“best rule is promotion-ready”** — `strict_scout_clue_pass=False`; validation PF 1.05864 < 1.2
- **WFO / MT5 / runtime parity / Tier B·combined readiness** — 본 단계 범위 밖; Tier B·combined는 `missing_required`로만 기록
- **probability scores = calibrated truth(확률 점수 = 보정된 진실)** — ranking scores for scout contract only(탐색 계약용 순위 점수)
- Frontier06 내부 **추가 threshold grid expansion(임계값 격자 확장)** — 마감 후 금지

---

**Grok receipt(그록 영수증) 요약:** review_size = medium; direction_before_grok = Codex close proposal; advice_classification = **accepted** close_negative_memory_preserved_clue; forbidden_claim_check = pass (Grok did not assert promotion/runtime/baseline). Codex는 위 needs_local_verification 3건을 재검증한 뒤 `frontier06C_stage_closeout_v1`을 진행하면 됩니다.
