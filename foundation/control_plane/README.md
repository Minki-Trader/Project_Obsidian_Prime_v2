# Control Plane Utilities

Shared control-plane helpers for experiment identity, register, and KPI flows.

Use this package for behavior that should stay the same across Stage 10+ alpha runs:

- ledger serialization and upsert mechanics
- MT5 KPI ledger row construction
- common alpha run register shapes

Run scripts should keep experiment-specific choices close to the run, and import shared KPI/ledger behavior from here instead of copying it between stages.
