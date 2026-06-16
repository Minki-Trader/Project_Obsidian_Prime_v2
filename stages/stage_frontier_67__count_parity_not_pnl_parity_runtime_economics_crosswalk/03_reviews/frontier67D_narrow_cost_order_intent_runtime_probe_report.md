# F67D Narrow Cost/Order-Intent MT5 Runtime Probe(F67D 좁은 비용/주문 의도 MT5 런타임 탐침)

Updated(갱신): 2026-06-16T14:16:12Z

Status(상태): `completed_runtime_probe_observation_no_authority`

Action(행동): F31 OOS(F31 표본외) 한 조각을 F67D 전용 run root(실행 루트)에서 MT5 Strategy Tester(MT5 전략 테스터)로 재실행했습니다.

Effect(효과): F66 기존 실행을 덮어쓰지 않고, cost identity(비용 정체성), order intent receipt(주문 의도 영수증), accounting gap(회계 간극)을 F67 단계 근거로 새로 남겼습니다.

## Selected Slice(선택 조각)

- selected_slice(선택 조각): `F31_oos`
- test_period(테스트 기간): `2025-10-01`..`2026-04-14`
- selection_reason(선택 이유): dominant trade shape(주요 거래 형태) `hold12 + ATR SLTP 1/1`, meaningful DD gap(의미 있는 손실폭 간극), order-fill/deal mismatch(주문 체결/딜 불일치)
- source_attempt(원천 시도): `f66_f31_f31b_0013_oos`
- claim_boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only(만 해당)

## Order Intent Receipt(주문 의도 영수증)

- expected_signal_count(예상 신호 수): `876`
- signal_count(신호 수): `876`
- signal_count_diff(신호 수 차이): `0`
- order_attempt_count(주문 시도 수): `361`
- order_fill_count(주문 체결 수): `361`
- trade_count(거래 수): `259`
- trades_per_day(일 거래 수): `1.3282051282051281`
- deal_count(딜 수): `518`
- deal_in_count/deal_out_count(진입/청산 딜 수): `259` / `259`
- deal_minus_order_fill(딜-주문 체결 차이): `157`

## Economics(경제성)

- net_profit(순수익): `2.31`
- gross_profit/gross_loss(총이익/총손실): `721.66` / `-719.35`
- profit_factor(수익 팩터): `1.0`
- win_rate_percent(승률 %): `36.29`
- average_win/average_loss(평균 이익/평균 손실): `7.6772340425531915` / `-4.359696969696969`
- payoff_ratio(손익비): `1.760955886593837`
- expectancy(기대값): `0.01`
- recovery_factor(회복 계수): `0.01`
- max_drawdown_percent(최대 손실폭 %): `30.58`
- long/short breakdown(롱/숏 분해): `259` / `0`
- proxy_dd(프록시 손실폭): `4.811684180485509`
- dd_delta_runtime_minus_proxy(런타임-프록시 손실폭 차이): `25.76831581951449`
- deal_commission_sum(딜 수수료 합계): `0.0`
- deal_swap_sum(딜 스왑 합계): `-14.24`

## Gap Classification(간극 분류)

| layer(층) | metric(지표) | gap_class(간극 분류) | delta(차이) |
|---|---|---|---:|
| `count_parity` | `signal_count` | `count_parity_exact` | `0` |
| `feature_readiness` | `feature_ready_count` | `feature_ready_exact` | `0` |
| `accounting_parity` | `order_fill_vs_deal_count` | `deal_minus_order_fill_positive` | `157` |
| `economics_parity` | `drawdown_percent` | `runtime_dd_exceeds_proxy_dd` | `25.76831581951449` |
| `cost_identity` | `swap_commission` | `observed_swap_with_missing_config_cost_identity` | `-14.24` |

Runtime claim boundary(런타임 주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).
