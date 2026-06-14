# Frontier16 Selection Metric Spec(프론티어16 선택 지표 명세)

- strict scout clue(엄격 탐색 단서): `edge_margin__target8`가 validation/OOS(검증/표본밖) 양쪽에서 PF/density/DD/subperiod/parity(수익 팩터/빈도/손실폭/하위기간/동등성)를 통과해야 합니다.
- preserved clue(보존 단서): density(빈도)가 5~10/day(일 5~10회)를 유지하고 PF/DD/smoothness(수익 팩터/손실폭/매끄러움) 중 좁은 축이 개선될 때만 기록합니다.
- negative memory(부정 기억): 0 strict + 0 preserved(엄격 0 + 보존 0)이면 같은 단계 안 repair ladder(수리 사다리)를 열지 않습니다.
