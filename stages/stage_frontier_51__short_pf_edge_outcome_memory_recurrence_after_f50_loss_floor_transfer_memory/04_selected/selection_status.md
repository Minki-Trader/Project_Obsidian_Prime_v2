# F51 Selection Status(선택 상태)

- closeout_class(마감 분류): `negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- runtime_probe_run(런타임 탐침 실행): `frontier51Z_runtime_probe_backfill_v1`
- runtime_probe_candidate(런타임 탐침 후보): `f51c_0046`
- next_stage(다음 단계): `stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory`
- next_run(다음 실행): `frontier52A_stage_open_short_pf_edge_order_path_cost_recurrence_hypothesis_design_v1`

## Proxy Result(프록시 결과)

- scout/seed/runtime(탐색/씨앗/런타임): 0/0/0
- representative_candidate(대표 후보): `f51c_0046`, selected as best simultaneous axis-gap observation(동시 축 간극 최선 관찰) only.
- proxy_validation(프록시 검증): PF=1.037473, DD=4.485937, trades(거래)=549, density(밀도)=2.656489/day
- proxy_oos(프록시 표본외): PF=1.067510, DD=2.877573, trades(거래)=348, density(밀도)=3.0/day
- order_path_keep_rate(주문 경로 유지율): 0.346743

## MT5 Runtime Probe(MT5 런타임 탐침)

- validation_is(검증 내부): PF=0.78, DD=86.37%, trades(거래)=123, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos(표본외): PF=0.86, DD=50.15%, trades(거래)=86, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Judgment(판정)

F51 is negative_memory(부정 기억). Outcome-memory recurrence(결과 기억 재발) plus order-path proxy(주문 경로 프록시)는 Python proxy(파이썬 프록시)에서 약한 PF/DD 개선을 보였지만, MT5 single-position/order execution(단일 포지션/주문 실행)에서 PF가 1 미만으로 꺾이고 DD가 크게 폭증했다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않는다.
