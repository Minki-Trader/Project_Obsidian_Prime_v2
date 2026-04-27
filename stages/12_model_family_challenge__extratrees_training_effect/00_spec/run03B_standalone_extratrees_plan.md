# RUN03B Standalone ExtraTrees Plan

## Intake(인입)

- active stage(활성 단계): `12_model_family_challenge__extratrees_training_effect`
- run_id(실행 ID): `run03B_et_standalone_fwd12_v1`
- standalone rule(단독 규칙): Stage 10/11(10/11단계) run artifact(실행 산출물)와 기준선(baseline, 기준선)을 쓰지 않는다.

## Experiment Design(실험 설계)

- hypothesis(가설): ExtraTrees(엑스트라 트리)를 foundation model input(기반 모델 입력)에 단독 학습하면 새 확률 표면(probability surface, 확률 표면)과 신호 밀도(signal density, 신호 밀도)를 볼 수 있다.
- decision_use(결정 용도): Stage 12(12단계)에서 standalone(단독) 새 모델 축을 더 팔 가치가 있는지 판단한다.
- comparison_baseline(비교 기준): `none(없음)`
- control_variables(통제 변수): `US100`, `M5`, canonical fwd12 label/split(정식 fwd12 라벨/분할), 58 feature MT5 price-proxy input(58개 피처 MT5 가격 대리 입력)
- changed_variables(변경 변수): model family(모델 계열) = `ExtraTreesClassifier(엑스트라 트리 분류기)`
- sample_scope(표본 범위): Tier A full-context(Tier A 전체 문맥) Python data(파이썬 데이터)
- success_criteria(성공 기준): validation/OOS(검증/표본외)에서 충분한 standalone signals(단독 신호)와 hit rate(적중률)
- failure_criteria(실패 기준): OOS(표본외) hit rate(적중률)가 약하거나 신호가 과하게 적음
- invalid_conditions(무효 조건): feature hash(피처 해시) 불일치, split(분할) 누락, 비유한값(non-finite, 비유한값)
- stop_conditions(중지 조건): MT5(메타트레이더5) 없이 운영 의미(operational meaning, 운영 의미)를 주장하지 않는다.
- evidence_plan(근거 계획): manifest(목록), KPI(핵심 성과 지표), predictions(예측), ledgers(장부), result summary(결과 요약)
