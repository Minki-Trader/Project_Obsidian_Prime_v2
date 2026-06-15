# Frontier57 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier57Z_runtime_probe_backfill_v1`
- candidate(후보): `f57b_fast_exit_execution_extratrees_d6_l80_short_h4_pnl50_q90`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_fast_exit_execution_source_did_not_transfer(부정 기억, 빠른 청산 실행 원천이 MT5로 전이되지 않음)`
- failure_mode(실패 모드): `{'failure_mode_observed': ['density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)', 'source_no_transfer(원천 전이 실패)'], 'density_match_within_30pct': True, 'economics_match': False, 'parity_recheck': 'pass_proxy_onnx_only(프록시 ONNX만 통과)', 'proxy_validation_pf': 0.9406792484315578, 'proxy_oos_pf': 1.0518745268223901, 'comparison_note': 'MT5 rows compared against all-signal proxy rows; filtered proxy kept as secondary context.'}`
- hypothesis(가설): fast-exit positive execution PF source(빠른 청산 양수 실행 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): all-signal PF(전체 신호 수익 팩터) `0.9406792484315578` / `1.0518745268223901`, DD(손실폭) `17.491016868391295` / `7.077610435743598`, trade density(거래 밀도) `7.355191256830601` / `7.076335877862595`, raw signal density(원신호 밀도) `7.355191256830601` / `7.076335877862595`
- filtered proxy density(필터 프록시 밀도): `3.07103825136612` / `3.114503816793893`
- label(라벨): hold_limit(보유 한계)=`4`, pnl_q(손익 분위수)=`0.5`, pnl_cut(손익 절단값)=`-0.00032635909583289676`, score_q(점수 분위수)=`0.9`

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
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.43, DD(손실폭)=32.41, trades(거래)=1331, density/day(일 밀도)=7.273224043715847, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.68, DD(손실폭)=11.12, trades(거래)=902, density/day(일 밀도)=6.885496183206107, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.5106792484315579, DD gap(MT5-proxy, MT5-프록시)=14.918983131608702, density gap(MT5-proxy, MT5-프록시)=-0.08196721311475397
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.3718745268223901, DD gap(MT5-proxy, MT5-프록시)=4.042389564256402, density gap(MT5-proxy, MT5-프록시)=-0.1908396946564883

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
