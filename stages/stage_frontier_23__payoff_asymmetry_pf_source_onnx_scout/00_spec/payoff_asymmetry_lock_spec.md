# Frontier23 Payoff Asymmetry Lock Spec(전선23 보상 비대칭 잠금 명세)

Payoff metrics(보상 지표):
- avg_win_loss_ratio: mean(winning proxy pnl) / abs(mean(losing proxy pnl))
- right_tail_loss_tail_ratio: positive p90 proxy pnl / abs(negative p10 proxy pnl)
- adverse_loss_containment: conditional negative-tail loss vs unconditional same-side train baseline
- profit_factor: gross positive proxy pnl / abs(gross negative proxy pnl)

Locks(잠금):
- selection_axis: outcome_conditioned_train_payoff_distribution_first
- label_horizon: fwd12 fixed future_log_return_12
- selection_split: train_only
- forward_splits: validation_oos_read_only
- pre_scout_sanity_gate: single_condition_payoff_asymmetry_must_beat_unconditional_train_baseline
- no_lifecycle_until_seed: no lifecycle repair until proxy seed surface exists
- no_onnx_until_handoff: no model training or ONNX branch until handoff candidate exists
- f22_reference_boundary: F22 low-DD lifecycle is risk containment reference only
