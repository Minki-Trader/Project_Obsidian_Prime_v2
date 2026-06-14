Frontier14 개방 검토입니다. Grok 협업 규칙과 Frontier12/13 맥락을 먼저 확인한 뒤, 이 응답 안에서만 분류·이유·로컬 확인·반복 금지·금지 주장을 정리하겠습니다.
## Frontier14 Stage-Open Review (프론티어14 단계 개방 검토)

**Review size (검토 크기):** small review (소규모 검토)

---

### 1. Classification (분류)

**`accepted` (수용)** — bounded conditions (조건부 경계) 포함

---

### 2. One-sentence reason (한 문장 이유)

F12/F13(프론티어12/13)이 trade-shape wrapping·regime-scale repair(거래 형상 감싸기·국면 척도 수리)로 density cliff(빈도 절벽)를 못 넘긴 뒤, F14(프론티어14)는 **상류 opportunity budget(진입 기회 할당량)** 으로 “어떤 봉이 기회인지”를 바꾸는 별도 가설이라, F13 마감이 권한한 upstream frequency hypothesis(상류 빈도 가설)와 맞고 탐색 전선(exploration frontier, 탐색 전선)으로 열 가치가 있습니다.

**Plain meaning (쉬운 설명):** F12/F13은 “거래 모양·국면” 라벨을 더 만지는 쪽이었고, 빈도는 여전히 너무 낮았습니다. F14는 그 전에 “하루/세션에 몇 개의 기회만 라벨로 남길지”를 정해 보겠다는 다른 질문입니다. 그래서 F12/13 반복 수리가 아니라 새 프론티어 가설로 봅니다. 다만 `q`(할당량)와 `h`(지평)를 결과 본 뒤 고르면 숨은 임계값 탐색(hidden threshold search, 숨은 임계값 탐색)이 됩니다.

---

### 3. Required local checks before execution (실행 전 필수 로컬 확인)

Codex(코덱스)가 stage materialization(단계 물질화) **전**에 아래를 로컬로 고정·검증해야 합니다.

| Check (확인) | What to verify (확인 내용) |
|---|---|
| F13 closeout lock (F13 마감 잠금) | `workspace_state.yaml`, F13 closeout report, `selection_status.md`가 `closed_negative_memory_no_authority`이고 strict/preserved rows = 0인지 |
| Opening contract (개방 계약) | `frontier_governance.md` 6항목 — thesis, novelty_delta, prior_stage_scan, do_not_repeat, exit_rule, claim_boundary — 이 `00_spec/`에 모두 있는지 |
| F12/F13 do-not-repeat carry (반복 금지 이월) | label knob loosening, regime-scale wrapping, class-weight density forcing, threshold micro-search가 F14 spec에 명시 금지로 복사됐는지 |
| Quota variant pre-registration (할당 변형 사전 등록) | `day_q6_h8`, `cash_q8_h8`, `cash_q10_h12`의 bucket 정의, utility 공식, quota 수, horizon, tie-break가 **run 전** 고정됐는지; metrics 본 뒤 best-variant pick(사후 최고 변형 선택) 금지 |
| Label vs model density split (라벨 vs 모델 빈도 분리) | train/validation/OOS 각각에 **label-side opportunities/day**(라벨 쪽 일일 기회 수)와 **model argmax trades/day**(모델 최대확률 거래 수)를 분리 기록하는지 — F14 핵심 검증 |
| Train-only calibration boundary (학습 전용 보정 경계) | bucket 경계, utility scale, quota tie-break가 train split(학습 구간)에서만 fit(적합)되는지 |
| Label causality audit (라벨 인과성 감사) | feature row(피처 행)는 closed-bar only(확정 봉만); label utility(라벨 효용)는 정의상 future path(미래 경로)를 쓰되 ranking/quota 적용이 bar 시점 이후 정보를 feature 쪽으로 역류하지 않는지 |
| Leakage guard (누수 방지) | validation/OOS bucket 통계로 quota를 재조정하지 않는지; session/day bucket이 broker session calendar(브로커 세션 달력)와 일치하는지 |
| Overfit guard (과적합 방지) | 3 variants × bucket × horizon 자유도가 pre-registered(사전 등록) 범위를 넘지 않는지; label density는 맞는데 model density cliff(모델 빈도 절벽)면 **failure criteria(실패 기준)** 로 바로 닫을지 |
| Hidden-threshold guard (숨은 임계값 방지) | quota `q`/`h`를 density 5–10/day에 맞게 사후 조정하지 않는지; post-fit selector(적합 후 선택기), threshold micro-search(임계값 미세 탐색), class-weight ladder(클래스 가중 사다리)가 없는지 |
| Signal contract freeze (신호 계약 고정) | fixed 3-class ONNX(고정 3클래스 온엑스), argmax-only, same feature order(동일 피처 순서), same model specs(동일 모델 규격) |
| Tier ledger plan (티어 장부 계획) | Tier A separate(티어 A 분리) 필수; Tier B separate + Tier A+B combined(티어 B 분리 + 합산) 원천 없으면 `missing_required`로 빈칸 없이 기록 |
| Success/failure boundary freeze (성공/실패 경계 고정) | strict scout clue(엄격 탐색 단서) = val+OOS 모두 positive net / PF≥1.2 / density 5–10/day / DD≤15% + subperiod DD controlled(하위기간 손실폭 통제); 그 외는 seed/negative memory/invalid/blocked만 |
| Required records (필수 기록) | `00_spec/` opening contract, label manifest + hash(라벨 목록+해시), per-variant label-density table(변형별 라벨 빈도표), per-variant model KPI table(변형별 모델 KPI표), label–model density gap(라벨–모델 빈도 격차), subperiod slice definition(하위기간 조각 정의), `stage_run_ledger.csv` row, ONNX parity receipt(온엑스 동등성 영수증) if export |

