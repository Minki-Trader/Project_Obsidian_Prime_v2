---
name: obsidian-work-packet-router
description: Route each Project Obsidian Prime v2 request as a multi-phase work packet across design, code, experiment, verification, evidence, judgment, report, and publish phases; use project-wide and never bind routing to one stage.
---

# Obsidian Work Packet Router

Use this skill after session intake and before planning or implementation.

Most Obsidian requests are not one mode. A normal request may start with an idea, write code, run an experiment, record evidence, judge results, and explain the outcome to the user. Route the whole lifecycle before acting.

## Must Read

- `docs/policies/agent_trigger_policy.md`
- `docs/policies/branch_policy.md`
- `docs/policies/reentry_order.md` when current truth is uncertain
- `AGENTS.md`
- The SKILL.md files for any selected skills

## Required Output

- Always emit(항상 남김) `routing_receipt(라우팅 기록)`: lifecycle(생명주기), selected skill bundles(선택된 스킬 묶음), omitted high-relevance skills(관련성이 높은데 빠진 스킬), one-line reasons(한 줄 이유)를 담은 compact record(압축 기록).
- `work_packet_lifecycle`: one of `information_only`, `design_only`, `code_to_verify_to_report`, `experiment_to_evidence_to_report`, `code_to_experiment_to_evidence_to_report`, `policy_skill_governance`, `publish_or_handoff`, or a short custom lifecycle(짧은 사용자 정의 생명주기)
- `phase_plan`: ordered phases(순서 있는 단계) for the current packet(현재 작업 묶음); low-risk `information_only`(낮은 위험 정보 작업)는 compact(압축), code/experiment/MT5/policy/publish/ambiguous work(코드/실험/MT5/정책/발행/애매한 작업)는 expanded(확장)
- `skills_considered`: compact packets(압축 작업 묶음)는 bundle level(묶음 단위), high-risk packets(고위험 작업 묶음)는 individual skill level(개별 스킬 단위)로 고려한 repo-scoped skills(저장소 전용 스킬)
- `skills_selected`: each phase(각 단계)에 붙인 skills(스킬)
- `skills_not_used`: attached(선택)하지 않은 high-relevance skills(고관련 스킬)와 one-line reasons(한 줄 이유); trigger policy(작동 조건 정책)가 자연스럽게 요구하는 skill(스킬)을 조용히 버리지 않는다
- `branch_worktree_fit`: whether the current branch/worktree matches the requested packet
- `branch_action`: stay, switch, create_new_branch, create_or_select_worktree, or stop_for_user
- `phase_stop_conditions`: where to stop or downgrade claims
- `final_answer_filter`: normally `obsidian-answer-clarity` plus `obsidian-claim-discipline`
- `handoff_surface`: files, registers, PR, artifact, or user action touched by the packet

## Default Phase Library

- reentry and current truth: `obsidian-reentry-read`
- lifecycle routing: `obsidian-session-intake`, then this skill
- branch/worktree fit: `docs/policies/branch_policy.md`
- architecture or policy: `obsidian-architecture-guard`
- code placement: `obsidian-code-surface-guard`
- implementation quality: `obsidian-code-quality`
- external correctness: `obsidian-reference-scout`
- experiment design: `obsidian-experiment-design`
- data and time integrity: `obsidian-data-integrity`
- model or threshold validation: `obsidian-model-validation`
- MT5 or live-like parity: `obsidian-runtime-parity`
- tester evidence: `obsidian-backtest-forensics`
- run evidence and registers: `obsidian-run-evidence-system`
- artifact lineage: `obsidian-artifact-lineage`
- environment reproducibility: `obsidian-environment-reproducibility`
- KPI explanation: `obsidian-performance-attribution`
- result boundary: `obsidian-result-judgment`, then `obsidian-claim-discipline`
- final user report: `obsidian-answer-clarity`

## Do Not

- Treat code, experiment, evidence, and report as mutually exclusive.
- Stop at code generation when the user asked for work that naturally requires verification or reporting.
- Work in a branch or worktree that belongs to a different stage, PR, experiment, or policy scope.
- Mix two open PR scopes in one worktree unless the user explicitly asks for that combined patch.
- Create stage-specific routing skills when a project-wide lifecycle responsibility fits.
- Skip answer clarity because a result is technically correct.
- Skip reference scouting silently; record why it was not required.
- Replace(대체) the compact routing receipt(압축 라우팅 기록)를 unrecorded private decision(기록 없는 내부 판단)으로 바꾸지 않는다; receipt(기록)는 abandoned skills(유기되는 스킬)을 막는 guard(가드)다.
