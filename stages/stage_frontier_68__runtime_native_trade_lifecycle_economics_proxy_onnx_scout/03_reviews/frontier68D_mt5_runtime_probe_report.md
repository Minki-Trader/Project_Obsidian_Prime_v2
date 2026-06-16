# F68D MT5 Runtime Probe(F68D MT5 런타임 탐침)

Updated(갱신): 2026-06-16T17:38:28Z

## Action And Effect(행동 및 효과)

Action(행동): F68C에서 ONNX export(ONNX 내보내기)와 parity pass(동등성 통과)를 받은 두 후보 축을 MT5 Strategy Tester(MT5 전략 테스터)에서 validation/OOS(검증/표본외)로 실행했다.

Effect(효과): winner(승자)를 고르지 않고 density axis(밀도 축)와 PF axis(수익 팩터 축)의 proxy/runtime KPI gap(프록시/런타임 KPI 간극), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), accounting/trade-shape gap(회계/거래 형태 간극)을 분리 기록했다.

- status(상태): `completed_mt5_runtime_probe_observation_no_authority(MT5 런타임 탐침 관찰 완료, 권위 없음)`
- judgment(판정): `runtime_probe_observation_recorded_no_authority(MT5 런타임 탐침 관찰 기록, 권위 없음)`
- attempts(시도 수): `4`
- local_verification_passed(로컬 검증 통과): `True`

## Runtime KPI(런타임 핵심 성과 지표)

| axis(축) | split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `density_axis` | `validation` | `2025-01-02..2025-10-01` | `-294.46` | `2885.89` | `-3180.35` | `0.91` | `71.13` | `1860` | `6.838235` | `0` | `0` |
| `density_axis` | `oos` | `2025-10-01..2026-04-14` | `103.48` | `2655.46` | `-2551.98` | `1.04` | `26.84` | `1649` | `8.45641` | `0` | `0` |
| `pf_axis` | `validation` | `2025-01-02..2025-10-01` | `2.12` | `2.17` | `-0.05` | `43.4` | `0.35` | `2` | `0.007353` | `0` | `0` |
| `pf_axis` | `oos` | `2025-10-01..2026-04-14` | `1.52` | `1.52` | `0` | `0` | `0.31` | `1` | `0.005128` | `0` | `0` |

## Gap Notes(간극 메모)

- `density_axis/validation`: proxy PF/DD/trades_day(프록시 수익 팩터/손실폭/일 거래) `1.043101/11.9191/7.476015` -> runtime(런타임) `0.91/71.13/6.838235`; gap_cause(간극 원인) `tester_economics_observed(테스터 경제성 관찰)`.
- `density_axis/oos`: proxy PF/DD/trades_day(프록시 수익 팩터/손실폭/일 거래) `1.047846/12.756/9.659794` -> runtime(런타임) `1.04/26.84/8.45641`; gap_cause(간극 원인) `tester_economics_observed(테스터 경제성 관찰)`.
- `pf_axis/validation`: proxy PF/DD/trades_day(프록시 수익 팩터/손실폭/일 거래) `99/0/1` -> runtime(런타임) `43.4/0.35/0.007353`; gap_cause(간극 원인) `proxy_pf_saturation_ceiling(PF 포화 상한);tester_economics_observed(테스터 경제성 관찰)`.
- `pf_axis/oos`: proxy PF/DD/trades_day(프록시 수익 팩터/손실폭/일 거래) `99/0/1` -> runtime(런타임) `0/0.31/0.005128`; gap_cause(간극 원인) `proxy_pf_saturation_ceiling(PF 포화 상한);tester_economics_observed(테스터 경제성 관찰)`.

Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
