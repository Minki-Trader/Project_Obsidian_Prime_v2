# Artifact Policy

- heavy datasets, model binaries, runtime logs, and tester outputs may live outside Git
- dataset, bundle, runtime, and report identity must live inside Git-tracked docs
- record durable artifact identity in `docs/registers/artifact_registry.csv`
- use explicit ids such as `dataset_id`, `bundle_id`, and `runtime_id`
- add a freeze card or equivalent note when an artifact becomes a durable input to later work
- keep stage-specific one-off outputs under `stages/<nn_name>/02_runs/`
- promote only stable reusable outputs into `data/processed/`
- do not let `data/processed/` become a dump of one-off experiment clutter

## Artifact Registry Serialization

- keep simple scalar columns as plain scalars or empty strings; do not use prose in scalar fields
- use repo-relative forward-slash paths in `path_or_ref` when the artifact is tracked inside this workspace
- if a single registry field must carry multiple keyed values, serialize it as `key=value|key=value` with no spaces
- sort composite keys alphabetically so repeated writes stay stable
- `required_contract_versions` must use `role=repo/path@YYYY-MM-DD`
- `required_artifact_hashes` must use `role=sha256:<hex>` when the hash is known
- if a required value is not materialized yet, use an explicit pending token instead of ad hoc prose
- allowed pending tokens are `pending_first_materialized_export`, `pending_first_fixture_inventory`, and `not_applicable`
- explanations, caveats, and planning notes belong in `notes`, not inside serialized composite fields
