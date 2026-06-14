Frontier12 개방 검토를 위해 프로젝트 규칙·프론티어 거버넌스·F11 맥락을 먼저 확인합니다.
# Frontier12 Stage-Open Review(프론티어12 단계 개방 검토)

**Review size(검토 크기):** small review(소규모 검토)
**Bounded evidence(제한 근거):** Frontier11 closeout(`closed_negative_memory_no_authority`), `docs/policies/frontier_governance.md`, Frontier04/07/09/10/11 stage briefs, `do_not_repeat_list.md`

---

## 1. Classification(분류)

**`accepted`(수용)**

## 2. One-sentence reason(한 문장 이유)

Frontier11(프론티어11)이 같은 F10C(전선10C) 후보군의 적합 후 선택(post-fit selection, 적합 후 선택)만으로 validation DD 바닥(검증 손실폭 바닥)을 깨지 못했으므로, 라벨 원천(label source, 라벨 원천)과 거래 생명주기 정의(trade lifecycle definition, 거래 생명주기 정의)를 바꾸는 trade-shape scout(거래 형상 탐색)는 frontier governance(전선 운영 규칙)상 정당한 격상(escalation, 격상)이며 F11 반복 수리(repetitive repair, 반복 수리)와 분리됩니다.

## 3. Required local checks(필수 로컬 확인)

Codex(코덱스)가 stage(단계)를 물질화(materialize, 물질화)하기 **전**에 아래를 확인해야 합니다.

1. **Frontier11 closeout lock(마감 잠금):** `frontier11C_stage_closeout` 산출물, `workspace_state.yaml`의 F11 종료 상태, negative memory(부정 기억) 3건이 로컬에서 일치하는지 확인합니다.
2. **Opening contract completeness(개방 계약 완성):** `frontier_governance.md` 6항목 — `frontier_thesis`, `novelty_delta`, `prior_stage_scan`, `do_not_repeat`, `exit_rule`, `claim_boundary` — 이 `00_spec/`에 모두 있어야 합니다.
3. **Prior-stage scan with paths(경로 포함 이전 단계 점검):** Frontier04(path-aware, 경로 인식), Frontier07(adverse excursion, 불리 이동), Frontier09(clean-path, 깨끗한 경로), Frontier10(utility distillation, 효용 증류), Frontier11(selector-only failure, 선택기 단독 실패), Stage12~364 trade-shape archive(거래 형상 보관소)를 **reference-only(참조 전용)**로 스캔하고, F12가 무엇을 **재시험하지 않는지**를 명시합니다.
4. **Novelty delta proof(신규성 차이 증명):** “terminal 12-bar(종단 12봉)” / “post-fit selector(적합 후 선택기)” / “F10C pool reuse without refit(F10C 후보군 재적합 없이 재사용)” / “density bridge(빈도 브리지)” / “threshold micro-search(임계값 미세 탐색)” 금지가 spec에 박혀 있는지 확인합니다.
5. **Label causality audit(라벨 인과성 감사):** MAE/MFE(최대 불리/유리 이동), early adverse excursion veto(초기 불리 이동 배제), favorable path confirmation(유리 경로 확인), capped hold duration(상한 보유 기간)이 **decision bar(결정 봉) 이후 미래 경로만** 쓰는지, train/val/OOS split(학습/검증/표본밖 분할) 오염이 없는지 확인합니다.
6. **Pre-registered label knobs(사전 등록 라벨 파라미터):** 첫 scout(탐색)에서 MAE/MFE 임계값, hold cap(보유 상한), path-confirmation window(경로 확인 창), neutral-class density prior(중립 클래스 빈도 사전분포)를 **고정 소수 variant(고정 소수 변형)**로만 두고, grid/sweep(격자/스윕)이 없는지 확인합니다.
7. **Train-only materialization boundary(학습 전용 물질화 경계):** label materialization(라벨 물질화)이 train-only(학습 전용)이고, validation/OOS metric(검증/표본밖 지표) 계산에 label refit(라벨 재적합)이 없는지 확인합니다.
8. **Signal contract freeze(신호 계약 고정):** argmax-only(최대확률 전용), no threshold search(임계값 탐색 없음), no post-fit selector(적합 후 선택기 없음), no WFO/MT5 at stage-open(단계 개방 시 WFO/MT5 없음)이 run manifest(실행 목록)에 박혀 있는지 확인합니다.
9. **Tier ledger plan(티어 장부 계획):** Tier A separate(티어 A 분리)는 계산 가능 경로를, Tier B/combined(티어 B/합산)는 source unavailable(원천 없음) 시 `missing_required`(필수 누락)로 **빈칸 없이** 표기할 계획이 있는지 확인합니다.
10. **Feature/model lineage(피처/모델 계보):** F10C ONNX surface(온엑스 표면)를 **winner/baseline(승자/기준선)으로 상속하지 않고**, feature order(피처 순서)와 model input contract(모델 입력 계약)만 재사용 가능한지 문서화합니다.
11. **ONNX parity scope(온엑스 동등성 범위):** parity check(동등성 확인)가 export argmax path(보내기 최대확률 경로)에 한정되고, runtime authority(런타임 권위) 주장과 분리되는지 확인합니다.
12. **Success/failure boundary freeze(성공/실패 경계 고정):** density 5~10/day, PF≥1.2, DD≤15%, positive net(양수 순손익), worst subperiod DD improvement(최악 하위기간 손실폭 개선) vs F11 ~59.5% validation DD reference(검증 손실폭 참조)가 `00_spec`에 scout clue(탐색 단서) 수준으로만 정의되는지 확인합니다.

