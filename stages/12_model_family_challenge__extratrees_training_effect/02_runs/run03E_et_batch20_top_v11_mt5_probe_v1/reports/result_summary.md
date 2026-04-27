# run03E RUN03D Top Variant MT5 Probe(상위 변형 MT5 검증)

## Boundary(경계)

- run(실행): `run03E_et_batch20_top_v11_mt5_probe_v1`
- source run(원천 실행): `run03D_et_standalone_batch20_v1`
- source variant(원천 변형): `v11_base_leaf20_q85`
- standalone boundary(단독 경계): Stage10/11(10/11단계) inheritance(계승)와 baseline(기준선)은 사용하지 않았다.
- external verification(외부 검증): `completed`
- judgment(판정): `inconclusive_run03d_top_variant_mt5_runtime_probe_completed`
- effect(효과): RUN03D(실행 03D) 최고 변형을 MT5(`MetaTrader 5`, 메타트레이더5) 런타임으로 확인하되, alpha quality(알파 품질)나 operating promotion(운영 승격)으로 말하지 않는다.

## Python Replay(파이썬 재현)

| split(분할) | signals(신호) | hit rate(적중률) |
|---|---:|---:|
| validation(검증) | 1477 | 0.3926878808395396 |
| OOS(표본외) | 1148 | 0.4573170731707317 |

## MT5 Strategy Tester(MT5 전략 테스터)

| split(분할) | status(상태) | net profit(순손익) | PF(수익팩터) | trades(거래) | max DD(최대 손실) |
|---|---|---:|---:|---:|---:|
| validation(검증) | completed | -205.14 | 0.88 | 301 | 335.29 |
| OOS(표본외) | completed | 362.83 | 1.44 | 210 | 118.56 |

## Runtime Parity(런타임 동등성)

- ONNX parity(ONNX 동등성): `True`
- max abs diff(최대 절대 차이): `1.616518588987148e-07`
- threshold(임계값): `0.4205732909508156`
- effect(효과): Python probability(파이썬 확률)와 MT5 model handoff(모델 인계)가 같은 확률 표면을 쓰는지 확인한다.
