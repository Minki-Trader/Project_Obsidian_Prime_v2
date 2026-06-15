# Frontier56 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier56Z_runtime_probe_backfill_v1`
- candidate(후보): `f56b_adverse_excursion_extratrees_d6_l80_short_mae65_mfe55_q85`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_adverse_excursion_source_did_not_transfer(부정 기억, 불리 이동 회피 원천이 MT5로 전이되지 않음)`
- hypothesis(가설): adverse-excursion stop-avoidance PF source(불리 이동 손절 회피 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): PF(수익 팩터) `1.0547158637235754` / `1.053491019549931`, DD(손실폭) `4.540304264664064` / `3.4813582772239893`, proxy trade density(프록시 거래 밀도) `3.1639344262295084` / `3.4656488549618323`, raw signal density(원신호 밀도) `7.628415300546448` / `7.893129770992366`
- label(라벨): mae_q(불리 이동 분위수)=`0.65`, mfe_q(유리 이동 분위수)=`0.55`, score_q(점수 분위수)=`0.85`

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
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.46, DD(손실폭)=29.91, trades(거래)=1389, density/day(일 밀도)=7.590163934426229, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.74, DD(손실폭)=9.27, trades(거래)=1018, density/day(일 밀도)=7.770992366412214, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시-런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.5947158637235754, DD gap(MT5-proxy, MT5-프록시)=25.369695735335938, density gap(MT5-proxy, MT5-프록시)=4.426229508196721
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.31349101954993097, DD gap(MT5-proxy, MT5-프록시)=5.78864172277601, density gap(MT5-proxy, MT5-프록시)=4.305343511450381

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
