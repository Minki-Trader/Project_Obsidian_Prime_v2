# Current Working State

- updated_on: `2026-04-20`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `06_tiered_readiness_exploration`
- active_branch: `codex/stage06-tiered-readiness-open`

## Read This First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- latest durable decisions to expect during that pass:
  - `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
  - `docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
  - `docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
  - `docs/decisions/2026-04-20_stage05_dual_followup_order.md`
  - `docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
  - `docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
  - `docs/decisions/2026-04-19_stage04_close_and_stage05_open.md`
  - `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- the foundation closure path is now explicit through `05_exploration_kernel_freeze`; `00_foundation_sprint`, `01_dataset_contract_freeze`, `02_feature_dataset_closure`, `03_runtime_parity_closure`, `04_artifact_identity_closure`, and `05_exploration_kernel_freeze` are all now closed on materialized v2 evidence
- current v2 operating truth still has no promoted operating line; the only current runtime rule remains the strict `Tier A` contract-aligned line, and Stage `06` does not change that by itself
- the first Stage 03 evaluated pack still closes model-input parity on the contract surface with `tolerance_parity=true`, `max_abs_diff=1.6846210968424202e-06`, `4 ready rows + 1 negative non-ready row`, and zero features over the agreed tolerance
- the remaining `exact_parity=false` note on Stage 03 remains bounded to floating-point serialization drift and is not treated as a contract-surface blocker
- Stage 04 remains closed because the first v2-native machine-readable identity chain stayed aligned across the request pack, MT5 snapshot rows, comparison summary, rendered report, and registry rows
- Stage 05 is now also closed, but only on its own boundary: the active `broader_0002` twenty-four-window pack reached the first broader tolerance-closed exact-open read, `helper_0001` reached the first separate helper-focused tolerance-closed exact-open read on a frozen eight-window subset, and the non-overlapping additive `broader_0003` reinforcement pack now also reproduced a native MT5 tolerance-closed exact-open read with `matched_fixtures=24`, `unexpected_record_count=0`, `tolerance_parity=true`, `exact_parity=false`, and `max_abs_diff=7.160007811535252e-06`
- that Stage 05 closure does not claim separate runtime-helper parity closure, does not claim separate broader-sample parity closure, and does not promote any operating line; it closes only the exploration-kernel freeze boundary by making the first downstream exploration family explicit enough that later work cannot drift open by implication
- `06_tiered_readiness_exploration` is now the active stage because the future `Tier A / Tier B / Tier C` readiness family already had an accepted policy home, and Stage 05 now hands that downstream exploration family a bounded foundation evidence base instead of a branch-only question
- Stage 06 begins with the Stage 05 evidence family frozen in place: `broader_0002` remains the first active broader pack, `helper_0001` remains the first helper-focused pack, and `broader_0003` remains additive reinforcement evidence rather than a replacement for the active broader read
- all future Tier B or Tier C exploration must stay separate from the current strict Tier A runtime rule and must carry explicit readiness labels, missing-group summaries, and separate reporting lanes
- legacy winners remain archive notes and design evidence only; they do not define current v2 foundation truth or current v2 operating truth

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. materialize the first explicit Stage 06 `Tier B / Tier C` readiness boundary so reduced-risk exploration cannot blur with the current strict Tier A line
2. decide the first durable readiness-label and missing-group-summary scheme for any Stage 06 dataset, runtime, report, or scorecard artifact
3. decide whether any first Stage 06 reduced-risk experiment can reuse the frozen Stage 05 evidence family as-is or needs additional helper-lane or broader-lane support first
4. keep the current strict Tier A runtime rule unchanged until a later exploration read says otherwise
5. keep placeholder weights caveat explicit until a real monthly-weight source replaces the equal-weight table
6. keep branch truth aligned to `codex/stage06-tiered-readiness-open` until the handoff is merged

## Foundation Closure Path

1. `00_foundation_sprint`
2. `01_dataset_contract_freeze`
3. `02_feature_dataset_closure`
4. `03_runtime_parity_closure`
5. `04_artifact_identity_closure`
6. `05_exploration_kernel_freeze`

All six foundation stages are now explicitly closed.

## Active Exploration Stage

1. `06_tiered_readiness_exploration`

## Do Not Do First

- do not reopen `05_exploration_kernel_freeze` unless a new contradiction breaks the frozen `broader_0002 + helper_0001 + broader_0003` read
- do not treat Stage 05 closure as runtime-helper parity closure, broader-sample parity closure, or operating promotion
- do not let any Stage 06 artifact imply that Tier B is contract-equivalent to the current strict Tier A line
- do not compare future Tier B reduced-risk outputs head-to-head with Tier A without separate reporting lanes
- do not let durable conclusions live only in branch notes or scratch files
