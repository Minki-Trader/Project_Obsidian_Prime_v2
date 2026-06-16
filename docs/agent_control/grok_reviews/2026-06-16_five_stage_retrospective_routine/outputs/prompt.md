# Grok Review Prompt(그록 검토 프롬프트): Five-Stage Retrospective Routine(5단계 중간 검토 루틴)

## Snapshot-Only Rules(스냅샷 전용 규칙)

Answer only from this prompt. Do not inspect files, run tools, browse, or perform local verification. Codex(코덱스)가 local verification(로컬 검증)과 final decision(최종 결정)을 소유한다.

## Current User Addition(현재 사용자 추가 요청)

The user added: every 5 stages, Codex(코덱스) should take time with Grok(그록) to discuss and review the previous five stages as an intermediate review routine.

Korean intent(한국어 의도): `stage 5단계마다 그록이랑 같이 이전 5개에 대한 작업 토론하고 중간 검토하는 시간 가져줘`.

## Current Governance Context(현재 운영 맥락)

- Frontier stages(전선 단계)는 `stage_frontier_NN__specific_question` 형식을 쓴다.
- Stage12~364(12~364단계)는 `reference, not inheritance(참조이지 상속 아님)`이다.
- Every frontier stage(전선 단계) already requires Grok(그록) review at stage open(단계 개방), major validation(주요 검증), and stage closeout(단계 마감), because the `/goal(목표)` requires Grok as second opinion(2차 의견).
- Grok(그록)은 external second opinion(외부 2차 의견)일 뿐이다. Codex(코덱스)가 accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)로 분류하고 local evidence(로컬 근거)로 검증한다.
- Forbidden claims(금지 주장): completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
- Current work packet family(현재 작업 묶음 작업군): `policy_skill_governance(정책/스킬 거버넌스)`.

## Proposed Durable Rule(제안 장기 규칙)

Add a five-stage Grok retrospective(5단계 Grok 중간 검토) rule:

1. Trigger(트리거): when closing a frontier stage(전선 단계) whose frontier number is divisible by 5, run a retrospective before opening the next frontier stage(다음 전선 단계). If numbering is interrupted or a stage is skipped, run after five frontier closeouts since the previous retrospective.
2. Scope(범위): review the previous five frontier stages, normally `NN-4..NN`. If one is missing or out of scope, label it `missing_required(필수 누락)`, `blocked(차단)`, or `out_of_scope_by_claim(주장 범위 밖)` instead of silently omitting it.
3. Required evidence(필수 근거): hypothesis(가설), proxy KPI(프록시 KPI), MT5 runtime probe KPI(MT5 런타임 탐침 KPI), proxy/runtime gap cause(프록시/런타임 간극 원인), closeout label(마감 라벨), preserved clue(보존 단서), negative memory(부정 기억), repeated systemic issue(반복 시스템성 문제), and next action(다음 행동).
4. Required output(필수 출력): Grok receipt(그록 영수증), Codex local verification(코덱스 로컬 검증), accepted/rejected/needs_local_verification classification(조언 분류), and a compact retrospective report(압축 중간 검토 보고).
5. Claim boundary(주장 경계): this retrospective can change next-stage direction(다음 단계 방향) or repair priority(수리 우선순위), but it cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Focus Question(집중 질문)

Critique this proposed rule. Is the trigger clear enough? What field or guard is missing to make it durable across frontier stages? Keep the answer concrete and limited to policy/skill governance(정책/스킬 거버넌스).
