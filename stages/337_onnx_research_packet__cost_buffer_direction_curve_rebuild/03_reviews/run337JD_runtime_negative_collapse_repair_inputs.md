# run337JD Runtime Negative Collapse Repair Inputs(run337JD 런타임 음성 붕괴 수리 입력)

## Summary(요약)

- run_id(실행 ID): `run337JD_materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JC_design_runtime_negative_collapse_cost_stress_trade_shape_repair_without_db_v1`
- judgment(판정): `timestamp_safe_runtime_negative_collapse_repair_inputs_materialized_review_required`
- gates(게이트): `13/13`
- rows(행): `87666`
- feature_count(피처 수): `58`
- weight_count(가중치 수): `8`
- target_valid_rows(목표 유효 행): `87612`
- task_seed_rows(작업 씨앗 행): `8`

## Action(행동)

JC design(JC 설계)을 JD input frame(JD 입력 프레임), train-only label/weight(학습 전용 라벨/가중치), task seed(작업 씨앗)로 물질화했다.
Effect(효과): MT5 negative collapse(MT5 음성 붕괴)를 다음 JE review(JE 검토)와 JF training(JF 학습)의 실제 입력으로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
