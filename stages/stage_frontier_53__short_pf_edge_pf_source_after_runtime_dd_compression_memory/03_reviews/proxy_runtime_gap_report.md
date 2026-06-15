# Frontier53 Proxy Runtime Gap(프록시-런타임 차이)

Action(행동): path-quality PF source(경로 품질 수익 팩터 원천)를 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.

Effect(효과): Python proxy(파이썬 프록시)의 독립 선도달 손익과 EA order path(EA 주문 경로)의 실제 손익 차이를 분리해 본다.

- validation_is: PF(수익 팩터) 1.0018671479142887 -> 0.37; DD(손실폭) 7.96045908880354 -> 31.92; density/day(일 밀도) 7.256830601092896 -> 7.240437158469946; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
- oos: PF(수익 팩터) 1.0961906495988258 -> 0.56; DD(손실폭) 7.350606304191166 -> 19.18; density/day(일 밀도) 10.236641221374045 -> 10.206106870229007; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
