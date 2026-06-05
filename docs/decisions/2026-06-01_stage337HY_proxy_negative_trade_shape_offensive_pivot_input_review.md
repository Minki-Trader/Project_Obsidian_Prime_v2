﻿# Decision: Stage 337HY Input Review

- date: `2026-06-01`
- run_id: `run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`
- decision: `stage337HY_open_run337HZ_proxy_negative_trade_shape_offensive_pivot_candidate_training`
- judgment: `offensive_pivot_inputs_timestamp_safe_training_ready_with_tier_b_missing_required_named`
- next_run_id: `run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1`

## Reason

HX materialization(물질화)은 label(라벨), valid flag(유효 플래그), weight(가중치), task seed(작업 씨앗), feature boundary(피처 경계)를 만들었고 HY review(검토)는 이를 통과시켰다.

## Effect

HZ training(학습)은 Tier A scoped(Tier A 범위) 공격 탐색으로 열리며, Tier B missing_required(필수 누락)는 운영 주장(operating claim, 운영 주장)을 막는 경계로 남는다.

## Boundary

`research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_no_runtime_package_no_candidate_selection_no_operating_or_goal_claim`
