# Frontier11 Experiment Design(전선11 실험 설계)

## Hypothesis(가설)

When choosing fixed 3-class ONNX candidates(고정 3분류 ONNX 후보 선택) for US100 M5, subperiod stability(하위기간 안정성), worst-slice drawdown(최악 구간 손실폭), time-under-water proxy(회복 전 체류 시간 프록시), and equity smoothness proxy(자산곡선 매끄러움 프록시) may reduce zoomed DD(확대 구간 손실폭) and curve chop(곡선 출렁임) better than aggregate validation/OOS(검증/표본밖 합계) selection.

## Decision Use(결정 사용)

Action(행동): stage-open design(단계 개방 설계)으로 다음 proxy scout(프록시 탐색)의 selection metric(선택 지표)과 대조군(control arm, 대조군)을 고정합니다.

Effect(효과): aggregate PF/density(합계 수익 팩터/밀도)만 좋은 후보가 zoomed DD(확대 구간 손실폭)를 숨기지 못하게 합니다.

## Comparison Baseline(비교 기준)

- same candidate pool aggregate-only selector(같은 후보 풀의 합계 전용 선택기)
- Frontier10 utility-margin preserved clue(전선10 효용 마진 보존 단서)
- Stage171/273 archive stability failures(171/273단계 보관소 안정성 실패)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 티어 A)
- fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)
- fixed 3-class ONNX output `[p_short, p_flat, p_long]`(고정 3분류 ONNX 출력)
- no threshold search(임계값 탐색 없음)
- no density bridge(밀도 브리지 없음)

## Changed Variables(변경 변수)

- post-fit candidate ranking(적합 후 후보 순위)
- subperiod KPI aggregation(하위기간 KPI 집계)
- worst-slice DD and TUW proxy(최악 구간 손실폭과 회복 전 체류 시간 프록시)
- trade distribution entropy(거래 분포 엔트로피)

## Sample Scope(표본 범위)

Data source(데이터 원천): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`. Tier B(티어 B) and combined(합산)은 materialized source(물질화 원천)가 없으면 `missing_required(필수 누락)`로 기록합니다.

## Success Criteria(성공 기준)

- strict scout clue(엄격 탐색 단서): validation/OOS(검증/표본밖) aggregate(합계)와 worst-slice(최악 구간) 모두 개선, DD <= 15%(손실폭 15% 이하) scout boundary(탐색 경계), density 5~10/day(일 5~10회), ONNX parity(ONNX 동등성) 통과
- preserved clue(보존 단서): aggregate selector(합계 선택기) 대비 worst-slice DD(최악 구간 손실폭), TUW proxy(회복 전 체류 시간 프록시), smoothness proxy(매끄러움 프록시) 중 2개 이상 개선

## Failure Criteria(실패 기준)

- subperiod selector(하위기간 선택기)가 validation DD(검증 손실폭)를 줄이지 못함
- aggregate PF/density(합계 수익 팩터/밀도)는 좋지만 worst-slice(최악 구간)가 악화
- selection metric(선택 지표)이 hidden threshold search(숨은 임계값 탐색)로 변질

## Invalid Conditions(무효 조건)

- validation/OOS(검증/표본밖) 정보를 model fit(모델 적합)에 사용
- subperiod slices(하위기간 구간)를 결과를 본 뒤 재정의
- missing ONNX parity(ONNX 동등성 누락)를 무시

## Evidence Plan(근거 계획)

- stage run manifest(단계 실행 목록)
- candidate summary(후보 요약)
- aggregate-only control arm(합계 전용 대조군)
- monthly/quarterly subperiod KPI(월별/분기별 하위기간 KPI)
- strict/preserved clue row definitions(엄격/보존 단서 행 정의)
- run registry and paired Tier records(실행 등록부와 티어 쌍 기록)

## Data Integrity(데이터 무결성)

- time_axis(시간축): closed US100 M5 bars(확정 US100 5분봉)
- feature_label_boundary(피처-라벨 경계): subperiod ranking(하위기간 순위)은 post-fit evaluation(적합 후 평가)만 사용
- split_boundary(분할 경계): model fit(모델 적합)은 train only(학습 전용), selector report(선택기 보고)는 validation/OOS(검증/표본밖)를 분리 기록
- leakage_risk(누수 위험): subperiod metric(하위기간 지표)을 모델 학습 목표로 되먹이는 경우
- integrity_judgment(무결성 판정): usable_with_boundary(경계 포함 사용 가능)

## Model Validation(모델 검증)

- model_family(모델군): ONNX-exportable fixed 3-class classifiers(ONNX 내보내기 가능한 고정 3분류 분류기)
- target_and_label(목표와 라벨): frozen reference label/objective family(고정 참조 라벨/목적군)
- selection_metric(선택 지표): stability-first score(안정성 우선 점수)
- threshold_policy(임계값 정책): argmax-only(최대확률 전용)
- overfit_risk(과적합 위험): candidate ranking(후보 순위)이 validation subperiod(검증 하위기간)에 과적합
- calibration_risk(보정 위험): scores are ranking evidence only(점수는 순위 근거 전용)
- validation_judgment(검증 판정): exploratory(탐색)
