**Grok 컨설팅 보고서: Codex Super-Agent Design (사용자 맞춤 수퍼에이전트화)**

### 핵심 진단 (Executive diagnosis)
Codex의 현재 운영 모델은 이미 연구 무결성과 실행 규율을 잘 지키는 packet 중심(작업 묶음 중심) 시스템이다. `obsidian-session-intake` → `obsidian-work-packet-router` → 정확히 1개의 `primary_family` + 1개의 `primary_skill` + 최소 `support_skills` + `required_gates` + receipt + `final_claim_guard` 흐름이 핵심이다. 

이 구조는 "스킬을 많이 붙여 보이게 하는" 위험을 막고, 탐색(exploration)에는 게이트가 없으며, 운영 의미(operating meaning) 주장(runtime authority, operating promotion, live readiness)에는 강한 증거를 요구하는 점에서 강점이다. 

문제는 두 가지다. 
- 설명과 계약이 여러 문서(AGENTS.md, agent_trigger_policy.md, work_family_registry.yaml, skill_receipt_schema.yaml)에 중복/장황하게 퍼져 있어 미래 에이전트가 혼란스러울 수 있다. 
- 사용자 맞춤(user-tailored) 요소(한국어 우선 보고, action + effect, co-pilot 느낌, 사용자 부담 최소화)가 "기본값"으로 충분히 강제되지 않아 "완전 슈퍼똑똑이 + 나 맞춤" 느낌이 약하다.

사용자가 원하는 것은 더 많은 규칙이나 의식(ritual)이 아니라, **더 날카로운 기본값(sharper defaults)**, **더 명확한 영수증(clearer receipts)**, **더 적은 중복**이다. 복잡도를 늘리는 제안은 모두 배제했다.

### 현재 코덱스 작동 모델 (Mental model of current Codex behavior)
Codex는 매 작업 회차(pass)마다 다음을 강제한다:
- reentry_order.md 순서로 current truth(현재 진실)를 먼저 읽음 (`workspace_state.yaml`, `current_working_state.md`, 활성 단계 ledger, AGENTS.md 등).
- `obsidian-session-intake`로 scope를 좁히고 work family 후보를 잡음.
- `obsidian-work-packet-router`가 `work_family_registry.yaml`을 단일 진실 원천으로 사용해 정확히 **1 primary_family + 1 primary_skill**을 고르고, 필요한 만큼만 support를 붙임 (기본 limit 3, 일부 family 4).
- phase별 스킬 실행 → receipt 생산 (`skill_receipt_schema.yaml` 준수).
- `required_gates` + `required_gate_coverage_audit` 통과 후에만 claim.
- 항상 `obsidian-answer-clarity` + `obsidian-claim-discipline`으로 최종 필터링.
- 보고는 한국어 주 + 영어 용어 병기 + 행동(action)의 효과(effect) 설명 + 짧고 쉽게.

탐색 레인(exploration lane)에서는 자유롭게 아이디어를 밀고, Tier A/B paired 기록을 강제하며, external verification가 필요한 주장은 같은 pass에서 좁은 충분 검증을 시도하거나 blocked/inconclusive/out_of_scope로 명확히 낮춘다. `runtime_authority`와 `operating_promotion`은 workspace_state에서 명시적으로 `not_claimed` 상태를 유지한다.

이 모델은 "코드만 쓰고 끝"이나 "실험 결과만 나열"하는 것을 막는 데 효과적이다.

### 유지 / 단순화 / 강화 표 (Keep / simplify / strengthen table)

