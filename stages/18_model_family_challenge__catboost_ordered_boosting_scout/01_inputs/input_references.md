# Stage18 Input References(18단계 입력 참조)

Stage18(18단계)은 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting scout(순서 부스팅 탐색) 주제로 열린다.

효과(effect, 효과): Stage17(17단계) XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) closeout(마감)은 참고 단서로만 읽고, CatBoost(캣부스트)의 baseline(기준선)으로 쓰지 않는다.

## Available Context(사용 가능한 문맥)

- current truth(현재 진실): `docs/context/current_working_state.md`
- workspace state(작업공간 상태): `docs/workspace/workspace_state.yaml`
- model input contract(모델 입력 계약): `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`
- training label/split contract(학습 라벨/분할 계약): `docs/contracts/training_label_split_contract_fpmarkets_v2.md`
- Stage17 XGBoost closeout(17단계 XGBoost 마감): `stages/17_model_family_challenge__xgboost_regularized_boosting_scout/03_reviews/stage17_closeout_packet.md`
- Stage17 selection status(17단계 선택 상태): `stages/17_model_family_challenge__xgboost_regularized_boosting_scout/04_selected/selection_status.md`
- Stage17 closeout decision(17단계 마감 결정): `docs/decisions/2026-05-03_stage17_xgboost_dart_attribution_closeout.md`

## Guardrails(가드레일)

- Stage17(17단계)의 XGBoost(익스트림 그래디언트 부스팅) DART(드롭아웃 부스팅) 결과는 comparison reference(비교 참조)일 뿐 selected baseline(선택 기준선)이 아니다.
- Stage18(18단계)의 첫 run(실행)은 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 함께 남겨야 한다.
- CatBoost(캣부스트)는 현재 58 feature(58개 피처) 계약에서 categorical feature(범주형 피처) 장점보다 ordered boosting(순서 부스팅), symmetric tree(대칭 트리), regularization(규제) 행동을 먼저 본다.
- MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)는 Python structural scout(파이썬 구조 탐색)가 다음 후보를 줄인 뒤 별도 근거로 만든다.
