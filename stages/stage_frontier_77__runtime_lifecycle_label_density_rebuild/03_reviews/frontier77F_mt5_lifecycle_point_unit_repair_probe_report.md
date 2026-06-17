# Frontier77F MT5 Lifecycle Point-Unit Repair Probe(F77F MT5 생명주기 포인트 단위 수리 탐침)

Updated(갱신): 2026-06-17T07:45:28Z

- status(상태): `completed_mt5_lifecycle_point_unit_repair_probe_observation_no_authority`
- judgment(판정): `point_unit_repair_probe_completed_gap_analysis_required_no_authority`
- repair action(수리 행동): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환했다.
- attempts/completed(시도/완료): `2/2`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `4.48/1.23/1.41/0.14871794871794872`
- claim boundary(주장 경계): `repair_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래 수) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `14.64` | `104.01` | `-89.37` | `1.16` | `3.33` | `129` | `0.4742647058823529` | `43.41` | `1.8573214285714286` | `-1.2242465753424658` | `1.5171138445307628` | `0.11` | `0.85` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `oos` | `2025-10-01..2026-04-14` | `4.48` | `23.96` | `-19.48` | `1.23` | `1.41` | `29` | `0.14871794871794872` | `44.83` | `1.843076923076923` | `-1.2175` | `1.5138208813773495` | `0.15` | `0.63` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |

## Repair Boundary(수리 경계)

Action(행동): F77D order fill gap(주문 체결 간극)을 수리하기 위해 SL/TP point scale(SL/TP 포인트 배율)만 1에서 100으로 바꿨다.

Effect(효과): 결과가 좋아도 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않고, F77G gap analysis(간극 분석)로 보낸다.

## Next Action(다음 행동)

`frontier77G_post_repair_gap_analysis_or_closeout_decision_v1`.
