# Time Semantics Probe Review(시간 의미 탐침 검토)

## 판정(Judgment, 판정)

`20260424_time_semantics_probe` 실행(run, 실행)은 두 가지 판정을 남긴다.

- `negative(부정)`: 원천 timestamp(타임스탬프)를 직접 UTC(direct UTC, 직접 협정세계시)로 보고 미국 정규장 피처(US cash-session features, 미국 정규장 피처)를 계산하는 가정
- `positive(긍정)`: 원천 timestamp(타임스탬프)가 브로커/서버 시계 후보(broker/server clock candidate, 브로커/서버 시계 후보)처럼 동작한다는 해석

쉽게 말하면, 지금 시간값을 그대로 UTC(협정세계시)라고 믿고 세션 피처(session features, 세션 피처)를 만들면 틀릴 가능성이 크다.

## 확인한 것(What Was Checked, 확인한 것)

`AAPL`, `MSFT`, `AMZN`, `AMD`, `GOOGL.xnas`, `META`, `NVDA`, `TSLA`의 원천 `M5` 첫 봉(first open, 첫 봉)을 뉴욕 정규장 시작 시각(New York cash open, 뉴욕 정규장 시작)과 비교했다.

## 결과(Result, 결과)

- 관측 심볼-일수(observed symbol-days, 관측 심볼-일수): `7417`
- 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율): `0.0`
- 브로커 시계 유사율(broker wall-clock-like ratio, 브로커 시계 유사율): `0.929082`
- 주요 오프셋(main offsets, 주요 시간 차이): `+3h`, `+2h`

## 효과(Effect, 효과)

첫 피처 프레임(feature frame, 피처 프레임)을 만들기 전에 timestamp policy(타임스탬프 정책)를 정해야 한다.

선택지는 두 개다.

- 원천 timestamp(타임스탬프)를 브로커 시계 정렬 키(broker-clock alignment key, 브로커 시계 정렬 키)로 유지한다.
- 원천 timestamp(타임스탬프)를 명시적 UTC 이벤트 시간(explicit UTC event time, 명시적 UTC 이벤트 시간)으로 변환한다.

## 경계(Boundary, 경계)

이 검토(review, 검토)는 시간 의미 후보(time semantics candidate, 시간 의미 후보)를 세운다. 아직 피처 프레임 폐쇄(feature-frame closure, 피처 프레임 폐쇄), 모델 준비(model readiness, 모델 준비), 런타임 권위(runtime authority, 런타임 권위)를 주장하지 않는다.
