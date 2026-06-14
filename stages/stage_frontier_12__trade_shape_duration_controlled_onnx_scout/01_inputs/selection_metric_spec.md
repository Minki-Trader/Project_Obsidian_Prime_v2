# Frontier12 Selection Metric Spec(프론티어12 선택 지표 명세)

## Metric Set(지표 세트)

- aggregate PF/density/DD(합계 수익 팩터/빈도/손실폭)
- month and quarter subperiod PF/density/DD(월/분기 하위기간 수익 팩터/빈도/손실폭)
- worst subperiod DD(최악 하위기간 손실폭)
- underwater ratio proxy(회복 전 체류 비율 프록시)
- smoothness proxy(매끄러움 프록시)
- ONNX parity(온엑스 동등성)

## Selection Rule(선택 규칙)

Strict clue(엄격 단서)는 validation/OOS(검증/표본밖) 네 축을 동시에 보며, one-axis improvement(한 축 개선)만으로는 앞으로 보내지 않습니다.

## Claim Boundary(주장 경계)

This metric(이 지표)는 scout ranking(탐색 순위) 전용입니다. Effect(효과): baseline/promotion/runtime authority/live readiness(기준선/승격/런타임 권위/실거래 준비)를 만들지 않습니다.
