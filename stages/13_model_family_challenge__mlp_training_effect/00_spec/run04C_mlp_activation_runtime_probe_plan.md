# RUN04C MLP Activation Runtime Probe Plan

- hypothesis(가설): ReLU MLP(렐루 다층 퍼셉트론)가 Tier A/B(티어 A/B)와 validation/OOS(검증/표본외)에서 dead unit(죽은 유닛), sparsity(희소성), high activation(높은 활성화) 차이를 보일 수 있다.
- decision_use(결정 용도): MLP(다층 퍼셉트론) 내부 표현이 탐색 가치가 있는지 보는 구조 단서로만 쓴다.
- comparison_baseline(비교 기준): train split(학습 분할) 내부 활성화와 Tier A/B(티어 A/B) 요약 차이이며, Stage10/11/12(10/11/12단계) 실행은 기준선으로 쓰지 않는다.
- control_variables(고정 변수): 58 feature(58개 피처), fwd12 label(60분 라벨), split_v1(분할 v1), no-trade threshold(무거래 임계값) 1.01.
- changed_variables(변경 변수): 관찰 대상이 probability surface(확률 표면)에서 hidden activation(은닉 활성화)으로 바뀐다.
- evidence_plan(근거 계획): activation CSV/JSON(활성화 CSV/JSON), ONNX parity(ONNX 동등성), MT5 Strategy Tester(전략 테스터) 무거래 인계, ledgers(장부).

효과(effect, 효과): 거래 성과를 보지 않고 MLP(다층 퍼셉트론) 특유의 내부 표현만 얕게 확인한다.
