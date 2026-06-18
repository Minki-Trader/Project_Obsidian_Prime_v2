# F83F Short Density Proxy/Runtime Gap Analysis(F83F 숏 밀도 프록시/런타임 간극 분석)

Updated(갱신): 2026-06-18T08:40:25Z

- run id(실행 ID): `frontier83F_short_density_proxy_runtime_gap_analysis_v1`
- parent run(부모 실행): `frontier83E_short_side_density_runtime_materialization_v1`
- status(상태): `f83f_gap_attributed_runtime_winrate_erosion_after_signal_parity_no_authority`
- judgment(판정): `short_density_proxy_positive_runtime_negative_due_winrate_dd_erosion_requires_repair_or_rotation_no_authority`
- target(대상): `f82b_10355` / `extra_trees_d7_l120`
- claim boundary(주장 경계): `gap_attribution_negative_memory_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Observed Change(관찰 변화)

F83D proxy(F83D 프록시)는 short density target(숏 밀도 대상)을 양수로 골랐지만, F83E MT5 runtime(F83E MT5 런타임)은 validation/OOS(검증/외표본) 모두 손실로 뒤집혔다.

- validation(검증): proxy net/PF/DD/trades-day(프록시 순손익/수익 팩터/손실폭/일 거래) `264.3228505696317/1.2026641999408263/11.388546118365435/8.317343173431734` -> runtime(런타임) `-285.66/0.83/58.86/8.213235294117647`
- OOS(외표본): proxy net/PF/DD/trades-day(프록시 순손익/수익 팩터/손실폭/일 거래) `401.02621043351246/1.4727443088117345/4.6767732618809985/8.350515463917526` -> runtime(런타임) `-37.17/0.97/19.24/8.266666666666667`

## Attribution(귀속)

Primary attribution(주 귀속): `runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)`.

- validation win-rate delta(검증 승률 변화): `-11.663637976929902` percentage points(퍼센트포인트), DD delta(손실폭 변화) `47.47145388163457`
- OOS win-rate delta(외표본 승률 변화): `-11.93691358024691` percentage points(퍼센트포인트), DD delta(손실폭 변화) `14.563226738118999`
- fill gap share(체결 간극 설명 비중): validation `0.004264436438169483`, OOS `0.004519382643361078`

Effect(효과): order fill gap(주문 체결 간극)은 너무 작아서 손익 반전을 설명하기 어렵고, 같은 신호가 런타임에서 win rate/DD(승률/손실폭)를 잃는 것이 핵심 간극이다.

## Closeout KPI(마감 핵심 지표)

- validation(검증): gross profit/loss(총이익/총손실) `1394.4/-1680.06`, win rate(승률) `0.3004`, avg win/loss(평균 이익/손실) `2.078092399403875/-1.07489443378119`, payoff(손익비) `1.9332990609075014`, expectancy(기대값) `-0.13`, recovery(회복 계수) `-0.97`, long/short(롱/숏) `0.0/2234.0`
- OOS(외표본): gross profit/loss(총이익/총손실) `1114.06/-1151.23`, win rate(승률) `0.3331`, avg win/loss(평균 이익/손실) `2.0745996275605214/-1.0709116279069768`, payoff(손익비) `1.9372276605261853`, expectancy(기대값) `-0.02`, recovery(회복 계수) `-0.36`, long/short(롱/숏) `0.0/1612.0`

Unavailable runtime fields(미확보 런타임 항목): time under water(회복 전 체류 시간), max consecutive loss(최대 연속 손실)은 현재 normalized runtime receipt(정규화 런타임 영수증)에 없다.

## Next(다음)

Next probe(다음 탐침): `frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1`.

Repair boundary(수리 경계): same threshold/filter/parameter-only repair(동일 임계값/필터/파라미터만 수리)는 금지한다. 새 runtime-realized outcome label(런타임 실현 결과 라벨), stop-touch/fill-path target(스톱 터치/체결 경로 목표), risk logic(위험 로직), regime/session split(장세/세션 분할) 중 하나 이상이 필요하다.

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
