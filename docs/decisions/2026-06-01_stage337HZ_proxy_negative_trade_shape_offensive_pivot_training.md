﻿# Decision: Stage 337HZ Candidate Training

- date: `2026-06-01`
- run_id: `run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1`
- decision: `stage337HZ_open_run337IA_review_offensive_pivot_training`
- judgment: `offensive_pivot_candidates_trained_with_onnx_parity_and_proxy_score_review_required`
- next_run_id: `run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1`

## Reason

HY review(검토)가 HX input(입력)을 training-ready(학습 준비)로 열었으므로 HZ는 LightGBM(라이트GBM), ExtraTrees(엑스트라트리스), XGBoost(엑스지부스트) 후보를 학습했다.

## Effect

다음 IA review(검토)는 proxy(프록시)가 좋아 보이는 후보가 있어도 MT5(메타트레이더5) KPI(핵심 성과 지표)로 오해하지 않고, ONNX parity(ONNX 동등성)와 proxy score(프록시 점수)를 분리해 판정한다.

## Boundary

`research_development_candidate_training_only_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_no_forward_no_runtime_package_no_operating_or_goal_claim`
