# Frontier12 Experiment Design(프론티어12 실험 설계)

## Hypothesis(가설)

US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) can reduce validation/OOS DD(검증/표본밖 손실폭) only if the label source(라벨 원천) encodes a trade lifecycle(거래 생명주기): early adverse excursion veto(초기 불리 이동 배제), favorable path confirmation(유리 경로 확인), capped hold duration(상한 보유 기간), MAE/MFE quality(최대 불리/유리 이동 품질), and density-aware neutral(빈도 인식 중립) before model fitting(모델 적합 전).

## Decision Use(결정 사용)

Action(행동): this stage-open packet(이 단계 개방 묶음)은 Frontier12B(프론티어12B) proxy scout(프록시 탐색)의 label contract(라벨 계약), data boundary(데이터 경계), and success/failure boundary(성공/실패 경계)를 고정합니다.

Effect(효과): early exploration(초기 탐색)은 자유롭게 하되 completion(완성)이나 baseline(기준선)처럼 말하지 않습니다.

## Control Variables(고정 변수)

- instrument/timeframe(종목/시간봉): FPMarkets US100 M5(FPMarkets US100 5분봉)
- split policy(분할 정책): existing fixed train/validation/OOS(기존 고정 학습/검증/표본밖)
- output schema(출력 스키마): `[p_short, p_flat, p_long]`
- signal policy(신호 정책): argmax-only(최대확률 전용)
- no WFO/MT5 at stage-open(단계 개방에서 WFO/MT5 없음)

## Changed Variables(변경 변수)

- label source(라벨 원천)
- trade lifecycle definition(거래 생명주기 정의)
- neutral class construction(중립 클래스 구성)
- train-only label knob registration(학습 전용 라벨 파라미터 등록)

## Scout Success Boundary(탐색 성공 경계)

- validation and OOS density(검증과 표본밖 빈도): 5_to_10(일 5~10회)
- validation and OOS PF(검증과 표본밖 수익 팩터): >=1.2_scout_floor(탐색 바닥)
- validation and OOS DD(검증과 표본밖 손실폭): <=15_percent_scout_boundary(탐색 경계)
- net profit(순손익): positive(양수)
- ONNX parity(온엑스 동등성): required_for_model_rows(모델 행 필수)

## Failure Boundary(실패 경계)

Strict rows(엄격 행) 0 and preserved rows(보존 행) 0, high validation DD floor(높은 검증 손실폭 바닥), or repeated repair without novelty(신규성 없는 반복 수리)는 negative memory(부정 기억) 또는 capped repair(상한 수리)로 닫습니다.

## Data Integrity(데이터 무결성)

Feature-label boundary(피처-라벨 경계)는 closed bar features(확정 봉 피처)와 future path label(미래 경로 라벨)을 분리합니다. Train-only materialization(학습 전용 물질화)은 validation/OOS metrics(검증/표본밖 지표)를 라벨 파라미터 선택에 쓰지 않습니다.

## Model Validation(모델 검증)

Model rows(모델 행)는 ONNX parity(온엑스 동등성), aggregate KPI(합계 KPI), subperiod KPI(하위기간 KPI), and paired Tier record(짝 티어 기록)를 가져야 합니다. Effect(효과): one-axis illusion(한 축 착시)을 줄입니다.
