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

## 테스트(Test, 테스트)

기본 test command(테스트 명령)는 빠른 검증(fast verification, 빠른 검증)만 실행한다.

```powershell
py -3.13 -m unittest discover -s tests
```

raw data integration tests(원천 데이터 통합 테스트)는 느리므로 명시적으로 켠다.

```powershell
$env:OBSIDIAN_RUN_SLOW_TESTS='1'
py -3.13 -m unittest tests.test_materialize_fpmarkets_v2_dataset tests.test_materialize_feature_frame_freeze tests.test_feature_frame_target_probe
Remove-Item Env:\OBSIDIAN_RUN_SLOW_TESTS
```

효과(effect, 효과)는 일반 확인에서 timeout(시간 초과)을 피하고, 무거운 full raw-data check(전체 원천 데이터 확인)는 필요할 때 분리해서 실행하는 것이다.

## 현재 상태(Current Truth, 현재 진실)

이 README는 live status ledger(실시간 상태 장부)가 아니다.

현재 active stage(현재 활성 단계), open items(열린 항목), pre-alpha stage queue(알파 전 단계 대기열)는 아래 문서를 따른다.

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- `docs/workspace/pre_alpha_stage_plan.md`

효과(effect, 효과)는 README가 오래된 단계 번호를 들고 drift(드리프트, 방향 이탈)를 만들지 않게 하는 것이다.
