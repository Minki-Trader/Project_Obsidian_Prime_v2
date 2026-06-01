# Stage359C High-Density Label Pivot MT5 Probe Review(359C 고밀도 라벨 전환 MT5 탐침 검토)

## Judgment(판정)

- status(상태): `reviewed_stage359C_high_density_label_pivot_mt5_probe_oos_positive_validation_negative_no_selection`
- judgment(판정): `runtime_probe_positive_oos_only_validation_unstable_no_operating_claim`
- decision(결정): `stage359C_open_run359D_branch_to_stage360_regime_stability_pivot_v1`
- next_run_id(다음 실행 ID): `run359D_branch_to_stage360_regime_stability_pivot_v1`
- claim_boundary(주장 경계): `reviewed_runtime_probe_positive_oos_only_validation_negative_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): Stage359B(359B 실행)의 MT5 Strategy Tester(MT5 전략 테스터) 결과를 KPI(핵심 성과 지표), proxy-MT5 diff(프록시-MT5 차이), trade shape(거래 형태), cost stress(비용 압박)로 검토했다.

Effect(효과): OOS(표본외) 긍정 단서는 다음 공격 탐색 씨앗으로 남기고, validation(검증) 음수와 drawdown(낙폭) 때문에 candidate selection(후보 선택)과 operating promotion(운영 승격)은 닫아 둔다.

## MT5 KPI(MT5 핵심 성과 지표)

| attempt(시도) | split(분할) | net(순수익) | PF(수익 팩터) | expectancy(기대값) | RF(회복 계수) | DD(낙폭) | trades(거래수) | trades/day(일별 거래수) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| q01_pside_all_oos | oos | 191.02 | 1.09 | 0.28 | 0.66 | 287.40 | 678 | 5.18 |
| q01_pside_all_validation | validation | -495.32 | 0.65 | -1.56 | -0.98 | 504.98 | 318 | 1.74 |
| q05_pside_all_oos | oos | 262.85 | 1.09 | 0.28 | 0.92 | 285.94 | 936 | 7.15 |
| q05_pside_all_validation | validation | -222.41 | 0.95 | -0.17 | -0.46 | 483.00 | 1283 | 7.01 |

## Runtime Parity(런타임 동등성)

- proxy-MT5 rows(프록시-MT5 행): `27869`
- mismatch rows(불일치 행): `0`
- max probability diff(최대 확률 차이): `0.00000039`

Action(행동): proxy expected value(프록시 예상값)를 MT5 runtime telemetry(MT5 런타임 원격측정)와 행 단위로 비교했다.

Effect(효과): probability/decision parity(확률/판정 동등성)는 강하지만, 이 근거는 runtime probe(런타임 탐침)이지 runtime authority(런타임 권위)가 아니다.

## Attribution(귀속)

- best read(최선 판독): `q05_pside_all_oos`
- OOS positive rows(표본외 양수 행): `2/2`
- validation positive rows(검증 양수 행): `0/2`
- q05 OOS monthly positive(월별 양수): `2/7`
- q05 validation net(검증 순수익): `-222.41`
- q05 validation max DD%(검증 최대 낙폭%): `94.77`

| q05 OOS month(q05 표본외 월) | trades(거래수) | net(순수익) | win%(승률) |
|---|---:|---:|---:|
| 2025-10 | 133 | -55.67 | 45.1 |
| 2025-11 | 151 | 339.19 | 45.7 |
| 2025-12 | 143 | -124.53 | 45.5 |
| 2026-01 | 140 | -22.29 | 45.7 |
| 2026-02 | 128 | 307.73 | 49.2 |
| 2026-03 | 172 | -67.95 | 43.0 |
| 2026-04 | 69 | -117.82 | 42.0 |

## Cost Stress(비용 압박)

| extra drag/trade(거래당 추가 비용) | q05 OOS net after drag(비용 후 순수익) | survives(양수 유지) |
|---:|---:|---:|
| 0.2 | 75.65 | True |
| 0.3 | -17.95 | False |

Action(행동): 거래당 추가 drag(비용 끌림)를 proxy stress(프록시 압박)로 적용했다.

Effect(효과): q05 OOS(표본외)는 `0.20` 추가 비용까지 양수지만 `0.30`에서는 음수로 전환되어 cost buffer(비용 완충)가 얇다.

## Next Action(다음 행동)

`run359D_branch_to_stage360_regime_stability_pivot_v1`에서 Stage360(360단계) regime stability pivot(국면 안정성 전환)을 연다. 우선순위는 q05 OOS long/cash edge(표본외 롱/현금장 우위)를 살리고, validation short/cash loss(검증 숏/현금장 손실), 월별 불안정(monthly instability, 월별 불안정), 비용 민감도(cost sensitivity, 비용 민감도)를 직접 제약으로 거는 것이다.
