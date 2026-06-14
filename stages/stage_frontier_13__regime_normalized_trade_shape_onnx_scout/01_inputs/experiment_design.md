# Frontier13 Experiment Design(프론티어13 실험 설계)

## Hypothesis(가설)

US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) may improve the DD/density tradeoff(손실폭/빈도 상충) if trade-shape labels(거래 형상 라벨) are normalized by train-only regime buckets(학습 전용 레짐 버킷) rather than globally loosened label knobs(전역 라벨 파라미터 완화).

## Decision Use(결정 사용)

Action(행동): Frontier13B(프론티어13B) proxy scout(프록시 탐색)가 regime-normalized labels(레짐 정규화 라벨)이 F12(프론티어12)의 sparse low-DD surface(희소한 낮은 손실폭 표면)를 넓히는지 확인합니다.

Effect(효과): useful seed surface(유용한 씨앗 표면)인지 negative memory(부정 기억)인지 가릅니다.

## Control Variables(고정 변수)

- US100 M5(US100 5분봉), fixed split(고정 분할), output schema `[p_short, p_flat, p_long]`(출력 스키마)
- argmax-only signal(최대확률 전용 신호)
- no WFO/MT5 at proxy stage(프록시 단계에서 WFO/MT5 없음)

## Changed Variables(변경 변수)

- train-only regime bucket scale(학습 전용 레짐 버킷 척도)
- regime scheme(레짐 방식): session/volatility/trend/squeeze(세션/변동성/추세/압축)

## Success Criteria(성공 기준)

validation/OOS density(검증/표본밖 빈도) 5~10/day(일 5~10회), PF(수익 팩터) >= 1.2, DD(손실폭) <= 15%, positive net(양수 순손익), ONNX parity(온엑스 동등성), and better worst subperiod DD(더 나은 최악 하위기간 손실폭).

## Failure Criteria(실패 기준)

strict/preserved rows(엄격/보존 행) 0, density-only improvement(빈도만 개선), DD rise(손실폭 상승), or regime bucket overfit(레짐 버킷 과적합).
