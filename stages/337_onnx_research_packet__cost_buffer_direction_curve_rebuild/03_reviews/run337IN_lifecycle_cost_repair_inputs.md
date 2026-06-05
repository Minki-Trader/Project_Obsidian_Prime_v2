# run337IN Lifecycle Cost Repair Inputs(run337IN 생명주기 비용 수리 입력)

## Summary(요약)

- run_id(실행 ID): `run337IN_materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IM_design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_without_db_v1`
- judgment(판정): `timestamp_safe_lifecycle_cost_trade_shape_repair_inputs_materialized_review_required`
- gates(게이트): `11/11`
- rows(행): `87666`
- feature_count(피처 수): `58`
- new_weight_count(새 가중치 수): `7`
- task_seed_rows(작업 씨앗 행): `7`
- max_weight_saturation_rate(최대 가중치 포화율): `0.0006159742659639998`

## Action(행동)

IM design(설계)을 받아 train-only weight(학습 전용 가중치) 7개와 task seed(작업 씨앗) 7개를 만들었다.
Effect(효과): lifecycle/cost/side/drawdown(생명주기/비용/방향/낙폭) 수리 후보를 학습 전 검토할 수 있게 했다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IO_review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db_v1`에서 input review(입력 검토)를 수행한다.
