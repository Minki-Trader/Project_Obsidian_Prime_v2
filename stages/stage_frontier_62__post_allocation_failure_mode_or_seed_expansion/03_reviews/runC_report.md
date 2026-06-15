# F62 Runtime Probe Report(F62 런타임 탐침 보고)

- judgment(판정): `runtime_probe_observation_no_authority`
- run(실행): `frontier62Z_runtime_probe_backfill_v1`

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | orders/day(일 주문시도) | raw signals/day(일 원신호) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| validation_is | completed | completed | 0.36 | 22.31 | 4.901639344262295 | 4.907103825136612 | 28.55191256830601 | -685 | 0 |
| oos | completed | completed | 0.61 | 9.53 | 5.67175572519084 | 5.709923664122138 | 31.9618320610687 | -532 | 0 |

Read(판독): density(밀도)는 target neighborhood(목표 근처)로 이동했지만 PF translation(PF 전환)은 실패했다.
Signal caveat(신호 주의): signal diff(신호 차이)는 event-gated decision(이벤트 게이트 결정) 근사 차이로만 읽고, feature_ready_diff=0(피처 준비 차이 0)와 ONNX parity(온엑스 동등성)를 함께 본다.
Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).

# F62 Proxy-Runtime Gap Report(F62 프록시-런타임 차이 보고)

| split(분할) | proxy PF(프록시 PF) | MT5 PF(MT5 PF) | PF gap(PF 차이) | proxy DD(프록시 DD) | MT5 DD(MT5 DD) | density gap(밀도 차이) |
|---|---:|---:|---:|---:|---:|---:|
| validation_is | 1.0977429734981603 | 0.36 | -0.7377429734981603 | 3.3675692177402294 | 22.31 | 0.6939890710382519 |
| oos | 0.9826772240239987 | 0.61 | -0.3726772240239987 | 5.642512356890384 | 9.53 | 0.8702290076335881 |
