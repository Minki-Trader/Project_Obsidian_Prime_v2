# Control Plane Utilities

Shared control-plane helpers for experiment identity, register, and KPI flows.

Use this package for behavior that should stay the same across Stage 10+ alpha runs:

- ledger serialization and upsert mechanics
- MT5 KPI ledger row construction
- common alpha run register shapes

Run scripts should keep experiment-specific choices close to the run, and import shared KPI/ledger behavior from here instead of copying it between stages.

## Closeout gate

Use `foundation.control_plane.closeout_gate` before any user-facing `completed`, `reviewed`, or `verified` claim for non-trivial experiment packets.

The gate compares requested scope against actual artifacts, checks required skill receipts when supplied, audits KPI files and ledger rows when supplied, then blocks final claims that are not supported by evidence.

Blocked closeouts exit non-zero. Use `--allow-blocked-exit-zero` only for diagnostics.

Stage 12 scope-shrink regression example:

```powershell
python -m foundation.control_plane.closeout_gate `
  --packet-id stage12_run03d_run03e_scope_audit `
  --requested-claim completed `
  --requested-claim mt5_verification_complete `
  --scope-csv-rows python_structural_results 20 stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03D_et_standalone_batch20_v1/results/variant_results.csv "Python structural results" `
  --scope-file-count mt5_validation_reports 20 "stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03E_et_batch20_top_v11_mt5_probe_v1/mt5/reports/*validation*.htm" "MT5 validation reports" `
  --scope-file-count mt5_oos_reports 20 "stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03E_et_batch20_top_v11_mt5_probe_v1/mt5/reports/*oos*.htm" "MT5 OOS reports"
```

That packet must report partial or blocked until the MT5 report counts match the requested scope or an explicit user quote authorizes reduced scope.

## Preflight clarification

Use `foundation.control_plane.preflight_clarifier` before launching ambiguous batch work. It turns prompts such as "run about 20 hypotheses through verification" into explicit user choices before any run starts.

The clarifier blocks execution until the user picks a scope when it detects:

- approximate batch counts
- ambiguous execution layer
- ambiguous verification layer
- unattended batch work
- MT5-required context that was not explicitly confirmed

The generated choices are designed to prevent silent scope shrink:

- Python + MT5 full verification for every requested variant
- Python structural scout only, with MT5 claims forbidden
- Python full scout plus MT5 top-K only, recorded as explicit reduced scope

Use the selected option as the work packet acceptance criteria, then enforce it with the closeout gate.

## Agent-control contracts

Use `foundation.control_plane.agent_control_contracts` to check that the repo-level operating contracts are present before a large run replay or KPI rebuild.

The audit checks:

- work packet schema
- N/A reason registry
- claim vocabulary
- KPI source authority
- row grain contract
- work packet, run plan, closeout, and normalized KPI templates

The contracts live under `docs/agent_control/` and `docs/templates/`. They do not replace the existing run registry or alpha ledgers; they define the operating format that future packets must use.

## Experiment inventory packet

Use `foundation.control_plane.experiment_inventory` before rebuilding historical KPI rows.

The inventory packet reads the existing run registry and alpha ledgers, then materializes:

- `experiment_inventory.csv`
- `inventory_summary.json`
- `work_packet.yaml`
- `run_plan.yaml`
- `skill_receipts/*.yaml`

It does not rerun Python experiments, run MT5, or overwrite ledgers. Its default target policy is Stage 10 through the active stage `run01/run02/run03` sequence, excluding invalid scope-mismatch rows until the user explicitly confirms otherwise.

Example:

```powershell
python -m foundation.control_plane.experiment_inventory `
  --packet-id kpi_rebuild_inventory_v1
```

## Code-surface audit

Use `foundation.control_plane.code_surface_audit` before editing large pipeline files, MT5 EA files, `.mqh` modules, reusable logic, or run materializers.

The audit checks:

- large file line budgets against `docs/agent_control/code_surface_baseline.yaml`
- direct `foundation/control_plane` imports from stage pipelines
- the temporary MT5 runtime compatibility shim

Example:

```powershell
python -m foundation.control_plane.code_surface_audit --root .
```

The effect is that code placement and monolith growth are checked by a machine-readable gate, not only by memory or review notes.
