# Frontier77D MT5 Lifecycle Negative-Control Runtime Probe Report(F77D MT5 생명주기 부정 대조 런타임 탐침 보고서)

Updated(갱신): 2026-06-17T07:27:15Z

- status(상태): `completed_mt5_lifecycle_negative_control_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- source candidate(원천 후보): `f77b_07979`
- blocked best candidate(차단된 최선 후보): `f77b_08051` because HistGBM ONNX export failed(HistGBM 온엑스 내보내기 실패).
- attempts/completed(시도/완료): `2/2`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `0.0/0.0/0.0/0.0`
- claim boundary(주장 경계): `negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `0.0` | `0.0` | `0.0` | `0.0` | `0.0` | `0` | `0.0` | `0.0` | `None` | `None` | `None` | `0.0` | `0.0` | `0` | `0` | `order_fill_gap_after_signal_parity` |
| `oos` | `2025-10-01..2026-04-14` | `0.0` | `0.0` | `0.0` | `0.0` | `0.0` | `0` | `0.0` | `0.0` | `None` | `None` | `None` | `0.0` | `0.0` | `0` | `0` | `order_fill_gap_after_signal_parity` |

## Probe Boundary(탐침 경계)

Action(행동): F77C에서 조건부 수용된 exportable surrogate(내보내기 가능한 대리 후보)를 MT5 Strategy Tester(전략 테스터)로 물질화했다.

Effect(효과): 이번 결과는 best HistGBM proxy(최선 히스토그램 그래디언트 부스팅 프록시)의 런타임 권위가 아니라, lifecycle trade mechanics(생명주기 거래 메커니즘)가 EA bridge(EA 연결)에서 어떻게 달라지는지 보는 runtime probe observation(런타임 탐침 관찰)이다.

## Next Action(다음 행동)

`frontier77E_proxy_runtime_gap_analysis_and_repair_decision_v1`.
