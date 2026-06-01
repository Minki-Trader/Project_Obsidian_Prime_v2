# Stage354 Proxy Trade Shape Scout(354단계 프록시 거래 형태 탐색)

- canonical_stage_id(정식 단계 ID): `354_proxy_trade_shape_scout__small_candidate_queue`
- subtitle(부제): `small_candidate_queue`
- current_run_id(현재 실행 ID): `run354B_lightweight_proxy_trade_shape_scan_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run354A_branch_stage353_to_lightweight_proxy_trade_shape_scout_without_db_v1`
- source_stage(원천 단계): `353_trade_shape_offense__report_recovered_density_ok_edge_rebuild`

## Question(질문)

Stage352B(352B 실행)의 MT5 runtime probe(MT5 런타임 탐침)는 density(밀도)는 통과했지만 OOS loss(표본외 손실)와 high drawdown(높은 낙폭)이 남았다. Stage353(353단계)이 너무 무거우므로, expected tape(예상 테이프)와 runtime features(런타임 피처)만 사용해 작은 proxy candidate queue(프록시 후보 대기열)를 먼저 만들 수 있는가?

## Source Truth(원천 진실)

- combined net profit(합산 순수익): `41.48`
- profit factor(수익 팩터): `1.0079426019`
- expectancy(기대값): `0.0315917746`
- max drawdown percent(최대 낙폭률): `65.34`
- recovery factor(회복 계수): `0.1107935575`
- trade count(거래수): `1313`
- trade density(거래 밀도): `4.1815286624`
- OOS net profit(표본외 순수익): `-200.11`
- long/short count(롱/숏 수): `700/613`

## Scope(범위)

Stage354(354단계)는 proxy scout(프록시 탐색)만 한다. MT5 runtime probe(MT5 런타임 탐침), ONNX export(온엑스 내보내기), EA handoff(EA 인계)는 positive queue(긍정 대기열)가 생긴 뒤 별도 Stage(단계)나 run(실행)으로 넘긴다.

## Boundary(경계)

Proxy expected value(프록시 예상값)는 signal sanity check(신호 점검)와 후보 선별 보조로만 쓴다. MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(Goal Achieve, 목표 달성)은 주장하지 않는다.

## Density Constraint(밀도 제약)

`trade_per_day_min_3_to_10_plus_no_trade_splitting`

Action(행동): trade per day(일별 거래수) 3~10+ 조건을 유지하되, trade splitting(거래 쪼개기)로 수익을 부풀리는 방식은 금지한다.

Effect(효과): Stage354B(354B 실행)의 proxy candidate(프록시 후보)는 신호가 많아도 MT5 trade count(MT5 거래수)와 비교되기 전까지 운영 후보로 보지 않는다.

## Next Action(다음 행동)

`run354B_lightweight_proxy_trade_shape_scan_without_db_v1`에서 ADX25(ADX25 국면), cash-open clue(현금장 단서), threshold surface(임계값 표면)를 좁게 재현한다.

Effect(효과): Stage354B(354B 실행)는 후보를 많이 만들기보다 MT5 probe package(MT5 탐침 패키지)로 넘길 작은 queue(대기열)를 만든다.
