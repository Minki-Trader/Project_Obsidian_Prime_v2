# Artifact Policy

- heavy datasets, model binaries, runtime logs, and tester outputs may live outside Git
- dataset, bundle, runtime, and report identity must live inside Git-tracked docs
- record durable artifact identity in `docs/registers/artifact_registry.csv`
- use explicit ids such as `dataset_id`, `bundle_id`, and `runtime_id`
- add a freeze card or equivalent note when an artifact becomes a durable input to later work
- keep stage-specific one-off outputs under `stages/<nn_name>/02_runs/`
- promote only stable reusable outputs into `data/processed/`
- do not let `data/processed/` become a dump of one-off experiment clutter
