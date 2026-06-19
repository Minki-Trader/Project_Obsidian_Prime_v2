# Decision: Stage 337HX Offensive Pivot Inputs

- date: `2026-06-01`
- run_id: `run337HX_materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`
- decision: `stage337HX_open_run337HY_proxy_negative_trade_shape_offensive_pivot_input_review`
- judgment: `timestamp_safe_offensive_pivot_inputs_materialized_review_required`
- next_run_id: `run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`

## Reason

HU/HV repair(수리)는 proxy net(프록시 순수익)을 개선했지만 여전히 negative(음수)였다.
HW는 weight-only repair(가중치만 수리)를 멈추고 offensive pivot(공격 전환)을 열었다.
HX는 그 설계를 timestamp-safe(시점 안전) input(입력)과 task seed(작업 씨앗)로 만들었다.

## Effect

다음 HY 검토(review, 검토)는 새 수익 원천 후보를 학습하기 전에 leakage(누수), tier omission(티어 누락), invalid label(무효 라벨)을 먼저 잡을 수 있다.

## Boundary

`research_development_input_materialization_only_no_model_training_no_mt5_no_runtime_package_no_operating_or_goal_claim`
