# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-19_stage04_close_stage05_open`
- `reviewed_on`: `2026-04-19`
- `owner`: `codex + user`
- `decision`: `close Stage 04 after the explicit first-pack artifact-identity read and open Stage 05 for exploration-kernel freeze`

## What Was Decided

- adopted:
  - close `04_artifact_identity_closure` because the first v2-native five-window pack now carries one aligned machine-readable identity chain across the request pack, MT5 snapshot rows, comparison summary, rendered report, and registry rows
  - treat the Stage 04 required-hash read as satisfied because the recorded request, snapshot, comparison, and report hashes remain internally consistent on the materialized first pack
  - treat the Stage 04 runtime self-check meaning as satisfied because the MT5 audit path loaded the declared identity inputs, echoed them into every snapshot row, and the comparison summary verified those exported values and derived feature-order hashes against the declared request pack
  - open `05_exploration_kernel_freeze` as the new active stage
- not adopted:
  - claiming runtime-helper parity closure from the current evidence
  - claiming broader-sample parity from the current five-window pack
  - opening alpha or range exploration in the same pass as the Stage 04 closure
  - treating future `Tier B` reduced-risk work as if it were already part of the current strict Tier A runtime rule

## Why

- the Stage 04 contract closes `artifact_identity_closure` only when machine-readable identities remain aligned, required hashes are internally consistent, and runtime self-check can prove the loaded artifact set matches the declared contract surface
- the comparison summary already proves that the request pack and MT5 snapshot rows agree on dataset, fixture, bundle, runtime, report, parser, contract-version, and contract-order identities, and it also confirms the derived MT5 feature-order hash matches the declared request value
- the rendered report carries the same first-pack identities and records the request-side required hashes it checked directly, while the artifact registry links the same report row to the fixture inventory and comparison summary hashes
- the recorded digests for the first materialized pack remain consistent with the current files for the fixture bindings, Python snapshot, MT5 request, MT5 snapshot, comparison summary, and rendered report
- that explicit read closes Stage 04 without requiring the comparison summary itself to ingest the rendered report, because the report and registry links are now named and re-read as part of the closure decision

## What Remains Open

- the first explicit `05_exploration_kernel_freeze` read that names which downstream lane may open first
- separate runtime-helper parity evaluation in v2
- broader-sample parity beyond the first five windows
- any later `Tier B` reduced-risk line or alpha exploration

## Evidence Used

- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `docs/registers/artifact_registry.csv`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`

## Operational Meaning

- `active_stage changed?`: `yes, Stage 04 closed and Stage 05 opened`
- `artifact-identity closure closed?`: `yes, on the explicit first-pack read`
- `runtime self-check meaning satisfied?`: `yes, on the first machine-readable pack`
- `runtime-helper parity closed?`: `no`
- `broader-sample parity closed?`: `no`
- `workspace_state update needed?`: `yes, completed with the Stage 04 close and Stage 05 open transition`
