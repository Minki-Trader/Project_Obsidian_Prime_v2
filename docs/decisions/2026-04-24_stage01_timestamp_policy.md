# Decision Memo

## 결정(Decision, 결정)

Stage 01(1단계)은 FPMarkets 원천 timestamp(타임스탬프)에 대해 이중 시간축 정책(dual time axis policy, 이중 시간축 정책)을 채택한다.

원천 `time_close_unix`는 우선 브로커 시계 정렬 키(broker-clock alignment key, 브로커 시계 정렬 키)로 사용한다. 미국 세션 피처(US session features, 미국 세션 피처)는 별도 `timestamp_event_utc(이벤트 UTC 타임스탬프)` 또는 검증된 브로커 세션 달력(broker session calendar, 브로커 세션 달력)이 생기기 전에는 닫힌 것으로 보지 않는다.

## 이유(Why, 이유)

`20260424_time_semantics_probe`가 원천 timestamp(타임스탬프)를 직접 UTC(direct UTC, 직접 협정세계시)로 보는 가정을 부정했다.

- 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율): `0.0`
- 브로커 시계 유사율(broker wall-clock-like ratio, 브로커 시계 유사율): `0.929082`

## 효과(Effect, 효과)

- 외부 심볼 정렬(external symbol alignment, 외부 심볼 정렬)은 원천 브로커 시계 키(raw broker-clock key, 원천 브로커 시계 키)를 계속 쓴다.
- 세션 피처(session features, 세션 피처)는 직접 UTC 변환(direct UTC conversion, 직접 UTC 변환)에 기대지 않는다.
- 다음 작업은 브로커 세션 달력 매퍼(broker session calendar mapper, 브로커 세션 달력 매퍼)를 만드는 것이다.

## 경계(Boundary, 경계)

이 결정은 데이터 시간축(data time axis, 데이터 시간축) 결정이다.

모델 준비(model readiness, 모델 준비), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)을 주장하지 않는다.
