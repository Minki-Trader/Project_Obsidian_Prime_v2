# Decision Memo

## 결정(Decision, 결정)

agent guard(에이전트 가드)와 policy routing(정책 라우팅)을 단순하게 정리한다.

- `obsidian-stage-transition`에서 번호가 붙은 단계(stage, 단계)에 고정 의미를 박아 둔 문장을 제거한다.
- `obsidian-claim-discipline`은 `docs/policies/agent_trigger_policy.md`에 명시한다.
- `obsidian-task-packet`과 `obsidian-publish-merge`는 별도 repo-scoped skill(저장소 전용 스킬)에서 제거한다.
- `obsidian-architecture-guard`의 `agents/openai.yaml` 설명은 실제 담당 범위에 맞게 넓힌다.
- `validate_agent_settings.py`는 agent settings(에이전트 설정) 파일, 필수 interface key(인터페이스 키), 그리고 최소 prompt concept(프롬프트 개념)을 확인한다.

## 이유(Why, 이유)

이 변경은 guard(가드)를 더 많이 만드는 것이 아니라, 헷갈리는 길을 줄이기 위한 것이다.

기존 `obsidian-stage-transition`은 오래된 단계 의미(stage meaning, 단계 의미)를 일부 들고 있었다. 현재 Stage 03(3단계)은 training label(학습 라벨)과 split contract(분할 계약)를 정하는 단계인데, runtime parity(런타임 동등성)를 소유한 것처럼 읽힐 수 있었다.

또한 `obsidian-task-packet`과 `obsidian-publish-merge`는 useful helper(유용한 보조 도구)일 수 있지만, 현재 저장소 운영에서는 별도 스킬로 둘 만큼 필수적이지 않다. 범위 고정(scope fixing, 범위 고정)은 `obsidian-session-intake`가 맡고, main merge(메인 병합) 제한은 branch policy(브랜치 정책)와 명시 사용자 요청으로 충분히 다룬다.

반대로 `obsidian-claim-discipline`은 필요하다. 이 프로젝트는 planning(계획), materialized evidence(물질화된 근거), reviewed(검토됨), runtime authority(런타임 권위), operating promotion(운영 승격)을 엄격하게 구분해야 하기 때문이다.

## 효과(Effect, 효과)

- stage transition(단계 전환)은 현재 진실(current truth, 현재 진실) 문서에서 단계 의미를 읽는다.
- claim discipline(주장 규율)은 공식 trigger policy(트리거 정책)에 남는다.
- 불필요한 별도 skill route(스킬 경로)를 줄여 로컬 Codex가 더 단순하게 읽을 수 있다.
- agent settings validator(에이전트 설정 검사기)는 `openai.yaml`이 없거나 너무 좁은 설명으로 바뀌는 일을 잡는다.

## 경계(Boundary, 경계)

이 결정은 agent/policy 정리(agent/policy cleanup, 에이전트/정책 정리)다.

Stage 03(3단계)의 label definition(라벨 정의), split contract(분할 계약), training dataset materialization(학습 데이터셋 물질화)은 아직 바꾸지 않는다.
