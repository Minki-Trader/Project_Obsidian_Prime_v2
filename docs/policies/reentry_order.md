# Re-entry Order

This file is the single authoritative re-entry order and truth precedence note for `Project_Obsidian_Prime_v2`.

Do not maintain a second full ordered re-entry list in `README.md`, `AGENTS.md`, status notes, or repo-scoped skills. Those files may point here, but this file owns the full order and the precedence language.

## Bootstrap

- if you are entering the repo cold, open `AGENTS.md` first
- once `AGENTS.md` is loaded, follow the order below

## Canonical Read Order

1. `docs/workspace/workspace_state.yaml`
2. `docs/context/current_working_state.md`
3. the latest durable handoff or stage-transition decision in `docs/decisions/*.md`
4. the active stage `04_selected/selection_status.md`
5. the active stage `03_reviews/review_index.md`
6. the active stage `00_spec/stage_brief.md`
7. the active stage `01_inputs/input_refs.md`
8. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
9. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
10. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
11. `docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
12. `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
13. `docs/policies/agent_trigger_policy.md` when the task will use repo-scoped skills
14. `docs/policies/artifact_registry_schema.md` when the task will create, update, or review durable artifact identity
15. `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the task touches feature/model/pipeline/artifact architecture, alpha-search framing, repo-scoped skills, agent settings, or Korean encoding
16. `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md` when the task touches exploration, idea variants, Tier B/C research, WFO, negative-result closure, legacy lessons, or extra stages
17. `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`, and `docs/registers/run_registry.csv` when the task touches run creation, KPI reporting, run review, result judgment, or run closeout
18. `docs/registers/legacy_lesson_register.md` when legacy lessons are used

## Truth Precedence

When repo documents disagree, resolve in this order:

1. `docs/workspace/workspace_state.yaml`
2. the active stage `04_selected/selection_status.md`
3. the latest durable decision memo in `docs/decisions/*.md`
4. `docs/context/current_working_state.md`
5. `AGENTS.md`
6. this file
7. `docs/policies/agent_trigger_policy.md`
8. `docs/policies/architecture_invariants.md` for architecture ownership and encoding guardrails
9. `docs/policies/exploration_mandate.md` for exploration discipline and lane separation
10. `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, and `docs/policies/result_judgment_policy.md` for run evidence measurement, management, and judgment
11. stage briefs, review indexes, templates, and other supporting notes

If `workspace_state.yaml` and the active stage `selection_status.md` imply different active stages, treat that as state fragmentation and resolve it before continuing.

## Truth Vocabulary

- `foundation truth`: the current authoritative state of the reboot while Stages `00` to `05` are still open; it is anchored in `workspace_state.yaml`, the active stage `selection_status.md`, and durable decision memos
- `operating truth`: claims that are safe for a promoted v2 operating line; this requires the relevant foundation gates to be closed with materialized dataset evidence, evaluated parity evidence, artifact identity closure, and an explicit operating promotion
- `planning scaffold`: a named or registered planning artifact with structure and intent but without the full materialized backing values
- `materialized evidence`: an artifact whose row counts, source identities, hashes, snapshots, or evaluated results are backed by real outputs rather than placeholders or planning tokens
- `prior evidence only`: legacy findings or archived notes that may guide design but do not define current v2 foundation truth or current v2 operating truth
- `architecture debt`: a known structure problem recorded in `docs/registers/architecture_debt_register.md`; it is bounded debt, not a normal pattern to copy
- `materialized model`: a model with a reproducible artifact or frozen parameter/spec bundle, not only a probability table or review summary
- `exploration mandate`: the inherited spirit of pushing ideas to meaningful evidence boundaries without inheriting legacy code, run results, or promotion history
- `promotion-ineligible`: not eligible for operating promotion; this does not by itself mean the idea is dead
- `promotion_candidate`: a bounded candidate read that does not replace or confirm the operating line
- `operating_promotion`: an incumbent replacement or confirmation claim that requires hard-gate evidence
- `runtime_probe`: runtime observation without runtime parity closure or live-like authority
- `runtime_authority`: runtime parity closure, bundle handoff authority, or live-like readiness claim
- `tier_c_local_research`: local-only research on valid base/session rows with missing external context; it is not a runtime lane
- `run evidence`: the combined measurement, managed identity, and lane-aware judgment required before a run can be treated as reviewed or closed
- `negative result`: a valid result that weakens or closes a hypothesis while preserving reusable evidence
- `invalid result`: a result that should not be interpreted because a contract, data, parity, or execution assumption failed

## Re-entry Output Expectation

After following this order, restate all of the following before making durable changes:

- active stage
- current foundation truth
- current operating-truth boundary
- what is still planning only
- what is already materialized
- what remains open
- whether architecture-sensitive work needs the architecture guard
- the primary lane and whether exploration-sensitive work needs lane classification or exploration-mandate handling
- whether promotion/runtime language is candidate/probe evidence or an operating-truth claim
- whether run/KPI/result work needs the run evidence system

## Maintenance Rule

- update this file when the canonical re-entry order or truth precedence changes
- do not update other documents with a second full ordered list; point back here instead
