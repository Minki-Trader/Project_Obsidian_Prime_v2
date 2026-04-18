# Parity

Put reusable Python to MT5 comparison helpers, fixtures, and shared parity assets here.

Keep stage-local parity investigations inside the relevant stage unless the artifact becomes a reusable shared tool or fixture.

Current reusable helpers:

- `materialize_fpmarkets_v2_runtime_minimum_pack.py`: bind the first Stage 03 minimum runtime parity pack and write the Python snapshot and MT5 request artifacts
- `compare_fpmarkets_v2_runtime_parity.py`: compare the materialized Python snapshot against an MT5 feature snapshot audit JSONL export and write a machine-readable parity summary
- `render_fpmarkets_v2_runtime_parity_report.py`: render a Stage 03 markdown parity report from the machine-readable comparison summary
- `render_fpmarkets_v2_mt5_snapshot_audit_set.py`: render a loadable MT5 `.set` helper for the Stage 03 snapshot audit inputs
- `import_fpmarkets_v2_mt5_snapshot_audit.py`: copy the MT5 snapshot audit JSONL from Common Files into the Stage 03 run folder before comparison
- `run_fpmarkets_v2_runtime_parity_after_mt5.py`: run the import, compare, and report-render sequence in one pass after the MT5 JSONL export exists
- `run_fpmarkets_v2_runtime_parity_native.py`: guard against an already-running `terminal64.exe`, launch the v2-native MT5 tester ini, wait for the Common Files JSONL, then hand off to the import/compare/render chain
