# Selection Status

## Current Read

- current incumbent: `none, by policy`
- current challenger: `none, by policy`
- current read: `Stage 03 now has a v2-native MT5 snapshot artifact and a first evaluated five-window parity report, but the result is mismatch open so model-input parity remains open while v2 stays in foundation mode`
- scoreboard used: `foundation_stage_read`

## Promotion Gates

- the first evaluated parity report must keep model-input parity, runtime-helper parity, and Stage 04 artifact-identity closure explicitly separate
- a repaired rerun on the same five-window pack must close the localized mismatch before any model-input parity closure claim is made
- `workspace_state.yaml` and `current_working_state.md` must stay aligned with the Stage 03 read

## Scoreboards

- structural_scout: `n/a`
- regular_risk_execution: `n/a`
- parity / special scoreboard: `Stage 03 active`

## Headline

- return_pct: `n/a`
- profit_factor: `n/a`
- trade_count: `n/a`
- max_dd_pct: `n/a`

## Risk

- biggest current risk: `treating the first v2-native evaluated pack as close-enough parity even though six ready-row features still breach tolerance and max_abs_diff remains 7.285655212821098`
- state fragmentation risk: `reduced now that the v2-native MT5 snapshot artifact and the evaluated report both exist, but only if workspace docs and the artifact registry are updated in the same pass`
- parity overconfidence risk: `high if model-input parity and runtime-helper parity are conflated`
- current v2 operating risk metrics: `n/a`

## Diagnostics

- first materialized dataset-contract evidence pack: `yes`
- deterministic feature-dataset rerun match: `yes`
- first bound fixture timestamps: `yes`
- first Python snapshot artifact: `yes`
- first MT5 snapshot artifact: `yes`
- first evaluated parity report: `yes`
- placeholder weights caveat: `still open`

## Execution

- fixture timestamps bound: `yes`
- python snapshot ref recorded: `yes`
- mt5 snapshot ref recorded: `yes`
- evaluated parity result written: `yes`
- stage status: `open`

## Decision

- keep_or_replace: `keep foundation mode`
- promoted / kept / closed: `Stage 03 open`
- next required evidence: `a repaired v2-native rerun that closes the localized mismatch on the same five-window pack, or a durable root-cause note that keeps Stage 03 open with the mismatch explicitly bounded`

## Follow-Up Bias

- continue: `trace and repair the localized MT5 feature drift, then rerun runtime_parity_pack_0001 on the same v2-native path`
- do_not_reopen_without_new_hypothesis: `artifact-closure claims or alpha search before Stages 03 to 05 are closed`
- next best question: `which contract or MT5 path is causing the dominant drift on ema50_ema200_diff and the smaller RSI / ATR family mismatches?`
- downstream note: `Tier A / Tier B / Tier C readiness remains a later separate exploration family and does not relax current Stage 03 strict-line parity scope`

## Report Refs

- `../00_spec/stage_brief.md`
- `../01_inputs/input_refs.md`
- `../03_reviews/review_index.md`
- `../01_inputs/first_bound_runtime_minimum_fixture_inventory.md`
- `../03_reviews/report_fpmarkets_v2_runtime_parity_0001.md`
- `../../00_foundation_sprint/03_reviews/first_v2_runtime_parity_report.md`
- `../../02_feature_dataset_closure/04_selected/selection_status.md`
- `../../../docs/context/current_working_state.md`
