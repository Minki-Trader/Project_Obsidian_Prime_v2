# Frontier18 Selection Metric Spec(전선18 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본외) PF, density, DD, smoothness(수익 팩터, 빈도, 손실폭, 매끄러움)를 함께 봅니다.
- seed surface(씨앗 표면): DD/smoothness(손실폭/매끄러움)를 줄이면서 density(빈도)가 3/day(일 3회) 아래로 무너지지 않는 profile(프로필)만 기록합니다.
- negative memory(부정 기억): Stage344(344단계)처럼 exit overlay(청산 덧씌움)가 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손하거나, F17(전선17)처럼 MT5 DD collapse(MT5 손실폭 붕괴)가 반복되면 닫습니다.
- runtime probe observation(런타임 탐침 관찰): closeout(마감) 전 best-or-seed candidate(최선 또는 씨앗 후보) 1개를 MT5 runtime probe(MT5 런타임 탐침)로 시도합니다.
