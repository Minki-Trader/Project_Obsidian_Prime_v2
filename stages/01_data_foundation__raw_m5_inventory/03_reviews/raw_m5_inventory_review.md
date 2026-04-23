# Raw M5 Inventory Review(원천 M5 재고 검토)

## 판정(Judgment, 판정)

`20260424_raw_m5_inventory` 실행(run, 실행)은 `positive(긍정)`로 본다.

쉽게 말하면, 우리가 기대한 원천 `M5` 파일(raw M5 files, 원천 5분봉 파일)은 모두 있다. 이 판정은 데이터 재고(data inventory, 데이터 재고)에만 해당하고, 모델이 준비됐다는 뜻은 아니다.

## 확인한 것(What Was Checked, 확인한 것)

- 예상 심볼(expected symbols, 예상 심볼) 12개를 검사했다.
- 각 심볼(symbol, 심볼)의 CSV(csv, 표 파일)와 manifest(목록 파일)를 비교했다.
- 행 수(row count, 행 수), 첫 봉(first open, 첫 봉), 마지막 봉(last open, 마지막 봉)이 manifest(목록 파일)와 맞는지 확인했다.
- 5분봉 정렬(M5 alignment, 5분봉 정렬), 중복 봉(duplicate opens, 중복 봉), 닫힘 시간(close span, 닫힘 간격)을 확인했다.

## 결과(Result, 결과)

- 사용 가능 심볼(usable symbols, 사용 가능 심볼): `12 / 12`
- manifest mismatch(목록 불일치): `0`
- timing issue(시간 구조 문제): `0`
- 공통 첫 봉(common first open, 공통 첫 봉): `2022-08-01T16:35:00Z`
- 공통 마지막 봉(common last open, 공통 마지막 봉): `2026-04-13T22:55:00Z`
- `US100` 첫 봉(first open, 첫 봉): `2022-08-01T01:00:00Z`
- `US100` 마지막 봉(last open, 마지막 봉): `2026-04-13T23:55:00Z`

## 열린 부분(Open Boundary, 열린 경계)

시간대 상태(timezone status, 시간대 상태)는 아직 `UNRESOLVED_REQUIRES_MANUAL_BINDING`이다.

효과(effect, 효과): 원천 파일은 쓸 수 있지만, 다음 단계에서 시간대와 캘린더(calendar, 달력) 해석을 명확히 적어야 한다. 이걸 하지 않으면 피처 프레임(feature frame, 피처 프레임)의 시간 의미가 흐려진다.

## 다음 질문(Next Question, 다음 질문)

첫 피처 프레임(feature frame, 피처 프레임)은 전체 공통 창(common window, 공통 기간)인 `2022-08-01T16:35:00Z`부터 시작할지, 기존 실용 모델링 시작(practical modeling start, 실용 모델링 시작)인 `2022-09-01`부터 시작할지 결정해야 한다.