| 영역                  | 유지 (Keep) — 이유 | 단순화 (Simplify) — 대상 | 강화 (Strengthen) — 방법 |
|-----------------------|--------------------|---------------------------|---------------------------|
| **primary_family + primary_skill 정확히 1개** | Router의 핵심 규율. 스킬 남발 방지, receipt 의미를 지킴 | - | Router가 "왜 이 family/skill인가"를 receipt에 1줄로 강제 기록 |
| **work_family_registry.yaml 단일 진실 원천** | stage-agnostic, 5~50+ 단계까지 안정적 | family description 장황하고 한글/영어 섞임 (일부 1줄 요약으로 압축) | support_skill_limit을 모든 family에 명시적으로 두고 default 3을 더 강하게 적용 |
| **exploration 무게이트 + Progressive Hardening 어휘** | promotion_candidate vs operating_promotion 구분이 핵심 가치 | - | - |
| **final filter (answer-clarity + claim-discipline)** | 사용자 보고 품질과 과장 방지의 마지막 방어선 | - | 하드코딩 수준으로 고정 (policy_governance family 외 override 금지) |
| **reentry_order + current truth 문서** | 오래된 stage drift 방지, 진실 우선순위 명확 | - | 사용자 관심(현재 run judgment + next action)을 최상위로 더 강조 |
| **Language Rule (한국어 주 + action/effect + 짧게)** | 사용자 요구와 일치, co-pilot 느낌의 기반 | - | "사용자 맞춤 보고 스타일"을 2~3줄로 명시적으로 추가 |
| **Architecture invariants + tier paired 기록** | 코드 배치와 Tier A/B 증거 무결성 | - | - |
| **Receipt + gate coverage audit** | claim의 실제 근거가 됨 | receipt schema 설명이 여러 곳에 흩어짐 | "user_facing_impact" 1줄을 router 기본 receipt에 넣어 사용자 친화도 높임 |
| **Self-correction (plan_only 기본)** | 자동 수정의 위험을 막음 | - | plan_only에서 "사용자에게 물어볼 다음 좁은 질문"을 자동 생성 규칙 추가 |

### 사용자 맞춤 권고 (User-tailoring recommendations)
- 보고 기본값을 "co-pilot" 스타일로 고정: 한국어 우선 + 행동의 효과 함께 + 실행 가능한 다음 옵션 1~2개 + 근거/판정 요약. "더 자세히 설명해" 같은 vague 요청이 아니면 장황한 설명 금지.
- Router가 매 packet 시작 시 사용자 선호(현재는 Language Rule + observed behavior)를 자동 주입. receipt에 "이번 packet이 사용자에게 주는 가치" 1줄을 의무화.
- "나(사용자) 맞춤"은 새 prefs 파일이나 복잡한 context layer로 만들지 말고, AGENTS.md Language Rule + router default + answer-clarity 스킬 안에 녹여라. 사용자가 느끼는 부담(장황한 출력, 불필요한 스킬 나열, fake certainty)을 가장 먼저 줄이는 방향.
- 현재 run의 judgment와 next action을 current_working_state.md에서 더 사용자 친화적으로 유지 (이미 일부 되어 있음, 일관성만 강화).

### 최소 AGENTS.md 개선 계획 (Minimal AGENTS.md improvement plan)
모두 작은 변경. 새 섹션 대량 추가 금지.
- Language Rule 끝에 "사용자 협업 스타일" 2~3줄 추가: 한국어 주 + action/effect + co-pilot 느낌(실행 옵션 + 근거 제시) + fake certainty 금지.
- Codex 작업 생명주기 섹션에 "User intent를 routing의 최상위 필터로 사용" 한 문장 명시.
- Non-Negotiable Principle에 "사용자 부담을 늘리지 않는 변화만 허용" 한 줄 추가.
- 현재 진실(Current Truth) 섹션에 "사용자가 보는 current_working_state.md는 항상 한국어 action/effect 중심으로 유지" 강조.

### 스킬 시스템 개선 계획 (Skill system improvement plan)
- `work_family_registry.yaml`의 family description을 1~2줄로 압축하고 "언제 쓰는가(when to use)"를 명확한 1줄로 통일. 중복 설명 제거.
- Router가 support_skills를 고를 때 "not_required_for_this_packet", "enforced_as_required_gate_not_support_skill" 같은 이유를 항상 receipt에 남기게 강제 (이미 일부 있음, 더 일관되게).
- `skill_receipt_schema.yaml`은 router가 쉽게 주입할 수 있는 최소 contract으로 유지. 새 필드는 "user_facing_impact" 하나만 검토.
- final_answer_filter를 "항상 answer-clarity + claim-discipline (policy_governance family 외 override 불가)"로 router 설명과 registry에 명시.
- 새로운 스킬이나 family는 절대 만들지 말고, 기존 router sharpening으로 해결. support_skill_limit을 family별로 더 명확히 두어 자동 선택 범위를 줄임.

