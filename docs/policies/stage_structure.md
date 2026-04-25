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

## 알파 탐색 이름 규칙(Alpha Exploration Naming, 알파 탐색 이름 규칙)

Stage 10(10단계)부터 alpha exploration(알파 탐색)이 닫히는 단계(stage, 단계)까지는 정식 단계 이름(canonical stage id, 정식 단계 ID)과 탐색 라벨(exploration label, 탐색 라벨)을 함께 쓴다.

- 정식 단계 이름(canonical stage id, 정식 단계 ID)은 기존 형식 `NN_area__specific_question`을 유지한다.
- 탐색 라벨(exploration label, 탐색 라벨)은 `stageN_exploration_group__specific_detail` 형식을 쓴다.
- 예시(example, 예시): 정식 단계 이름(canonical stage id, 정식 단계 ID)이 `10_alpha_scout__default_split_model_threshold_scan`이면 탐색 라벨(exploration label, 탐색 라벨)은 `stage10_Model__LGBM`처럼 짧게 쓸 수 있다.

효과(effect, 효과)는 프로젝트의 단계 질문(stage question, 단계 질문)을 유지하면서도, 알파 탐색(alpha exploration, 알파 탐색)의 축(axis, 축)과 세부 후보(candidate, 후보)를 빠르게 읽게 하는 것이다.

## 알파 탐색 실행 번호 규칙(Alpha Run Numbering, 알파 실행 번호 규칙)

알파 탐색 단계(alpha exploration stage, 알파 탐색 단계)의 실행(run, 실행)은 단계 로컬 번호(stage-local ordinal, 단계 로컬 번호)를 쓴다.

- 실행 번호(run number, 실행 번호)는 탐색 상한(limit, 한계)이 아니다.
- `run01A`, `run01B`, `run01C`처럼 같은 단계(stage, 단계)의 같은 핵심 주제(core topic, 핵심 주제)를 계속 밀어붙이는 순서 번호(sequence number, 순서 번호)로 쓴다.
- 주변 흔들기(neighborhood shake, 주변 흔들기), 극단값 탐색(extreme sweep, 극단값 탐색), 경계값 확인(boundary check, 경계값 확인), 복구 실행(recovery run, 복구 실행), MT5(`MetaTrader 5`, 메타트레이더5) 재검증(reverification, 재검증)은 모두 같은 단계(stage, 단계) 안에서 이어갈 수 있다.
- `run02A`는 새 단계(new stage, 새 단계)나 새 핵심 주제(new core topic, 새 핵심 주제)를 뜻하지 않는다. 같은 단계(stage, 단계) 안에서 탐색 묶음(exploration packet, 탐색 묶음)을 새로 나눌 필요가 있을 때만 쓴다.

각 단계(stage, 단계)는 하나의 핵심 주제(core topic, 핵심 주제)를 끝까지 탐색한다. 미리 정한 실행 개수(run count, 실행 개수)나 탐색 폭(search width, 탐색 폭)으로 닫지 않는다. 다음 단계(next stage, 다음 단계)는 현재 단계의 핵심 주제(core topic, 핵심 주제)가 충분히 밀렸고, 남은 갈래(branches, 갈래)가 positive handoff(긍정 인계), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건) 중 하나로 정리됐을 때만 연다.

효과(effect, 효과)는 label(라벨), feature(피처), model(모델), decision surface(의사결정 표면), entry(진입), exit(청산), sizing/overlay(사이징/오버레이), retrain/carry(재학습/유지)가 한 단계(stage, 단계) 안에서 충분히 압박 시험(stress test, 압박 시험)되게 하는 것이다.

## 공회전 방지(No-Spin Rule, 공회전 방지)

단계 질문(stage question, 단계 질문)을 답하려면 외부 검증(external verification, 외부 검증)이 필요한데 그 검증을 하지 않았다면, 단계(stage, 단계)를 닫지 않는다.

다음 중 하나를 같은 작업 회차(pass, 회차)에 해야 한다.

- 외부 검증(external verification, 외부 검증)을 실행한다.
- 주장 범위(claim scope, 주장 범위)를 외부 검증이 필요 없는 수준으로 낮춘다.
- 실행할 수 없는 이유(blocker, 차단 사유)와 다시 시도할 조건(retry condition, 재시도 조건)을 적고 차단(blocked, 차단)으로 남긴다.

같은 빠진 검증(missing verification, 빠진 검증)을 반복해서 다음 작업(next work, 다음 작업)으로만 넘기는 것은 단계 진행(stage progress, 단계 진행)이 아니다.
