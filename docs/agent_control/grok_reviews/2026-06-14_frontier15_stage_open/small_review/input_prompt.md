# Frontier15 Stage Open Review(프론티어15 단계 개방 검토)

You are Grok acting as external second opinion(외부 2차 의견). Return one classification(분류): accepted(수용), rejected(거절), or needs_local_verification(로컬 검증 필요).

## Current Truth(현재 진실)

Frontier14(프론티어14)는 `closed_preserved_clue_negative_memory_no_authority`로 닫혔다.

Key evidence(핵심 근거):
- strict scout clue rows(엄격 탐색 단서 행): 0
- preserved clue rows(보존 단서 행): 5
- best preserved clue(최고 보존 단서): `f14b_cash_q8_h8__flat8x_safest__lr_plain`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): 0.709064 / 0.098361/day / 6.754780%
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): 3.356730 / 0.068702/day / 0.388877%
- negative memory(부정 기억): daily/session opportunity-budget labels(일/세션별 기회 예산 라벨)은 label-side density(라벨 쪽 밀도)를 약 8/day로 만들었지만, plain argmax ONNX(평범 최대확률 온엑스)는 model-side trade density(모델 쪽 거래 밀도)를 0.07~0.10/day로만 전달했다.
- do-not-repeat(반복 금지): same quota/flat subset repair(같은 할당량/평면 부분 표본 수리), class-weight density forcing(클래스 가중치 밀도 강제), threshold micro-search on same label family(같은 라벨 계열 임계값 미세 탐색).

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

## Codex Direction Before Grok(그록 전 Codex 방향)

Open Frontier15(프론티어15) as:

`stage_frontier_15__score_threshold_density_controlled_onnx_scout`

Hypothesis(가설):
Fixed 3-class ONNX(고정 3클래스 온엑스)가 argmax class(최대확률 클래스)만 바로 거래 신호로 쓰면 density cliff(밀도 절벽)가 생긴다. 그러나 ONNX probability tensor(온엑스 확률 텐서)를 score surface(점수 표면)로 보고, train-only fixed density thresholds(학습 구간 전용 고정 밀도 임계값)를 사전 등록하면 5/8/10 trades/day(일 5/8/10회) 축을 더 직접 제어할 수 있다.

Changed variable(변경 변수):
- runtime representation(런타임 표현): argmax signal(최대확률 신호) -> probability score threshold contract(확률 점수 임계값 계약)

Controls(통제):
- same Tier A dataset(같은 티어 A 데이터)
- same feature order(같은 피처 순서)
- same F14 opportunity label variants initially(초기에는 같은 F14 기회 라벨 변형)
- no validation/OOS threshold calibration(검증/표본밖 임계값 보정 없음)
- no quota or horizon retuning(할당량 또는 보유기간 재조정 없음)

Pre-registered score contracts(사전 등록 점수 계약):
1. `edge_margin`: `max(p_short, p_long) - p_flat`
2. `side_gap`: `abs(p_long - p_short)`
3. `utility_tilt`: `max(p_short, p_long) - 0.5 * p_flat`

Pre-registered density targets(사전 등록 밀도 목표):
- 5/day, 8/day, 10/day

Threshold policy(임계값 정책):
Thresholds(임계값)는 train split(학습 분할)에서만 target trades/day(목표 거래/일)에 맞도록 고정한다. validation/OOS(검증/표본밖)에서는 그대로 적용한다.

Success criteria(성공 기준):
- strict scout clue(엄격 탐색 단서): validation and OOS(검증과 표본밖) both net positive(순수익 양수), PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%(손실폭 15% 이하), worst subperiod DD <= 30%(최악 하위기간 손실폭 30% 이하), ONNX parity(온엑스 동등성) pass(통과)
- preserved clue(보존 단서): one or two axes improve without forbidden claim(금지 주장 없이 한두 축 개선)

Failure criteria(실패 기준):
- train-only thresholds(학습 전용 임계값)이 validation/OOS density(검증/표본밖 밀도)를 유지하지 못함
- density rises but PF/DD(수익 팩터/손실폭)가 깨짐
- score contracts(점수 계약)이 F14 argmax failure(프론티어14 최대확률 실패)와 같은 sparse result(희소 결과)만 반복함

Claim boundary(주장 경계):
This is proxy scout(프록시 탐색) only. No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Review size(검토 크기): small review(소규모 검토).

## Review Questions(검토 질문)

1. Is this novelty delta(신규성 차이) sufficiently different from F14(프론티어14), or is it just threshold micro-search(임계값 미세 탐색) disguised?
2. Are the controls(통제) strong enough to prevent validation/OOS leakage(검증/표본밖 누수)?
3. Should Frontier15(프론티어15) proceed with these score contracts(점수 계약), or should Codex(코덱스) change the stage-open hypothesis before materializing it?
