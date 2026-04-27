# Advisory: Stage 10-11 Scout Modularization

- date(날짜): `2026-04-27`
- scope(범위): Stage 10-11 alpha scout code surface(Stage 10-11 알파 탐색 코드 표면)
- status(상태): `advisory_only_not_adopted`
- change type(변경 유형): documentation-only advice(문서 전용 조언)

## 성격(Boundary, 경계)

이 문서는 바로 적용할 결정(decision, 결정)이 아니다.

코드(code, 코드), 정책(policy, 정책), active stage(활성 단계), run judgment(실행 판정), artifact identity(산출물 정체성)를 바꾸지 않는다.

효과(effect, 효과)는 Stage 10-11(10-11단계)에서 관찰된 code surface drift(코드 표면 드리프트)를 다음 정리 작업의 후보로만 남기고, 현재 결과나 장부를 조용히 고치지 않는 것이다.

## 관찰(Observation, 관찰)

Stage 09(9단계)까지는 foundation closure(기반 종결) 성격이 강했다. contract(계약), policy(정책), register(등록부), current truth(현재 진실)가 비교적 안정된 구조를 이뤘다.

Stage 10-11(10-11단계)은 alpha scout(알파 탐색)가 실제로 빠르게 늘어난 구간이다. run(실행)이 늘면서 model training(모델 학습), threshold selection(임계값 선택), context gate(문맥 제한), MT5 materialization(MT5 물질화), tester execution(테스터 실행), KPI ledger write(KPI 장부 기록)가 큰 pipeline script(파이프라인 스크립트)에 함께 모였다.

이 상태는 작동하는 연구 코드(working research code, 작동하는 연구 코드)로는 이해된다. 하지만 다음 run(다음 실행)을 더 많이 열수록 ownership(소유권), test boundary(테스트 경계), reuse boundary(재사용 경계)가 흐려질 수 있다.

## 왜 생겼는가(Probable Cause, 추정 원인)

1. Stage 10(10단계)의 큰 scout script(탐색 스크립트)가 MT5까지 성공하면서 이후 작업의 gravity center(중력 중심)가 되었다.
2. modularization rule(모듈화 규칙)은 있었지만, line count(줄 수), owner module(소유 모듈), spec-only run(명세 전용 실행)을 강제하는 validator(검증기)는 없었다.
3. run evidence(실행 근거), same-pass MT5 verification(같은 회차 MT5 검증), claim boundary(주장 경계)가 강해서 code surface cleanup(코드 표면 정리)보다 run completion(실행 완료)이 우선되기 쉬웠다.
4. Stage 11(11단계)은 Stage 10(10단계)의 helper function(보조 함수)을 재사용했지만, 그 helper(보조 함수)를 별도 shared module(공유 모듈)로 끌어올리는 마지막 단계는 아직 남았다.

## 권고(Advice, 조언)

다음 정리 작업은 새 alpha result(알파 결과)를 만들기보다, scout engine(탐색 엔진)과 scout spec(탐색 명세)을 분리하는 작은 구조 작업으로 여는 편이 좋다.

권고 구조는 다음과 같다.

| area(영역) | 현재 압력(current pressure, 현재 압력) | 권고(advice, 조언) |
|---|---|---|
| model training(모델 학습) | run script(실행 스크립트)가 model family(모델 계열)와 export(내보내기)를 직접 소유 | `foundation/scouting/models.py` 같은 shared model adapter(공유 모델 어댑터) 후보로 분리 |
| threshold(임계값) | absolute/rank/context threshold(절대/순위/문맥 임계값)가 run별로 흩어짐 | `foundation/scouting/thresholds.py` 후보로 분리하고 threshold spec(임계값 명세)을 데이터화 |
| context gate(문맥 제한) | idea burst(아이디어 확장) 조건이 script-level branching(스크립트 분기)로 커짐 | `foundation/scouting/context_gates.py` 후보로 분리 |
| MT5 materialization(MT5 물질화) | `.set`, `.ini`, Common Files copy(Common Files 복사), report collection(보고서 수집)이 scout script에 같이 있음 | `foundation/mt5_runtime/` 또는 `foundation/scouting/mt5_materialization.py` 후보로 분리 |
| ledger write(장부 기록) | project/stage ledger row(프로젝트/단계 장부 행)를 각 script가 직접 구성 | `foundation/ledgers/alpha_runs.py` 후보로 분리 |
| run definition(실행 정의) | 새 run이 새 code branch(코드 분기)처럼 열림 | `ScoutSpec(탐색 명세)` 또는 JSON/YAML spec(명세)로 run difference(실행 차이)를 표현 |

