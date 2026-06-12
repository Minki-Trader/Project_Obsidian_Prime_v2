# Grok Output(Grok 출력)

Source(출처): successful `grok.exe -p` single prompt(단일 프롬프트) call on 2026-06-12, using compact text-only consultation(압축 텍스트 상담).

## Accepted(수용)

- External reviewer mode(외부 검토자 모드) plus compact `-p` prompts(압축 단일 프롬프트)는 맞는 방향이다.
- Wrapper script(래퍼 스크립트) is accepted(수용): preflight(사전 확인), timeout(시간 제한), log-strip(로그 제거), clean output capture(정리 출력 캡처), and packet record(묶음 기록)을 담당해야 한다.
- Codex remains the verifier(검증자): Grok advice(Grok 조언)는 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 만들 수 없다.

## Risky(위험)

- Short `-p` prompts(짧은 단일 프롬프트)는 large review(대규모 검토)에서 context loss(문맥 손실)를 만들 수 있다.
- Wrapper(래퍼)가 stderr(표준 오류)를 너무 많이 숨기면 real failure(실제 실패)를 놓칠 수 있다.
- Wrapper(래퍼)를 permanent crutch(영구 목발)로만 쓰고 prompt-file/MCP environment(프롬프트 파일/MCP 환경) 문제를 고치지 않으면 maintenance debt(유지보수 부채)가 된다.

## Protocol(절차)

- Codex speaks first(Codex가 먼저 말함): current truth snapshot(현재 진실 스냅샷), exact review request(정확한 검토 요청), success criteria(성공 기준), claim boundary(주장 경계)를 prompt(프롬프트)에 넣는다.
- Non-trivial reviews(비사소 검토)는 staged narrow reviews(단계별 좁은 검토)로 쪼갠다: architecture(구조), KPI/evidence(KPI/근거), external verification(외부 검증), policy compliance(정책 준수)처럼 나눈다.
- Every Grok response(Grok 응답)는 prompt hash(프롬프트 해시), timestamp(시각), review packet id(검토 묶음 ID)와 함께 기록한다.
- Codex verification note(Codex 검증 기록)는 Grok 의견이 claim boundary(주장 경계)를 바꾸는지, 로컬에서 무엇을 재확인했는지 적는다.
- Grok output(Grok 출력)은 external second opinion(외부 2차 의견)으로만 라벨링한다.

## Wrapper(래퍼)

- Wrapper(래퍼)는 transport hygiene(전송 위생)과 recording(기록)만 담당한다.
- Required behaviors(필수 동작):
  - prompt length preflight(프롬프트 길이 사전 확인)
  - empty prompt guard(빈 프롬프트 방지)
  - timeout with partial output salvage(시간 제한과 부분 출력 회수)
  - deterministic noise stripping(결정적 잡음 제거)
  - clean output artifact(정리 출력 산출물) 저장
  - structured packet record(구조화 묶음 기록) 생성
- Wrapper(래퍼)는 Grok content(Grok 내용)를 해석하거나 결정하지 않는다.

## Policy(정책)

- Grok Collaboration Rule(Grok 협업 규칙) and agent trigger policy(에이전트 트리거 정책)에 `Grok review receipt + Codex verification + local evidence` triple(3종 묶음)을 required gate artifact(필수 게이트 산출물)로 적는다.
- Complex review(복합 검토)는 monolithic prompt(단일 거대 프롬프트) 대신 multiple narrow passes(여러 좁은 회차)를 기본값으로 한다.
- Exploration(탐색)은 gate 없이 가능하지만, operating claims(운영 주장)는 Grok review(Grok 검토)만으로 닫을 수 없다.

