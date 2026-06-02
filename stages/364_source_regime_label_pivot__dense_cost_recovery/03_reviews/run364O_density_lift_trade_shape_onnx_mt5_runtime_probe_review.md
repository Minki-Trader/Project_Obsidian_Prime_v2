# Stage364O density lift trade shape ONNX MT5 runtime probe review(364O단계 밀도 상승 거래 형태 온엑스 MT5 런타임 탐침 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`
- judgment(판정): `positive_runtime_probe_profit_and_parity_clue_promotion_ineligible_drawdown_long_only_review_required_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## KPI read(KPI 판독)

- MT5 net profit(MT5 순수익): `818.67`
- profit factor(수익 팩터): `1.26`
- trade count(거래수): `1047`
- expectancy(기대값): `0.78`
- recovery factor(회복 계수): `3.85`
- max drawdown(최대 낙폭): `38.21%`
- long/short(롱/숏): `1047/0`
- trade/day(일 거래수, business day(영업일) 기준): `3.144144`

## Positive clue(긍정 단서)

- MT5 runtime probe(MT5 런타임 탐침)가 net profit(순수익) 818.67, profit factor(수익 팩터) 1.26, trade count(거래수) 1047를 냈다. 효과(effect, 효과): 새 수익원 탐색을 이어갈 실거래형 단서로 보되 운영 승격(operating promotion, 운영 승격)은 금지한다.
- probability parity(확률 동등성)는 17428/17428 matched(일치), mismatch(불일치) 0이다. 효과(effect, 효과): Python research(파이썬 연구)와 MT5 runtime(MT5 런타임) 사이 모델 handoff(인계) 문제 가능성을 낮춘다.
- business day(영업일) 기준 trade/day(일 거래수)는 3.144이고 trade splitting(거래 쪼개기) 근거는 없다. 효과(effect, 효과): 고밀도 후보라는 탐색 방향은 유지한다.

## Promotion blockers(승격 차단)

- equity drawdown(평가자본 낙폭)은 38.21%, closed balance drawdown(청산 잔액 낙폭)은 34.17%다. 효과(effect, 효과): positive net(양수 순수익)이어도 live readiness(실거래 준비)나 runtime authority(런타임 권위)를 주장하지 않는다.
- long trade(롱 거래) 1047, short trade(숏 거래) 0으로 side balance(방향 균형)가 깨졌다. 효과(effect, 효과): 다음 작업에서 short head(숏 헤드) 또는 side router(방향 라우터)를 공격 탐색한다.
- calendar hold(달력 기준 보유)는 median(중앙값) 8.0 M5, max(최대) 1670 M5이고 MT5 report(MT5 보고서)의 max holding time(최대 보유시간)은 91:10:00다. 효과(effect, 효과): max hold(최대 보유) 의미를 calendar bar(달력 봉)와 broker holding time(브로커 보유시간)으로 분리 검증한다.
- swap(스왑) 합계는 -48.84이고 net profit(순수익)에 직접 반영됐다. 효과(effect, 효과): 긴 보유 꼬리(long hold tail, 긴 보유 꼬리)가 비용 압박(cost stress, 비용 압박)으로 이어지는지 다음 입력에 넣는다.

## Proxy vs MT5(프록시 대 MT5)

- proxy(프록시)는 expected native combined(예상 네이티브 합산) net profit(순수익) `574.693`, trade count(거래수) `1047`, profit factor(수익 팩터) `1.1727732809`였다.
- MT5(MT5)는 net profit(순수익) `818.67`, trade count(거래수) `1047`, profit factor(수익 팩터) `1.26`였다.
- diff(차이): net profit(순수익) `+243.977`, trade count(거래수) `0`.
- effect(효과): proxy(프록시)는 선별 보조이고 MT5 Strategy Tester(MT5 전략 테스터)가 KPI authority(KPI 권위)다.

## Next action(다음 행동)

`run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`에서 calendar hold cap(달력 보유 상한), drawdown tail exit(낙폭 꼬리 청산), short side balance(숏 방향 균형), session/regime stability(세션/국면 안정성) 입력을 materialize(구체화)한다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
