# RUN28E Tier A Markov Broader Entry Proxy Packet(28E 실행 티어 A 마르코프 넓은 진입 대리 묶음)
## Judgment(판정)
- run(실행): `run28E_tier_a_markov_broader_entry_proxy_probe_v1`
- status(상태): `reviewed_monthly_mt5_probe_completed`
- judgment(판정): `inconclusive_tier_a_markov_broader_entry_proxy_probe_completed`
- rule(규칙): `exclude_vol_high_or_adx_20_25`
- external verification(외부 검증): `completed`
- boundary(경계): `stage34_broader_entry_proxy_monthly_mt5_probe_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28F_tier_a_markov_vol_adx_component_dependency_probe_v1`

효과(effect, 효과): 월별 생존성(monthly robustness, 월별 버팀)을 먼저 보고, 같은 후보를 MT5(`MetaTrader 5`, 메타트레이더5) feature CSV row omission(피처 CSV 행 제거) 방식으로 실제 Strategy Tester(전략 테스터)에 찔렀다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Monthly Read(월별 판독)
- validation(검증): trades(거래 수) `59`, net(순손익) `211.31`, PF(수익 팩터) `2.081755`, min leave-one-out net(월 하나 제외 최저 순손익) `132.72`, status(상태) `pass`
- OOS(표본외): trades(거래 수) `32`, net(순손익) `78.42`, PF(수익 팩터) `1.541089`, min leave-one-out net(월 하나 제외 최저 순손익) `4.91`, status(상태) `warn`
- OOS dependency(OOS 의존성): top positive month(최대 양수 월) `2025-10`, top positive share(최대 양수 월 비중) `0.66555`, flags(표식) `oos_leave_one_net_margin_thin;top_positive_month_dependency`

효과(effect, 효과): 후보는 한 달을 빼도 전체 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않는다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `4.91`까지 얇아져서, main seed(메인 씨앗)가 아니라 dependency clue(의존성 단서)로 다루는 편이 맞다.

## MT5 Runtime Probe(MT5 런타임 탐침)
- validation(검증): trades(거래 수) `59`, net(순손익) `202.52`, PF(수익 팩터) `1.77`, feature_ready(피처 준비 수) `472`
- OOS(표본외): trades(거래 수) `35`, net(순손익) `92.67`, PF(수익 팩터) `1.43`, feature_ready(피처 준비 수) `322`

효과(effect, 효과): 이번 MT5(메타트레이더5) 검증은 EA(`Expert Advisor`, 전문가 자문) 로직을 새로 바꾸지 않고, `vol_high` 또는 `adx_20_25`에 걸린 feature row(피처 행)를 빼서 해당 시간 신호를 만들지 않게 한 좁은 runtime probe(런타임 탐침)다. 그래서 “터미널에서도 대략 같은 필터 방향이 살아 있는가”는 보지만, operating rule(운영 규칙) 확정은 아니다.

## Files(파일)
- monthly leave-one-out(월 하나 제외): `stages/34_regime_mechanism__tier_a_markov_long_permission_attribution/02_runs/run28E_tier_a_markov_broader_entry_proxy_probe_v1/results/monthly_leave_one_out.csv`
- monthly summary(월별 요약): `stages/34_regime_mechanism__tier_a_markov_long_permission_attribution/02_runs/run28E_tier_a_markov_broader_entry_proxy_probe_v1/results/monthly_survival_summary.csv`
- aggregate summary(집계 요약): `docs/agent_control/packets/stage34_run28E_tier_a_markov_broader_entry_proxy_probe_v1/aggregate_summary.json`
