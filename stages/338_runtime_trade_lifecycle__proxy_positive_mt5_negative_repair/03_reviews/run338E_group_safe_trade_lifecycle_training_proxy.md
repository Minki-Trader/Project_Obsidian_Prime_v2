# run338E Group-Safe Training Proxy(묶음 안전 학습 프록시)

## Summary(요약)

- run_id(실행 ID): `run338E_train_runtime_trade_lifecycle_repair_models_group_safe_without_db_v1`
- status(상태): `completed_stage338E_group_safe_trade_lifecycle_training_proxy_onnx_no_selection`
- judgment(판정): `onnx_models_trained_proxy_scored_review_required_no_mt5_no_selection`
- gates(게이트): `10/10`
- train_rows(학습 행): `70131`
- holdout_rows(홀드아웃 행): `17481`
- features(피처): `53`
- models(모델): `3`
- best_model(최고 프록시 모델): `logreg_balanced_c025`
- best_proxy_net_log_return(최고 프록시 순로그수익): `0.2140180738`
- best_proxy_profit_factor(최고 프록시 수익 팩터): `1.39846904`
- next_run(다음 실행): `run338F_review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db_v1`

## Action(행동)

run338D(338D 실행)의 group-safe split(묶음 안전 분할)과 training feature schema(학습 피처 스키마)만 사용해 sklearn(사이킷런) 모델을 학습하고 ONNX(온엑스)로 변환했다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 전에 proxy(프록시)로 볼 수 있는 ONNX(온엑스) 산출물이 생겼다.

## Evidence(근거)

- model scorecard(모델 점수표): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/run338E_model_scorecard.csv`
- proxy threshold grid(프록시 임계값 표면): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/run338E_proxy_threshold_grid.csv`
- ONNX parity audit(온엑스 동등성 감사): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/run338E_onnx_parity_audit.csv`
- feature order(피처 순서): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/run338E_feature_order.csv`
- next queue(다음 대기열): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/run338F_proxy_review_queue.csv`

## Boundary(경계)

run338E(338E 실행)는 training/proxy evaluation(학습/프록시 평가)이다. Candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
