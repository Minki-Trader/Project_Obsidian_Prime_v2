# Alpha Stage Transition Philosophy Correction(알파 단계 전환 철학 정정)

- date(날짜): `2026-05-01`
- status(상태): `accepted_policy_sync(정책 동기화 수락)`
- scope(범위): Stage 10(10단계), Stage 11(11단계), future alpha exploration stages(향후 알파 탐색 단계)
- boundary(경계): interpretation and policy correction only(해석 및 정책 정정만 해당); no trading result change(거래 결과 변경 없음)

## Decision(결정)

알파 탐색 단계(alpha exploration stage, 알파 탐색 단계)의 stage transition(단계 전환)은 baseline selection(기준선 선택)이 아니라 topic pivot(주제 전환)이다.

closeout(마감)은 기준 run(기준 실행)을 정하는 자리가 아니다. closeout(마감)은 남은 branch(갈래)를 seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건)으로 분류하는 자리다.

baseline(기준선), operating reference(운영 기준), promotion_candidate(승격 후보), runtime_authority(런타임 권위)는 별도 promotion/operating packet(승격/운영 작업 묶음)이 열리고 필요한 gate(게이트)가 닫힐 때만 선언한다.

## Stage 10 to Stage 11 Correction(Stage 10에서 Stage 11 정정, 10단계에서 11단계 정정)

Stage 10(10단계) closeout(마감)의 과거 표현에는 `run01Y(실행 01Y)`가 baseline candidate(기준선 후보) 또는 selected baseline(선택 기준선)처럼 적힌 부분이 있다.

현재 진실(current truth, 현재 진실)은 그 표현을 superseded historical wording(대체된 역사적 표현)으로 본다.

정정된 해석(corrected interpretation, 정정 해석)은 다음과 같다.

- `run01Y(실행 01Y)`는 seed surface(씨앗 표면), preserved clue(보존 단서), reference surface(참고 표면)다.
- Stage 10(10단계)에서 Stage 11(11단계)로 간 것은 winner selection(승자 선택)이 아니라 topic pivot(주제 전환)이다.
- Stage 11(11단계)은 LightGBM(`LightGBM`, 라이트GBM), label horizon(라벨 예측수평선), rank threshold(순위 임계값), context gate(문맥 제한), routed fallback(라우팅 대체)을 파는 새 질문(question, 질문)이다.
- Stage 11(11단계)은 Stage 10(10단계) 기준선(baseline, 기준선)을 검증하는 단계가 아니다.

## Future Rule(향후 규칙)

각 alpha exploration stage(알파 탐색 단계)는 주제 제한(subject restriction, 주제 제한)으로 탐색을 좁히지 않는다. 더 이상 의미 있게 파볼 branch(갈래)가 없을 때까지 broad sweep(넓은 탐색), extreme sweep(극단 탐색), stress test(압박 시험), failure boundary(실패 경계)를 확인한다.

의미 없는 미세조정(meaningless micro-tuning, 의미 없는 미세조정)은 하지 않는다. 같은 임계값(threshold, 임계값) 주변을 반복하는 작업은 새 정보를 만들 때만 허용한다.

## Updated Policy Docs(갱신된 정책 문서)

- `docs/policies/stage_structure.md`
- `docs/policies/exploration_mandate.md`

효과(effect, 효과)는 앞으로 Stage 13(13단계), Stage 20(20단계) 같은 미래 stage(미래 단계)에서도 closeout(마감)을 baseline(기준선) 선언으로 오해하지 않게 하는 것이다.

## Claim Boundary(주장 경계)

이 decision memo(결정 메모)는 trading result(거래 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다.

효과(effect, 효과)는 Stage 10(10단계)과 Stage 11(11단계)의 역사적 기록(historical record, 역사 기록)을 지우지 않고, 현재 해석(current interpretation, 현재 해석)과 미래 규칙(future rule, 미래 규칙)을 분리하는 것이다.
