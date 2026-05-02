# Stage 14 Margin Kernel Training Effect(14단계 마진 커널 학습 효과)

Stage14(14단계)는 SVM(`Support Vector Machine`, 서포트 벡터 머신) 계열의 margin/kernel(마진/커널) 학습 특성을 독립 주제로 얕게 탐색한다.

- independence(독립성): Stage10/11/12/13(10/11/12/13단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않는다.
- depth(깊이): 깊은 최적화가 아니라 SVM(서포트 벡터 머신) 특성이 잘 보이는 구조만 확인한다.
- first planned run(첫 예정 실행): `run05A_svm_margin_kernel_characteristic_scout_v1`.

효과(effect, 효과): 모델 계열의 decision boundary(결정 경계), margin geometry(마진 기하), probability calibration(확률 보정) 특성을 edge search(거래 우위 탐색)와 분리해서 기록한다.

## Experiment Design(실험 설계)

- hypothesis(가설): margin/kernel(마진/커널) 학습은 LogReg(로지스틱 회귀), LightGBM(라이트GBM), ExtraTrees(엑스트라 트리), MLP(다층 퍼셉트론)와 다른 확률 모양과 신호 밀도 흔적을 남길 수 있다.
- decision_use(결정 용도): Stage14(14단계) 안에서 shallow follow-up(얕은 후속 탐색)을 할지, 다른 모델 계열로 넘어갈지 판단한다.
- comparison_baseline(비교 기준): 거래 baseline(기준선)은 없다. 같은 Stage14(14단계) 안에서 만든 변형끼리만 비교한다.
- control_variables(고정 변수): `US100 M5`, `label_v1_fwd12`, `split_v1`, Tier A/B paired reporting(Tier A/B 쌍 보고), 기존 MT5(`MetaTrader 5`, 메타트레이더5) 인계 규칙.
- changed_variables(변경 변수): linear SVM(선형 서포트 벡터 머신), calibrated linear margin(보정된 선형 마진), kernel approximation(커널 근사), probability shape(확률 모양).
- sample_scope(표본 범위): Stage02/03/04(2/3/4단계)에서 닫힌 58 feature(58개 피처) 모델 입력과 train/validation/OOS(학습/검증/표본외) 분할.
- success_criteria(유용 근거): validation/OOS(검증/표본외)에서 margin(마진), entropy(엔트로피), signal density(신호 밀도)가 설명 가능한 방식으로 유지된다.
- failure_criteria(실패 근거): 신호가 지나치게 희박하거나, 한 split(분할)에만 몰리거나, 확률 보정이 validation/OOS(검증/표본외)에서 무너진다.
- invalid_conditions(무효 조건): Stage10/11/12/13(10/11/12/13단계) threshold/context(임계값/문맥)을 기준선처럼 가져오거나, 첫 실행 전 운영 의미를 주장한다.
- stop_conditions(중지 조건): 첫 coarse scout(거친 탐색)가 SVM(서포트 벡터 머신) 고유 흔적을 거의 못 보이면 Stage14(14단계)를 빠르게 닫거나 다른 모델 주제로 전환한다.
- evidence_plan(근거 계획): stage run ledger(단계 실행 장부), project alpha ledger(프로젝트 알파 장부), run registry(실행 등록부), run manifest(실행 목록), probability/margin report(확률/마진 보고), 필요 시 MT5 runtime_probe(MT5 런타임 탐침).

## Boundary(경계)

Stage14(14단계) 개방은 설계 상태다. baseline(기준선), alpha quality(알파 품질), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다.
