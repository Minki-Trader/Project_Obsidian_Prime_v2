# Frontier79E Proxy/Runtime Gap Analysis and Repair Decision(F79E 프록시/런타임 간극 분석과 수리 결정)

Updated(갱신): 2026-06-17T11:18:50Z

- status(상태): `completed_proxy_runtime_gap_analysis_repair_required_no_authority`
- judgment(판정): `runtime_economics_gap_caused_by_intrabar_fill_order_and_bidask_geometry_no_authority`
- claim boundary(주장 경계): `gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Finding(발견)

- signal count parity(신호 수 동등성): passed(통과). MT5 order count(MT5 주문 수)는 proxy selected count(프록시 선택 수)와 같다.
- feature readiness parity(피처 준비 동등성): passed(통과). feature_ready_diff(피처 준비 차이)는 0이다.
- economic gap(경제성 간극): validation(검증)은 proxy PF 3.70에서 runtime PF 1.04로 줄었고, OOS(표본외)는 proxy PF 2.26에서 runtime PF 1.53으로 줄었다.
- dominant cause(주요 원인): M5 close_direction fill order(M5 종가방향 체결 순서)가 real-tick order(실제 틱 순서)를 대체하지 못했다. long entry(롱 진입)는 raw open(원시 시가)이 아니라 ask entry(매수 호가 진입)로 spread(스프레드)만큼 이동한다.

## Split KPI(분할 핵심 성과 지표)

| split(분할) | proxy net/PF/DD/trades(프록시 순수익/수익 팩터/손실폭/거래) | runtime net/PF/DD/trades(런타임 순수익/수익 팩터/손실폭/거래) | signal diff(신호 차이) | feature diff(피처 차이) | both-hit rows(동시 도달 행) | close-direction mismatch(종가방향 불일치) |
|---|---|---|---:|---:|---:|---:|
| `validation` | `8.037095173111059/3.696428571428572/0.19870963783409934/12.0` | `0.28/1.04/0.76/12.0` | `0.0` | `0.0` | `3` | `3` |
| `oos` | `3.566128321843979/2.2641509433962264/0.18806447866440976/8.0` | `2.19/1.53/0.53/8.0` | `0.0` | `0.0` | `4` | `4` |

## Repair Decision(수리 결정)

- next action(다음 행동): `frontier79F_ambiguous_fill_order_guard_repair_proxy_v1`
- repair scope(수리 범위): ambiguous both-hit bars(손절/익절 동시 도달 봉)를 거부하거나 pessimistic order(보수 체결 순서)로 라벨링하는 proxy repair(프록시 수리)를 실행한다.
- expected effect(예상 효과): real tick order(실제 틱 순서)를 모르는 M5 OHLC(5분봉 시가/고가/저가/종가)의 낙관 편향을 줄인다.
- stop condition(중단 조건): density(밀도)가 더 낮아지거나 dual positive(검증/표본외 양수)가 사라지면 F79는 negative memory(부정 기억) 쪽으로 닫는다.

## Global Diagnostics(전체 진단)

- diagnostic_trade_rows(진단 거래 행): `20`
- both_hit_ambiguous_rows(동시 도달 모호 행): `7`
- close_direction_vs_runtime_win_mismatch_rows(종가방향/런타임 승패 불일치 행): `7`
- pessimistic_vs_runtime_win_mismatch_rows(보수순서/런타임 승패 불일치 행): `2`
