# run337JF Runtime Negative Collapse Repair Candidate Training(run337JF 런타임 음수 붕괴 수리 후보 학습)

## Summary(요약)

- run_id(실행 ID): `run337JF_train_runtime_negative_collapse_cost_stress_trade_shape_repair_candidates_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JE_review_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1`
- judgment(판정): `runtime_negative_collapse_repair_candidates_trained_with_onnx_parity_and_proxy_score_review_required`
- gates(게이트): `11/11`
- trained_model_rows(학습 모델 수): `8`
- onnx_parity(ONNX 동등성): `8/8`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `4.852932238507492`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `1.1593873748454389`
- positive_inner_holdout_proxy_rows(내부 보류 프록시 양수 수): `4`

## Action(행동)

JE review(JE 입력 검토)에서 적격 판정된 8개 task seed(작업 씨앗)를 학습하고 ONNX(온엑스) 산출물과 proxy scorecard(프록시 점수표)를 만들었다.
Effect(효과): JG review(JG 검토)가 proxy usability(프록시 사용성), ONNX parity(ONNX 동등성), side/PF/drawdown/cost(방향/PF/낙폭/비용)를 함께 볼 수 있다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337JG_review_runtime_negative_collapse_cost_stress_trade_shape_repair_training_without_db_v1`에서 학습 산출물을 검토한다.
