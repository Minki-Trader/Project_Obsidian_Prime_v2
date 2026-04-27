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

- `work_packet_lifecycle`: one of `information_only`, `design_only`, `code_to_verify_to_report`, `experiment_to_evidence_to_report`, `code_to_experiment_to_evidence_to_report`, `policy_skill_governance`, `publish_or_handoff`, or a short custom lifecycle
- `phase_plan`: ordered phases for the current packet
- `skills_considered`: all repo-scoped skills considered at shallow level
- `skills_selected`: skills attached to each phase
- `skills_not_used`: skills not attached with one-line reasons
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
