# Frontier52 Proxy Runtime Gap(프록시 런타임 차이)

Action(행동): F51 representative clue(대표 단서)를 reference-only(참조 전용)로 재물질화하고 MT5 Strategy Tester(전략 테스터)에 order-path policy(주문 경로 정책)를 적용했다.

Effect(효과): Python proxy(파이썬 프록시)와 EA order path(EA 주문 경로)의 차이가 런타임 정책으로 줄어드는지 관찰한다.

- validation_is: PF 1.03747333031916 -> 0.41; DD 4.485936564780124 -> 7.36; trades 549.0 -> 324.0; signal_diff=-1269; feature_ready_diff=0
- oos: PF 1.0675099684626137 -> 0.66; DD 2.877572942079498 -> 2.5; trades 348.0 -> 193.0; signal_diff=-914; feature_ready_diff=0