## 4. Key design risks(핵심 설계 위험)

| Risk(위험) | Why it matters(왜 중요한가) |
|---|---|
| **Label leakage(라벨 누수)** | trade-shape label(거래 형상 라벨)은 미래 고저가 경로(future high/low path, 미래 고저가 경로)를 씁니다. hold cap(보유 상한)이나 favorable-path rule(유리 경로 규칙)이 decision-time feature(결정 시점 피처)에 섞이면 validation/OOS가 과대평가됩니다. |
| **Lifecycle–deployment mismatch(생명주기–배포 불일치)** | 라벨은 이상적 hold/cap lifecycle(보유/상한 생명주기)으로 정의되지만, scout는 argmax-only ONNX(최대확률 전용 온엑스)로 평가됩니다. 라벨 semantics(라벨 의미)와 실제 signal contract(신호 계약)가 어긋나면 proxy clue(프록시 단서)가 무의미해집니다. |
| **Archive re-thread(보관소 재실행)** | Frontier07(전선07)은 이미 adverse-excursion label(불리 이동 라벨)로 OOS DD(표본밖 손실폭) 단서를 남겼지만 validation DD(검증 손실폭)는 높았고 strict rows(엄격 행)는 0이었습니다. F12가 F07/F04/F09 조합을 이름만 바꿔 재시험하면 novelty delta(신규성 차이)가 약해집니다. |
| **Structural DD inheritance(구조적 손실폭 상속)** | F10C/F11이 ~59.5% validation DD floor(검증 손실폭 바닥)를 보여줬습니다. feature surface(피처 표면)와 split(분할)을 그대로 두고 label만 바꾸면 DD floor(손실폭 바닥)가 구조적으로 남을 수 있습니다. |
| **Overfit via label complexity(라벨 복잡도 과적합)** | early AE veto + favorable path + hold cap + MAE/MFE quality + density-aware neutral(빈도 인식 중립)은 supervision surface(감독 표면) 자체가 복잡합니다. threshold search(임계값 탐색) 없이도 label family(라벨 계열)가 validation에 맞춰질 수 있습니다. |
| **Hidden threshold search(숨은 임계값 탐색)** | MAE/MFE cut(절단), cap bars(상한 봉 수), confirmation bars(확인 봉 수), neutral prior(중립 사전분포)를 scout variant grid(탐색 변형 격자)로 훑으면 Frontier08/09의 density bridge(빈도 브리지) 수리를 라벨 축으로 재포장한 것이 됩니다. |
| **Density-aware neutral as bridge(중립 클래스를 브리지로 사용)** | neutral class(중립 클래스)를 density target(빈도 목표)에 맞추면 class-prior bridge(클래스 사전분포 브리지)와 동일한 수리 루프가 됩니다. F07 negative memory(부정 기억)와 충돌합니다. |
| **One-axis illusion(한 축 착시)** | OOS PF(표본밖 수익 팩터)만 좋아지고 validation DD(검증 손실폭)가 그대로면 F11과 같은 split-stress failure(분할 스트레스 실패) 패턴입니다. hard DNR #2(강한 반복 금지 2번) 위반 위험이 있습니다. |

## 5. Forbidden claims check(금지 주장 확인)

**모두 금지(forbidden, 금지)입니다.** 이 stage-open(단계 개방) 시점에서 아래 주장은 할 수 없습니다.

| Forbidden claim(금지 주장) | Status(상태) |
|---|---|
| completion(완성) | **forbidden(금지)** — scout hypothesis only(탐색 가설만) |
| baseline(기준선) | **forbidden(금지)** — F10C/F11 결과는 reference-only(참조 전용) |
| promotion(승격) | **forbidden(금지)** — explicit promotion packet(명시적 승격 작업 묶음) 없음 |
| runtime authority(런타임 권위) | **forbidden(금지)** — ONNX parity(온엑스 동등성) ≠ MT5 authority(MT5 권위) |
| live readiness(실거래 준비) | **forbidden(금지)** — proxy scout only(프록시 탐색만) |
| Goal Achieve(목표 달성) | **forbidden(금지)** — early strict clue(초기 엄격 단서)도 final completion(최종 완성) 아님 |

---

**Final Codex direction(최종 코덱스 방향):** 위 12개 로컬 확인을 통과하면 `stage_frontier_12__trade_shape_duration_controlled_onnx_scout`를 열고, 첫 실행은 `frontier12B` label-proxy scout(라벨 프록시 탐색)로 제한하세요. F10C 후보군 재사용·post-fit selector·density bridge는 열기 전에 spec에서 명시적으로 금지해야 합니다.
