﻿# Stage 337HZ Offensive Pivot Candidate Training

## Summary

- run_id: `run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1`
- parent_run_id: `run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`
- judgment: `offensive_pivot_candidates_trained_with_onnx_parity_and_proxy_score_review_required`
- gates: `11/11`
- trained_models(학습 모델): `7`
- onnx_parity(ONNX 동등성): `7/7`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `1.3964926912813098`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `2`

## Result

HZ trained(학습) seven offensive pivot candidates(공격 전환 후보 7개) and exported(내보내기) seven ONNX(온엑스) artifacts.
Effect(효과): IA review(검토)가 model artifacts(모델 산출물), ONNX parity(ONNX 동등성), proxy trade score(프록시 거래 점수)를 같이 볼 수 있다.

## Boundary

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no runtime package(런타임 패키지 없음), no operating claim(운영 주장 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1` to review training score(학습 점수), ONNX parity(ONNX 동등성), proxy usability(프록시 활용성), and next runtime/proxy action(다음 런타임/프록시 행동).
