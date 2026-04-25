# Stage 04 Model Input Readiness: Weights Parity Feature Audit

## 질문(Question, 질문)

첫 training dataset(학습 데이터셋)을 첫 model training(모델 학습)에 넣기 전에, 입력 feature set(피처 세트)을 의심 없이 고정할 수 있는가?

쉽게 말하면, 정답지와 시험 구간은 생겼으니 이제 시험 문제에 임시 재료가 섞였는지 확인하는 단계다.

## 범위(Scope, 범위)

- `placeholder_equal_weight(임시 동일가중)` top3 weight features(top3 가중치 피처)를 임시로 격리한 56 feature(56개 피처) artifact(산출물)를 보조 근거로 남긴다.
- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 계약과 산출물을 만든다.
- 58 feature set(58개 피처 세트)을 정식 pre-alpha(알파 전) model input(모델 입력)으로 다시 물질화한다.
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)와 58 feature(58개 피처) 정식 경로의 관계를 문서화한다.
- Stage 05(5단계) feature integrity audit(피처 무결성 감사)에 넘길 입력 목록을 고정한다.

## 범위 밖(Not In Scope, 범위 밖)

- full Python/MT5 runtime parity closure(완전 파이썬/MT5 런타임 동등성 폐쇄)
- alpha selection(알파 선택)
- model quality claim(모델 품질 주장)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- live execution(실거래 실행)

## 첫 선택(First Decision, 첫 선택)

첫 선택은 `placeholder_equal_weight(임시 동일가중)`에 의존하는 두 feature(피처)를 56 feature(56개 피처) model input(모델 입력)에서 격리한 것이다.

- `top3_weighted_return_1`
- `us100_minus_top3_weighted_return_1`

효과(effect, 효과)는 MT5 price-proxy monthly weights(MT5 가격 대리 월별 가중치)가 생기기 전까지 임시값이 조용히 모델 입력에 섞이지 않는 것이다.

단, 이것은 최종 pre-alpha(알파 전) 경로가 아니다. 정식 경로는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 만든 뒤 58 feature(58개 피처)를 다시 고정하는 것이다.

## 종료 조건(Exit Condition, 종료 조건)

이 단계(stage, 단계)는 다음이 모두 명시되면 닫을 수 있다.

- first model input dataset(첫 모델 입력 데이터셋) 또는 명시적 quarantine manifest(격리 목록)
- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 계약과 산출물
- 58 feature(58개 피처) model input dataset(모델 입력 데이터셋)과 feature order hash(피처 순서 해시)
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)의 보조 근거 상태
- Stage 05(5단계)로 넘길 feature formula/time/external/label audit(피처 공식/시간/외부/라벨 감사) 입력 목록

이 조건은 alpha exploration(알파 탐색)을 허가하는 게이트(gate, 제한문)가 아니라, 모델 기반 근거를 의심 없이 읽기 위한 준비도(readiness, 준비도) 기준이다.
