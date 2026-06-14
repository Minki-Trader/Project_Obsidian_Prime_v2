# Frontier30 Experiment Design(전선30 실험 설계)

- hypothesis(가설): A train-density-preserving preselector, computed only on train split source-union diagnostics before loss veto, can reduce the density-thinning failure mode that made F29 scout rows zero.
- decision_use(결정 사용처): decide whether density-preserving preselection deserves proxy scout, repair, or handoff consideration
- comparison_baseline(비교 기준): F28/F29 surfaces are reference-only clues, not inherited baselines
- control_variables(통제 변수): US100 M5 Tier A dataset, feature_set_v2 58 features, fwd12 label horizon, F28/F29 source-union semantics as reference only, validation/OOS read-only
- changed_variables(변경 변수): train_density_preserving_preselector_before_loss_veto, train_density_margin, loss_capture_per_removed_trade, density_thinning_penalty
- sample_scope(표본 범위): Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split
- success_criteria(성공 기준): {"scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal", "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10", "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass", "not_completion": "final_goal_gates_not_applicable_until_final_completion_review"}
- failure_criteria(실패 기준): zero scout, seed, and handoff rows under frozen density-preserving preselector contract, apparent forward improvement only from validation/OOS-targeted density tuning, density preservation keeps trades but PF/DD does not improve enough for scout clue
- invalid_conditions(무효 조건): validation/OOS used for preselector threshold or rank selection, F29 veto thresholds relaxed to rescue near_scout rows, exit-shape pivot activated in F30B proxy, feature hash mismatch
- stop_conditions(중단 조건): handoff rows >0 triggers pre-expensive Grok before ONNX/MT5/WFO, seed or scout only triggers repair-or-closeout decision, zero seed and zero handoff after capped repair closes negative memory
- evidence_plan(근거 계획): F30B preselector ledger(사전 선택기 장부), before/after density(전후 밀도), train-only rank inputs(학습 전용 순위 입력), read-only validation/OOS summary(읽기 전용 검증/표본외 요약), runtime probe status(런타임 탐침 상태).
