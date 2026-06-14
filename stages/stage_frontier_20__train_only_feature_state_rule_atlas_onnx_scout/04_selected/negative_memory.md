# Frontier20 Negative Memory(전선20 부정 기억)

Negative memory(부정 기억): `train_only_depth2_rule_atlas_alone_does_not_reduce_dd_or_create_runtime_handoff(학습 전용 깊이2 규칙 지도 단독은 손실폭을 충분히 줄이거나 런타임 인계를 만들지 못함)`

Why failed(실패 이유): strict/handoff(엄격/인계) count is `0/0`, DD(손실폭)는 약 14~33% 범위로 남았고 capped train-risk rerank(상한 학습 위험 재순위)는 OOS PF(표본외 수익 팩터)를 1 미만으로 악화했습니다.

Do not repeat(반복 금지): same train-only depth-2 atlas rerank(같은 학습 전용 깊이2 지도 재순위)를 F20 안에서 반복하지 않습니다.

Reopen condition(재개 조건): DD containment mechanism(손실폭 억제 메커니즘)이나 runtime representation(런타임 표현)이 바뀌는 새 가설에서만 참고합니다.