### 그록 협업 설계 (Grok collaboration design)
Grok은 항상 **external snapshot consultant** 모드로만 사용.
- Codex가 Grok을 부를 때: 제공된 snapshot + 구체적인 consulting question + "hard boundary(도구 사용 금지, 복잡도 증가 금지, runtime/operating claim 금지)"를 함께 전달.
- Grok은 제공된 snapshot만으로 답변. 이 repo를 직접 읽거나 편집하거나 shell을 쓰지 않음.
- 용도: architecture/policy cross-check, result judgment 2차 검토, design alternative 제안, receipt가 실제로 gate를 커버하는지 외부 검토.
- Codex는 Grok 제안을 "external review note"로 receipt에 남기고, 실제 적용은 Codex 내부 packet(`policy_skill_governance` 또는 해당 family)으로 처리.
- 절대 Grok에게 "이 run을 promotion candidate로 보자"나 runtime parity 최종 판단을 넘기지 않음.
- 협업은 information_only family + answer-clarity primary로 별도 관리. Grok 컨설팅 자체가 운영 권위를 주장하지 않게 함.

### 가치순 다음 수정 10개 (Concrete next 10 edits, ordered by value)
1. work_family_registry.yaml family description 전체를 1~2줄로 압축 + "user value" 1줄 추가 (가장 큰 중복 제거 효과).
2. Router의 final_answer_filter를 하드 규칙으로 고정 (answer-clarity + claim-discipline 항상, policy_governance 외 override 금지).
3. AGENTS.md Language Rule에 사용자 맞춤 보고 스타일 2~3줄 추가 (한국어 주 + action/effect + co-pilot).
4. agent_trigger_policy.md와 AGENTS.md의 긴 스킬 나열 중복을 제거하고 registry를 단일 참조로 명확히.
5. Router receipt에 "user_facing_impact" 1줄 (또는 skills_not_used 이유 표준화)을 기본으로 강제.
6. reentry_order.md에 "사용자 현재 관심(현재 run judgment + next action)"을 최우선 읽기 항목으로 더 강조.
7. 모든 family의 support_skill_limit을 registry에서 명시적으로 관리 (일관성 + 자동 선택 범위 축소).
8. self_correction_policy.yaml plan_only 모드에 "사용자에게 제안할 다음 좁은 질문" 생성 규칙 추가.
9. skill_receipt_schema.yaml에 최소한의 user-facing 필드만 검토하고, schema 설명을 router 문서로 통합.
10. AGENTS.md "Codex 작업 생명주기" 섹션 끝에 "User intent를 최상위 필터로 사용" + "receipt는 abandoned skills를 막는 guard" 문장 보강.

### 피해야 할 안티패턴 (Anti-patterns to avoid)
- 스킬이나 family를 "완벽해 보이게" 추가하는 행위 (router sharpening으로 해결).
- receipt를 의식처럼 길게 만드는 것 (guard 역할만 하면 충분).
- exploration 단계에서 operating vocabulary를 슬쩍 쓰는 것.
- "Grok이 대신 해줄 거야" 식 외부 의존을 내부 규율로 착각.
- stage-specific routing 규칙이나 복잡한 context injection layer 새로 만들기.
- 사용자 맞춤을 위해 새 파일이나 설정 계층을 늘리는 것 (기존 Language Rule + router default + answer-clarity 안에 녹여야 함).
- "더 rigorous해 보이게" 복잡도를 늘리는 제안.

### 확신도와 근거 한계 (Confidence and evidence limits)
이 보고서는 제공된 snapshot(2026-06-12T01:48:13+09:00 생성, workspace_state, AGENTS.md 전체, agent_trigger_policy.md, work_family_registry.yaml 전체, 주요 policy 문서, observed behavior, skill 목록 등)만을 근거로 작성했다. 

강한 확신: 운영 모델의 의도, primary+support+receipt+gate 구조의 가치, exploration vs operating 구분, Language Rule의 효과. 

중간 확신: 구체적인 family description의 장황함 정도와 실제 실행 중 router 선택 패턴 (yaml은 상세하지만 실시간 receipt 예시는 없음). 

한계: 실제 파일 시스템의 최신 상태, skill_receipt_schema.yaml 전체 정확한 스키마, 최근 run들의 실제 receipt/gate coverage 예시, 사용자의 과거 대화 이력에 기반한 세밀한 "맞춤" 패턴은 확인하지 못함. 추천은 snapshot에 드러난 원칙과 observed behavior에 기반한 최소 변화 제안이며, 실행 전 사용자 확인이 필요하다. 이 보고서는 컨설팅 제안일 뿐, 어떤 파일도 수정하지 않았다.

이 방향으로 가면 Codex는 더 날카롭고, 사용자에게 더 자연스럽게 느껴지는 연구 co-pilot이 될 수 있다. 추가 질문이 있으면 snapshot + 좁은 질문 형태로 다시 요청하세요.
