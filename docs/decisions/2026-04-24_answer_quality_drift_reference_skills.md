# Decision Memo

## 결정(Decision, 결정)

네 가지 repo-scoped skill(저장소 전용 스킬)을 추가한다.

- `obsidian-answer-clarity`: 사용자 답변을 쉬운 설명으로 만든다.
- `obsidian-code-quality`: 구현 품질(code quality, 코드 품질)을 전문가 답안지처럼 높인다.
- `obsidian-workflow-drift-guard`: 원재료, 도구, 환경, 목표가 서로 헷갈리며 작업이 새는 일을 막는다.
- `obsidian-reference-scout`: 함수 사용법, 문법, 외부 구현 패턴, MQL5/MQL5 forum, GitHub, 공식 문서를 찾아 프로젝트에 맞게 걸러 쓴다.

## 이유(Why, 이유)

기존 skill set(스킬 구성)은 구조, 배치, 단계, 실행 근거를 잘 지키는 쪽에 강했다. 하지만 세 가지 공백이 남아 있었다.

첫째, 답변은 한국어 병행 표기만으로 충분하지 않았다. 사용자가 비개발자이거나 trading specialist(트레이딩 전문가)가 아니어도, 왜 중요한지와 어떤 효과가 있는지 따라올 수 있어야 한다.

둘째, 코드에는 placement(배치)뿐 아니라 quality(품질)가 필요하다. 좋은 코드는 맞는 답만 내는 것이 아니라 책임, 흐름, 근거, 경계, 검증이 읽혀야 한다.

셋째, 작업이 막혔을 때 source data(원천 데이터), tool(도구), environment(환경), permission(권한), goal(목표)을 헷갈리면, 실제 blocker(차단 지점)를 해결하지 못하고 검토 문구만 늘어날 수 있다.

넷째, 올바른 API usage(API 사용법), syntax(구문), MQL5 behavior(MQL5 동작), LightGBM 등 외부 라이브러리 사용법은 프로젝트 기억만으로 단정하지 않고 공식 문서와 신뢰 가능한 reference(참고자료)를 찾아 확인해야 한다.

## 효과(Effect, 효과)

- 답변은 쉬운 의미, 이유, 효과를 같이 설명한다.
- 코드 작성은 단순 실행보다 구현 품질을 더 강하게 본다.
- 작업 시작과 막힘 상황에서 실제 blocker를 더 정확히 분류한다.
- 외부 자료는 복사 대상이 아니라, 확인과 아이디어 후보로 다룬다.

## 경계(Boundary, 경계)

이 결정은 agent behavior(에이전트 행동)와 skill routing(스킬 라우팅)을 보강한다.

Stage 03(3단계)의 label definition(라벨 정의), split contract(분할 계약), training dataset materialization(학습 데이터셋 물질화)은 아직 바꾸지 않는다.
