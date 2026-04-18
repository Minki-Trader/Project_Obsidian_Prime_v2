# Artifact Registry Schema

This file defines the column meaning, enum discipline, and hash-update procedure for `docs/registers/artifact_registry.csv`.

Use `docs/policies/artifact_policy.md` for serialization syntax. Use this file for schema meaning and allowed state values.

## Purpose

- keep `artifact_registry.csv` machine-readable
- prevent ad hoc status labels and approval labels
- make hash updates explicit whenever tracked artifacts change

## Column Meaning

- `artifact_id`: stable logical id for one durable artifact record
- `artifact_role`: the artifact's role, such as `dataset_freeze_card`, `gold_fixture_inventory`, or `runtime_parity_report`
- `dataset_id`: dataset identity when the artifact belongs to a dataset
- `fixture_set_id`: fixture identity when the artifact belongs to a parity fixture set
- `bundle_id`: bundle identity when the artifact belongs to a model or runtime bundle
- `runtime_id`: runtime snapshot or execution identity
- `report_id`: report identity when the artifact is a review or parity report
- `feature_order_hash`: contract-order feature fingerprint when relevant
- `path_or_ref`: repo-relative path or stable external reference for the backing artifact
- `produced_by_stage`: stage that created or materially updated the artifact
- `required_contract_versions`: composite field of contract-version dependencies
- `required_artifact_hashes`: composite field of dependent artifact hashes
- `sha256`: direct hash of the artifact recorded in this row
- `status`: lifecycle state from the allowed status enum
- `approved_for`: gate or use-case approval from the allowed approval enum
- `created_on`: date the row was first created
- `notes`: human-readable caveats, exceptions, or planning qualifiers

## Allowed Status Enum

- `draft`: the row exists, but one or more required values or dependent artifacts remain planning-only or pending
- `materialized`: the backing artifact exists and the row points to a real artifact path or reference with a real hash
- `evaluated`: the artifact has been materially reviewed or used to close a gate beyond mere existence
- `superseded`: the artifact remains in the ledger but has been replaced by a later durable artifact
- `archived`: the artifact remains for historical traceability and is no longer an active dependency

Do not invent new status labels inside the CSV. If a new lifecycle state is genuinely needed, update this policy in the same pass.

## Allowed Approval Enum

- `planning_freeze`
- `planning_fixture_inventory`
- `planning_parity_scaffold`
- `dataset_contract_closure`
- `feature_dataset_closure`
- `runtime_parity_closure`
- `artifact_identity_closure`
- `operating_reference`
- `archive_note`
- `not_applicable`

Do not use free-form approval text in the CSV.

## Role Discipline

- prefer existing roles when they already fit the artifact meaning
- if a new `artifact_role` is needed, add it intentionally and explain it in the same pass through `notes` or a policy/decision update
- do not overload one role so far that downstream readers cannot infer the artifact type

## Hash Update Procedure

1. create a row as soon as a durable artifact identity appears, even if the artifact is still `draft`
2. when the tracked artifact file changes but the logical artifact remains the same:
   - update `sha256`
   - update `required_artifact_hashes` in dependent rows
   - update `status`, `approved_for`, and `notes` if the lifecycle meaning changed
3. when the artifact meaning changes enough that it becomes a new durable artifact, create a new `artifact_id` and mark the old row `superseded`
4. when a row moves from planning-only to real backing evidence, promote `status` from `draft` to `materialized` in the same pass that writes the real hash
5. if an artifact has been evaluated to close a gate, promote `status` to `evaluated` and set `approved_for` to the corresponding closure gate

## Validation Checklist

- `status` uses an allowed enum value
- `approved_for` uses an allowed enum value
- `path_or_ref` is a repo-relative forward-slash path or a stable external reference
- composite fields follow the serialization rules in `docs/policies/artifact_policy.md`
- pending values use only the allowed pending tokens from `docs/policies/artifact_policy.md`
- `notes` carries prose; composite fields do not
