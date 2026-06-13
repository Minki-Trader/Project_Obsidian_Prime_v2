# Utility Distillation Plan(효용 증류 계획)

## Families(군)

- utility_consensus(효용 합의): train subwindows(학습 하위구간)에서 side utility(방향 효용)가 안정적인 행만 long/short(롱/숏) 후보로 둡니다.
- utility_margin(효용 마진): 승리 방향 효용이 반대 방향과 flat(관망)보다 train-only margin(학습 전용 마진) 이상 커야 합니다.
- drawdown_veto_distillation(손실폭 거부 증류): raw return(원시 수익)이 양수여도 underwater burden(수중 부담)이 높으면 flat/no-trade(관망/무거래)로 증류합니다.

## First Scout Boundary(첫 탐색 경계)

Action(행동): no threshold search(임계값 탐색 없음), no class-prior bridge(클래스 사전분포 브리지 없음), argmax-only(최대확률 전용)로 확인합니다.

Effect(효과): Frontier09C(전선09C)의 density bridge repair(밀도 브리지 수리)를 반복하지 않고, target supervision(목표 감독) 자체가 네 축을 개선하는지 봅니다.
