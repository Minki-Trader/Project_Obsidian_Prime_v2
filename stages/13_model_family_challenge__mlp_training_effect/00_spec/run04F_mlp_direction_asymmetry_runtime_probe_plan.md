# RUN04F MLP Direction Asymmetry Runtime Probe Plan

- hypothesis(가설): RUN04E(실행 04E)의 손상은 Tier A(티어 A) 안에서도 long/short(롱/숏) 비대칭으로 설명될 수 있다.
- decision_use(결정 용도): q90 threshold(q90 임계값)를 더 튜닝할지, 다른 MLP(다층 퍼셉트론) 가설로 갈지 정하는 참고 근거다.
- comparison_baseline(비교 기준): 같은 모델/같은 threshold(임계값)에서 long-only(롱 전용), short-only(숏 전용), both no-fallback(양방향 대체 없음)을 비교한다.
- controls(고정값): RUN04E(실행 04E) model(모델), Tier A feature matrix(Tier A 피처 행렬), q90 threshold(q90 임계값), max_hold_bars(최대 보유 봉) 9.
- threshold(임계값): `0.5919602995462544`.
- evidence_plan(근거 계획): MT5 Strategy Tester(전략 테스터), ONNX parity(ONNX 동등성), ledger(장부), report(보고서).
