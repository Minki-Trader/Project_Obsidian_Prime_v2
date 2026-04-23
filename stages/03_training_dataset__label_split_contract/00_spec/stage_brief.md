# Stage 03 Training Dataset: Label Split Contract

## 질문(Question, 질문)

첫 shared feature frame freeze(공유 피처 프레임 동결 산출물) 위에서 첫 training label(학습 라벨)과 split contract(분할 계약)를 재현 가능하게 정할 수 있는가?

## 범위(Scope, 범위)

- label definition(라벨 정의)을 정한다.
- train, validation, OOS(`out-of-sample`, 표본외) split boundary(분할 경계)를 정한다.
- 첫 training dataset(학습 데이터셋) 물질화 경로(materialization path, 물질화 경로)를 정한다.

## 범위 밖(Not In Scope, 범위 밖)

- 알파 선택(alpha selection, 알파 선택)
- 운영 승격(operating promotion, 운영 승격)
- 런타임 권위(runtime authority, 런타임 권위)
- 실거래 실행(live execution, 실거래 실행)

## 종료 조건(Exit Condition, 종료 조건)

첫 training dataset contract(학습 데이터셋 계약)가 label(라벨), split(분할), 산출물 경로(artifact path, 산출물 경로)까지 명시되면 닫을 수 있다.
