Frontier13 단계 개방 검토를 위해 Grok 협업 스킬과 관련 컨텍스트를 먼저 확인합니다.
## Frontier13 Stage-Open Review(프론티어13 단계 개방 검토)

### 1. Classification(분류)

**`accepted`(수용)**

### 2. One-sentence reason(한 문장 이유)

F12(프론티어12)가 놓친 validation PF/density/subperiod(검증 수익 팩터·빈도·하위기간) 축을, 금지된 label-knob loosening(라벨 파라미터 완화) 대신 train-only regime path scaling(학습 전용 레짐 경로 척도)으로 바꾸는 가설이라, 탐색 전선(exploration frontier, 탐색 전선)으로 열 가치가 있습니다.

### 3. Required local checks(필수 로컬 확인)

단계를 물질화(materialize, 물질화)하기 **전**에 Codex(코덱스)가 아래를 로컬로 확인·고정해야 합니다.

| Check(확인) | What to verify(확인 내용) |
|---|---|
| F12 closeout lock(F12 마감 잠금) | `workspace_state.yaml`, F12 closeout report(마감 보고서), `selection_status.md`가 `closed_negative_memory_no_authority`이고 strict/preserved rows(엄격/보존 행) = 0인지 |
| Opening contract(개방 계약) | `frontier_governance.md` 6항목 — thesis, novelty_delta, prior_stage_scan, do_not_repeat, exit_rule, claim_boundary — 이 `00_spec/`에 모두 있는지 |
| F12 do-not-repeat carry(F12 반복 금지 이월) | label knob loosening, class-weight density forcing, threshold micro-search가 F13 spec(명세)에 명시 금지로 복사됐는지 |
| Three schemes pre-registration(3개 방식 사전 등록) | regime-normalization scheme(레짐 정규화 방식) 3개가 **이름·버킷 정의·path_scale 공식**까지 run 전에 고정됐는지; 사후 선택(post-hoc pick, 사후 선택) 금지 |
| Train-only bucket edges(학습 전용 버킷 경계) | volatility tercile(변동성 삼분위), trend-strength(추세 강도), squeeze(압축) 경계가 train split(학습 구간)에서만 fit(적합)되는지 |
| Label causality audit(라벨 인과성 감사) | regime bucket(레짐 버킷)이 closed-bar features(확정 봉 피처)만 쓰고, label path(라벨 경로)에 future bar(미래 봉)가 안 들어가는지 |
| F12 label contract reuse(F12 라벨 계약 재사용) | early-adverse veto, capped duration, MAE/MFE quality, argmax-only signal(최대확률 전용 신호)이 F13에도 유지되는지 |
| Signal contract freeze(신호 계약 고정) | `[p_short, p_flat, p_long]` + argmax-only, threshold micro-search(임계값 미세 탐색) 없음 |
| Tier ledger plan(티어 장부 계획) | Tier A separate(티어 A 분리) 경로 확인; Tier B/combined(티어 B/합산) 원천 없으면 `missing_required`(필수 누락)로 **빈칸 없이** 기록 |
| ONNX parity scope(ONNX 동등성 범위) | F12 scout pipeline(탐색 파이프라인) 재사용 가능 여부와 parity check(동등성 검사) 범위가 manifest(실행 목록)에 있는지 |
| Success/failure boundary freeze(성공/실패 경계 고정) | density 5–10/day, PF ≥ 1.2, DD ≤ 15%, positive net(양수 순손익), worst subperiod DD(최악 하위기간 손실폭) 개선이 scout boundary(탐색 경계)로만 선언됐는지 |
| Feature/model lineage(피처/모델 계보) | regime feature(레짐 피처) 목록, ONNX export hash(온엑스보내기 해시), label manifest hash(라벨 목록 해시) 추적 가능한지 |

