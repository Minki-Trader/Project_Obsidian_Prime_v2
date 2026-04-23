# Current Working State

- updated_on: `2026-04-24`
- project_mode: `clean_stage_restart`
- active_stage: `01_data_foundation__raw_m5_inventory`
- active_branch: `codex/stage01-raw-m5-inventory`

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

## 현재 단계(Current Stage, 현재 단계)

`01_data_foundation__raw_m5_inventory`

이 단계는 간단한 질문(question, 질문)을 답한다.

우리가 실제로 가진 `M5` 데이터가 무엇이고, 그 데이터가 어떤 첫 모델링 창(modeling window, 모델링 창)을 지탱할 수 있는가?

## 확인된 재고(Confirmed Inventory, 확인된 재고)

`20260424_raw_m5_inventory` 실행(run, 실행)이 원천 `M5` 재고(raw M5 inventory, 원천 M5 재고)를 만들었다.

- 예상 심볼(expected symbols, 예상 심볼): `12`
- 사용 가능 심볼(usable symbols, 사용 가능 심볼): `12`
- 공통 첫 봉(common first open, 공통 첫 봉): `2022-08-01T16:35:00Z`
- 공통 마지막 봉(common last open, 공통 마지막 봉): `2026-04-13T22:55:00Z`
- `US100` 첫 봉(first open, 첫 봉): `2022-08-01T01:00:00Z`
- `US100` 마지막 봉(last open, 마지막 봉): `2026-04-13T23:55:00Z`

효과(effect, 효과): Stage 01은 이제 “파일이 있는지”를 추측하지 않아도 된다. 다음 작업은 시간대(timezone, 시간대) 해석을 묶고 첫 피처 프레임(feature frame, 피처 프레임)을 정하는 것이다.

## 다음 일(Next Useful Work, 다음 작업)

1. 원천 export(내보내기)의 시간대(timezone, 시간대)와 캘린더(calendar, 달력) 해석을 분명히 적는다.
2. 첫 깨끗한 피처 프레임(feature frame, 피처 프레임)에 쓸 창(window, 기간)을 정한다.
3. 학습 데이터셋(training dataset, 학습 데이터셋)은 피처 프레임과 검증 규칙(validation rule, 검증 규칙)이 준비된 뒤 정한다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 모델 연구(model study, 모델 연구) 전에 끝없는 사전검증(pre-validation, 사전검증)을 받아야 한다는 주장
