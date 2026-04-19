# Changelog

## 2026-04-20

- realigned the active working branch name from the lingering Stage 03 label to `codex/stage05-broader-rebind` so the live workspace truth matches the actual Stage 05 foundation boundary
- synchronized `workspace_state.yaml` and `current_working_state.md` to the active Stage 05 branch truth instead of the older Stage 03 handoff branch name
- carried the active Stage 05 read forward so `broader_0001` stays retained pre-alignment evidence, `broader_0002` stays the active contract-aligned pack, and Stage 05 still remains open on localized residual mismatch evidence
- appended the `broader_0002` artifact identity rows to `artifact_registry.csv` instead of overwriting the retained `broader_0001` evidence chain

## 2026-04-19

- repaired the v2-native MT5 audit path so the main symbol uses the full contract window history through each audited close rather than a short trailing slice
- reran the first five-window v2-native parity pack and closed Stage 03 model-input parity within the agreed tolerance with `tolerance_parity=true`
- embedded machine-readable identity fields directly into the MT5 snapshot rows and extended the comparison summary to verify the first request-to-snapshot identity chain
- aligned the rendered parity report to distinguish tolerance-based closure from the bounded exact-open float-noise note
- closed `03_runtime_parity_closure` and opened `04_artifact_identity_closure`
- synchronized the workspace read to the working branch `codex/stage03-v2-native-parity-sync`
- aligned the artifact registry schema to carry `parser_version` and corrected the Stage 04 live-state wording to match the current automated proof boundary
- closed `04_artifact_identity_closure` on the explicit first-pack identity and required-hash read and opened `05_exploration_kernel_freeze`
- wrote the first explicit Stage 05 blocker read so the unresolved downstream ordering between broader-sample parity, runtime-helper parity, and later exploration work now has a durable home
- froze `broader-sample parity` as the first downstream Stage 05 lane and added a fixed `24-window` stratified charter without changing the current strict Tier A runtime rule
- generalized the runtime-pack materializer into a shared `minimum_0001 | broader_0001` builder and kept the old minimum-pack entrypoint as a compatibility wrapper
- bound the first Stage 05 broader-sample `24-window` inventory and machine-readable selection manifest and materialized the first local broader Python snapshot, MT5 request, MT5 helper `.set`, and MT5 tester `.ini` pack without claiming broader parity closure
- generalized the runtime parity import, compare, render, and native-run flows around `mt5_request`-anchored pack-aware path resolution instead of Stage 03-only default paths
- split the Stage 05 broader MT5 target-window helper inputs across multiple EA input fields so the full frozen `24-window` pack reaches MT5 without truncation
- imported the first Stage 05 broader MT5 snapshot, wrote the first broader comparison summary and rendered broader parity report on the same frozen `24-window` pack, and kept Stage 05 open because that first evaluated pack remains `mismatch_open`
- corrected Python proxy external features to compute on each symbol's own raw `M5` series before exact-timestamp merge and documented that raw-series-first rule explicitly in the feature contract
- aligned the MT5 broader audit path to the full declared contract window and aligned MT5 `supertrend_10_3` seeding to the current Python contract surface
- retained `broader_0001` as pre-alignment mismatch evidence, rebound the active Stage 05 broader pack to `broader_0002`, and evaluated that active pack without closing Stage 05
- synchronized the active Stage 05 read so `broader_0002` is the active contract-aligned pack, `broader_0001` remains retained evidence, and the remaining residual mismatch stays localized to early-history equity drift plus pre-open skip-reason semantics

## 2026-04-18

- aligned the workspace charter around a concept-preserving reboot and explicit foundation-first closure language
- clarified the contract hierarchy as three constitutional contracts plus one auxiliary frozen mirror
- added dataset/row-state and runtime parity/artifact identity supplemental contracts for Stage 00 foundation closure
- aligned Stage 00 documents around closure-readiness instead of alpha comparison semantics
- aligned the dataset freeze and runtime parity templates to the supplemental contracts instead of looser placeholder fields
- added a reusable gold fixture inventory template for the first v2 parity fixture pack
- widened `artifact_registry.csv` so dataset, fixture, bundle, runtime, and report identity can become machine-readable
- added artifact-registry serialization rules so composite CSV fields can stay machine-readable without ad hoc prose
- wrote the first v2 planning freeze card and registered it as a draft Stage 00 identity artifact
- fixed the contract-order feature hash for the planning freeze using the frozen 58-feature order
- wrote the first planning gold fixture inventory and first planning runtime parity report scaffold
- aligned Stage 00 live docs so remaining work now points only to materialized row summaries, bound fixture timestamps, and evaluated parity results
- closed `00_foundation_sprint` as planning scaffold complete and opened `01_dataset_contract_freeze`
- moved the first materialized dataset evidence tasks into Stage 01 while keeping parity and broader artifact identity closure assigned to later foundation stages
- added a repo-scoped skill layer and trigger policy for re-entry reads, claim discipline, and stage-transition sync
- centralized the canonical re-entry order and truth precedence into `docs/policies/reentry_order.md`
- removed duplicated full read-order lists from repo entry docs and switched them to policy references
- reduced active-stage hardcoding inside repo-scoped skills and added validation around stage alignment
- added `docs/policies/artifact_registry_schema.md` to define registry enums and hash-update discipline
- added a reusable MT5 raw-bar export script and materialized the first raw `M5` source roots plus manifests for all 12 required Stage 01 symbols
- added a tracked raw-source identity inventory so the local-only exports have Git-visible identity before processed dataset closure
- materialized the first reusable Stage 01 dataset freeze under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`
- wrote the first row summary, invalid-reason breakdown, and processed-output hashes back into the freeze card and artifact registry
- closed `01_dataset_contract_freeze` and opened `02_feature_dataset_closure`
- reran the first materialized freeze and confirmed the same row summary, invalid-reason breakdown, and tracked output hashes on repeat
- closed `02_feature_dataset_closure` and opened `03_runtime_parity_closure`
- added a downstream `Tier A / Tier B / Tier C` readiness exploration policy so future reduced-risk partial-context work stays separate from the current strict Tier A line

## 2026-04-17

- aligned the shared non-stage workspace skeleton across `docs/`, `data/`, and `foundation/`
- added tracked README placeholders so the `data/` tree can stay visible in Git while heavy artifacts remain local
- added `docs/archive/` and foundation subfolders for collectors, features, pipelines, MT5 helpers, parity assets, and shared reports

## 2026-04-16

- created the clean restart workspace `Project_Obsidian_Prime_v2`
- copied the v2 contract documents and placeholder monthly weights from the legacy project
- added a v2-specific `AGENTS.md`, `workspace_state.yaml`, restart decision memo, registers, and Stage 00 foundation sprint scaffold
- set the workspace into `foundation_restart` mode with no promoted v2 alpha incumbent yet
