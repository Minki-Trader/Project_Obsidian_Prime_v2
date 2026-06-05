# run337IH Runtime Positive Repair Candidate Training(run337IH 런타임 양수 수리 후보 학습)

## Summary(요약)

- run_id(실행 ID): `run337IH_train_runtime_positive_low_pf_drawdown_side_balance_repair_candidates_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IG_review_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db_v1`
- status(상태): `completed_stage337IH_runtime_positive_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `runtime_positive_repair_candidates_trained_with_onnx_parity_and_proxy_score_review_required`
- gates(게이트): `11/11`
- trained_models(학습 모델): `6`
- onnx_parity(ONNX 동등성): `6/6`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순익): `0.4754999014553505`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `1`

## Action(행동)

IG에서 적격 판정된 6개 작업을 학습하고 ONNX(온엑스) 산출물을 만들었다.
Effect(효과): II review(II 검토)가 proxy usability(프록시 활용성), ONNX parity(ONNX 동등성), side/PF/drawdown/cost(방향/PF/낙폭/비용)를 함께 볼 수 있다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no runtime package authority(런타임 패키지 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337II_review_runtime_positive_low_pf_drawdown_side_balance_repair_training_without_db_v1`에서 학습 결과를 검토한다.
