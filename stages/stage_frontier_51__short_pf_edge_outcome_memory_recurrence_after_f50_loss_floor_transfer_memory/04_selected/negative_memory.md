# F51 Negative Memory(부정 기억)

F51 closes as `negative_memory`(부정 기억).

Do not repeat(반복 금지): train-only outcome-memory recurrence(학습 전용 결과 기억 재발) + `outcome_memory_recurrence_decay_q86_w12_36` + single-position order-path proxy(단일 포지션 주문 경로 프록시)를 primary lever(주 레버)로 다시 밀지 않는다.

Why(이유):
- proxy(프록시)는 scout/seed/runtime(탐색/씨앗/런타임) 후보를 만들지 못했다.
- representative(대표) `f51c_0046`도 density(밀도) 2.66~3.0/day로 목표 5~10/day보다 낮았다.
- MT5 runtime probe(MT5 런타임 탐침)는 signal_diff=0, feature_ready_diff=0으로 handoff parity(인계 동등성)는 맞았지만, validation_is PF=0.78/DD=86.37%, OOS PF=0.86/DD=50.15%로 무너졌다.
- proxy/runtime gap(프록시/런타임 차이)은 validation DD +81.88, OOS DD +47.27로 F50의 order-path collapse(주문 경로 붕괴)를 반복했다.

Next useful question(다음 유용 질문): model input surface(모델 입력 표면)를 더 비트는 대신 MT5 order path/cost/fill/position constraint(주문 경로/비용/체결/포지션 제약)를 직접 다룬다.
