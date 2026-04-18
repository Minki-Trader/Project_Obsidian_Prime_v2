# Stage 04 Artifact Identity Closure

- stage: `04_artifact_identity_closure`
- stage_type: `foundation_stage`
- updated_on: `2026-04-19`
- owner_path: `stages/04_artifact_identity_closure/`

## Purpose

- close the first explicit artifact-identity read for the v2-native five-window parity pack
- prove that dataset, fixture, bundle, runtime, and report identities remain machine-readable and hash-consistent across request, MT5 snapshot, comparison summary, rendered report, and registry rows
- keep artifact identity closure distinct from runtime-helper parity, broader-sample parity, and operating promotion

## Inherited Context

- `00_foundation_sprint` is closed as planning scaffold complete
- `01_dataset_contract_freeze` is closed after the first materialized dataset-contract evidence pack
- `02_feature_dataset_closure` is closed after a deterministic rerun reproduced the same row summary and tracked output hashes
- `03_runtime_parity_closure` is closed after the first v2-native five-window pack matched within the agreed tolerance while the remaining exact-open note was bounded to floating-point serialization drift
- the first MT5 snapshot rows now carry explicit machine-readable identity fields and the first comparison summary now verifies those values against the request pack

## Scope

- in scope:
  - the first explicit Stage 04 artifact-identity read for `runtime_parity_pack_0001`
  - required-hash consistency across request, snapshot, comparison, report, and registry rows
  - explicit runtime self-check meaning for the machine-readable first-pack identity chain
  - Stage 04 live read path and selection note
- not in scope:
  - runtime-helper parity
  - broader-sample parity beyond the first five windows
  - operating promotion
  - new alpha or range search

## Success Criteria

- the first artifact-identity closure read states clearly whether the first pack is machine-readable and hash-consistent enough to close Stage 04
- dataset, fixture, bundle, runtime, report, parser, and contract-order identities remain aligned across the request, MT5 snapshot, comparison summary, report, and registry
- any remaining blocker has an explicit durable home rather than living as branch-only context

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `../../03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json`
- `../../03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- `../../03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- `../../../docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `../../../docs/policies/artifact_registry_schema.md`

## Required Outputs

- updated `03_reviews/review_index.md`
- updated `04_selected/selection_status.md`
- explicit Stage 04 closure or blocker decision for the first pack

## Close Bias

- close Stage 04 only after the explicit artifact-identity read names the backing machine-readable fields and required hashes
- do not reopen Stage 03 unless Stage 04 evidence falsifies the already closed tolerance-based model-input parity read
