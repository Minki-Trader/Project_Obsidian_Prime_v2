# Stage 01 Data Foundation: Raw M5 Inventory

## 질문(Question, 질문)

우리가 실제로 가진 브로커 원천 `M5` 데이터(broker-native M5 data, 브로커 원천 M5 데이터)는 무엇이고, 첫 깨끗한 모델링 창(modeling window, 모델링 창)을 어디까지 지탱할 수 있는가?

## 범위(Scope, 범위)

- 심볼(symbol, 심볼)별 원천 봉(raw bars, 원천 봉)을 조사한다.
- 날짜 범위(date coverage, 날짜 범위)를 확인한다.
- 빠진 원천(missing source, 누락 원천)이나 의심스러운 원천(suspicious source, 의심 원천)을 표시한다.
- 다음 피처 프레임 단계(feature-frame stage, 피처 프레임 단계)를 준비한다.

## 범위 밖(Not In Scope, 범위 밖)

- 모델 학습(model training, 모델 학습)
- 알파 선택(alpha selection, 알파 선택)
- 운영 승격(operating promotion, 운영 승격)
- 런타임 권위(runtime authority, 런타임 권위)

## 종료 조건(Exit Condition, 종료 조건)

쓸 수 있는 원천 재고(usable raw source inventory, 사용 가능 원천 재고)가 작성되고, 다음 데이터 또는 피처 프레임 질문(next data or feature-frame question, 다음 데이터/피처 질문)이 분명해지면 닫을 수 있다.
