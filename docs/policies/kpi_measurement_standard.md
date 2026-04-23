# KPI Measurement Standard (핵심 성과 지표 측정 표준)

This policy defines how Project Obsidian Prime v2 records KPI (`key performance indicator`, 핵심 성과 지표) evidence for run (`실행`) results. It covers measurement only; run identity and judgment live in `run_result_management.md` and `result_judgment_policy.md`.

## Core Rule

Every non-trivial reviewed or selected run must record KPI evidence in layered form before it is treated as reviewed (`검토됨`) or closed (`닫힘`). Early scout runs (`초기 스카우트 실행`) may carry partial KPI records when the missing layers are labeled.

Use `n/a` (`not applicable`, 해당 없음) with a reason when a value is unavailable. Do not leave blanks or write ambiguous `None`.

## Scoreboard Types

- `structural_scout` (`구조 탐색 점수판`): fast rule-shape read used to understand an idea, not to promote an operating line.
- `regular_risk_execution` (`정규 위험 실행 점수판`): live-like risk/execution read used for incumbent/challenger judgment.
- `wfo_oos` (`walk-forward optimization out-of-sample`, 워크포워드 표본외): rolling or staged out-of-sample evidence.
- `runtime_parity` (`런타임 동등성`): execution or feature parity evidence, not alpha performance.
- `diagnostic_special` (`특수 진단`): bounded diagnostic read with its own charter.

Do not treat a `structural_scout` winner as `operating_promotion` unless a matching `regular_risk_execution` read agrees and the remaining hard gates are closed.

## KPI Layers

Each `kpi_record.json` should use these layers when applicable:

- `headline` (`대표 성과`): `return_pct`, `net_profit`, `profit_factor`, `trade_count`, `win_rate`, `expectancy_per_trade`, `max_dd_pct`, `recovery_factor`.
- `risk` (`위험`): `max_dd_amount`, `equity_dd_pct`, `ulcer_index`, `worst_day`, `worst_week`, `time_under_water`, `longest_recovery_duration`, `consecutive_losses`, `min_free_margin`, `margin_call_proximity`.
- `diagnostics` (`진단`): `no_trade_rate`, `avg_hold`, `long_count`, `short_count`, `long_expectancy`, `short_expectancy`, `avg_win`, `avg_loss`, `payoff_ratio`, `rule_pass_rates`.
- `trade_shape` (`거래 모양`): `mfe_mean`, `mfe_median`, `mfe_p90`, `mae_mean`, `mae_median`, `mae_p90`, `realized_over_mfe`, `win_trade_mae`, `loss_trade_mfe`.
- `execution` (`실행`): `skip_rate`, `ready_row_gap`, `external_skip_pressure`, `top_skip_reasons`, `avg_spread`, `avg_slippage`, `fill_rate`, `runtime_warning_counts`, `broker_constraint_events`.
- `stability` (`안정성`): `validation_test_gap`, `profit_factor_gap`, `expectancy_gap`, `rank_consistency`, `parameter_surface_smoothness`, `subperiod_consistency`, `regime_slice_consistency`, `long_short_mix_shift`.
- `search` (`탐색`): `search_space_id`, `trial_count`, `broad_sweep_range`, `extreme_sweep_range`, `micro_search_used`, `selection_rule`, `selection_rank`.
- `parity` (`동등성`): `parity_level`, `exact_match_rate`, `max_abs_diff`, `decision_flip_rate`, `decision_flip_attribution`, `cluster_localization`, `zero_shift_share`.
- `continuity` (`연속성`): `continuous_bridge_net`, `continuous_bridge_return_pct`, `yearly_contribution`, `same_trade_count_quality_delta`, `carried_risk_delta`.

## Tier And Lane Boundaries

- Tier A (`티어 A`) KPI may become operating-promotion (`운영 승격`) evidence only after the relevant operating-promotion/runtime-authority gates close.
- Tier A KPI may still support `promotion_candidate` (`승격 후보`) comparison before those gates close when the evidence boundary is explicit.
- Tier B (`티어 B`) KPI must stay in its own exploration/reporting lane unless a later packet explicitly opens a candidate or promotion handoff through stricter gates.
- Tier C local research (`티어 C 로컬 연구`) may record indicator-only research KPI, but it is not runtime, reduced-risk, or promotion evidence.
- Runtime parity (`런타임 동등성`) KPI must not be blended into alpha performance KPI. A `runtime_probe` (`런타임 탐침`) observes behavior; `runtime_authority` (`런타임 권위`) claims closure.

## WFO And Search Accounting

WFO (`walk-forward optimization`, 워크포워드 최적화) is the default optimization evidence for exploration candidates. If WFO is absent, set `wfo_status` to `exception` or mark the result as scout-only (`탐색 전용`).

Record the search surface, trial count, and selection rule. Winner-only reporting is not sufficient evidence because it hides search breadth (`탐색 폭`) and overfit risk (`과최적화 위험`).
