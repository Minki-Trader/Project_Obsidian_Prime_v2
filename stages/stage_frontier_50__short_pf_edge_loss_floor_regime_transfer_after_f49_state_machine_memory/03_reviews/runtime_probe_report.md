# Frontier50 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier50Z_runtime_probe_backfill_v1`
- candidate(후보): `f50c_0064`
- status(상태): `runtime_probe_observation_no_authority`
- proxy_forward_min_pf(프록시 전진 최소 PF): 1.0578280140948615
- proxy_forward_max_dd(프록시 전진 최대 DD): 15.637907152330031
- proxy_forward_density(프록시 전진 밀도): 6.961832061068702 ~ 7.005464480874317

## Runtime KPI(런타임 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.81, DD=76.21, trades(거래)=99, signal_diff(신호 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고서 상태)=completed, PF=0.99, DD=31.52, trades(거래)=71, signal_diff(신호 차이)=0

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy)=-0.32496745295052976, DD gap(MT5-proxy)=66.72119846915706, trade gap(MT5-proxy)=-1183.0
- oos: PF gap(MT5-proxy)=-0.0678280140948615, DD gap(MT5-proxy)=15.882092847669968, trade gap(MT5-proxy)=-841.0

Claim boundary(주장 경계): runtime_probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
