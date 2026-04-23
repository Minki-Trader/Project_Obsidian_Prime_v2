# Project Obsidian Prime v2

## Scope

This workspace is the clean-restart FPMarkets `US100` `M5` data, feature, runtime, and stage pipeline for Project Obsidian Prime.

## Core Principles

- contract-first
- closed-bar only
- exact timestamp alignment
- contract fidelity over platform built-in convenience
- Python-led orchestration, MT5 as execution and verification engine
- one regular operating alpha line at a time
- diagnostic evidence is not the same thing as operating promotion
- legacy is a lesson source, not an automatic truth source
- concept contract is inherited, promotion history is not
- legacy exploration mandate is inherited, legacy code/result/promotion history is not
- foundation closure comes before new alpha search
- operating discipline and exploration discipline must stay separate

## Codex Response Rule

- when using English expressions, pair them with Korean notation in the same local context
- avoid unexplained abbreviations; expand terms such as WFO (`walk-forward optimization`, 워크포워드 최적화) and OOS (`out-of-sample`, 표본외) before relying on them
- when describing an action, also describe the effect of that action so users do not have to infer the meaning from context

## Contract Hierarchy

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- auxiliary frozen mirror: `docs/contracts/feature-list_fpmarkets_v2.txt`

Implementation notes, review files, selection files, and the auxiliary frozen mirror do not override the three constitutional contracts.

## Working Vocabulary

- use `foundation gate`, `parity closure`, `artifact identity closure`, and `promotion gate`
- avoid `release gate` and `release closure`

## Directory Rules

- keep the root limited to `docs`, `data`, `foundation`, and `stages`, with repo-scoped `.agents/skills/` allowed as a narrow exception for reusable agent triggers
- keep source-of-truth contracts in `docs/contracts`
- keep current state in `docs/workspace`
- keep policies in `docs/policies`
- keep durable decisions in `docs/decisions` and `docs/adr`
- keep registries in `docs/registers`
- keep reusable code in `foundation`
- keep shared datasets in `data/processed`
- keep stage-local outputs under `stages/<nn_name>/`
- do not create a top-level dump folder for scratch artifacts

## Data And Time Semantics

- use `US100` `M5` as the base frame
- compute external-symbol features on each symbol's own raw `M5` series, then merge onto the `US100` frame by bar-close timestamp
- use `GOOGL.xnas` as the contract Google symbol unless explicitly changed
- treat `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` as a placeholder until real monthly weights are supplied
- default shared working window: `2022-08-01` through `2026-04-13` inclusive, pending the first v2 dataset freeze
- default practical modeling start: `2022-09-01`
- no partial current-bar values are allowed in model inputs

## Runtime Fidelity Rule

- model-input feature parity is a first-class gate
- helper/runtime parity is a separate gate from model-input parity
- bundle handoff verification is a separate gate from full parity closure
- if built-in MT5 helpers disagree with the contract surface, the contract wins
- all required inputs missing means `all-or-skip`, not degrade-with-warning

## Architecture Invariants (`구조 불변 규칙`)

- `docs/policies/architecture_invariants.md` owns cross-stage architecture guardrails (`단계 공통 구조 가드레일`)
- `foundation/features` owns reusable feature logic (`재사용 피처 로직`); `foundation/pipelines` may orchestrate (`조율`) but must not become the feature source of truth (`피처 진실 원천`)
- a model is not `materialized` (`물질화됨`) unless a reproducible model artifact (`재현 가능한 모델 산출물`) or frozen parameter/spec bundle (`동결 파라미터/규격 번들`) exists under a tracked stage run path or registered artifact path
- alpha search (`알파 탐색`) must not silently become only source cleanup (`소스 정리`) or validation debt closure (`검증 부채 정리`) without an explicit durable decision
- known architecture debt (`구조 부채`) belongs in `docs/registers/architecture_debt_register.md`; registered debt is not a healthy pattern to copy

## Exploration Mandate (`탐색 명령`)

- `docs/policies/exploration_mandate.md` owns the stage-agnostic exploration rules (`단계 독립 탐색 규칙`)
- every non-trivial task must name a primary lane (`주 레인`): `exploration` (`탐색`), `evidence` (`근거`), `promotion` (`승격`), `runtime` (`런타임`), or `extra` (`추가`)
- promotion-ineligible (`승격 부적격`) does not mean idea-dead (`아이디어 사망`)
- alpha search (`알파 탐색`) should push serious ideas through broad sweep (`광역 탐색`), extreme sweep (`극단값 탐색`), WFO (`walk-forward optimization`, 워크포워드 최적화), stress/readout (`스트레스/판독`), and negative-result memory (`부정 결과 기록`) when relevant
- micro search (`미세 탐색`) is allowed only after broad evidence identifies a robust region (`견고한 구간`)
- Tier A/B/C (`티어 A/B/C`) remains the default readiness vocabulary (`준비도 어휘`), but Tier C (`티어 C`) may support local-only research (`로컬 전용 연구`) only when base/session semantics are valid and external context is the missing part
- user-requested extra stages (`사용자 요청 추가 단계`) are allowed, but they must declare charter (`헌장`), lane (`레인`), exit condition (`종료 조건`), and no-promotion boundary (`비승격 경계`)

