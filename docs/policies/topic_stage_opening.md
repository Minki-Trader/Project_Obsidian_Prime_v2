# Topic Stage Opening Policy

이 문서는 사용자가 stage open(단계 개방) 전에 던진 topic(주제)을 Codex(코덱스)가 stage question(단계 질문)으로 바꾸는 규칙을 정한다.

목적은 사용자 주제를 fixed layer(고정 계층), axis(축), handle(손잡이), mandatory checklist(필수 체크리스트)로 굳히지 않고, 하나의 구체적인 stage(단계) 질문으로 좁혀 탐색하는 것이다.

## 핵심 원칙(Core Principle, 핵심 원칙)

사용자 topic(주제)은 stage(단계)의 출발점이지 저장소 운영 문법(repository operating vocabulary, 저장소 운영 문법)이 아니다.

Codex(코덱스)는 사용자가 던진 말을 먼저 하나의 stage question(단계 질문)으로 바꾼다.

효과(effect, 효과)는 "이번에는 BE/partial 쪽을 보자" 같은 말을 "본전 이동/부분청산이 어떤 거래 생명주기 패턴을 만드는가?"처럼 탐색 가능한 질문으로 바꾸는 것이다.

## 변환 순서(Conversion Order, 변환 순서)

1. `user_topic(사용자 주제)`: 사용자가 stage open(단계 개방) 전에 던진 방향.
2. `stage_question(단계 질문)`: Codex(코덱스)가 한 문장으로 좁힌 이번 stage(단계)의 핵심 질문.
3. `stage_probe(단계 탐침)`: 그 질문을 확인하기 위한 좁은 실험, 문서 조사, runtime probe(런타임 탐침), 또는 KPI read(KPI 판독).
4. `named_pattern(이름 붙은 패턴)`: 반복되거나 설명 가능한 고유 반응.
5. `candidate_role(후보 역할)`: 살아남은 패턴의 다음 쓰임. 예: shadow(그림자), sidecar(보조), overlay(덧씌움), baseline candidate(기준선 후보), bundle candidate(번들 후보), ONNX candidate(ONNX 후보), diagnostic branch(진단 갈래), negative memory(부정 기억).

효과(effect, 효과)는 "무슨 축인가"를 먼저 묻지 않고, "이번 stage(단계)가 답할 질문은 무엇인가"를 먼저 묻게 하는 것이다.

## 이름 붙이기 규칙(Naming Rules, 이름 붙이기 규칙)

- 이름(name, 이름)은 발견된 pattern(패턴)을 요약하는 provisional label(임시 라벨)이다.
- 이름은 stage question(단계 질문)과 evidence(근거)를 따라 바뀔 수 있다.
- 사용자 표현을 그대로 taxonomy(분류표)로 만들지 않는다.
- topic(주제), layer(계층), axis(축), adapter(어댑터), ONNX(온닉스), runtime(런타임), operating(운영)을 한 번에 묶어 이름 붙이지 않는다.
- 더 정확한 이름이 생기면 rename(이름 변경)을 허용하고, 이전 이름은 alias(별칭)나 closed memory(닫힌 기억)로 남긴다.

효과(effect, 효과)는 빠른 대화의 자유도는 유지하되, 이름이 결론처럼 굳는 drift(드리프트)를 막는 것이다.

## Stage 개방 규칙(Stage Opening Rule, 단계 개방 규칙)

새 stage(단계)를 열 때는 하나의 `stage_question(단계 질문)`만 핵심 질문(core question, 핵심 질문)으로 둔다.

사용자가 명시적으로 실행을 요청하기 전에는 `docs/templates/stage_open_draft.md` 형식의 stage_open_draft(단계 개방 초안)를 먼저 작성하고, stage folder(단계 폴더), current truth(현재 진실), run registry(실행 등록부), code(코드)를 먼저 바꾸지 않는다.

우선순위는 다음 순서로 본다.

- 사용자가 방금 던진 topic(주제)이 무엇인가.
- 현재 v2 current truth(현재 진실)에서 그 질문을 어디까지 확인할 수 있는가.
- 기존 artifact(산출물), score table(점수표), MT5 report(MT5 보고서), KPI ledger(KPI 장부)로 측정 가능한가.
- full period(전체 기간)와 time segment(시간 구간)를 같이 볼 수 있는가.
- 실패해도 negative memory(부정 기억)나 diagnostic branch(진단 갈래)로 남길 수 있을 만큼 질문이 좁은가.

효과(effect, 효과)는 이후 새 stage(단계)가 미리 정한 분류표를 채우는 작업이 아니라, 사용자가 던진 주제를 하나씩 끝까지 파는 흐름이 되게 하는 것이다.

## ONNX와 Runtime 경계(ONNX and Runtime Boundary, ONNX와 런타임 경계)

ONNX(온닉스), runtime handoff(런타임 인계), operating candidate(운영 후보)는 `named_pattern(이름 붙은 패턴)`과 `candidate_role(후보 역할)`이 충분히 정리된 뒤에만 다음 질문으로 올린다.

처음 stage question(단계 질문)에 ONNX(온닉스)나 runtime(런타임)이 포함될 수는 있다. 하지만 그 경우에도 무엇을 검증하는지, 어떤 근거가 없으면 주장하지 않을지 먼저 적는다.

효과(effect, 효과)는 pattern discovery(패턴 발견), export readiness(내보내기 준비), runtime verification(런타임 검증), operating claim(운영 주장)을 서로 다른 증거 단계로 분리하는 것이다.

## 코드 배치 경계(Code Placement Boundary, 코드 배치 경계)

Stage-local prototype(단계 로컬 원형)은 필요할 때 `stage_pipelines/`나 `stages/<stage_id>/02_runs/`에 둘 수 있다.

`foundation/`에는 같은 역할이 여러 stage(단계)에서 반복되고, input/output contract(입출력 계약)가 안정된 뒤에만 둔다.

효과(effect, 효과)는 아직 탐색 중인 이름과 구조를 reusable foundation(재사용 기반)처럼 굳히지 않는 것이다.

## 금지 주장(Forbidden Claims, 금지 주장)

다음 주장은 별도 근거 없이 금지한다.

- user_topic(사용자 주제)을 fixed layer(고정 계층), axis(축), handle(손잡이), adapter taxonomy(어댑터 분류표)로 읽는 주장
- stage_question(단계 질문)을 곧바로 implementation plan(구현 계획), ONNX target(ONNX 대상), runtime handoff(런타임 인계), operating candidate(운영 후보)로 읽는 주장
- named_pattern(이름 붙은 패턴) 없이 candidate_role(후보 역할)을 확정하는 주장
- ONNX parity(ONNX 동등성) 없이 runtime handoff(런타임 인계)를 완료로 읽는 주장
- MT5(`MetaTrader 5`, 메타트레이더5) 외부 검증 없이 runtime authority(런타임 권위)를 주장하는 일
- positive KPI(긍정 KPI)를 baseline(기준선), promotion candidate(승격 후보), operating promotion(운영 승격)으로 읽는 주장

효과(effect, 효과)는 사용자 주제에서 운영 주장까지 가는 길이 증거 없이 앞질러 가지 못하게 하는 것이다.
