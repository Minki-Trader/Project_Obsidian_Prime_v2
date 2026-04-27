# RUN03C Standalone ExtraTrees MT5 Runtime Probe(단독 엑스트라 트리 MT5 런타임 탐침)

- run_id(실행 ID): `run03C_et_standalone_mt5_runtime_probe_v1`
- source model run(원천 모델 실행): `run03B_et_standalone_fwd12_v1`
- standalone scope(단독 범위): `true(참)`
- Stage 10/11 inheritance(Stage 10/11 계승): `false(아님)`
- comparison baseline(비교 기준선): `none(없음)`
- threshold method(임계값 방식): `standalone_validation_nonflat_confidence_q90`
- nonflat threshold(비평탄 임계값): `0.4516214515113969`
- ONNX parity(온닉스 동등성): `True`
- external verification status(외부 검증 상태): `completed`

## Python Replay(파이썬 재현)

| split(분할) | signals(신호) | hit rate(적중률) |
|---|---:|---:|
| validation(검증) | `604` | `0.3526490066225166` |
| OOS(표본외) | `463` | `0.42764578833693306` |

## MT5 Strategy Tester(MT5 전략 테스터)

| split(분할) | status(상태) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max drawdown(최대 손실) |
|---|---|---:|---:|---:|---:|
| validation(검증) | `completed` | `-13.18` | `0.98` | `120` | `173.72` |
| OOS(표본외) | `completed` | `249.57` | `1.69` | `89` | `107.93` |

## Judgment(판정)

`inconclusive_standalone_extratrees_mt5_runtime_probe_completed`

효과(effect, 효과): 이 실행은 Stage 12(12단계) 단독 ExtraTrees(엑스트라 트리)를 MT5 runtime_probe(런타임 탐침)로 본 것이다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 주장하지 않는다.
