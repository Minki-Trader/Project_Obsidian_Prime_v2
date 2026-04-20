# Stage 05 Exploration Kernel Freeze

- stage: `05_exploration_kernel_freeze`
- stage_type: `foundation_stage`
- updated_on: `2026-04-20`
- owner_path: `stages/05_exploration_kernel_freeze/`

## Purpose

- freeze the first downstream exploration kernel after the explicit Stage 04 artifact-identity closure
- freeze `broader-sample parity` as the first post-foundation validation lane without blurring strict Tier A runtime truth with future reduced-risk or exploration-only work
- keep exploration-kernel freeze distinct from runtime-helper parity closure, broader-sample parity closure, and operating promotion

## Inherited Context

- `00_foundation_sprint` is closed as planning scaffold complete
- `01_dataset_contract_freeze` is closed after the first materialized dataset-contract evidence pack
- `02_feature_dataset_closure` is closed after a deterministic rerun reproduced the same row summary and tracked output hashes
- `03_runtime_parity_closure` is closed after the first v2-native five-window pack matched within the agreed tolerance while the remaining exact-open note was bounded to floating-point serialization drift
- `04_artifact_identity_closure` is closed after the explicit first-pack read confirmed machine-readable identity alignment, required-hash consistency, and the first runtime self-check meaning

## Scope

- in scope:
  - the first explicit Stage 05 exploration-kernel freeze read
  - the decision that `broader-sample parity` is the first downstream lane
  - the ordered next-step plan that first opened `runtime-helper parity` after the current broader_0002 read, then materialized `broader_0003` as the additive broader reinforcement family, and now keeps native evaluation of that reinforcement pack as the required next follow-up lane
  - the execution charter for the first `24-window` broader-sample audit pack
  - the first helper-focused `8-window` reuse subset derived from the active broader_0002 family
  - the separation between the current strict Tier A line and any later Tier B or Tier C exploration family
  - the live Stage 05 read path and selection note
- not in scope:
  - operating promotion
  - new alpha or range search
  - claiming runtime-helper parity is already closed
  - claiming broader-sample parity is already closed

## Success Criteria

- the first Stage 05 read states clearly that `broader-sample parity` is the first downstream lane and what still remains separately bounded
- the active Stage 05 read states clearly that `helper_0001` now exists as the first helper-focused evaluated pack, `broader_0003` now exists as the first additive broader reinforcement family, and the native evaluation of `broader_0003` is the next required follow-up without claiming Stage 05 closure
- the broader-sample charter fixes pack size, strata, selection rules, reserved identifiers, and reusable artifact-family expectations
- the first charter-aligned broader-sample inventory, selection manifest, and local request-pack materialization exist without claiming that broader-sample parity is already evaluated or closed
- the first helper-focused inventory, selection manifest, local request-pack materialization, and evaluated read exist without claiming runtime-helper parity closure
- the strict Tier A runtime rule remains distinct from any future Tier B or Tier C exploration family
- any remaining blocker to post-foundation exploration has an explicit durable home rather than living as branch-only context

## Required Inputs

- `../01_inputs/input_refs.md`
- `../01_inputs/next_evidence_dual_lane_plan.md`
- `../../../docs/decisions/2026-04-20_stage05_dual_followup_order.md`
- `../../../docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
- `../../../docs/adr/0002_broader_sample_parity_charter.md`
- `../../04_artifact_identity_closure/03_reviews/review_index.md`
- `../../04_artifact_identity_closure/04_selected/selection_status.md`
- `../../../docs/policies/tiered_readiness_exploration.md`
- `../../../docs/context/current_working_state.md`

## Required Outputs

- updated `03_reviews/review_index.md`
- updated `04_selected/selection_status.md`
- explicit Stage 05 kernel-freeze decision
- broader-sample parity charter with fixed pack shape, selection rules, and reserved identifiers
- first broader-sample fixture inventory and machine-readable selection manifest
- first local broader request-pack materialization path under `02_runs/`
- first helper-focused fixture inventory and machine-readable selection manifest
- first local helper-focused request-pack materialization path under `02_runs/`
- first additive broader reinforcement fixture inventory and machine-readable selection manifest when the ordered follow-up lane opens
- first additive broader reinforcement request-pack materialization path under `02_runs/` when the ordered follow-up lane opens

## Close Bias

- close Stage 05 only after the first downstream exploration boundary is frozen clearly enough that alpha or range work cannot drift open by implication
- do not let Stage 05 imply that runtime-helper parity, broader-sample parity, or Tier B exploration are already closed or promoted
