# Stage 06 Tier B Robustness Read (Stage 06 Tier B 강건성 판독)

## Identity (식별 정보)
- reviewed_on: `2026-04-22`
- followup_pack_id: `followup_pack_fpmarkets_v2_tier_b_0001`

## Missing-Pattern Read (결손 패턴 판독)
- `validation` / `g3_macro_proxy`: `row_count=2156`, `row_share=0.135888`, `log_loss=3.142515`, `macro_f1=0.288660`, `balanced_accuracy=0.350201`
- `validation` / `g4_leader_equity|g5_breadth_extension`: `row_count=13710`, `row_share=0.864112`, `log_loss=2.322189`, `macro_f1=0.350454`, `balanced_accuracy=0.393827`
- `holdout` / `g3_macro_proxy`: `row_count=1699`, `row_share=0.094504`, `log_loss=2.663845`, `macro_f1=0.315516`, `balanced_accuracy=0.357785`
- `holdout` / `g4_leader_equity|g5_breadth_extension`: `row_count=16278`, `row_share=0.905440`, `log_loss=1.890656`, `macro_f1=0.338034`, `balanced_accuracy=0.370660`
- `holdout` / `g5_breadth_extension`: `row_count=1`, `row_share=0.000056`, `log_loss=0.000000`, `macro_f1=0.333333`, `balanced_accuracy=0.333333`

## Month Read (월별 판독)
- `validation` / `2025-01`: `row_count=1498`, `log_loss=2.663751`, `macro_f1=0.332283`
- `validation` / `2025-02`: `row_count=1408`, `log_loss=2.353663`, `macro_f1=0.307531`
- `validation` / `2025-03`: `row_count=2356`, `log_loss=2.479276`, `macro_f1=0.300677`
- `validation` / `2025-04`: `row_count=3101`, `log_loss=3.139607`, `macro_f1=0.350487`
- `holdout` / `2025-09`: `row_count=1559`, `log_loss=1.653676`, `macro_f1=0.329991`
- `holdout` / `2025-10`: `row_count=2995`, `log_loss=1.416093`, `macro_f1=0.365199`
- `holdout` / `2025-11`: `row_count=1848`, `log_loss=2.434072`, `macro_f1=0.326129`
- `holdout` / `2025-12`: `row_count=2356`, `log_loss=1.497004`, `macro_f1=0.335696`

## Draft Evidence Sufficiency Read (초안 근거 충분성 판독)
- observed_missing_pattern_count: `{'validation': 2, 'holdout': 3}`
- dominant_holdout_pattern: `g4_leader_equity|g5_breadth_extension`
- dominant_holdout_pattern_share: `0.905440`
- stage05_carry_forward_read: `current broader_0002 + helper_0001 + broader_0003 evidence remains sufficient for continued offline Tier B exploration, but the follow-up pack still does not authorize MT5-path work or operating promotion`

## Notes (메모)
- the dominant Tier B missing pattern still comes from `g4_leader_equity|g5_breadth_extension`, so the current Tier B read should not be described as a fully balanced subgroup family
- this report is still enough to move the open question into a durable artifact instead of leaving it as chat-only intent (채팅 전용 의도)
