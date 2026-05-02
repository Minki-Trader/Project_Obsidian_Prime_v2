# RUN04D MLP Convergence + Threshold Feasibility Plan

- hypothesis(가설): MLPClassifier(다층 퍼셉트론 분류기)는 loss curve(손실 곡선), validation score(검증 점수), probability density(확률 밀도)에서 특성이 보일 수 있다.
- decision_use(결정 용도): 다음 trading runtime handoff(거래 런타임 인계)를 열기 전에 threshold density(임계값 밀도)가 너무 마르거나 넘치는지 확인한다.
- comparison_baseline(비교 기준): Stage10/11/12(10/11/12단계) run(실행)을 쓰지 않고 Tier A/B(티어 A/B) 내부 표본만 비교한다.
- controls(고정값): 58 feature(58개 피처), fwd12 label(60분 라벨), split_v1(분할 v1), no-trade threshold(무거래 임계값) 1.01.
- changed_variables(변경값): 관찰 대상만 convergence(수렴)와 threshold feasibility(임계값 가능성)로 바꾼다.
- evidence_plan(근거 계획): convergence CSV/JSON(수렴 CSV/JSON), threshold CSV/JSON(임계값 CSV/JSON), ONNX parity(ONNX 동등성), MT5 Strategy Tester(전략 테스터) 무거래 인계, ledger(장부).
