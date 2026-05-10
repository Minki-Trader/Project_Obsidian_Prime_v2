# run42A_survivor_cluster_concentration_scout_v1 Packet

- stage_id: `48_robustness_attribution__survivor_cluster_concentration_scout`
- judgment: `reviewed_completed_inconclusive_concentration_attribution_scout_only`
- source candidate count: `42`
- source MT5 rows: `84`
- concentration rows: `84`
- supported candidate count: `1`
- concentration risk candidate count: `39`
- best combined-net candidate: `m03_low_trade_guard_c02_top8_stability_ranked_elasticnet` from Stage `43`
- best combined-net validation/OOS net: `563.28` / `308.75`
- claim boundary: `attribution_scout_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Stage48 is an attribution scout. It checks signal-level concentration by month, week, day, UTC session bucket, volatility bucket, ADX bucket, and Tier B fallback share.

Trade-level PnL clustering is not claimed because the tracked repo has Stage43-47 KPI ledgers and packet summaries, not the full heavy trade-level report artifacts.
