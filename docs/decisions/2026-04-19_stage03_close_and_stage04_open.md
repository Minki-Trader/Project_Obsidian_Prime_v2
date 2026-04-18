# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-19_stage03_close_stage04_open`
- `reviewed_on`: `2026-04-19`
- `owner`: `codex + user`
- `decision`: `close Stage 03 after the first v2-native five-window pack matches within the agreed tolerance and open Stage 04 for the explicit artifact-identity closure read`

## What Was Decided

- adopted:
  - close `03_runtime_parity_closure` on the first v2-native five-window pack because the contract-surface comparison now satisfies the agreed tolerance with `tolerance_parity=true`
  - keep the remaining `exact_parity=false` note bounded as floating-point serialization drift rather than a Stage 03 blocker
  - treat the first MT5 snapshot rows plus the first comparison summary as the first machine-readable identity chain for Stage 04
  - open `04_artifact_identity_closure` as the active stage
  - align the workspace state and current working state to the actual branch `codex/stage03-v2-native-parity-sync`
- not adopted:
  - claiming runtime-helper parity closure from the current evidence
  - claiming broader-sample parity from the current five-window pack
  - claiming operating promotion from the Stage 03 closure alone
  - claiming Stage 04 artifact-identity closure in the same pass without an explicit Stage 04 read

## Why

- the runtime parity contract closes `parity_closure` when the ordered feature vectors, session fields, timestamp identity, and negative fixture behavior match within the agreed tolerance
- the repaired v2-native rerun now reproduces all five bound fixtures, keeps the negative non-ready behavior intact, and leaves `max_abs_diff=1.6846210968424202e-06` with zero features above the agreed `1e-05` tolerance
- the MT5 snapshot rows now embed machine-readable identity fields and the comparison summary proves those values match the request pack on the first evaluated line
- keeping Stage 04 explicit still prevents conflating model-input parity closure with broader artifact identity closure

## What Remains Open

- the explicit Stage 04 artifact-identity closure read for the first machine-readable identity chain
- separate runtime-helper parity evaluation in v2
- broader-sample parity beyond the first five windows
- `05_exploration_kernel_freeze`

## Evidence Used

- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- `stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `foundation/mt5/ObsidianPrimeV2_RuntimeParityAuditEA.mq5`
- `docs/registers/artifact_registry.csv`

## Operational Meaning

- `active_stage changed?`: `yes, Stage 03 closed and Stage 04 opened`
- `model-input parity closed?`: `yes, within the agreed tolerance on the first five-window pack`
- `exact parity closed?`: `no, the remaining note stays bounded to float serialization drift`
- `runtime-helper parity closed?`: `no`
- `machine-readable first-pack identity chain materialized?`: `yes`
- `workspace_state update needed?`: `yes, completed with the Stage 03 close and Stage 04 open transition`