**로컬 재검증 결과(이번 턴):** F12 closeout(마감) 수치·상태는 저장소 파일과 사용자가 준 current truth(현재 진실)가 일치합니다. F13 stage folder(단계 폴더)와 3 scheme contract(3개 방식 계약)는 아직 없습니다.

### 4. Key design risks(핵심 설계 위험)

**Leakage(누수)**
- volatility tercile(변동성 삼분위)·squeeze threshold(압축 임계값)를 validation/OOS(검증/표본밖)에서 fit(적합)하면 라벨이 미래 정보를 먹습니다.
- bucket별 path_scale(경로 척도)도 train-only(학습 전용)여야 합니다.
- session/cash-open(세션/현금장 개장)은 시간대 라벨이라 누수는 적지만, bucket 경계가 bar 시점 이후 정보를 쓰면 안 됩니다.

**Overfit(과적합)**
- scheme 3개 × bucket 수만큼 자유도(degrees of freedom, 자유도)가 늘어납니다.
- F12 OOS density(표본밖 빈도) 0.64/day는 희소 신호 패턴입니다. regime split(레짐 분할)이 validation density(검증 빈도)만 올리고 generalization(일반화)은 깨질 수 있습니다.
- 희소 bucket(희소 버킷)은 path_scale 추정이 불안정해집니다.

**Regime bucketing selection bias(레짐 버킷 선택 편향)**
- session / vol tercile / trend / squeeze 조합은 사전 등록 없이 고르면 “맞는 레짐 세트”를 고른 셈입니다.
- F12 worst subperiod DD(최악 하위기간 손실폭) 30.5%는 regime별 편중이 숨겨져 있을 수 있습니다. normalization(정규화)이 약한 bucket(약한 버킷)을 과대 표본화(oversample, 과대 표본화)할 위험이 있습니다.

**Hidden threshold search(숨은 임계값 탐색)**
- “fixed 3 schemes(고정 3개 방식)”가 metrics 본 뒤 best scheme(최고 방식) 고르기로 바뀌면 F12 금지 항목의 변형입니다.
- regime path_scale이 사실상 global knob loosening(전역 파라미터 완화)의 bucket-wise 버전이면 do-not-repeat(반복 금지) 위반입니다.
- density 5–10/day 목표가 class-weight forcing(클래스 가중 빈도 강제)으로 우회되면 안 됩니다.

**추가 위험**
- F12는 validation PF < 1(0.965)인데 OOS PF 1.88·DD 3%로 **split instability(구간 불안정)** 패턴이 있습니다. F13 scout success(탐색 성공)가 validation 쪽만 개선되면 같은 함정입니다.
- worst subperiod DD(최악 하위기간 손실폭) 개선을 scout success에 넣은 것은 맞지만, month/quarter slice(월/분기 조각) 정의도 사전 고정이 필요합니다.

### 5. Forbidden claims check(금지 주장 확인)

| Forbidden claim(금지 주장) | Status(상태) |
|---|---|
| completion(완성) | **not_claimed(주장 없음)** — scout boundary(탐색 경계)만 제시 |
| baseline(기준선) | **not_claimed** |
| promotion(승격) | **not_claimed** |
| runtime authority(런타임 권위) | **not_claimed** |
| live readiness(실거래 준비) | **not_claimed** |
| Goal Achieve(목표 달성) | **not_claimed** |

제안은 exploration-only(탐색 전용) 범위 안에 있고, 금지 주장을 만들지 않습니다. Grok(그록)도 이 검토로 위 항목을 만들 수 없습니다.

---

**Claim boundary(주장 경계):** 이번 검토는 stage-open direction(단계 개방 방향)만 수용합니다. scout clue(탐색 단서), preserved clue(보존 단서), negative memory(부정 기억), 또는 completion(완성)은 **아직 주장하지 않습니다**. Codex(코덱스)는 위 local checks(로컬 확인)를 통과한 뒤 `frontier13A_stage_open_new_hypothesis_design_v1` 물질화를 진행하면 됩니다.
