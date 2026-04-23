# Current Working State

- updated_on: `2026-04-24`
- project_mode: `clean_stage_restart`
- active_stage: `02_feature_frame__practical_full_cash_freeze`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 깨끗한 단계 구조(clean stage structure, 깨끗한 단계 구조)로 다시 시작했다.

이전 `Stage 00`부터 `Stage 07`까지의 흐름(flow, 흐름)은 더 이상 현재 진실(current truth, 현재 진실)이 아니다. 저장소 바깥 압축 스냅샷(zip snapshot, 압축 스냅샷)을 만든 뒤 작업 트리(working tree, 작업 트리)에서 제거했다.

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

`01_data_foundation__raw_m5_inventory`

Stage 01(1단계)은 원천 `M5` 재고(raw M5 inventory, 원천 M5 재고), 시간 의미(time semantics, 시간 의미), 세션 달력(session calendar, 세션 달력), 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)을 정리한 뒤 닫혔다.

`20260424_feature_frame_target_probe` 실행(run, 실행)이 고른 목표는 이거다.

- target_id(목표 ID): `practical_start_full_cash_day_valid_rows_only`
- practical modeling start(실용 모델링 시작): `2022-09-01T00:00:00Z`
- row scope(행 범위): `valid_row_only`
- day scope(일 범위): `full_cash_session_days_only`
- valid rows(유효행 수): `54439`
- full cash days(완전 정규장 일수): `890`
- valid-row NY days(유효행이 실제로 존재한 뉴욕 일수): `887`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- excluded partial-day valid rows(제외된 부분 정규장 유효행 수): `252`

효과(effect, 효과): practical start(실용 시작)는 유지하면서, 첫 freeze(첫 동결)는 부분 정규장 일자를 끌고 가지 않아도 된다.

## 현재 단계(Current Stage, 현재 단계)

`02_feature_frame__practical_full_cash_freeze`

지금 질문(question, 질문)은 이거다.

선택된 target(목표)을 실제 shared feature frame freeze(공유 피처 프레임 동결 산출물)로 물질화할 수 있는가?

필요한 일(work, 작업)은 다음이다.

- 선택된 범위(selected scope, 선택된 범위)로 피처 프레임(feature frame, 피처 프레임)을 만든다.
- dataset summary(데이터셋 요약), row validity(행 유효성), feature order hash(피처 순서 해시), source identity(원천 정체성)를 남긴다.
- shared artifact identity(공유 산출물 정체성)를 등록할 수 있게 만든다.

## 현재 경계(Current Boundary, 현재 경계)

이 상태는 아직 model training(모델 학습)도 아니고 runtime authority(런타임 권위)도 아니다.

지금은 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 정직하게 만들기 위한 단계다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 모델 연구(model study, 모델 연구) 전에 끝없는 사전검증(pre-validation, 사전검증)을 받아야 한다는 주장
