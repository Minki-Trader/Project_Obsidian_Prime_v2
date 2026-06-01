# Stage357 Input Refs(357단계 입력 참조)

- source_final_decision(원천 최종 결정): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/final_decision.json`
- source_best_scorecard(원천 최선 점수표): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/best_expansion_scorecard.csv`
- source_mt5_probe_queue(원천 MT5 탐침 대기열): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/mt5_probe_candidate_queue.csv`
- source_gate_audit(원천 게이트 감사): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/required_gate_coverage_audit.csv`
- source_regression_sweep(원천 회귀 탐색): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/regression_density_sweep_scorecard.csv`
- source_union_sweep(원천 합집합 탐색): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/union_density_sweep_scorecard.csv`
- source_onnx_parity(원천 온엑스 동등성): `stages/356_density_recovery_training__proxy_model_queue_scout/02_runs/run356C/onnx_regression_parity_matrix.csv`
- input_manifest(입력 목록): `stages/357_high_density_label_pivot__trade_frequency_recovery/01_inputs/stage357_input_manifest.csv`

Action(행동): Stage356C(356C 실행)의 큰 02_runs(실행 산출물) 파일은 hash/manifest(해시/목록)로 연결하고, Stage357(357단계)은 작은 state sync(상태 동기화) 산출물만 추적한다.

Effect(효과): 무거운 proxy artifact(프록시 산출물)를 다시 커밋하지 않고도 Stage357B(357B 실행)가 같은 source identity(원천 정체성)를 재사용할 수 있다.
