# Grok Review Snapshot(Grok 검토 스냅샷)

Created(생성): 2026-06-12

Topic(주제): `stages_frontier` active stage root(활성 단계 루트) proposal(제안)

## User Intent(사용자 의도)

The user wants to leave existing `stages/` as legacy(레거시) inside the same Project Obsidian Prime v2 workspace and start new work under `stages_frontier/`.

They asked whether existing pipeline folders(파이프라인 폴더), agents(에이전트), and skills(스킬) need to become complicated again.

## Current Local Truth(현재 로컬 진실)

- Workspace(작업공간): Project Obsidian Prime v2
- Current stage(현재 단계): `364_source_regime_label_pivot__dense_cost_recovery`
- Current status(현재 상태): `closed_stage364_dense_cost_recovery_no_strict_joint_pass_no_next_stage_no_authority`
- Runtime authority(런타임 권위): not claimed(주장 안 함)
- Operating promotion(운영 승격): not claimed(주장 안 함)
- Goal achieve(목표 달성): not claimed(주장 안 함)

The active old stage is closed. Starting a new stage root would be structure governance(구조 관리), not a model or runtime promotion(모델 또는 런타임 승격).

## Relevant Rules(관련 규칙)

- `foundation/` owns reusable code(재사용 코드) and shared tools(공유 도구).
- `data/` owns raw and processed data(원천/처리 데이터).
- `docs/` owns contracts(계약), policies(정책), current state(현재 상태), decisions(결정), registers(등록부), and templates(템플릿).
- `stage_pipelines/` owns stage-specific execution adapters(단계 전용 실행 어댑터).
- Existing `stages/` currently owns numbered stage work(번호 단계 작업).
- AGENTS.md currently names the stage ledger path(단계 장부 경로) as `stages/<stage_id>/03_reviews/stage_run_ledger.csv`.
- Architecture invariants(구조 불변 규칙) say `stages/*` contains stage-local artifacts(단계 로컬 산출물), reports(보고서), and decisions(결정).

## Observed Folder Shape(확인한 폴더 형태)

- `stages/` already contains many historical stage folders, including stages from `01_*` through `364_*`.
- `stage_pipelines/` already contains many `stageNN` folders and some non-numbered helpers such as `auto_campaign_02`.
- `foundation/` already contains reusable modules(재사용 모듈): `features`, `models`, `pipelines`, `mt5`, `parity`, `risk`, and others.
- `.agents/skills/` already contains repo-scoped skills(저장소 전용 스킬), including routing(라우팅), re-entry(재진입), architecture guard(구조 가드), result judgment(결과 판정), and Grok collaboration(Grok 협업).

## Codex Direction Proposal(Codex 방향 제안)

Recommended direction(추천 방향):

1. Create `stages_frontier/` as the new active stage root(활성 단계 루트).
2. Leave `stages/` as legacy(레거시) read-only by convention(관례상 읽기 전용), unless an explicit archive or audit task needs it.
3. Do not duplicate `foundation/`, `data/`, `docs/`, or `.agents/skills/`.
4. Add a small policy/state update declaring:
   - active stage root(활성 단계 루트): `stages_frontier/`
   - legacy stage root(레거시 단계 루트): `stages/`
5. Use default stage layout under `stages_frontier/<stage_id>/`:
   - `00_spec/`
   - `01_inputs/`
   - `02_runs/active/`
   - `02_runs/archived/`
   - `03_reviews/`
   - `04_selected/`
6. For stage-specific orchestration(단계 전용 실행 지휘), use either:
   - `stage_pipelines/frontier/<stage_id>/`, or
   - `stage_pipelines/stage_frontier_<stage_id>/`

Codex currently prefers `stage_pipelines/frontier/<stage_id>/` because it separates new active frontier work from old numeric legacy adapters without copying shared logic.

## Claim Boundary(주장 경계)

This review cannot create runtime authority(런타임 권위), operating promotion(운영 승격), selected baseline(선택 기준선), live readiness(실거래 준비), or goal achieve(목표 달성).

The only claim being reviewed is structure direction(구조 방향): how to start `stages_frontier/` without making agents(에이전트), skills(스킬), and pipelines(파이프라인) messy.

