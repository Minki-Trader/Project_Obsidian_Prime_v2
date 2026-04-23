# Stage 06 Tier B Reduced-Context Modeling Anchor (Stage 06 Tier B 축약 문맥 모델링 앵커)

## Identity (식별 정보)
- noted_on: `2026-04-22`
- anchor_id: `note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001`
- stage: `06_tiered_readiness_exploration`
- status: `draft_only_planning_anchor`

## Boundary (경계)
- this note is a `planning scaffold (계획 비계)` only and does not update `workspace_state (워크스페이스 상태)`, `selection_status (선정 상태)`, or any `official Stage 07 open (공식 Stage 07 개시)` read
- this note does not authorize `MT5 path (MT5 경로)` work, `simulated execution (가상 실행)`, or `operating promotion (운영 승격)`
- the current `strict Tier A runtime rule (엄격 Tier A 런타임 규칙)` remains unchanged

## Why This Anchor Exists (이 앵커가 존재하는 이유)
- the current `Tier B (티어 B)` follow-up evidence suggests `Tier B` is worth continued `offline-only (오프라인 전용)` exploration, but not yet as a `Tier A-equivalent (Tier A 동급)` lane
- the dominant `Tier B` holdout missing pattern still concentrates in `g4_leader_equity|g5_breadth_extension`, while a smaller but distinct `g3_macro_proxy` family remains visible
- the current working idea is to explore whether a `Tier B reduced-context model (Tier B 축약 문맥 모델)` can be useful when external-symbol context is partially absent, rather than treating all `Tier B` rows only as imputed extensions of the `Tier A` model

## Current Anchor Point (현재 고착점)
- preferred direction: one shared `Tier B reduced-context model (Tier B 공용 축약 문맥 모델)` first
- do not open three separate `Tier B subtype models (Tier B 하위 타입별 모델)` yet
- use `Tier B subtype tags (Tier B 하위 타입 태그)` for reporting and later calibration/control reads only:
  - `b_eq_dark (주식문맥 전면결손형)`
  - `b_macro_late (매크로문맥 후반결손형)`
  - `b_residual_sparse (희소 예외형)`
- working rationale: current evidence supports `subtype-aware handling (하위타입 인지형 처리)` more strongly than an immediate three-model split

## Recommended Next Session Entry (다음 세션 시작점)
- keep the work in `Stage 06 (06단계)` unless a later explicit decision changes the active stage
- start with a `Tier B-safe feature schema (Tier B 안전 피처 스키마)` draft:
  - `keep (유지)` features that remain stable without frequent `g3/g4/g5` external-symbol dependence
  - `drop (제외)` features that directly require the commonly missing external context
  - `conditional (조건부)` features that may stay only if a later reduced-context contract still supports them
- after the schema draft, evaluate whether the first `Tier B reduced-context model` should stay one shared model or split later into at most two model families

## Explicit Non-Goals (명시적 비목표)
- do not describe this anchor as `materialized evidence (물질화된 근거)` or a finalized `Stage 07 charter (Stage 07 헌장)`
- do not update `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`, or the active `selection_status.md` from this note alone
- do not treat `Tier B subtype tags` as a new official readiness boundary

## Restart Prompt (재시작 프롬프트)
- `Stage 06 continues. No official state change. Use this note as a draft-only anchor and start with the Tier B-safe feature schema for one shared Tier B reduced-context model plus subtype tags.`
