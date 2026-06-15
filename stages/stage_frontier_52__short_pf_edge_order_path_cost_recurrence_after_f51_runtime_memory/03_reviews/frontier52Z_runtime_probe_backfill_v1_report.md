# Frontier52 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier52Z_runtime_probe_backfill_v1`
- reference_candidate(참조 후보): `f51c_0046`
- status(상태): `runtime_probe_observation_no_authority`
- source_boundary(원천 경계): F51 candidate is reference-only(F51 후보는 참조 전용)
- proxy_forward_min_pf(프록시 전진 최소 PF): 1.03747333031916
- proxy_forward_max_dd(프록시 전진 최대 DD): 4.485936564780124
- proxy_forward_density(프록시 전진 거래 밀도): 2.6564885496183206 ~ 3.0
- order_path_keep_rate(주문 경로 유지율): 0.346743295019157

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: True
- InpEntryTransitionOnly: True
- InpEntryTransitionRearmMinConfidenceDelta: 0.02
- InpMaxHoldBars: 6
- InpReentryCooldownBars: 3
- InpSameDirectionReentryCooldownBars: 6
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.8
- InpAtrTakeProfitMultiplier: 1.2
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 180.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 260.0

## Runtime KPI(런타임 성과 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.41, DD=7.36, trades(거래)=324, signal_diff(신호 차이)=-1269, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.66, DD=2.5, trades(거래)=193, signal_diff(신호 차이)=-914, feature_ready_diff(피처 준비 차이)=0

Signal_diff note(신호 차이 메모): negative signal_diff(음수 신호 차이)는 entry-transition/close-on-flat policy(전환 진입/무신호 청산 정책)가 expected export signal(예상 내보내기 신호)을 의도적으로 억제한 값이다. Feature_ready_diff(피처 준비 차이)는 `0`이어야 local parity boundary(로컬 동등성 경계)가 유지된다.

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy)=-0.62747333031916, DD gap(MT5-proxy)=2.8740634352198766, trade gap(MT5-proxy)=-225.0
- oos: PF gap(MT5-proxy)=-0.40750996846261367, DD gap(MT5-proxy)=-0.3775729420794982, trade gap(MT5-proxy)=-155.0

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
