# Frontier51 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier51Z_runtime_probe_backfill_v1`
- candidate(후보): `f51c_0046`
- status(상태): `runtime_probe_observation_no_authority`
- proxy_forward_min_pf(프록시 전진 최소 PF): 1.03747333031916
- proxy_forward_max_dd(프록시 전진 최대 DD): 4.485936564780124
- proxy_forward_density(프록시 전진 거래 밀도): 2.6564885496183206 ~ 3.0
- order_path_keep_rate(주문 경로 유지율): 0.346743295019157

## Runtime KPI(런타임 성과 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.78, DD=86.37, trades(거래)=123, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.86, DD=50.15, trades(거래)=86, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy)=-0.25747333031915987, DD gap(MT5-proxy)=81.88406343521989, trade gap(MT5-proxy)=-426.0
- oos: PF gap(MT5-proxy)=-0.20750996846261371, DD gap(MT5-proxy)=47.2724270579205, trade gap(MT5-proxy)=-262.0

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
