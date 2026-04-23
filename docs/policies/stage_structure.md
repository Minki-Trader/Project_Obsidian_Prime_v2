# Stage Structure

단계(stage, 단계)는 프로젝트 관리 단위(project-management unit, 프로젝트 관리 단위)다.

## 이름 규칙(Naming, 이름 규칙)

다음 형태를 쓴다.

`NN_area__specific_question`

예시(example, 예시)는 정책(policy, 정책)이 아니다. 실제 단계 이름(stage name, 단계 이름)은 현재 질문(current question, 현재 질문)을 설명해야 한다.

## 필수 폴더(Required Stage Folders, 필수 단계 폴더)

- `00_spec/`: 단계 목적(stage purpose, 단계 목적)과 범위(scope, 범위)
- `01_inputs/`: 입력 참조(input refs, 입력 참조)와 가정(assumptions, 가정)
- `02_runs/`: 실행 산출물(run outputs, 실행 산출물)
- `03_reviews/`: 검토(review, 검토)와 요약(summary, 요약)
- `04_selected/`: 선택 상태(selection status, 선택 상태)

## 규칙(Rule, 규칙)

단계(stage, 단계)는 질문(question, 질문)이 답해졌거나 명시적으로 포기(abandon, 포기)되었을 때 닫는다.

단계 이름(stage name, 단계 이름)이 너무 넓어서 미래의 모든 알파(alpha, 알파)가 갇힌 것처럼 느껴지면 안 된다.

학습(training, 학습)과 검증(validation, 검증)이 준비되는 순간 알파 연구(alpha research, 알파 연구)는 시작될 수 있다.
