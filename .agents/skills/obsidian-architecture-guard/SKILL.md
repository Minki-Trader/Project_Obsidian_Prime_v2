---
name: obsidian-architecture-guard
description: Guard Project Obsidian Prime v2 against stage-agnostic architecture and code-surface drift. Use when work touches feature calculation, model training/export, pipeline materialization, artifact claims, architecture debt, code placement, stage transitions, alpha search, repo-scoped skills, agent settings, or Korean BOM/encoding-sensitive docs.
---

# Obsidian Architecture Guard

Use this skill when a task can change architecture meaning (구조 의미), not only when a specific stage number is involved.

## Trigger Surface

Use this guard for work touching any of:

- feature calculation (피처 계산)
- model training or export (모델 학습 또는 내보내기)
- pipeline materialization (파이프라인 물질화)
- artifact registry or artifact claims (산출물 등록부 또는 산출물 주장)
- code placement or reusable logic ownership (코드 배치 또는 재사용 로직 소유권)
- stage transition or alpha search (단계 전환 또는 알파 탐색)
- repo-scoped skills or agent settings (저장소 범위 스킬 또는 에이전트 설정)
- Korean `.md` or `.txt` docs (한국어 문서)

Do not key this guard to Stage 06 or Stage 07 only. It applies to all future stages.

## Must Read

- `docs/policies/architecture_invariants.md`
- `docs/registers/architecture_debt_register.md`
- `docs/policies/agent_trigger_policy.md` when routing or skills change
- `docs/policies/reentry_order.md` when re-entry behavior changes
- `docs/policies/exploration_mandate.md` when alpha-search framing or exploration discipline changes
- the touched skill or policy files

## Required Output

Every architecture-sensitive packet or summary must include:

- `architecture_risk`: whether the work can move ownership, source of truth, model identity, alpha-search meaning, or encoding state
- `debt_interaction`: whether it touches registered architecture debt
- `allowed_debt_change`: `reduce`, `leave_unchanged`, or `blocked_without_decision`
- `encoding_check`: whether Korean docs or repo-scoped skills need UTF-8 with BOM validation
- `code_surface_check`: whether owner module, caller, input/output, and artifact/report effect must be named

## Guardrails

- Do not treat existing architecture debt as normal style.
- Do not describe a model as `materialized` unless a model artifact or frozen parameter/spec bundle exists.
- Do not add reusable feature logic to a stage script or orchestration pipeline when it belongs in `foundation/features`.
- Do not create all-in-one EA or pipeline monoliths when reusable logic can live in a smaller owner module.
- Do not let alpha search become source cleanup only unless a durable decision says so.
- Do not edit Korean `.md` or `.txt` docs without preserving UTF-8 with BOM.

## Validator

Run `scripts/validate_agent_settings.py --repo-root .` after editing agent settings, repo-scoped skills, architecture policies, debt registers, or Korean docs.
