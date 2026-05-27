# Stage337AS Completed-Day Attribution Without D/B(337AS D/B 제외 완성일 귀속)

- run_id(실행 ID): `run337AS_completed_day_attribution_without_db_and_forward_window_lock_v1`
- status(상태): `completed_stage337AS_completed_day_non_db_attribution_forward_window_locked_no_forward_decision`
- judgment(판정): `completed_day_attribution_usable_without_db_but_cost_direction_curve_fragility_remains`
- decision(결정): `stage337AS_open_run337AT_balanced_no_lookahead_repair_protocol_without_db_no_selection`
- next_action(다음 행동): `run337AT_balanced_no_lookahead_repair_protocol_without_db_v1`
- trade_count(거래 수): `344`
- net_profit(순수익): `99.89999999999999`
- profit_factor(수익 팩터): `1.1343066871017182`
- max_closed_drawdown(최대 종가 손실폭): `95.53000000000009`
- underwater_trade_share(수중 체류 거래 비중): `0.8982558139534884`
- proxy match(프록시 일치): `10/10`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Window Lock(구간 고정)

completed-day broker slice(완성일 브로커 구간)는 attribution-only(귀속 전용)이다. current-day intraday(현재일 장중) 구간은 tester cutoff(테스터 컷오프) 뒤라 Forward Passed/Failed(전진 통과/실패)에 쓰지 않는다. 효과(effect, 효과)는 보이는 구간 분석과 보이지 않는 전진 판정을 섞지 않는 것이다.

## Non-D/B Attribution(D/B 제외 귀속)

| axis(축) | bucket(버킷) | trades(거래) | net(순익) | PF(수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| `all` | `all` | `344` | `99.9` | `1.1343066871` | `cost_thin_constructive_but_fragile(수익은 있으나 비용 취약)` |
| `direction` | `buy` | `313` | `158.98` | `1.26727862679` | `constructive_completed_day_only(완성일 한정 양호)` |
| `direction` | `sell` | `31` | `-59.08` | `0.603516542514` | `negative_fragility(음수 취약)` |
| `chron_segment` | `chron_early` | `115` | `25.24` | `1.13972542073` | `cost_thin_constructive_but_fragile(수익은 있으나 비용 취약)` |
| `chron_segment` | `chron_late` | `114` | `-11.45` | `0.965924647342` | `negative_fragility(음수 취약)` |
| `chron_segment` | `chron_mid` | `115` | `86.11` | `1.37907201972` | `constructive_completed_day_only(완성일 한정 양호)` |

## Fragility Drivers(취약 동인)

| driver(동인) | severity(강도) | evidence(근거) | repair seed(수리 씨앗) |
|---|---|---|---|
| `direction_short_side_fragility` | `high` | net=-59.08;pf=0.6035165425139253;trades=31 | direction-symmetry repair(방향 대칭 수리) with no threshold search(임계값 탐색 없음) |
| `chron_late_curve_pocket` | `high` | net=-11.450000000000005;pf=0.9659246473424201;trades=114 | timestamp-safe pocket guard design(시점 안전 포켓 방어 설계) |
| `cost_buffer_thin` | `high` | one_point_pf=1.08630090555;five_point_net=-72.1175977083 | cost-buffer first pass(비용 버퍼 우선 회차) |
| `underwater_stretch` | `medium` | underwater_share=0.8982558139534884;longest=81;dd=95.53000000000009 | recovery-shape diagnostic(회복 형태 진단) |
| `db_source_absent` | `scope_lock` | direct_sidecar_ready=0 | no D/B attribution; use direction/regime/cost/curve axes only(D/B 귀속 제외, 방향/국면/비용/곡선 축만 사용) |
| `forward_window_hidden` | `scope_lock` | curve_read=cost_fragile_completed_day_slice;worst_month_net=8.48 | completed-day attribution-only until broker-visible latest window(브로커 가시 최신 구간 전까지 완성일 귀속 전용) |

## Boundary(경계)

D/B attribution(D/B 귀속)은 run337AR에서 out_of_scope_by_claim(주장 범위 밖)으로 고정했다. run337AS는 모델 학습(model training, 모델 학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화)을 하지 않았다. 다음 작업은 `run337AT_balanced_no_lookahead_repair_protocol_without_db_v1`에서 direction/cost/curve(방향/비용/곡선) 수리를 사전 선언 프로토콜로 설계하는 것이다.
