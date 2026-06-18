---
name: obsidian-task-force-review
description: Route Project Obsidian Prime v2 work through the permanent Codex Task Force roster. Use when replacing Grok-dependent review, changing AGENTS.md, repo skills, policy, work-family routing, receipt schemas, agent settings, five-stage retrospective behavior, or running Frontier80 open-to-closeout governance rehearsal.
---

# Obsidian Task Force Review

## Overview

Use this skill to run project-native Codex Task Force review(코덱스 태스크포스 검토) without treating Grok(그록) as inherited authority.

The skill adds a bounded internal review layer(제한 내부 검토층). It does not replace MT5 evidence(MT5 근거), runtime probes(런타임 탐침), gate coverage(게이트 커버리지), or claim discipline(주장 규율).

## Required Inputs

- Current truth(현재 진실): `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`, active selection status(활성 선택 상태).
- Roster registry(명단 등록부): `docs/agent_control/codex_task_force_registry.yaml`.
- Work family routing(작업군 라우팅): `docs/agent_control/work_family_registry.yaml`.
- Active goal(`/goal`, 활성 목표), work packet(작업 묶음), router-selected required overlay(라우터 선택 필수 오버레이), or explicit user instruction requiring review(검토를 요구하는 명시 사용자 지시) with claim boundary(주장 경계).

## Workflow

1. Confirm the request is project-native Task Force work, not Grok role succession(그록 역할 승계).
2. Treat Grok call/review(그록 호출/검토), external review(외부 리뷰), second opinion(2차 의견), no-solo-Codex judgment(코덱스 단독 판단 금지), stage-close adversarial review(단계 마감 비판 검토), and agent/skill consulting(요원/스킬 상담) as Task Force triggers, not Grok triggers.
3. Select the minimum necessary agents(요원) from the registry. Use all 8 only for architecture, policy, runtime, or stage-close work that materially needs them.
   - The governance/evidence balance rule(운영/근거 균형 규칙) alone is not a Task Force trigger(태스크포스 트리거). It only changes review routing when the current packet already requires Task Force review(태스크포스 검토).
4. Immediately call the selected agents(선택 요원) with real `spawn_agent(서브에이전트 생성 호출)` before making any Task Force reviewed/reviewed/verified/pass(태스크포스 검토됨/검토됨/검증됨/통과) claim.
   - If Task Force review(태스크포스 검토) is required by active goal(`/goal`, 활성 목표), packet(묶음), required gate(필수 게이트), family rule(작업군 규칙), router-selected required Task Force overlay(라우터 선택 필수 태스크포스 오버레이), explicit user instruction requiring review(검토를 요구하는 명시 사용자 지시), or closeout claim(마감 주장), unavailable or uncalled selected-agent `spawn_agent(선택 요원 서브에이전트 생성 호출)` sets status to `blocked_for_task_force_review(태스크포스 검토 차단)`.
   - Required Task Force review(필수 태스크포스 검토) cannot pass as `not_applicable_with_reason(사유 있는 해당 없음)` and cannot support reviewed/verified/pass/stage closeout pass/internally_reviewed/rehearsed_control_plane(검토됨/검증됨/통과/단계 마감 통과/내부 검토됨/제어면 리허설됨).
   - If Task Force review(태스크포스 검토) is optional, Codex(코덱스) may proceed only without any Task Force review claim(태스크포스 검토 주장).
   - The receipt(영수증) must record each actual call(실제 호출) with `roster_agent_id(명단 요원 ID)`, `spawned_agent_id(생성 요원 ID)`, `tool_name=multi_agent_v1.spawn_agent(도구 이름)`, `result_status(결과 상태)`, and `opinion_classification(의견 분류)`.
5. Do not use dormant/stale agents(대기 중이거나 낡은 맥락의 요원) as review evidence without sending an explicit current context update(현재 맥락 갱신).
6. Apply the model policy(모델 정책): current floor `gpt-5.5 xhigh(5.5 매우 높음)`, future default `highest_available_xhigh(사용 가능 최상위 매우 높음)` unless the user pins a model.
7. Record bounded evidence(제한 근거). Prefer index-first/receipt-first(색인 우선/영수증 우선) reads before raw artifact expansion.
8. Limit adversarial review(비판 검토) to two passes: critique(비판) and owner response plus local verification(소유자 응답 + 로컬 검증). Start a third pass only when new evidence appears.
9. Classify each agent output as `accepted`, `rejected`, or `needs_local_verification(로컬 검증 필요)`.
10. Keep final authority with Codex(코덱스) local verification and project evidence, not the agent discussion itself.

## Roster

Use the registry IDs, not ad hoc names:

1. `agent_01_system_governor(시스템 총괄)`
2. `agent_02_platform_routing_architect(플랫폼/라우팅 설계자)`
3. `agent_03_philosophy_policy_skill_governance(철학/정책/스킬 거버넌스 책임자)`
4. `agent_04_evidence_control_plane(근거/제어면 책임자)`
5. `agent_05_data_feature_contract(데이터/피처 계약 책임자)`
6. `agent_06_quant_research(정량 연구 책임자)`
7. `agent_07_model_validation_risk(모델 검증/위험 책임자)`
8. `agent_08_mt5_onnx_runtime(메타트레이더5/온엑스 런타임 책임자)`

## Claim Boundary

Task Force review(태스크포스 검토) can produce `internally_reviewed(내부 검토됨)` or `rehearsed_control_plane(제어면 리허설됨)` only when the matching evidence exists.

Matching evidence(일치 근거) requires actual selected-agent `spawn_agent(서브에이전트 생성 호출)` calls in the conversation before the claim. Self-review(자기검토), planned review(예정 검토), or stale agent output(낡은 요원 출력) is not Task Force review(태스크포스 검토).

`tool_unavailable/not_called(도구 사용 불가/호출 안 됨)` is block evidence(차단 근거), not review evidence(검토 근거), whenever Task Force review(태스크포스 검토) is required.

It cannot produce completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), or parity-only economics(동등성 단독 경제성).

## Frontier80 Rule

For Frontier80(전선80), do not reopen F79/F79A(전선79/79A). Treat F79 as closed negative memory(부정 기억) and preserved clue(보존 단서).

Frontier80(전선80) must rotate feature set, label, model family, trade shape, risk logic, and regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할). The closeout boundary is runtime probe quality closeout(런타임 탐침 품질 마감), not runtime authority(런타임 권위).

## Do Not

- Do not call internal agents an external second opinion(외부 2차 의견).
- Do not label self-review(자기검토) as Task Force review(태스크포스 검토).
- Do not defer selected agent calls until closeout(마감) after already relying on a Task Force review(태스크포스 검토) claim.
- Do not treat `tool_unavailable/not_called(도구 사용 불가/호출 안 됨)` or `not_applicable_with_reason(사유 있는 해당 없음)` as a passing state for required Task Force review(필수 태스크포스 검토).
- Do not spawn all 8 agents(8명 전원) by default.
- Do not let agent consensus replace MT5 output(MT5 출력), ledger rows(장부 행), hashes(해시), or local filesystem verification(로컬 파일시스템 검증).
- Do not hand current review, critique, stage closeout, external review, or explicit Grok wording back to Grok(그록).
- Do not trigger active five-stage Grok retrospective(활성 5단계 그록 회고) during the Task Force migration path. Preserve historical records(역사 기록) instead.
- Do not use cheap local check(싼 로컬 점검) as a final conclusion. It is preflight(사전 점검) only.
