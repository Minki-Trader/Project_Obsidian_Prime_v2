# Frontier59 Proxy Runtime Gap(프록시-런타임 차이)

Action(행동): directional long quality source(방향성 롱 품질 원천)를 direct p_long threshold(직접 p_long 임계값)로 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.

Effect(효과): proxy ranking(프록시 순위), signal density(신호 밀도), runtime economics(런타임 경제성)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이)로 분리한다.

- validation_is: PF(수익 팩터) 1.0578215704880256 -> 0.46; DD(손실폭) 11.437750113936607 -> 22.84; density/day(일 밀도) 5.551912568306011 -> 5.475409836065574; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
- oos: PF(수익 팩터) 1.0157994712511802 -> 0.58; DD(손실폭) 7.416280476978832 -> 10.27; density/day(일 밀도) 5.3816793893129775 -> 5.251908396946565; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
