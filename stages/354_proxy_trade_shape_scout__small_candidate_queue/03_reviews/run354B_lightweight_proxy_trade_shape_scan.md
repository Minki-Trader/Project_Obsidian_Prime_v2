# run354B Lightweight Proxy Trade Shape Scan(354B 경량 프록시 거래 형태 스캔)

- run_id(실행 ID): `run354B_lightweight_proxy_trade_shape_scan_without_db_v1`
- status(상태): `completed_stage354B_proxy_scan_no_strict_queue_expand_required_no_selection`
- judgment(판정): `negative_proxy_scout_no_mt5_queue_no_operating_claim`
- decision(결정): `stage354B_open_run354C_expand_proxy_filter_sweep_without_db_v1`
- broad_rows(넓은 스캔 행): `3600`
- confirmed_rows(비중첩 확인 행): `80`
- mt5_queue_rows(MT5 대기열 행): `0`
- next_run_id(다음 실행 ID): `run354C_expand_proxy_filter_sweep_without_db_v1`

## Action(행동)

Stage351B(351B 실행)의 probability tape(확률 테이프), runtime features(런타임 피처), training dataset future return(학습 데이터 미래 수익)을 timestamp-safe(시점 안전)하게 결합했다. 그 뒤 broad overlap signal scan(넓은 중첩 신호 스캔)으로 후보를 줄이고, 상위 후보만 `HOLD_BARS=12` non-overlap trade shape(비중첩 거래 형태)로 재확인했다.

## Effect(효과)

거래를 쪼개서 수익을 만드는 방식(trade splitting, 거래 쪼개기)을 피한 결과, 양수 proxy(프록시) 후보들은 있었지만 trade/day(일별 거래수) 3+ 조건을 통과하지 못해 MT5 queue(MT5 대기열)를 만들지 않았다.

## Best Proxy Queue Read(최상 프록시 대기열 판독)

- candidate_id(후보 ID): `b03_1d_logreg_cashopen_c050__adx30_extreme__s0.360__l0.400__m0.010`
- model_variant_id(모델 변형 ID): `b03_1d_logreg_cashopen_c050`
- filter_name(필터 이름): `adx30_extreme`
- validation net(검증 순수익 로그): `0.06817546911776`
- validation PF(검증 수익 팩터): `1.1711883873561042`
- validation trade/day(검증 일별 거래수): `1.9487179487179487`
- oos net(표본외 순수익 로그): `0.05192882987183399`
- oos PF(표본외 수익 팩터): `1.1789993675798731`
- oos trade/day(표본외 일별 거래수): `2.010752688172043`
- long/short validation(검증 롱/숏): `97/131`
- long/short oos(표본외 롱/숏): `96/91`

## Boundary(경계)

이 결과는 proxy scout(프록시 탐색)다. MT5 KPI(MT5 핵심 성과 지표), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
