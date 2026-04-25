# Decision: Stage 04 MT5 Price-Proxy Weights

- date(날짜): `2026-04-25`
- stage(단계): `04_model_input_readiness__weights_parity_feature_audit`
- status(상태): `accepted`

## 결정(Decision, 결정)

Stage 04(4단계)는 외부 실제 가중치(external actual weights, 외부 실제 가중치)를 기다리지 않고 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)로 58 feature(58개 피처) model input(모델 입력)을 재물질화한다.

대상 basket(바스켓)은 `MSFT`, `NVDA`, `AAPL`이다.

각 월 `YYYY-MM`의 가중치는 그 월 시작 전 마지막 공통 MT5 closed bar(닫힌 봉)의 close(종가)로 계산한다.

공식(formula, 공식):

`symbol_close / (MSFT_close + NVDA_close + AAPL_close)`

첫 월 `2022-08`은 prior bar(이전 봉)가 없어서 첫 공통 closed bar(닫힌 봉)를 bootstrap(초기값)으로 쓴다.

## 이유(Rationale, 이유)

외부 구독 데이터(external subscription data, 외부 구독 데이터)에 막히면 Stage 04(4단계)가 계속 멈춘다.

MT5 price-proxy weights(MT5 가격 대리 가중치)는 로컬 raw bars(원천 봉 데이터)만으로 재현된다.

효과(effect, 효과): placeholder_equal_weight(임시 동일가중)를 제거하면서도 첫 58 feature(58개 피처) model input(모델 입력)을 검토 가능한 산출물(artifact, 산출물)로 만들 수 있다.

## 산출물(Artifacts, 산출물)

- contract(계약): `docs/contracts/top3_price_proxy_weight_contract_fpmarkets_v2.md`
- weight table(가중치 표): `foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv`
- weight run(가중치 실행): `20260425_top3_price_proxy_weights_v1`
- model input run(모델 입력 실행): `20260425_model_input_feature_set_v2_mt5_price_proxy_58`
- feature_set_id(피처 세트 ID): `feature_set_v2_mt5_price_proxy_top3_weights_58_features`

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 actual index weight(실제 지수 가중치)를 만들었다는 뜻이 아니다.

이 가중치는 NDX 실제 구성비(actual NDX index weights, 실제 NDX 지수 가중치), QQQ 보유비중(QQQ holdings weights, QQQ 보유비중), 시가총액(market cap, 시가총액), 유동주식수(float, 유동주식수)를 반영하지 않는다.

따라서 Stage 05(5단계) handoff(인계)는 “가중치는 MT5 price proxy(가격 대리)”라는 audit input(감사 입력)을 포함해야 한다.

## 영향(Impact, 영향)

56 feature(56개 피처) model input(모델 입력)은 interim quarantine artifact(임시 격리 산출물)로 보존한다.

58 feature(58개 피처) model input(모델 입력)은 Stage 05(5단계)의 감사 입력(audit input, 감사 입력)이 된다.

운영 승격(operating promotion, 운영 승격), runtime authority(런타임 권위), model quality(모델 품질)는 아직 주장하지 않는다.
