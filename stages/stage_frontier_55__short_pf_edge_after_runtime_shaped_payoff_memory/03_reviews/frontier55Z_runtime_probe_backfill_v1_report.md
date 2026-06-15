# Frontier55 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier55Z_runtime_probe_backfill_v1`
- candidate(후보): `f55b_sparse_admission_extratrees_d6_l80_short_runtimepay_q65_b10_gap4`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_sparse_admission_runtime_veto_did_not_transfer(부정 기억, 희소 진입 허용 런타임 차단이 MT5로 전이되지 않음)`
- hypothesis(가설): runtime-density-aligned sparse admission source(런타임 밀도 정렬 희소 진입 허용 원천)
- proxy validation/OOS(프록시 검증/표본외): PF(수익 팩터) `1.1319474563209098` / `1.1273619272259114`, DD(손실폭) `4.467871622409481` / `5.624917165482857`, density(밀도) `4.306010928961749` / `4.6183206106870225`
- admission(진입 허용): score_q(점수 분위수)=`0.65`, daily_budget(일일 예산)=`10`, min_gap_bars(최소 간격 봉)=`4`

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
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.42, DD(손실폭)=20.84, trades(거래)=954, density/day(일 밀도)=5.213114754098361, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.64, DD(손실폭)=8.3, trades(거래)=711, density/day(일 밀도)=5.427480916030534, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시-런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.7119474563209098, DD gap(MT5-proxy, MT5-프록시)=16.37212837759052, density gap(MT5-proxy, MT5-프록시)=0.9071038251366117
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.48736192722591143, DD gap(MT5-proxy, MT5-프록시)=2.675082834517144, density gap(MT5-proxy, MT5-프록시)=0.8091603053435117

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