## Stage 09까지에 대한 조언(Advice For Stage 09 And Earlier, Stage 09 이전 조언)

Stage 09(9단계)까지의 기반 구조는 크게 다시 열 필요가 없어 보인다.

좋은 점은 다음과 같다.

- closed truth(닫힌 진실)와 not-current-truth(현재 진실 아님)를 분리한다.
- Tier A/B(티어 A/B)를 exploration label(탐색 라벨)로 유지한다.
- runtime authority(런타임 권위), alpha quality(알파 품질), operating promotion(운영 승격)을 섞지 않는다.

권고는 가볍다.

- Stage 02-09(2-9단계)의 artifact recovery map(산출물 복구 지도)을 나중에 별도 문서로 만들면 좋다.
- 현재 문서/계약 구조는 유지한다.
- 기반 단계(closed foundation stage, 닫힌 기반 단계)는 새 실험 구조 작업의 대상이 아니라 reference surface(참조 표면)로 둔다.

## Stage 10-11에 대한 조언(Advice For Stage 10-11, Stage 10-11 조언)

Stage 10-11(10-11단계)은 탐색 속도가 빠른 구간이라, 정책을 더 늘리기보다 작은 실행 구조를 만드는 편이 낫다.

권고 순서는 다음과 같다.

1. current scripts(현재 스크립트)를 먼저 그대로 둔다.
2. Stage 10 script(10단계 스크립트)의 reusable helper(재사용 보조 함수)를 `foundation/scouting/` 후보 모듈로 옮길 목록만 만든다.
3. Stage 11 script(11단계 스크립트)가 Stage 10 script(10단계 스크립트)를 shared library(공유 라이브러리)처럼 import하는 부분을 새 shared module(공유 모듈) 후보로 표시한다.
4. 새 run(새 실행)은 가능하면 code edit(코드 수정)보다 `ScoutSpec` addition(탐색 명세 추가)로 열 수 있게 한다.
5. RUN02G/RUN02N/RUN02P(실행 02G/02N/02P) 같은 salvage candidates(회수 가치 후보)는 promotion candidate(승격 후보)가 아니라 next-scout input candidate(다음 탐색 입력 후보)로 작게 묶는다.

## 하지 말 것(Non-Goals, 비목표)

이 advisory(권고)는 다음을 하지 않는다.

- Stage 10-11 result judgment(결과 판정)을 바꾸지 않는다.
- current state(현재 상태)를 바꾸지 않는다.
- run ledger(실행 장부)를 고치지 않는다.
- MT5 result(MT5 결과)를 재해석하지 않는다.
- 바로 large refactor(대형 리팩터링)를 요구하지 않는다.

## 다음 작업 후보(Next Work Candidates, 다음 작업 후보)

작게 시작한다면 다음 중 하나가 좋다.

1. `foundation/scouting/` skeleton(뼈대)만 만들고 기존 코드는 그대로 둔다.
2. `ScoutSpec` dataclass(탐색 명세 데이터클래스)를 먼저 만들고, 새 run 하나에만 시범 적용한다.
3. Stage 10 script(10단계 스크립트)에서 pure helper(순수 보조 함수)만 옮기고 MT5 execution path(MT5 실행 경로)는 건드리지 않는다.
4. architecture debt register(구조 부채 등록부)의 `AD-006`에 follow-up note(후속 메모)를 붙인다.

추천은 2번이다.

효과(effect, 효과)는 기존 성공 경로를 깨지 않고, 다음 실험부터 code growth(코드 증가)를 줄이는 것이다.
