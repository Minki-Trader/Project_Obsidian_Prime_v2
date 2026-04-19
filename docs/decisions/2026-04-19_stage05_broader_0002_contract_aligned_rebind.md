# 2026-04-19 Stage 05 Broader 0002 Contract-Aligned Rebind

## Status

- decided_on: `2026-04-19`
- stage: `05_exploration_kernel_freeze`
- decision_type: `active broader-pack rebind without Stage 05 closure`

## Decision

- retain `broader_0001` as pre-alignment mismatch evidence
- do not overwrite the first broader report, comparison summary, or registry rows
- move the active broader request-pack identity to `broader_0002`
- keep the Stage 05 charter shape unchanged at `24 windows / 16 ready / 8 negative`
- keep Stage 05 `open` even after the `broader_0002` evaluation result

## Why

- the first broader evaluated pack localized three repairable causes rather than disproving the broader-sample lane itself:
  - Python proxy external features were not fully following the symbol-native raw-series-first contract path
  - the MT5 broader audit path still depended on a short trailing-history slice instead of the full declared contract window
  - the MT5 `supertrend_10_3` seed rule still diverged from the current Python contract surface
- those causes were localized implementation mismatches, not a reason to rewrite the Stage 05 charter, reopen Stage 03, or reopen Stage 04
- keeping `broader_0001` visible preserves the pre-alignment diagnostic evidence and avoids rewriting history
- issuing `broader_0002` as the active pack makes the post-fix evidence chain machine-readable without pretending the first pack never existed

## What Changed In The Active Path

- Python external proxy features now compute on each symbol's own raw `M5` series before exact-timestamp merge onto `US100`
- MT5 broader audit loading now uses the full declared contract window through each audited close instead of the earlier short trailing slice
- MT5 `supertrend_10_3` now follows the current Python seed and updated-final-band order

## Evidence Boundary

- `broader_0001` remains retained evidence only:
  - `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0001.md`
  - `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0001.json`
- `broader_0002` is the active contract-aligned pack:
  - `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_inventory.md`
  - `stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json`
  - `stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
  - `stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0002.json`

## Current Read After Rebind

- `broader_0002` is materially better aligned than `broader_0001`, but it still remains `mismatch_open`
- the active residual mismatch is now localized rather than pack-wide:
  - one early-history ready row still carries `NVDA` and breadth-return drift
  - two pre-open negative rows remain non-ready on both sides but still diverge on skip-reason semantics
- this decision does not claim broader-sample parity closure
- this decision does not claim runtime-helper parity closure
- this decision does not promote any operating alpha line

## Consequences

- Stage 05 stays active
- the broader-sample lane stays first and stays separate from runtime-helper parity
- future reruns must reuse the `broader_0002` charter shape unless a new explicit decision changes the active pack identity
- registry rows for `broader_0002` must be appended as new artifact identities rather than replacing the retained `broader_0001` rows
