﻿# Stage 337HX Proxy-Negative Offensive Pivot Inputs

## Summary

- run_id: `run337HX_materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`
- parent_run_id: `run337HW_design_proxy_negative_trade_shape_offensive_pivot_without_db_v1`
- judgment: `timestamp_safe_offensive_pivot_inputs_materialized_review_required`
- gates: `13/13`
- rows: `87666`
- task_seed_rows: `7`

## What Changed

HW design(설계)을 HX input materialization(입력 물질화)으로 바꿨다.
효과는 fwd6/fwd18/fwd24 label(라벨), active-flat target(능동/평탄 타깃), side/regime weight(방향/국면 가중치), HY task seed(작업 씨앗)를 검토 가능한 산출물로 남긴 것이다.

## Tier Records

- Tier A separate(Tier A 분리): materialized(물질화), `87666` rows.
- Tier B separate(Tier B 분리): missing_required(필수 누락).
- Tier A+B combined(Tier A+B 합산): missing_required(필수 누락).

## Boundary

No model training(모델 학습 없음), no MT5(메타트레이더5) run(실행 없음), no runtime package(런타임 패키지 없음), no operating claim(운영 주장 없음).

## Next

Open `run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1` to review(검토) label validity(라벨 유효성), feature boundary(피처 경계), tier records(티어 기록), lineage(계보), and training guard(학습 보호조건).
