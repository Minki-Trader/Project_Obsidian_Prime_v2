# Run Result Management

실행(run, 실행)은 정체성(identity, 정체성)이 있어야 한다.

## 필수 개념(Required Ideas, 필수 개념)

- `run_manifest.json(실행 목록)`: 무엇을 어떤 입력으로 실행했는지
- `run_registry.csv(실행 등록부)`: 지속 실행 색인(durable run index, 지속 실행 색인)
- 출력 경로(output path, 출력 경로): 결과가 있는 곳
- 상태(status, 상태): planned, running, completed, reviewed, archived, invalid

## 규칙(Rule, 규칙)

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토됨(reviewed, 검토됨)이 된다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

실행(run, 실행)이 외부 환경(external environment, 외부 환경)에 기대는 주장을 만들면, `run_manifest.json(실행 목록)` 또는 검토 문서(review document, 검토 문서)에 외부 검증 상태(external verification status, 외부 검증 상태)를 적는다.

허용 상태(allowed states, 허용 상태)는 다음 중 하나다.

- `not_applicable(해당 없음)`: 외부 환경이 이 주장에 필요 없다.
- `completed(완료)`: 좁은 충분 검증(narrow sufficient check, 좁은 충분 검증)을 실행했다.
- `blocked(차단)`: 시도했지만 환경, 권한, 데이터, 도구 문제로 막혔다.
- `out_of_scope_by_claim(주장 범위 밖)`: 이번 주장을 낮춰서 외부 검증이 필요 없게 만들었다.

`blocked(차단)`나 `out_of_scope_by_claim(주장 범위 밖)`은 다음 작업(next work, 다음 작업)이 될 수 있지만, 같은 빠진 검증(missing check, 빠진 검증)을 반복해서 검토 완료(reviewed, 검토됨) 근거처럼 쓰면 안 된다.
