# Frontier50 Proxy Runtime Gap(프록시 런타임 차이)

Action(행동): F50 scout clue(탐색 단서)를 MT5 Strategy Tester(전략 테스터)에 넣어 proxy/runtime KPI(프록시/런타임 지표)를 비교했다.

Effect(효과): Python first-hit proxy(파이썬 첫 터치 프록시)와 실제 EA order path(EA 주문 경로)의 차이를 다음 stage(단계)의 negative memory/preserved clue(부정 기억/보존 단서)로 쓴다.

- validation_is: PF 1.1349674529505298 -> 0.81; DD 9.488801530842927 -> 76.21; trades 1282.0 -> 99.0; signal_diff=0; feature_ready_diff=0
- oos: PF 1.0578280140948615 -> 0.99; DD 15.637907152330031 -> 31.52; trades 912.0 -> 71.0; signal_diff=0; feature_ready_diff=0
