# Codex Local Verification(Codex 로컬 검증)

Created(생성): 2026-06-12

## Accepted(수용)

- Grok's main warning(주요 경고)은 accepted(수용)한다: `stages_frontier/`를 폴더만 만들어 active root(활성 루트)로 쓰면 기존 routing(라우팅), ledger(장부), reentry(재진입), audit(감사) 규칙과 충돌한다.
- Local evidence(로컬 근거):
  - `AGENTS.md` defines `stages/*` as stage-local artifact root(단계 로컬 산출물 루트).
  - `AGENTS.md` defines stage ledger(단계 장부) as `stages/<stage_id>/03_reviews/stage_run_ledger.csv`.
  - `docs/policies/architecture_invariants.md` defines `stage_pipelines/stageXX` and `stages/*`.
  - `foundation/alpha/specs.py` hard-codes `Path("stages")` for run output root(실행 출력 루트) and stage review ledger(단계 검토 장부).
  - `foundation/control_plane/code_surface_audit.py` uses `STAGE_PIPELINE_PATH_RE = ^stage_pipelines/stage(?P<stage>\d+)/`.
  - `foundation/control_plane/experiment_inventory.py` hard-codes `root_path / "stages" / stage_id / "03_reviews/stage_run_ledger.csv"`.
  - `docs/agent_control/surface_registry.yaml` tracks `stages/*` surfaces(표면).

## Rejected(거절)

- Grok's broad implication(넓은 암시) that every historical record(과거 기록)을 migrate(이전)해야 한다는 reading(해석)은 rejected(거절)한다. Legacy `stages/` can remain preserved(보존) if the new root is introduced through a formal routing contract(라우팅 계약).
- Grok's naming concern(명명 우려) about `frontier` is useful but not decisive(결정적 아님). The name can still be used if docs(문서)가 active root(활성 루트) and research label(연구 라벨)을 clearly separate(명확히 분리)한다.

## Needs Local Verification(로컬 검증 필요)

- Whether every future writer(미래 작성기) goes through `foundation/alpha/specs.py` or has its own direct `stages/` hard-code(고정 경로).
- Whether `stage_pipelines/frontier/<stage_id>/` is worth supporting, or whether new work should continue `stage_pipelines/stage365` while only the artifact root(산출물 루트) changes.
- Exact files(정확한 파일) needed for a minimal active-root change(최소 활성 루트 변경): likely `AGENTS.md`, `docs/policies/architecture_invariants.md`, `docs/agent_control/surface_registry.yaml`, `foundation/alpha/specs.py`, `foundation/control_plane/experiment_inventory.py`, and `foundation/control_plane/code_surface_audit.py`.

## Final Codex Direction(최종 Codex 방향)

Do not create `stages_frontier/` as an active production convention(활성 운영 관례) yet.

Safer path(더 안전한 경로):

1. Keep `stages_frontier` as a proposed name(제안 이름) for now.
2. First add an explicit stage root contract(단계 루트 계약): `active_stage_root`, `legacy_stage_root`, and ledger path rule(장부 경로 규칙).
3. Decide whether pipeline adapters(파이프라인 어댑터) remain numeric as `stage_pipelines/stageNN` or get a formal frontier namespace(프론티어 네임스페이스).
4. Only then create the first frontier stage(프론티어 단계).

