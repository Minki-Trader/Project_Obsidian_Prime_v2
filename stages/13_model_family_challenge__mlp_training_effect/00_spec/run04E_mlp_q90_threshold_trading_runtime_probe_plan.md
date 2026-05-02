# RUN04E MLP Q90 Threshold Trading Runtime Probe Plan

- hypothesis(가설): RUN04D(실행 04D)의 q90 threshold(90분위 임계값)를 거래로 붙이면 MLP(다층 퍼셉트론)의 거래 모양을 볼 수 있다.
- decision_use(결정 용도): 다음 탐색 방향을 정하는 참고 근거이며 threshold selection(임계값 선택)이 아니다.
- controls(고정값): RUN04D(실행 04D) model(모델), 58 feature(58개 피처), split_v1(분할 v1), max_hold_bars(최대 보유 봉) 9.
- thresholds(임계값): Tier A `0.5919602995462544`, Tier B fallback `0.4895868680769523`.
- evidence_plan(근거 계획): MT5 Strategy Tester(전략 테스터), ONNX parity(ONNX 동등성), ledger(장부), report(보고서).
