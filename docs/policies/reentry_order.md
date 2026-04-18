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

## Truth Precedence

When repo documents disagree, resolve in this order:

1. `docs/workspace/workspace_state.yaml`
2. the active stage `04_selected/selection_status.md`
3. the latest durable decision memo in `docs/decisions/*.md`
4. `docs/context/current_working_state.md`
5. `AGENTS.md`
6. this file
7. `docs/policies/agent_trigger_policy.md`
8. stage briefs, review indexes, templates, and other supporting notes

If `workspace_state.yaml` and the active stage `selection_status.md` imply different active stages, treat that as state fragmentation and resolve it before continuing.

## Truth Vocabulary

- `foundation truth`: the current authoritative state of the reboot while Stages `00` to `05` are still open; it is anchored in `workspace_state.yaml`, the active stage `selection_status.md`, and durable decision memos
- `operating truth`: claims that are safe for a promoted v2 operating line; this requires the relevant foundation gates to be closed with materialized dataset evidence, evaluated parity evidence, artifact identity closure, and an explicit operating promotion
- `planning scaffold`: a named or registered planning artifact with structure and intent but without the full materialized backing values
- `materialized evidence`: an artifact whose row counts, source identities, hashes, snapshots, or evaluated results are backed by real outputs rather than placeholders or planning tokens
- `prior evidence only`: legacy findings or archived notes that may guide design but do not define current v2 foundation truth or current v2 operating truth

## Re-entry Output Expectation

After following this order, restate all of the following before making durable changes:

- active stage
- current foundation truth
- current operating-truth boundary
- what is still planning only
- what is already materialized
- what remains open

## Maintenance Rule

- update this file when the canonical re-entry order or truth precedence changes
- do not update other documents with a second full ordered list; point back here instead
