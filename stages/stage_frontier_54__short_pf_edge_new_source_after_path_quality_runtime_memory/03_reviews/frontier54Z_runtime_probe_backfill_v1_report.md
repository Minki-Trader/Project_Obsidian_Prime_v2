# Frontier54 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier54Z_runtime_probe_backfill_v1`
- candidate(후보): `f54b_extratrees_d6_l80_short_runtimepay_s70`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_runtime_shaped_payoff_proxy_did_not_transfer(부정 기억, 런타임형 손익 프록시가 MT5로 전이되지 않음)`
- hypothesis(가설): runtime-shaped short payoff PF source(런타임형 숏 손익 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): PF(수익 팩터) `1.0279309034741884` / `1.0700525748726053`, DD(손실폭) `6.593274204464006` / `4.414364970697093`, density(밀도) `5.469945355191257` / `5.854961832061068`

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: False
- InpEntryTransitionOnly: False
- InpEntryTransitionRearmMinConfidenceDelta: 0.0
- InpMaxHoldBars: 6
- InpReentryCooldownBars: 0
- InpSameDirectionReentryCooldownBars: 0
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.8
- InpAtrTakeProfitMultiplier: 1.2
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 180.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 260.0

## Runtime KPI(런타임 성과 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.41, DD(손실폭)=63.63, trades(거래)=2781, density/day(일 밀도)=15.19672131147541, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.61, DD(손실폭)=28.22, trades(거래)=2163, density/day(일 밀도)=16.51145038167939, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시-런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.6179309034741884, DD gap(MT5-proxy, MT5-프록시)=57.036725795536, density gap(MT5-proxy, MT5-프록시)=9.726775956284152
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.4600525748726053, DD gap(MT5-proxy, MT5-프록시)=23.805635029302906, density gap(MT5-proxy, MT5-프록시)=10.65648854961832

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
