# RUN02W fwd18 Retrain MT5 Plan

## Scope

`RUN02W(실행 02W)`는 `RUN02T(실행 02T)`의 label/horizon sensitivity(라벨/예측수평선 민감도) 판독을 실제 retraining(재학습)과 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)로 확인한다.

## Hypothesis

fwd18 label horizon(90분 라벨 예측수평선)이 fwd12(60분)보다 RUN02S(실행 02S) 표면에 더 잘 맞았다면, fwd18(90분)으로 LGBM(`LightGBM`, 라이트GBM)을 다시 학습했을 때 MT5 routed total(라우팅 전체) 거래 품질이 좋아질 수 있다.

## Controls

- symbol/timeframe(심볼/시간프레임): `US100`, `M5`
- split(분할): train(학습) `2022-09-01~2024-12-31`, validation(검증) `2025-01-01~2025-09-30`, OOS(표본외) `2025-10-01~2026-04-13`
- features(피처): Stage 04(4단계) MT5 price-proxy 58 feature(58개 피처)
- session slice(시간 구간): `200 < minutes_from_cash_open <= 220`
- max hold bars(최대 보유 봉): `9`
- threshold(임계값): `short0.600_long0.450_margin0.000`

## Changed Variable

- label horizon(라벨 예측수평선): fwd12(60분)에서 fwd18(90분)으로 변경
- model seed(모델 시드): `18`

## Evidence Plan

- fwd18 training dataset(학습 데이터셋)과 model input(모델 입력) 물질화
- Tier A/Tier B(Tier A/티어 A, Tier B/티어 B) LGBM 재학습
- ONNX(`Open Neural Network Exchange`, 온닉스) probability parity(확률 동등성)
- MT5 Strategy Tester(전략 테스터) validation/OOS(검증/표본외) routed total(라우팅 전체)
- run registry(실행 등록부), alpha ledger(알파 장부), artifact registry(산출물 등록부) 기록

## Boundary

이 실행은 runtime_probe(런타임 탐침)다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.
