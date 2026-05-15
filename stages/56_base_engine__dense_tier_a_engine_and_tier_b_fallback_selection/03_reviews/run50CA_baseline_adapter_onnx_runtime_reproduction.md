# Stage56 run50CA BaselineAdapter ONNX Runtime Reproduction(Stage56 run50CA 기준선 어댑터 ONNX 런타임 재현)

- terminal_label(종료 라벨): `mt5_runtime_reproduction_attempted`
- adapter_id(어댑터 ID): `ba14_no_atr_sd5_lot025`
- development_anchor(개발 기준점): `run50BR/v64_v47_ctxgap14_refill_etfw_h2_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- runtime_gate_passed(런타임 게이트 통과): `True`

Action(행동): ba14 adapter(ba14 어댑터)를 ONNX backend(ONNX 백엔드)로 실제 MT5 validation/OOS(검증/표본외)에 다시 실행했다.
Effect(효과): Python adapter(Python 어댑터), ONNX parity(ONNX 동등성), MT5 runtime(MT5 런타임) 사이의 재현 차이를 한 경로에서 확인한다.

## ONNX Parity(ONNX 동등성)

- passed(통과): `True`
- max_abs_diff(최대 절대 차이): `4.237248085736667e-08`
- tolerance(허용 오차): `1e-06`
- onnx_sha256(ONNX 해시): `bc7981a7bda403c02b50ae08014d681f39212db0564f64be9f9f9688864b5e33`

## MT5 Runtime Metrics(MT5 런타임 지표)

| split(구간) | view(보기) | trades/day(일 거래 수) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | same move(동일 이동) | MFE | lot(랏) | floor(바닥) | SL | TP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| validation_is | tier_a_only | 7.420765 | 1.200000 | 1009.93 | 362.47 |  |  |  | 0.052976 | 0.000000 | 0.000000 | 0.000000 |
| validation_is | actual_routed_total | 7.420765 | 1.200000 | 1009.93 | 362.47 | 0.243689 | 0.326215 | 0.611745 | 0.052976 | 0.000000 | 0.000000 | 0.000000 |
| oos | tier_a_only | 5.200000 | 1.300000 | 1048.98 | 319.23 |  |  |  | 0.051853 | 0.000000 | 0.000000 | 0.000000 |
| oos | actual_routed_total | 5.200000 | 1.300000 | 1048.98 | 319.23 | 0.534497 | 0.349112 | 0.616732 | 0.051853 | 0.000000 | 0.000000 | 0.000000 |

## Phase A Comparison(Phase A 비교)

| split(구간) | Phase A day(Phase A 일 거래 수) | Runtime day(런타임 일 거래 수) | Phase A PF | Runtime PF(런타임 PF) | Phase A net(순손익) | Runtime net(런타임 순손익) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | 7.420765 | 7.420765 | 1.200000 | 1.200000 | 1009.93 | 1009.93 |
| OOS(표본외) | 5.200000 | 5.200000 | 1.300000 | 1.300000 | 1048.98 | 1048.98 |

## Tier Records(티어 기록)

- Tier A only validation/OOS(Tier A 단독 검증/표본외): day `7.420765` / `5.200000`, PF `1.200000` / `1.300000`, net `1009.93` / `1048.98`
- Tier B fallback-only(Tier B 대체 전용): `disabled_due_run50BR_fallback_only_damage`
- A+B actual routed total(A+B 실제 라우팅 전체): validation/OOS net `1009.93` / `1048.98`

## Gate(게이트)

- passed(통과): `True`
- failure_reasons(실패 사유): ``
- validation_reproduction_diff(검증 재현 차이): `{"max_drawdown_amount": {"abs_diff": 0.0, "passed": true, "phase_a": 362.47, "runtime": 362.47, "tolerance": 3.6247000000000003}, "net_profit": {"abs_diff": 0.0, "passed": true, "phase_a": 1009.93, "runtime": 1009.93, "tolerance": 10.0993}, "profit_factor": {"abs_diff": 0.0, "passed": true, "phase_a": 1.2, "runtime": 1.2, "tolerance": 0.02}, "trades_per_day": {"abs_diff": 0.0, "passed": true, "phase_a": 7.420765027322404, "runtime": 7.420765027322404, "tolerance": 0.02}}`
- oos_reproduction_diff(표본외 재현 차이): `{"max_drawdown_amount": {"abs_diff": 0.0, "passed": true, "phase_a": 319.23, "runtime": 319.23, "tolerance": 3.1923000000000004}, "net_profit": {"abs_diff": 0.0, "passed": true, "phase_a": 1048.98, "runtime": 1048.98, "tolerance": 10.4898}, "profit_factor": {"abs_diff": 0.0, "passed": true, "phase_a": 1.3, "runtime": 1.3, "tolerance": 0.02}, "trades_per_day": {"abs_diff": 0.0, "passed": true, "phase_a": 5.2, "runtime": 5.2, "tolerance": 0.02}}`

No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.
