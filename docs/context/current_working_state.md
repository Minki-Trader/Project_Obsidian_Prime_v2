# Current Working State

- updated_on: `2026-04-24`
- project_mode: `clean_stage_restart`
- active_stage: `03_training_dataset__label_split_contract`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 깨끗한 단계 구조(clean stage structure, 깨끗한 단계 구조)로 다시 시작한 뒤, 이제 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)까지 실제로 만들었다.

이전 `Stage 00`부터 `Stage 07`까지의 흐름(flow, 흐름)은 현재 진실(current truth, 현재 진실)이 아니다. 저장소 바깥 압축 스냅샷(zip snapshot, 압축 스냅샷)으로 남겨 둔 과거 이력(prior history, 과거 이력)일 뿐이다.

보존한 것(preserved assets, 보존 자산):

- 에이전트 스킬(agent skills, 에이전트 스킬)
- 계약 문서(contract documents, 계약 문서)
- 개념 노트(concept notes, 개념 노트)
- 데이터 루트(data roots, 데이터 루트)
- 재사용 foundation 도구(reusable foundation tools, 재사용 기반 도구)

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 어떤 표본(sample, 표본)을 공부했는지 알려주는 라벨(label, 라벨)이다.

## 방금 닫힌 단계(Just Closed Stage, 방금 닫힌 단계)

`02_feature_frame__practical_full_cash_freeze`

Stage 02(2단계)는 Stage 01(1단계)에서 고른 목표를 실제 shared freeze(공유 동결 산출물)로 물질화했다.

- run_id(실행 ID): `20260424_practical_full_cash_freeze_materialization`
- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- row scope(행 범위): `valid_row_only`
- session scope(세션 범위): `cash_open_rows_only`
- day scope(일 범위): `full_cash_session_days_only`
- selected rows(선택 행 수): `54439`
- eligible full cash days(사용한 완전 정규장 일수): `890`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

효과(effect, 효과): 이제 학습 데이터셋(training dataset, 학습 데이터셋)을 이야기할 때, 추상 목표가 아니라 실제 동결 산출물(frozen artifact, 동결 산출물)을 기준으로 말할 수 있다.

## 현재 단계(Current Stage, 현재 단계)

`03_training_dataset__label_split_contract`

지금 질문(question, 질문)은 이거다.

첫 shared feature frame freeze(공유 피처 프레임 동결 산출물) 위에서 첫 training label(학습 라벨)과 split contract(분할 계약)를 재현 가능하게 정할 수 있는가?

필요한 일(work, 작업)은 다음이다.

- label definition(라벨 정의)을 정한다.
- train, validation, OOS(`out-of-sample`, 표본외) split boundary(분할 경계)를 정한다.
- 첫 training dataset(학습 데이터셋) 물질화 경로(materialization path, 물질화 경로)를 정한다.

## 현재 경계(Current Boundary, 현재 경계)

이 상태는 아직 model training(모델 학습) 완료도 아니고 runtime authority(런타임 권위)도 아니다.

지금은 training dataset contract(학습 데이터셋 계약)를 닫기 위한 단계다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 모델 연구(model study, 모델 연구) 전에 끝없는 사전검증(pre-validation, 사전검증)을 받아야 한다는 주장
