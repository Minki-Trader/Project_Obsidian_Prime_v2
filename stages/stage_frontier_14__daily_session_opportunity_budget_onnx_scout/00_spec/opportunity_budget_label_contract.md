# Frontier14 Opportunity Budget Label Contract(프론티어14 기회 예산 라벨 계약)

Action(행동): daily/session bucket(일별/세션별 버킷) 안에서 future path utility(미래 경로 효용)를 사전 등록 quota(할당량)로 rank(순위화)합니다.

Effect(효과): label target density(라벨 표적 빈도)를 5~10/day(일 5~10회)에 가깝게 만들되, model argmax density(모델 최대확률 빈도)는 별도로 측정합니다.

## Pre-Registered Variants(사전 등록 변형)

- `f14b_day_q6_h8`: bucket(버킷) `broker_day(브로커 일자)`, quota(할당량) `6`, hold bars(보유 봉) `8`, tie-break(동점 규칙) `earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)`
- `f14b_cash_q8_h8`: bucket(버킷) `broker_day_x_cash_session(브로커 일자와 현금장 세션)`, quota(할당량) `8`, hold bars(보유 봉) `8`, tie-break(동점 규칙) `earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)`
- `f14b_cash_q10_h12`: bucket(버킷) `broker_day_x_cash_session(브로커 일자와 현금장 세션)`, quota(할당량) `10`, hold bars(보유 봉) `12`, tie-break(동점 규칙) `earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)`

## Guards(보호 장치)

- quota/horizon retuning after metrics(지표 확인 뒤 할당량/지평 재조정) 금지
- validation/OOS statistics calibration(검증/표본밖 통계 보정) 금지
- post-fit selector or threshold search(적합 후 선택기 또는 임계값 탐색) 금지
