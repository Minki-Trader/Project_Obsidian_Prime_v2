# Frontier57 Proxy Runtime Gap(프록시-런타임 차이)

Action(행동): fast-exit execution source(빠른 청산 실행 원천)를 all-signal direct threshold(전체 신호 직접 임계값)로 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.

Effect(효과): proxy ranking(프록시 순위), signal density(신호 밀도), runtime economics(런타임 경제성)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이)로 분리한다.

- validation_is: PF(수익 팩터) 0.9406792484315578 -> 0.43; DD(손실폭) 17.491016868391295 -> 32.41; density/day(일 밀도) 7.355191256830601 -> 7.273224043715847; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
- oos: PF(수익 팩터) 1.0518745268223901 -> 0.68; DD(손실폭) 7.077610435743598 -> 11.12; density/day(일 밀도) 7.076335877862595 -> 6.885496183206107; feature_ready_diff(피처 준비 차이)=0; signal_diff(신호 차이)=0
