# Stage 06 First Scorecard Review (첫 점수표 리뷰)

## Identity (식별 정보)
- reviewed_on: `2026-04-21`
- stage: `06_tiered_readiness_exploration`
- dataset_id: `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`
- scorecard_id: `scorecard_fpmarkets_v2_tiered_readiness_0001`
- report_id: `report_fpmarkets_v2_tiered_readiness_0001`
- readiness_policy_ref: `docs/policies/tiered_readiness_exploration.md@2026-04-20`
- readiness_decision_ref: `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md@2026-04-20`

## Boundary Read (경계 판독)
- strict `Tier A` (엄격 `Tier A`) remains the only current runtime rule (실행 규칙) and is unchanged by this scorecard (점수표)
- `Tier B` (부분 준비도 `Tier B`) is exploration-only (탐색 전용) and stays on the separate `tier_b_exploration` reporting lane (보고 레인)
- `Tier C` (스킵 준비도 `Tier C`) remains a skip classification (스킵 분류) rather than a reporting lane (보고 레인)
- no operating promotion (운영 승격) is claimed by this materialized scorecard (물질화 점수표)
- additional helper-lane or broader-lane evidence remains an open question (열린 질문)

## Shared Window (공유 구간)
- start: `2022-08-01`
- end_inclusive: `2026-04-13`
- row_count: `261344`
- tier_counts: `tier_a=56988|tier_b=88303|tier_c=116053`
- lane_counts: `strict_tier_a=56988|tier_b_exploration=88303|null=116053`
- top_missing_groups: `g5_breadth_extension=190434|g4_leader_equity=190431|g3_macro_proxy=126987|g2_session_semantics=12490`
- top_missing_symbols: `NVDA.xnas=190387|MSFT.xnas=189484|META.xnas=189482|TSLA.xnas=189482|GOOGL.xnas=189481|AMD.xnas=189466|AMZN.xnas=189461|AAPL.xnas=189459`

## Practical Window (실전 구간)
- start: `2022-09-01`
- end_inclusive: `2026-04-13`
- row_count: `255001`
- tier_counts: `tier_a=55457|tier_b=86192|tier_c=113352`
- lane_counts: `strict_tier_a=55457|tier_b_exploration=86192|null=113352`
- top_missing_groups: `g4_leader_equity=185826|g5_breadth_extension=185826|g3_macro_proxy=124328|g2_session_semantics=12039`
- top_missing_symbols: `NVDA.xnas=185791|MSFT.xnas=184925|TSLA.xnas=184921|META.xnas=184919|GOOGL.xnas=184918|AMD.xnas=184903|AMZN.xnas=184902|AAPL.xnas=184900`

## Notes (메모)
- this pass materializes row-level labels (행 단위 라벨), a machine-readable summary (기계가독 요약), and a review report (리뷰 보고서) only
- no reduced-risk runtime family (축소위험 런타임 계열) is materialized in this pass
- the placeholder weights table (임시 가중치 테이블) remains in force, so future counts may change if a real monthly-weight source replaces it
