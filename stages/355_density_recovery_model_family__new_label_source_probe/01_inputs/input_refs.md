# Stage355 Input Refs(355단계 입력 참조)

- source_final_decision(원천 최종 결정): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/final_decision.json`
- source_sweep(원천 스윕): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/expanded_outcome_horizon_sweep.csv`
- source_queue(원천 대기열): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/density_valid_queue.csv`
- source_failure_memory(원천 실패 기억): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/failure_memory.csv`

Action(행동): Stage354C(354C 실행)의 current truth(현재 진실)와 failure memory(실패 기억)를 입력으로 고정한다.

Effect(효과): 다음 실행이 같은 threshold-only search(임계값 전용 탐색)를 반복하지 않게 한다.
