# Frontier55 Proxy Runtime Gap(프록시-런타임 차이)

Action(행동): sparse admission source(희소 진입 허용 원천)를 runtime veto tape(런타임 차단 테이프)와 함께 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.

Effect(효과): admitted proxy(허용 프록시)와 EA order path(EA 주문 경로)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이)로 분리한다.

- validation_is: PF(수익 팩터) 1.1319474563209098 -> 0.42; DD(손실폭) 4.467871622409481 -> 20.84; density/day(일 밀도) 4.306010928961749 -> 5.213114754098361; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
- oos: PF(수익 팩터) 1.1273619272259114 -> 0.64; DD(손실폭) 5.624917165482857 -> 8.3; density/day(일 밀도) 4.6183206106870225 -> 5.427480916030534; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
