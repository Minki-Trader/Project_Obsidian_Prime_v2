# Broker Session Calendar Mapper Review(브로커 세션 달력 매퍼 검토)

## 판정(Judgment, 판정)

`20260424_broker_session_calendar_mapper` 실행(run, 실행)은 `positive(긍정)`로 본다.

쉽게 말하면, 원천 브로커 시계 키(raw broker-clock key, 원천 브로커 시계 키)를 이벤트 UTC(event UTC, 이벤트 UTC)와 뉴욕 세션 시간(New York session time, 뉴욕 세션 시간)으로 바꾸는 매퍼(mapper, 매퍼)를 만들었고 실제 원천 파일로 검토했다.

## 확인한 것(What Was Checked, 확인한 것)

- 브로커 시계 시간대(broker clock timezone, 브로커 시계 시간대): `Europe/Athens`
- 세션 시간대(session timezone, 세션 시간대): `America/New_York`
- 확인 심볼(symbols checked, 확인 심볼): `US100`, `AAPL`, `MSFT`, `AMZN`, `AMD`, `GOOGL.xnas`, `META`, `NVDA`, `TSLA`
- 세션 피처(session features, 세션 피처)가 직접 UTC 가정(direct UTC assumption, 직접 UTC 가정)을 쓰지 않는지 확인했다.

## 결과(Result, 결과)

- 전체 정규장 일수(cash session days, 정규장 일수): `8370`
- 완전 정규장 일수(full cash session days, 완전 정규장 일수): `7149`
- 부분 정규장 일수(partial cash session days, 부분 정규장 일수): `1221`
- 완전 정규장 비율(full cash session ratio, 완전 정규장 비율): `0.854122`

## 효과(Effect, 효과)

세션 피처(session features, 세션 피처)는 이제 `foundation/features/session_calendar.py`의 매퍼(mapper, 매퍼)를 통해 계산한다.

부분 세션(partial sessions, 부분 세션)은 숨기지 않는다. 효과(effect, 효과)는 다음 피처 프레임(feature frame, 피처 프레임)에서 행 유효성(row validity, 행 유효성)을 정직하게 나눌 수 있다는 것이다.

## 경계(Boundary, 경계)

이 검토(review, 검토)는 세션 시간 매퍼(session time mapper, 세션 시간 매퍼)를 닫는다.

모델 준비(model readiness, 모델 준비), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.
