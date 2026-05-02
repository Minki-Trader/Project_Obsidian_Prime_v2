# RUN04A MLP Characteristic Runtime Probe Plan

- run_id(실행 ID): `run04A_mlp_characteristic_runtime_probe_v1`
- purpose(목적): MLP model(다층 퍼셉트론 모델)의 얕은 특성 탐색과 좁은 MT5 runtime probe(MT5 런타임 탐침)를 함께 본다.
- independence(독립성): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않는다.
- depth(깊이): coarse characteristic scout(거친 특성 탐색)만 수행한다.
- MT5 view(MT5 보기): Tier A used(Tier A 사용), Tier B fallback used(Tier B 대체 사용), actual routed total(실제 라우팅 전체)을 기록한다.

효과(effect, 효과): 첫 작업에서 Python-only(파이썬만) 판독으로 끝내지 않고, Strategy Tester(전략 테스터) 반응까지 좁게 확인한다.
