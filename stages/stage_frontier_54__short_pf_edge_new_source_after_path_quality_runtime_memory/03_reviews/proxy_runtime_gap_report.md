# Frontier54 Proxy Runtime Gap(프록시-런타임 차이)

Action(행동): runtime-shaped payoff source(런타임형 손익 원천)를 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.

Effect(효과): sequential proxy(순차 프록시)와 EA order path(EA 주문 경로)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도)로 분리한다.

- validation_is: PF(수익 팩터) 1.0279309034741884 -> 0.41; DD(손실폭) 6.593274204464006 -> 63.63; density/day(일 밀도) 5.469945355191257 -> 15.19672131147541; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
- oos: PF(수익 팩터) 1.0700525748726053 -> 0.61; DD(손실폭) 4.414364970697093 -> 28.22; density/day(일 밀도) 5.854961832061068 -> 16.51145038167939; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
