# Stage17 Input References(17단계 입력 참조)

Stage17(17단계)은 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) regularized boosting scout(규제 부스팅 탐색) 주제로 열린다.

효과(effect, 효과): Stage16(16단계) QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) closeout(종료 기록)은 참고 단서로만 읽고, XGBoost(익스지부스트)의 baseline(기준선)으로 쓰지 않는다.

## Available Context(사용 가능한 문맥)

- current truth(현재 진실): `docs/context/current_working_state.md`
- workspace state(작업공간 상태): `docs/workspace/workspace_state.yaml`
- model input contract(모델 입력 계약): `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`
- training label/split contract(학습 라벨/분할 계약): `docs/contracts/training_label_split_contract_fpmarkets_v2.md`
- Stage11 LightGBM closeout(11단계 LightGBM 종료): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/stage11_closeout_packet.md`
- Stage12 ExtraTrees closeout(12단계 ExtraTrees 종료): `stages/12_model_family_challenge__extratrees_training_effect/03_reviews/stage12_closeout_packet.md`
- Stage16 closeout(16단계 종료): `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/stage16_closeout_packet.md`
- Stage16 decision(16단계 결정): `docs/decisions/2026-05-03_stage16_qda_closeout_stage17_open.md`

## Guardrails(가드레일)

- Stage10/11/12/16(10/11/12/16단계)의 strong clue(강한 단서)는 comparison reference(비교 참조)일 뿐 selected baseline(선택 기준선)이 아니다.
- Stage17(17단계)의 첫 run(실행)은 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 함께 남겨야 한다.
- MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)는 Python structural scout(파이썬 구조 탐색)가 다음 후보를 줄인 뒤 별도 근거로 만든다.
