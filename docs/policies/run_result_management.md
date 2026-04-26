# Run Result Management

실행(run, 실행)은 정체성(identity, 정체성)이 있어야 한다.

## 필수 개념(Required Ideas, 필수 개념)

- `run_manifest.json(실행 목록)`: 무엇을 어떤 입력으로 실행했는지
- `run_registry.csv(실행 등록부)`: 지속 실행 색인(durable run index, 지속 실행 색인)
- 출력 경로(output path, 출력 경로): 결과가 있는 곳
- 상태(status, 상태): planned, running, completed, reviewed, archived, invalid

## 규칙(Rule, 규칙)

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토됨(reviewed, 검토됨)이 된다.

## Run/Subrun Ledger(실행/하위 실행 장부)

알파 탐색(alpha exploration, 알파 탐색) 실행은 `run_registry.csv(실행 등록부)` 한 줄만으로 충분하지 않다.

필수 장부(required ledgers, 필수 장부):

- `docs/registers/run_registry.csv`: top-level run(상위 실행) 한 줄
- `docs/registers/alpha_run_ledger.csv`: run/subrun/view(실행/하위 실행/보기) 한 줄씩
- `stages/<stage_id>/03_reviews/stage_run_ledger.csv`: 해당 stage(단계) 내부의 run/subrun/view(실행/하위 실행/보기) 한 줄씩

`alpha_run_ledger.csv(알파 실행 장부)`와 stage-local ledger(단계 내부 장부)는 최소한 `run_id(실행 ID)`, `subrun_id(하위 실행 ID)`, `tier_scope(티어 범위)`, `record_view(기록 보기)`, `kpi_scope(KPI 범위)`, `status(상태)`, `judgment(판정)`, `path(경로)`를 가진다.

효과(effect, 효과)는 한 실행(run, 실행) 안의 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산), MT5 runtime probe(MT5 런타임 탐침) 같은 세부 판독을 한 줄씩 누적하는 것이다.

Stage 10(10단계) 이후 alpha run(알파 실행)은 Tier A/B paired records(티어 A/B 쌍 기록)가 없으면 완전한 reviewed run(검토 완료 실행)으로 닫지 않는다. 이미 닫힌 실행이 새 규칙보다 앞선 경우에는 `pre_pair_rule_requires_supplement(쌍 규칙 전 실행, 보강 필요)`로 표시한다.

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) routed run(라우팅 실행)은 같은 필수 장부를 쓰되, MT5(`MetaTrader 5`, 메타트레이더5) 행을 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 적는다.

Tier B fallback(Tier B 대체) 행은 subtype breakdown(하위유형 분해)과 no_tier labelable rows(티어 없음 라벨 가능 행)를 guardrail KPI(가드레일 핵심 성과 지표)에 포함한다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기) 구조를 유지하면서도, combined record(합산 기록)가 separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)인지 실제 라우팅 전체인지 헷갈리지 않게 하는 것이다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

실행(run, 실행)이 외부 환경(external environment, 외부 환경)에 기대는 주장을 만들면, `run_manifest.json(실행 목록)` 또는 검토 문서(review document, 검토 문서)에 외부 검증 상태(external verification status, 외부 검증 상태)를 적는다.

허용 상태(allowed states, 허용 상태)는 다음 중 하나다.

- `not_applicable(해당 없음)`: 외부 환경이 이 주장에 필요 없다.
- `completed(완료)`: 좁은 충분 검증(narrow sufficient check, 좁은 충분 검증)을 실행했다.
- `blocked(차단)`: 시도했지만 환경, 권한, 데이터, 도구 문제로 막혔다.
- `out_of_scope_by_claim(주장 범위 밖)`: 이번 주장을 낮춰서 외부 검증이 필요 없게 만들었다.

`blocked(차단)`나 `out_of_scope_by_claim(주장 범위 밖)`은 다음 작업(next work, 다음 작업)이 될 수 있지만, 같은 빠진 검증(missing check, 빠진 검증)을 반복해서 검토 완료(reviewed, 검토됨) 근거처럼 쓰면 안 된다.
