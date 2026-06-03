# Decision(결정): run364AR threshold-edge PF gap repair materialization(364AR 임계값 경계 PF 간극 수리 구체화)

- decision(결정): `stage364AR_open_run364AS_threshold_edge_pf_gap_repair_scout`
- action(행동): run364AQ(364AQ 실행)의 materialization queue(구체화 대기열)를 run364AS(364AS 실행) scout queue(정찰 대기열)로 바꿨다.
- effect(효과): 새 stage(단계) 분기 없이 Stage364(364단계) 안에서 threshold-edge(임계값 경계) 단서를 더 공격적으로 탐색한다.
- strict boundary(엄격 경계): no model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no runtime authority(런타임 권위 없음).
- queue(대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AR/run364AS_scout_queue.csv`
- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364AR_threshold_edge_pf_gap_repair_materialization.md`
- gate(게이트): `11/11`
