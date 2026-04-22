# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-23_stage07_tier_b_dual_verdict_packet_adopted`
- `reviewed_on`: `2026-04-23`
- `owner`: `codex + user`
- `decision`: adopt the first `Stage 07 Tier B dual verdict packet (Stage 07 Tier B 이중 판정 팩)` as the current bounded alpha-search packet so the repo can answer both `separate lane survival (별도 레인 생존)` and `MT5 feasibility candidate handoff (MT5 가능성 후보 이관)` on a validated user-weight rerun without changing the current strict Tier A runtime rule (엄격 Tier A 런타임 규칙)

## What Was Decided

- adopted:
  - the first `Stage 07 packet (Stage 07 팩)` is no longer the generic first alpha-search pack; it is now the first `Tier B dual verdict packet (Tier B 이중 판정 팩)`
  - require one validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)` before this packet may produce a durable verdict
  - reuse the current shared `keep42 reduced-context surface (keep42 축약 문맥 표면)` rather than opening a new model family in this packet
  - keep the dual verdict fields explicit as `separate_lane_verdict (별도 레인 판정)` and `mt5_candidate_verdict (MT5 후보 판정)`
  - keep `mt5_candidate_verdict=yes` limited to `next-stage candidate only (차기 단계 후보 전용)` meaning
- not adopted:
  - any opened `MT5 path (MT5 경로)` work in the same packet
  - any changed `Tier A runtime rule (Tier A 런타임 규칙)`
  - any `macro-aware variant (매크로 인지 변형)` before the dual-verdict packet exists
  - any promoted operating-line claim (승격 운영선 주장)

## Why

- the shared `keep42 reduced-context model (keep42 축약 문맥 모델)` is already materialized and gives Stage 07 a bounded surface that can be rerun honestly on a validated user-weight source
- the current `placeholder monthly weights (임시 월별 가중치)` file is still insufficient as a durable source boundary for the first `MT5 feasibility candidate (MT5 가능성 후보)` read
- the current active surface is weight-neutral on its direct inputs because `top3_weighted_return_1` and `us100_minus_top3_weighted_return_1` stay outside the shared keep42 active set, so the rerun is mainly about source-boundary closure rather than a new feature-surface search
- this packet keeps Stage 07 narrow enough that the next durable answer is a yes or no verdict rather than a broad search family

## What Remains Open

- the actual `user-weight rerun (사용자 가중치 재실행)` has not been materialized yet
- the first durable `separate_lane_verdict` and `mt5_candidate_verdict` remain open until that rerun exists
- an optional `macro-aware variant (매크로 인지 변형)` remains downstream-only and should be reconsidered only after this packet closes

## Operational Meaning

- `active_stage changed?`: `no`
- `current strict Tier A runtime rule changed?`: `no`
- `Stage 07 packet narrowed?`: `yes`
- `validated user-weight source now required for the first Stage 07 verdict?`: `yes`
- `opened MT5 path claimed?`: `no`
- `workspace_state result-level update needed?`: `yes, but only when the dual-verdict question closes; this pass only syncs the narrowed Stage 07 packet framing and open-question wording`
- `artifact_registry.csv update needed?`: `no, because this pass narrows the active Stage 07 packet but does not yet materialize a new dataset, bundle, runtime, or report artifact under the Stage 07 run root`
