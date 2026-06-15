# Frontier53 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier53Z_runtime_probe_backfill_v1`
- candidate(후보): `f53b_logreg_l2_c05_short_q25_q70_s90`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_path_quality_proxy_did_not_transfer_to_runtime(부정 기억, 경로 품질 프록시가 런타임으로 전이되지 않음)`
- hypothesis(가설): short-only path-quality PF source(숏 전용 경로 품질 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): PF(수익 팩터) `1.0018671479142887` / `1.0961906495988258`, DD(손실폭) `7.96045908880354` / `7.350606304191166`

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: True
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
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.37, DD(손실폭)=31.92, trades(거래)=1325, density/day(일 밀도)=7.240437158469946, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.56, DD(손실폭)=19.18, trades(거래)=1337, density/day(일 밀도)=10.206106870229007, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시-런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.6318671479142887, DD gap(MT5-proxy, MT5-프록시)=23.959540911196463, density gap(MT5-proxy, MT5-프록시)=-0.016393442622950616
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.5361906495988258, DD gap(MT5-proxy, MT5-프록시)=11.829393695808834, density gap(MT5-proxy, MT5-프록시)=-0.030534351145037775

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
