# Frontier29 Experiment Design(전선29 실험 설계)

- hypothesis(가설): A train-loss-conditioned veto mask, applied after reconstructing the F28/F27 same-side union masks, may reduce loss concentration and leave smoother forward PF/DD/density reads.
- decision_use(결정 사용처): decide whether train-loss veto masks deserve proxy scout, repair, or handoff consideration
- comparison_baseline(비교 기준): F28B 234 stability union surface is reference-only input, not inherited baseline
- control_variables(통제 변수): US100 M5 Tier A dataset, feature_set_v2 58 features, fwd12 label horizon, F28/F27 same-side OR-union semantics, validation/OOS read-only
- changed_variables(변경 변수): train_loss_conditioned_veto_mask, loss_capture_ratio, removed_train_trade_fraction
- sample_scope(표본 범위): Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split
- success_criteria(성공 기준): {"scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal", "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10", "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass", "not_completion": "final_goal_gates_not_applicable_until_final_completion_review"}
- failure_criteria(실패 기준): zero scout, seed, and handoff rows under frozen train-loss veto contract, apparent forward improvement only from density thinning, train loss concentration does not reduce while forward metrics move
- invalid_conditions(무효 조건): validation/OOS used for veto threshold or rank selection, veto contract edited after reading forward results, generic feature-veto replay without loss concentration metrics, feature hash mismatch
- stop_conditions(중단 조건): handoff rows >0 triggers pre-expensive Grok before ONNX/MT5/WFO, seed or scout only triggers repair-or-closeout decision, zero seed and zero handoff after capped repair closes negative memory
- evidence_plan(근거 계획): F29B variant ledger(변형 장부), before/after density(전후 밀도), train loss capture(학습 손실 포착), read-only forward summary(읽기 전용 전진 요약), run registry(실행 등록부), stage ledger(단계 장부).
