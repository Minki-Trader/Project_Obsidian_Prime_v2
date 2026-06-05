# run337IX Positive Low-Edge Expansion Candidate Training(run337IX 양수 낮은 엣지 확장 후보 학습)

## Summary(요약)

- run_id(실행 ID): `run337IX_train_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_candidates_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IW_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db_v1`
- judgment(판정): `positive_low_edge_expansion_candidates_trained_with_onnx_parity_and_proxy_score_review_required`
- gates(게이트): `11/11`
- trained_model_rows(학습 모델 수): `7`
- onnx_parity(ONNX 동등성): `7/7`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `4.124490419405447`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `1.1338998246730707`
- positive_inner_holdout_proxy_rows(내부 보류 프록시 양성 행): `4`

## Action(행동)

IW review(IW 검토)에서 적격 판정된 7개 task seed(작업 씨앗)를 학습하고 ONNX(온엑스) 산출물과 proxy scorecard(프록시 점수표)를 만들었다.
Effect(효과): IY review(IY 검토)가 proxy usability(프록시 활용성), ONNX parity(ONNX 동등성), cost/side/PF/drawdown/equity(비용/방향/PF/낙폭/수익곡선)를 함께 볼 수 있다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IY_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_training_without_db_v1`에서 학습 산출물을 검토한다.
