# Grok External Review Request(Grok 외부 검토 요청)

You are reviewing Project Obsidian Prime v2 structure governance(구조 관리), not judging model performance(모델 성능) or trading readiness(거래 준비).

Please critique the proposed transition from the legacy `stages/` folder to a new active `stages_frontier/` folder inside the same repository.

## Local Evidence(로컬 근거)

Use this bounded snapshot(제한된 스냅샷) summary as your evidence. Do not assume facts outside it.

- `docs/agent_control/grok_reviews/2026-06-12_stages_frontier_structure/inputs/local_truth_snapshot.md`
- Current stage(현재 단계): `364_source_regime_label_pivot__dense_cost_recovery`
- Current status(현재 상태): `closed_stage364_dense_cost_recovery_no_strict_joint_pass_no_next_stage_no_authority`
- Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), selected baseline(선택 기준선), and goal achieve(목표 달성) are not claimed(주장 안 함).
- Existing `stages/` already contains many historical stage folders from early numbered stages through Stage364(364단계).
- Existing `stage_pipelines/` already contains many `stageNN` folders.
- `foundation/` already owns reusable logic(재사용 로직), including features(피처), models(모델), pipelines(파이프라인), MT5 tools(MT5 도구), parity(동등성), and risk(리스크).
- `.agents/skills/` already owns repo-scoped routing and guard skills(저장소 전용 라우팅 및 가드 스킬).
- AGENTS.md currently names `stages/` as the numbered stage work root(번호 단계 작업 루트) and says the stage ledger path(단계 장부 경로) is `stages/<stage_id>/03_reviews/stage_run_ledger.csv`.
- Architecture invariants(구조 불변 규칙) currently say `stages/*` contains stage-local artifacts(단계 로컬 산출물), reports(보고서), and decisions(결정).

Important boundary(중요 경계): Grok cannot grant runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), selected baseline(선택 기준선), or goal achieve(목표 달성).

## Codex Proposal To Review(Codex 검토 대상 제안)

1. Keep `stages/` as legacy(레거시) historical stage storage.
2. Create `stages_frontier/` as the new active stage root(활성 단계 루트).
3. Do not duplicate `foundation/`, `data/`, `docs/`, or `.agents/skills/`.
4. Add a minimal policy/state declaration for active vs legacy stage roots.
5. Use `stages_frontier/<stage_id>/00_spec`, `01_inputs`, `02_runs/active`, `02_runs/archived`, `03_reviews`, and `04_selected`.
6. Put new stage-specific orchestration(단계 전용 실행 지휘) under `stage_pipelines/frontier/<stage_id>/` only when a stage needs custom orchestration.
7. Keep reusable logic(재사용 로직) in `foundation/`.

## Questions(질문)

1. Is `stages_frontier/` a good active stage root(활성 단계 루트) name, or would it create long-term ambiguity?
2. Is `stage_pipelines/frontier/<stage_id>/` better than continuing `stage_pipelines/stageNN` for new work?
3. What exact docs or routing files(라우팅 파일) must be updated to avoid old agents(에이전트) writing into `stages/` by habit?
4. What risks would you reject in the Codex proposal?
5. What minimal migration plan(최소 이전 계획) would you recommend?

## Required Output Format(필수 출력 형식)

Please answer with these sections:

- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)
- recommended_minimal_plan(추천 최소 계획)
- drift_risks(드리프트 위험)
