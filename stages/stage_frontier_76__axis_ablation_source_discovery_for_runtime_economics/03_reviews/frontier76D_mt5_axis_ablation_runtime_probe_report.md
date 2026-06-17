# Frontier76D MT5 Axis Ablation Runtime Probe Report(F76D MT5 축 제거 런타임 탐침 보고서)

Updated(갱신): 2026-06-17T06:07:32Z

- status(상태): `completed_mt5_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- candidate(후보): `f76d_runtime_f76b_06637` from `f76b_06637`
- attempts/completed(시도/완료): `2/2`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `66.09/1.47/10.04/0.19487179487179487`
- claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `152.99` | `294.13` | `-141.14` | `2.08` | `6.6` | `50` | `0.18382352941176472` | `64.0` | `9.1915625` | `-7.84111111111111` | `1.1722270440697182` | `3.06` | `4.36` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |
| `oos` | `2025-10-01..2026-04-14` | `66.09` | `206.2` | `-140.11` | `1.47` | `10.04` | `38` | `0.19487179487179487` | `63.16` | `8.591666666666667` | `-10.007857142857144` | `0.8584921371303499` | `1.74` | `1.13` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |

## Proxy/Runtime Gap Boundary(프록시/런타임 간극 경계)

Action(행동): F76B proxy meaningful signal(프록시 의미 신호)을 MT5 Strategy Tester(전략 테스터)로 관찰했다.

Effect(효과): 이 보고서는 runtime probe observation(런타임 탐침 관찰)만 만들며 runtime authority(런타임 권위)나 completion(완성)을 만들지 않는다.

## Next Action(다음 행동)

`frontier76E_proxy_runtime_gap_analysis_and_repair_decision_v1`.