## Verification Discipline (`검증 규율`)

- use the narrowest sufficient verification first, but include a real-environment check (`실환경 검증`) before calling work verified when the change touches MT5 execution, tester orchestration, import/export boundaries, runtime parity flow, or another path where mocks can miss environment-specific behavior
- prefer the active stage pack and the native MT5 runner as the real-environment check when that is the closest contract-surface verification
- docs-only, wording-only, registry-only, or isolated pure-Python changes may stop at local tests when they do not change an environment-dependent path
- if a real-environment check is not needed or is not feasible, say so explicitly and name the blocker or rationale instead of implying end-to-end verification

## Tester Defaults

- symbol: `US100`
- timeframe: `M5`
- tester model: `Every tick based on real ticks`
- deposit: `500 USD`
- leverage: `1:100`
- signal timing: new closed `M5` bar only

## Stage Governance

- start v2 with `00_foundation_sprint` before any new alpha search
- keep the foundation closure path explicit before opening range exploration:
  - `00_foundation_sprint`
  - `01_dataset_contract_freeze`
  - `02_feature_dataset_closure`
  - `03_runtime_parity_closure`
  - `04_artifact_identity_closure`
  - `05_exploration_kernel_freeze`
- every new stage needs a clear brief or charter before branching into runs
- diagnostic stages can close questions but cannot promote the operating line by themselves
- if execution semantics change, keep `structural_scout` and `regular_risk_execution` separate
- new telemetry cannot become a promotion gate until the incumbent/reference family is backfilled
- treat legacy winners, challengers, and operating defaults as archived evidence, not automatic v2 starting points
- do not open a new alpha or range stage until the foundation closure path is explicitly closed

## Document Placement

- `docs/workspace/workspace_state.yaml` is the current state source
- `stages/*/04_selected/selection_status.md` is the active stage read
- `stages/*/03_reviews/review_index.md` is the active stage reading map
- `docs/decisions/*.md` records durable operating decisions
- `docs/policies/reentry_order.md` defines the canonical re-entry order and truth precedence
- `docs/registers/artifact_registry.csv` records dataset, bundle, runtime, and report identity
- `docs/registers/idea_registry.md` records durable exploration ideas
- `docs/registers/negative_result_register.md` records reusable failed or closed hypotheses
- `docs/registers/legacy_lesson_register.md` records abstract legacy lessons without importing legacy code or run results
- `docs/policies/artifact_registry_schema.md` defines registry columns, enums, and hash-update discipline
- `docs/policies/architecture_invariants.md` defines stage-agnostic structure and encoding guardrails
- `docs/policies/exploration_mandate.md` defines exploration discipline, lane separation, WFO defaults, and failure-memory rules
- `docs/archive/` stores sealed legacy lessons and background notes, not current operating truth
- `docs/policies/agent_trigger_policy.md` records repo-scoped trigger-to-skill routing
- `.agents/skills/` stores repo-scoped reusable Codex skills for re-entry, claim discipline, and stage-transition workflows
- heavy local artifacts may stay outside Git, but their identity must stay in Git-tracked docs

## Re-entry Rule

- the single authoritative re-entry order and truth precedence live in `docs/policies/reentry_order.md`
- `README.md`, status notes, and repo-scoped skills may point to that policy but must not maintain a second full ordered list
- if project documents disagree, use the precedence defined in `docs/policies/reentry_order.md`

## Change Discipline

- update `AGENTS.md` only when project-wide rules change
- update `docs/policies/reentry_order.md` when the canonical re-entry order or truth precedence changes
- update `docs/workspace/workspace_state.yaml` when current truth changes
- update `docs/decisions` when a durable operating decision is taken
- update registers when new durable artifact identity appears
- update `docs/policies/artifact_registry_schema.md` when registry columns, enums, or hash-update rules change
- update `docs/policies/architecture_invariants.md` only when cross-stage architecture guardrails change
- update `docs/policies/exploration_mandate.md` only when cross-stage exploration discipline changes
- update `docs/registers/architecture_debt_register.md` when known architecture debt is discovered, reduced, deepened, or retired
- update `docs/registers/idea_registry.md`, `docs/registers/negative_result_register.md`, or `docs/registers/legacy_lesson_register.md` when durable idea, failure, or legacy-lesson memory changes
- keep Korean `.md` and `.txt` documents in `UTF-8 with BOM` when editing them for Windows-facing workflows
