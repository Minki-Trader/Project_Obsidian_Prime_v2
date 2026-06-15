# F61 Runtime Probe Report(F61 런타임 탐침 보고)

- judgment(판정): `runtime_probe_observation_no_authority`
- run(실행): `frontier61Z_runtime_probe_backfill_v1`

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|
| validation_is | completed | completed | 0.43 | 53.18 | 12.311475409836065 | 0 | 0 |
| oos | completed | completed | 0.71 | 15.16 | 11.442748091603054 | 0 | 0 |

Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).

# F61 Proxy-Runtime Gap Report(F61 프록시-런타임 차이 보고)

| split(분할) | proxy PF(프록시 PF) | MT5 PF(MT5 PF) | PF gap(PF 차이) | proxy DD(프록시 DD) | MT5 DD(MT5 DD) | density gap(밀도 차이) |
|---|---:|---:|---:|---:|---:|---:|
| validation_is | 0.9797838219739115 | 0.43 | -0.5497838219739115 | 5.755560108852686 | 53.18 | 7.519125683060109 |
| oos | 1.1169141590649971 | 0.71 | -0.40691415906499717 | 3.075204919576424 | 15.16 | 6.664122137404581 |
