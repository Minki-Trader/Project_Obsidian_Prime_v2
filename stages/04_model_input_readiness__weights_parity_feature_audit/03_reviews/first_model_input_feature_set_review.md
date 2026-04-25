# First Model Input Feature Set Review

## 판독(Read, 판독)

`20260425_model_input_feature_set_v1_no_placeholder_top3_weights` 실행(run, 실행)은 `placeholder_equal_weight(임시 동일가중)` 문제를 56 feature(56개 피처) interim model input(임시 모델 입력)에서 격리했다.

쉽게 말하면, 원천 training dataset(학습 데이터셋)은 보존하고, 첫 모델에게 실제로 줄 입력 파일에서는 임시 가중치 피처를 뺐다.

단, 이 파일은 final pre-alpha path(최종 알파 전 경로)가 아니다. 이후 정식 Stage 04(4단계) 경로는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 만든 뒤 58 feature(58개 피처) 입력을 다시 물질화하는 것으로 닫았다.

## 핵심 수치(Key Numbers, 핵심 수치)

- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights`
- source_training_dataset_id(원천 학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- rows(행 수): `46650`
- source feature count(원천 피처 수): `58`
- included feature count(포함 피처 수): `56`
- included feature order hash(포함 피처 순서 해시): `84f313815393429acb9690d727b61b4a3dfd2354678bd357a53db570ba37bc89`
- model input dataset SHA256(모델 입력 데이터셋 SHA256): `68d70d3fa2969b1e8c257c9cbe57428440832229d48446d5b84477da931b233d`
- model input summary SHA256(모델 입력 요약 SHA256): `af79872a96e2ecb6b1363df192528cee0d1b7997e0bdeaac48a4a5237c7d6f70`

## 격리된 피처(Quarantined Features, 격리된 피처)

- `top3_weighted_return_1`
- `us100_minus_top3_weighted_return_1`

이유(reason, 이유): top3 weight source(top3 가중치 원천)가 `placeholder_equal_weight(임시 동일가중)` 상태다.

효과(effect, 효과): 임시 동일가중 가정이 조용히 모델 입력에 섞이지 않는다.

## 분할 보존(Split Preservation, 분할 보존)

- train rows(학습 행): `29222`
- validation rows(검증 행): `9844`
- OOS rows(표본외 행): `7584`

label/split(라벨/분할)은 Stage 03(3단계) 산출물과 동일하게 유지했다.

## 코드 배치 판독(Code Placement Read, 코드 배치 판독)

- owner_module(소유 모듈): `foundation/pipelines/materialize_model_input_dataset.py`
- caller(호출자): Stage 04 evidence run(근거 실행)
- input_contract(입력 계약): Stage 03 training dataset(학습 데이터셋) + model input feature set contract(모델 입력 피처 세트 계약)
- output_contract(출력 계약): model input dataset(모델 입력 데이터셋), feature set manifest(피처 세트 목록), quarantine manifest(격리 목록), run evidence(실행 근거)
- artifact_or_report_relation(산출물/보고서 관계): 무거운 데이터 파일(heavy data files, 무거운 데이터 파일)은 로컬에 두고, 정체성(identity, 정체성)과 해시(hash, 해시)는 Git 추적 문서에 남긴다.
- monolith_risk(단일파일 위험): 낮음. 이 파일은 feature selection/quarantine(피처 선택/격리)만 담당하고 model training(모델 학습)이나 parity(동등성)를 소유하지 않는다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

`not_applicable(해당 없음)`

이 실행(run, 실행)은 pure Python artifact materialization claim(순수 파이썬 산출물 물질화 주장)만 다룬다. MT5 execution(MT5 실행), strategy tester(전략 테스터), runtime parity(런타임 동등성)를 주장하지 않으므로 외부 검증(external verification, 외부 검증)이 필요하지 않다.

## 남은 일(Remaining Work, 남은 일)

- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 계약과 산출물
- 58 feature(58개 피처) model input(모델 입력) 재물질화
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)와 58 feature(58개 피처) 정식 경로 관계 기록
- Stage 05(5단계) feature/time/external/label audit(피처/시간/외부/라벨 감사) 인계

## 경계(Boundary, 경계)

이 검토(review, 검토)는 model-input readiness(모델 입력 준비도)의 임시 격리 항목을 닫는다.

아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
