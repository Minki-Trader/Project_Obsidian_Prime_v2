# Stage 12 Standalone ExtraTrees Training Effect

## 질문(Question, 질문)

Stage 12(12단계)는 Stage 10/11(10/11단계)을 계승하지 않는 standalone(단독) 새 모델 실험이다.

효과(effect, 효과): 기존 run(실행), threshold(임계값), context gate(문맥 제한), session slice(세션 구간), comparison baseline(비교 기준선)을 가져오지 않고 ExtraTrees(엑스트라 트리) 자체 학습 효과만 본다.

## 범위(Scope, 범위)

- model family(모델 계열): `ExtraTreesClassifier(엑스트라 트리 분류기)`
- dataset(데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- label(라벨): fwd12(60분) canonical foundation label(정식 기반 라벨)
- feature set(피처 묶음): `feature_set_v2_mt5_price_proxy_top3_weights_58_features`
- threshold method(임계값 방식): `standalone_validation_nonflat_confidence_q90`

## 명시적 비계승(Explicit Non-Inheritance, 명시적 비계승)

- Stage 10(10단계) threshold(임계값): not used(미사용)
- Stage 10(10단계) session slice(세션 구간): not used(미사용)
- Stage 11(11단계) LightGBM(라이트GBM) surface(표면): not used(미사용)
- Stage 11(11단계) fwd18 inverse context(fwd18 역방향 문맥): not used(미사용)

## 경계(Boundary, 경계)

Python structural scout(파이썬 구조 탐침)만 주장한다. MT5 runtime_probe(MT5 런타임 탐침), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 주장하지 않는다.
