# Frontier10 Experiment Design(전선10 실험 설계)

## Hypothesis(가설)

A single fixed 3-class ONNX interface(고정 3분류 ONNX 인터페이스)가 train-only split-consistent utility distillation labels(학습 전용 분할 일관 효용 증류 라벨)을 배우면, 불안정하거나 DD-heavy(손실폭 큰) 행을 flat/no-trade(관망/무거래)로 보내고 밀도/PF/DD/매끄러움 네 축을 더 균형 있게 만들 수 있다.

## Decision Use(결정 사용)

Stage-open design(단계 개방 설계)입니다. Effect(효과): 다음 proxy scout(프록시 탐색)가 utility family(효용군), controls(대조군), stop conditions(중단 조건)을 어떤 경계로 가져야 하는지 고정합니다.

## Comparison Baseline(비교 기준)

- label_v1 reference(라벨 v1 참조)
- Frontier07 risk label reference(전선07 위험 라벨 참조)
- Frontier08 best sample-weight row(전선08 최상 표본 가중 행)
- Frontier09 payoff/adverse ratio preserved clue(전선09 수익/불리 이동 비율 보존 단서)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 Tier A)
- fixed 58 feature order(고정 58개 피처 순서)
- existing train/validation/OOS split(기존 학습/검증/표본밖 분할)
- fixed `[p_short, p_flat, p_long]` ONNX output(고정 ONNX 출력)
- argmax-only first scout(첫 탐색은 최대확률 전용)

## Changed Variables(변경 변수)

- train-only subwindow consensus target(학습 전용 하위구간 합의 목표)
- utility_margin target family(효용 마진 목표군)
- drawdown_veto_distillation family(손실폭 거부 증류군)
- explicit no-bridge control(명시적 무브리지 대조군)

## Sample Scope(표본 범위)

Data(데이터)는 기존 US100 M5 model input dataset(모델 입력 데이터셋)입니다. Tier B(티어 B)와 Tier A+B combined(Tier A+B 합산)는 사용 가능해지기 전까지 missing_required(필수 누락)로 기록합니다.

## Success Criteria(성공 기준)

- strict scout clue(엄격 탐색 단서): validation/OOS(검증/표본밖) 모두 density 5~10/day(일 5~10회), PF >= 1.2(수익 팩터 1.2 이상), DD <= 15%(손실폭 15% 이하), ONNX parity true(ONNX 동등성 참), paired axis improvement(짝 축 개선)
- preserved clue(보존 단서): strict clue(엄격 단서)는 없어도 3개 이상 축 개선, ONNX parity true(ONNX 동등성 참), class collapse(분류 붕괴) 없음

## Failure Criteria(실패 기준)

- validation DD(검증 손실폭)가 15%보다 크게 높고 개선 축이 없음
- density(밀도)가 2/day(일 2회) 아래로 붕괴
- Frontier09 bridge repair(전선09 브리지 수리)와 사실상 동일

## Invalid Conditions(무효 조건)

- validation/OOS(검증/표본밖) 정보를 target fit(목표 적합)에 사용
- feature-label boundary(피처-라벨 경계) 위반
- ONNX parity(ONNX 동등성) 실패를 무시

## Stop Conditions(중단 조건)

Strict clue(엄격 단서)가 없고 preserved clue(보존 단서)도 없으면 closeout(마감)으로 갑니다. Preserved clue(보존 단서)가 있으면 capped repair(상한 수리)를 한 번만 허용합니다.

## Evidence Plan(근거 계획)

- run_manifest.json(실행 목록)
- candidate summary CSV(후보 요약 CSV)
- ONNX parity audit(ONNX 동등성 감사)
- stage_run_ledger.csv(단계 실행 장부)
- alpha_run_ledger.csv(알파 실행 장부)
- required_gate_coverage_audit(필수 게이트 커버리지 감사)

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- time_axis(시간축): closed US100 M5 bars(확정 US100 5분봉), existing ordering(기존 순서)
- missing_or_duplicate_check(누락/중복 확인): next scout(다음 탐색)에서 row count/hash(행 수/해시)로 기록
- feature_label_boundary(피처-라벨 경계): future path utility(미래 경로 효용)는 label only(라벨 전용)
- split_boundary(분할 경계): train-only thresholds/scales/subwindows(학습 전용 임계값/스케일/하위구간)
- leakage_risk(누수 위험): subwindow consensus(하위구간 합의)가 validation/OOS(검증/표본밖)를 포함하는 경우
- data_hash_or_identity(데이터 해시/정체성): `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- integrity_judgment(무결성 판정): usable_with_boundary(경계 포함 사용 가능)

## Model Validation(모델 검증)

- model_family(모델군): ONNX-exportable sklearn classifiers(ONNX 내보내기 가능한 sklearn 분류기)
- target_and_label(목표와 라벨): split-consistent utility distillation(분할 일관 효용 증류)
- split_method(분할 방법): fixed train/validation/OOS(고정 학습/검증/표본밖)
- selection_metric(선택 지표): four-axis aspiration distance(네 축 목표거리)
- secondary_metrics(보조 지표): density/PF/DD/smoothness/class balance(밀도/수익 팩터/손실폭/매끄러움/클래스 균형)
- threshold_policy(임계값 정책): no threshold search(임계값 탐색 없음), argmax-only(최대확률 전용)
- overfit_risk(과적합 위험): train subwindow consensus over-selection(학습 하위구간 합의 과선택)
- calibration_risk(보정 위험): probabilities are ranking scores until calibrated(보정 전 확률은 순위 점수)
- validation_judgment(검증 판정): exploratory(탐색)
