# Changelog

## 2026-04-23

- added stage-agnostic architecture guardrails for feature/model/pipeline ownership, materialized-model claim discipline, alpha-search integrity, and Korean BOM/encoding validation; registered the current Stage 06/07 issues as architecture debt rather than normal project style
- synchronized the published Stage 07 workspace truth back to `main` after merging `codex/stage06-tierb-feature-schema` so the active-branch read no longer lags the merged repository state

## 2026-04-22

- closed `06_tiered_readiness_exploration` and opened `07_alpha_search` after syncing the additive follow-up pack plus the first shared keep42 `Tier B reduced-context model (Tier B 축약 문맥 모델)` into the official read while keeping the strict `Tier A` runtime rule unchanged and the separate `Tier B` lane `offline-only (오프라인 전용)`
- materialized the first shared Stage 06 `Tier B reduced-context model` on a fixed `keep=42` feature surface with a separate evaluation summary calibration read and report; the current Tier B holdout `log_loss` improved from `1.963620` on the full baseline to `1.503578` while all meaning stayed offline-only
- added a draft-only Stage 06 `Tier B-safe feature schema` so the first shared reduced-context model can start from a fixed keep=42, conditional=6, drop=10 surface without changing any official state document
- added a draft-only Stage 06 anchor note plus `review_index` routing for the current `Tier B reduced-context model` preference so later sessions can resume from one shared Tier B model plus subtype tags without changing any official state document
- materialized an additive Stage 06 `tier_b_followup_pack_0001` with separate `Tier B calibration fit`, coarse `threshold / exposure / sizing` sensitivity, robustness segmentation, placeholder-weight verdict, and draft-only `Stage 07` design/readout documents without reflecting an official stage transition
- added a Stage 06 local follow-up-pack spec plus a dedicated follow-up materializer and real-data tests for the calibration, control, robustness, and weight-verdict surfaces
- added new Stage 06 registry rows for the follow-up-pack manifest, four machine-readable summaries, four evaluation reports, and two draft-only handoff documents while keeping the official active-stage truth unchanged in this pass
- replaced the Stage 06 `baseline-family reuse` working hypothesis with `legacy non-inheritance` plus a first `Tier A`-trained `v2-native baseline seed`, then materialized the first `Tier B offline evaluation report` and `calibration read` without changing the strict Tier A runtime rule
- added a Stage 06 local baseline-seed spec, a dedicated `Gaussian Naive Bayes` materializer, and real-data tests for the first `tier_b_offline_eval_0001` artifact family
- added five new Stage 06 registry rows for the baseline-seed manifest, probability table, evaluation summary, calibration read, and report while keeping `approved_for=not_applicable` and leaving runtime-family or promotion claims closed

## 2026-04-21

- added repo-scoped `obsidian-session-intake` and `obsidian-task-packet` skills so turns now choose a narrow session mode, prefer warm-thread delta checks over repeated cold re-entry, and fix one bounded task packet before implementation drifts open
- weakened `obsidian-publish-merge` from default auto-publish to explicit-user-or-packet-gated `main` publish, while keeping `branch_only` as the default publish target
- expanded branch policy so one approved task packet can map to one branch more cleanly and stale ahead/behind branches now require an explicit `merge`, `re-cut-needed`, `superseded`, or `archived` resolution
- added a Stage 06 execution contract block so the next offline Tier B artifact stays bounded by allowed paths, do-not-touch rules, verification minimums, stop conditions, and a branch-first publish default
- adopted the first Stage 06 offline-only Tier B experiment charter on baseline-family reuse plus separate calibration and separate `tier_b_exploration` reporting, while keeping placeholder monthly weights bounded to offline exploration only
- materialized the first Stage 06 tiered-readiness scorecard as row-level labels plus a machine-readable summary and review report with shared-window counts `tier_a=56988`, `tier_b=88303`, `tier_c=116053` and practical-window counts `tier_a=55457`, `tier_b=86192`, `tier_c=113352`
- added the first Stage 06 registry rows for `readiness_row_labels`, `readiness_scorecard_summary`, and `readiness_scorecard_report` without claiming any reduced-risk runtime family or operating promotion
- added a dedicated Stage 06 scorecard materializer, real-data regression tests, and Git tracking exceptions for the first tracked `02_runs/tiered_readiness_scorecard_0001` artifact family

## 2026-04-20

- fixed the first Stage 06 deterministic readiness boundary as a docs-only governance lock, demoted heuristic Tier B notes to non-binding exploration notes, and synchronized Stage 06 plus workspace truth without adding new registry rows
- evaluated `broader_0003` on the native MT5 path as the first additive Stage 05 broader reinforcement pack with `matched_fixtures=24`, `unexpected_record_count=0`, `tolerance_parity=true`, and `max_abs_diff=7.160007811535252e-06`
- added a League/Riot process guard to the native MT5 runner so live game sessions are blocked by default and only proceed when `--allow-conflicting-games` is passed explicitly
- closed `05_exploration_kernel_freeze` on the explicit `broader_0002 + helper_0001 + broader_0003` kernel-freeze read and opened `06_tiered_readiness_exploration` as the first downstream exploration-only stage
- materialized `broader_0003` as the first additive Stage 05 broader reinforcement family on a non-overlapping twenty-four-window charter pack, while keeping native evaluation of that pack as the next required follow-up
- materialized and evaluated `helper_0001` as the first helper-focused Stage 05 subset derived from the active `broader_0002` pack; the separate helper pack now reaches a first tolerance-closed exact-open read on `8` frozen fixtures while Stage 05 still remains open
- fixed the next Stage 05 follow-up order so the first separate runtime-helper parity lane now opens before any additional broader-sample coverage pass, while the active broader_0002 read remains the current broader evidence
- reran the active Stage 05 broader_0002 pack through the native MT5 path after the tooling-hardening pass and reproduced the same first broader tolerance-closed exact-open read instead of changing the Stage 05 boundary
- added a project-wide verification discipline so agent work now escalates to the narrowest real-environment check for MT5 execution, orchestration, import/export, and other environment-dependent paths instead of stopping at local-only validation when the risk surface requires more
- aligned the same-pass synchronization norm across `docs/policies/agent_trigger_policy.md`, `.agents/skills/obsidian-stage-transition/SKILL.md`, and the runtime parity reporter `gate_before_closure` wording so policy/skill/reporter drift is reduced and `artifact_registry.csv` inclusion is explicit
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