**이번 턴 로컬 재검증:** F13 closeout 수치·상태는 제공된 current truth(현재 진실)와 저장소 closeout report가 일치합니다. F14 stage folder(단계 폴더)와 quota label contract(할당 라벨 계약)는 아직 없습니다.

---

### 4. Required do-not-repeat notes (필수 반복 금지 메모)

- **F12 carry:** same label knob loosening (같은 라벨 파라미터 완화), class-weight density forcing (클래스 가중 빈도 강제), threshold micro-search (임계값 미세 탐색)
- **F13 carry:** same regime-scale wrapping (같은 국면 척도 감싸기), trade-shape multiplier repair on same family (같은 계열 거래 형상 승수 수리), threshold micro-search on this label family (이 라벨 계열 임계값 미세 탐색)
- **F14-specific:** quota `q`/`h` retuning after seeing val/OOS density (검증/표본밖 빈도 본 뒤 할당량·지평 재조정); collapsing 3 pre-registered variants into best-after-metrics pick (3개 사전 등록 변형을 결과 본 뒤 1개로 축소); claiming label quota hit = model learned frequency (라벨 할당량 충족을 모델 빈도 학습 성공으로 주장); re-opening F12/F13 trade-shape or regime-normalized label families under new names (이름만 바꿔 F12/F13 라벨 계열 재개방); balanced argmax variants solely to force density (빈도 강제용 균형 최대확률 변형 추가)

---

### 5. Forbidden claims check (금지 주장 확인)

| Forbidden claim (금지 주장) | Status (상태) |
|---|---|
| completion (완성) | **not_claimed (주장 없음)** |
| baseline (기준선) | **not_claimed** |
| promotion (승격) | **not_claimed** |
| runtime authority (런타임 권위) | **not_claimed** |
| live readiness (실거래 준비) | **not_claimed** |
| Goal Achieve (목표 달성) | **not_claimed** |

제안은 scout/negative-memory boundary(탐색/부정기억 경계) 안에 있고, 금지 주장을 만들지 않습니다. Grok(그록)도 이 검토로 위 항목을 만들 수 없습니다.

---

**Claim boundary (주장 경계):** 이번 검토는 stage-open direction(단계 개방 방향)만 `accepted`합니다. scout clue(탐색 단서), preserved clue(보존 단서), negative memory(부정 기억), completion(완성)은 **아직 주장하지 않습니다**. Codex는 위 local checks(로컬 확인)를 통과한 뒤 `frontier14A_stage_open_new_hypothesis_design_v1` 물질화를 진행하면 됩니다.
