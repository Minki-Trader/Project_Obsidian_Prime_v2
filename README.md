# Project Obsidian Prime v2

FPMarkets `US100` `M5` 파이프라인(pipeline, 파이프라인)을 위한 깨끗한 연구 작업공간(research workspace, 연구 작업공간)이다.

이 저장소는 `2026-04-24`에 깨끗한 단계 재시작(clean stage restart, 깨끗한 단계 재시작)으로 정리했다. 이전 추적 상태(tracked state, 추적 상태)는 저장소 바깥 압축 스냅샷(zip snapshot, 압축 스냅샷)에 보존했다.

## 먼저 읽을 것(Read First, 먼저 읽기)

- 프로젝트 규칙(project rules, 프로젝트 규칙): `AGENTS.md`
- 현재 상태(current state, 현재 상태): `docs/workspace/workspace_state.yaml`
- 현재 설명(current narrative, 현재 설명): `docs/context/current_working_state.md`
- 재진입 순서(re-entry order, 재진입 순서): `docs/policies/reentry_order.md`

## 작업 원칙(Working Rule, 작업 원칙)

탐색(exploration, 탐색)은 열려 있다. `Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 탐색 가능한 표본 라벨(sample label, 표본 라벨)이다. 허가 게이트(permission gate, 허가 게이트)가 아니다.

운영 주장(operational claim, 운영 주장)은 별도 문제다. 실거래(live use, 실거래), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)은 더 강한 증거가 필요하다.

## 폴더 지도(Folder Map, 폴더 지도)

- `docs/`: 계약, 정책, 상태, 결정, 등록부, 템플릿
- `data/`: 원천 데이터와 처리 데이터
- `foundation/`: 재사용 수집기, 피처 작업, 파이프라인, MT5 도구, 동등성 도구
- `stages/`: 번호와 부제가 있는 단계 작업
- `tests/`: 재사용 코드 테스트
- `.agents/skills/`: 저장소 전용 Codex 스킬

## 현재 단계(Current Stage, 현재 단계)

`03_training_dataset__label_split_contract`

Stage 02(2단계)에서 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 실제로 만들었다.

- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- selected rows(선택 행 수): `54439`
- selection scope(선택 범위): `valid_row_only` + `cash_open_rows_only` + `full_cash_session_days_only`

이제 목표(goal, 목표)는 이 동결 산출물 위에 첫 training label(학습 라벨)과 split contract(분할 계약)를 정해서, 첫 training dataset(학습 데이터셋) 물질화 질문을 열어 두는 것이다.
