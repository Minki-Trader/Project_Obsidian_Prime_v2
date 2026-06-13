# Frontier07A Stage Open Report(전선07A 단계 개방 보고서)

Updated(갱신): 2026-06-13T20:29:28Z

Status(상태): `opened_frontier07_adverse_excursion_risk_shaped_labeling_no_authority`

Judgment(판정): `stage_opened_after_grok_review_no_authority`

## Action And Effect(행동과 효과)

Action(행동): Frontier07(전선07)을 adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링) 가설 생명주기(hypothesis lifecycle, 가설 생명주기)로 열었습니다.

Effect(효과): Frontier06(전선06)의 density/PF clue(밀도/수익 팩터 단서)를 threshold retry(임계값 재시도)로 반복하지 않고, DD(drawdown, 손실폭)를 직접 겨냥하는 label utility(라벨 효용) 축으로 이동합니다.

## Thesis(가설)

Risk-shaped labels that penalize adverse excursion before favorable movement may train ONNX to avoid drawdown-heavy entries(유리한 이동 전 불리한 이동을 벌점화한 위험 형성 라벨은 온엑스가 손실폭 큰 진입을 피하도록 학습시킬 수 있음).

## Novelty Delta(신규성 차이)

Label utility changes from path-event direction to adverse-excursion survival, while feature_set_v2 and split controls remain fixed(라벨 효용은 경로 이벤트 방향에서 불리한 이동 생존으로 바뀌고, 피처 세트 v2와 분할 통제는 고정).

## Grok Review(그록 검토)

Recommendation(권고): `open_frontier07(전선07 개방)`

Accepted(수용):
- open Frontier07 as adverse-excursion risk-shaped label hypothesis(전선07을 불리한 이동 위험 형성 라벨 가설로 개방)
- treat Frontier04/06 only as reference, not inheritance(전선04/06은 참조이지 상속 아님)
- use broad label variants before threshold or micro-search(임계값/미세탐색 전 넓은 라벨 변형 사용)
- add learnability-first gate before oracle metric celebration(오라클 지표를 기념하기 전에 학습 가능성 우선 게이트 추가)
- forbid F04 horizon-target-stop grid replay(F04 수평선-목표-손절 격자 재시도 금지)

Needs local verification(로컬 검증 필요):
- labels use future path only as target, never as feature(라벨은 미래 경로를 목표로만 쓰고 피처로 쓰지 않음)
- MAE/MFE path windows are right-indexed and split-safe(MAE/MFE 경로 창은 우측 인덱스와 분할 안전성 유지)
- thresholds or variant choice are not fitted on validation/OOS(임계값이나 변형 선택을 검증/표본밖에 적합하지 않음)
- Tier B and combined rows are recorded as missing_required if unavailable(티어 B와 합산 행은 불가 시 필수 누락으로 기록)
- Frontier07B compares label_v1, F04 locked path label, and F06 selective reference without inheriting them(전선07B는 label_v1/F04 고정 경로 라벨/F06 선택 참조를 상속 없이 비교)

## Frontier07B Required Bounds(전선07B 필수 경계)

- fixed feature_set_v2 input and small ONNX-exportable model family(고정 피처 세트 v2 입력과 작은 온엑스 내보내기 가능 모델군)
- argmax-only scout signal; no F06-style abstention threshold search(최대확률 전용 탐색 신호, 전선06식 기권 임계값 탐색 없음)
- mandatory references: label_v1 argmax, F04 locked path trainable reference, F06 best selective reference as comparison-only(필수 참조: label_v1 최대확률, F04 고정 경로 학습 참조, F06 최선 선택 참조를 비교 전용으로 사용)
- each label family must state how it differs from F04 event-label semantics(각 라벨군은 F04 이벤트 라벨 의미와 다른 점을 명시)
- learnability-first reporting: class balance, train-to-validation separability, ONNX parity, transfer gap tag(학습 가능성 우선 보고: 클래스 균형, 학습-검증 분리도, 온엑스 동등성, 전달 격차 태그)
- cap broad variants before micro-search: at most five families and four variants per family(미세탐색 전 넓은 변형 상한: 최대 5개 군과 군당 4개 변형)
- strict scout clue requires validation and OOS density/PF/DD/smoothness improvement without validation/OOS fitting(엄격 탐색 단서는 검증/표본밖 적합 없이 검증과 표본밖 밀도/수익 팩터/손실폭/매끄러움 개선 필요)
- DD-only improvement is preserved clue only, not strict scout clue(손실폭만 개선되면 엄격 탐색 단서가 아니라 보존 단서)

## Next Action(다음 행동)

`frontier07B_adverse_excursion_risk_label_proxy_scout_v1`. Action(행동)은 MAE/MFE(최대 불리/유리 이동) 기반 위험 형성 라벨 변형을 넓게 만들고 trainable proxy(학습 가능 프록시)를 확인하는 것입니다. Effect(효과)는 손실폭이 큰 진입을 모델이 학습으로 피할 수 있는지 보는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
