# Stage18 CatBoost Ordered Boosting Scout(18단계 캣부스트 순서 부스팅 탐색)

## Status(상태)

Stage18(18단계)은 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서 부스팅) 주제로 열린다.

효과(effect, 효과): Stage17(17단계) XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 단서를 baseline(기준선)으로 쓰지 않고, CatBoost(캣부스트)의 symmetric tree(대칭 트리), ordered boosting(순서 부스팅), Bayesian bootstrap(베이지안 부트스트랩)이 probability shape(확률 모양), signal density(신호 밀도), Tier B fallback(티어 B 대체) 행동을 다르게 만드는지 본다.

## Experiment Design(실험 설계)

- hypothesis(가설): CatBoost(캣부스트)의 ordered boosting(순서 부스팅)과 symmetric tree(대칭 트리) 구조가 XGBoost(익스트림 그래디언트 부스팅) DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)와 다른 calibration(보정), coverage(포괄률), direction balance(방향 균형)를 만들 수 있다.
- decision_use(결정 사용처): Stage18(18단계)에서 CatBoost(캣부스트)를 coarse characteristic scout(거친 특성 탐색), MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), 또는 조기 closeout(마감) 중 어디로 보낼지 판단한다.
- comparison_baseline(비교 기준): 운영 baseline(기준선)은 없다. 비교는 닫힌 data/label/split/model input contract(데이터/라벨/분할/모델 입력 계약)와 Stage17(17단계) XGBoost(익스트림 그래디언트 부스팅) 보존 단서에만 제한한다.
- control_variables(고정 변수): FPMarkets `US100` `M5`, 58 feature(58개 피처) model input(모델 입력), fwd12(60분) label(라벨), split contract(분할 계약), Tier A/B paired reporting(Tier A/B 쌍 보고)을 유지한다.
- changed_variables(변경 변수): CatBoostClassifier(캣부스트 분류기) model family(모델 계열), boosting_type(부스팅 유형), tree depth(트리 깊이), learning rate(학습률), l2 leaf regularization(잎 L2 규제), random strength(무작위 강도), bootstrap setting(부트스트랩 설정)을 흔든다.
- sample_scope(표본 범위): Stage04(4단계) 58-feature audited model input(감사된 58피처 모델 입력)과 Stage03(3단계) label/split contract(라벨/분할 계약)을 사용한다.
- success_criteria(성공 기준): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)에서 CatBoost(캣부스트) 특유의 확률 분포나 방향 균형이 다음 run(실행)을 정할 만큼 반복된다.
- failure_criteria(실패 기준): CatBoost(캣부스트) 고유 축이 보이지 않거나, validation/OOS(검증/표본외) 한쪽만 튀거나, Stage17(17단계) XGBoost(익스트림 그래디언트 부스팅) 실패 구조를 그대로 반복하면 negative memory(부정 기억)로 남긴다.
- invalid_conditions(무효 조건): Stage17(17단계) run(실행)을 baseline(기준선)으로 가져오거나, categorical feature handling(범주형 피처 처리)을 실제 58 feature(58개 피처) 계약에 없는 장점처럼 주장하거나, Tier B(티어 B)와 combined(합산) 기록을 생략하면 무효다.
- stop_conditions(중지 조건): coarse scout(거친 탐색)와 필요한 attribution follow-up(귀속 후속) 뒤에도 CatBoost-specific axis(캣부스트 고유 축)가 보이지 않으면 Stage18(18단계)을 닫는다.
- evidence_plan(근거 계획): 첫 후보는 `run12A_catboost_ordered_boosting_characteristic_scout_v1`이며, run_manifest(실행 목록), prediction tables(예측표), stage/project ledgers(단계/프로젝트 장부), state_sync_audit(상태 동기화 감사), skill receipts(스킬 영수증)를 남긴다.

## Boundary(경계)

- selected topic(선택 주제): CatBoost ordered boosting scout(캣부스트 순서 부스팅 탐색)
- current run(현재 실행): 없음
- selected operating reference(선택 운영 기준): none(없음)
- selected promotion candidate(선택 승격 후보): none(없음)
- selected baseline(선택 기준선): none(없음)

효과(effect, 효과): Stage18(18단계)은 CatBoost(캣부스트) 주제를 선택했지만, 아직 run(실행), model artifact(모델 산출물), KPI(`Key Performance Indicator`, 핵심 성과 지표), alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
