# Run335R Repaired Attribution And Proxy Scout(335R 수리 귀속 및 프록시 탐침)

- run_id(실행 ID): `run335R_materialize_repaired_attribution_and_branch_specific_proxy_scout_v1`
- status(상태): `completed_repaired_attribution_and_proxy_scout_materialized_no_forward_decision`
- decision(결정): `stage335R_materialized_same_bar_attribution_repair_and_proxy_scout_no_selection`
- repair(수리): same-bar attribution-only(동일 봉 귀속 전용) `9`행을 적용했고 remaining missing join(남은 조인 누락)은 `0`행이다.
- proxy(프록시): branch/attempt/trade grain(분기/시도/거래 단위) scout matrix(탐침 행렬) `14817`행과 proxy-vs-MT5 comparison(프록시 대 MT5 비교) `792`행을 만들었다.
- usability(활용성): old proxy expected value(기존 프록시 예상값)는 repeated aggregate(반복 집계)라 selection(선택)과 Forward decision(전진 판정)에 계속 `blocked`다. 새 scout(탐침)는 diagnostic-only(진단 전용)로 `run335S` 검토 전까지 선택 근거가 아니다.
- constraints(제약): predeclared constraints(사전 선언 제약) `6`행과 balanced package carry(균형 패키지 이월) `3`행을 다음 검토로 넘겼다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): `run335K`, `run335N`, `run335P`, `run335Q` 산출물.
- time_axis(시간축): MT5(`MetaTrader 5`, 메타트레이더5) server time(서버 시각) M5 bar(5분봉) 기준이며, 거래 open time(진입 시각)은 보존한다.
- feature_label_boundary(피처/라벨 경계): 새 label(라벨), training(학습), threshold retune(임계값 재조정)는 없다.
- leakage_risk(누수 위험): future shift(미래 이동) 또는 nearest shift(가까운 값 이동)를 쓰면 누수다. 이번 수리는 `:01` to same-bar `:00` only(동일 봉만)라 별도 guard(가드)로 막았다.

## Proxy Judgment(프록시 판정)

- old proxy(기존 프록시): MT5 runtime probe(런타임 탐침)와 차이는 기록하지만 rank/selection(순위/선택)에는 못 쓴다.
- branch scout(분기 탐침): branch rows(분기 행)는 물질화됐지만 많은 값은 attempt-level runtime value(시도 단위 런타임 값)를 공유한다. 그래서 diagnostic(진단)까지만 가능하다.
- next_action(다음 행동): `run335S_review_repaired_attribution_proxy_scout_and_open_constraint_bound_research_packet_v1`에서 수리/프록시/제약 묶음을 독립 검토한다.
