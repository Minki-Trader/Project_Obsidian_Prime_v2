# Stage356 Input Refs(356단계 입력 참조)

- source_final_decision(원천 최종 결정): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/final_decision.json`
- source_training_queue(원천 학습 대기열): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/run355C_training_queue.csv`
- tracked_training_queue_ref(추적 학습 대기열 참조): `stages/356_density_recovery_training__proxy_model_queue_scout/01_inputs/run356B_training_queue_ref.csv`
- feature_label_table(피처 라벨 표): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/feature_label_table.csv`
- label_variant_manifest(라벨 변형 목록): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/label_variant_manifest.csv`
- label_distribution(라벨 분포): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/label_distribution.csv`
- materialization_summary(물질화 요약): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355B/materialization_summary.csv`
- input_manifest(입력 목록): `stages/356_density_recovery_training__proxy_model_queue_scout/01_inputs/stage356_input_manifest.csv`

Action(행동): Stage355B(355B 실행)의 무거운 02_runs(실행 산출물) 파일은 hash(해시)와 manifest(목록)로 연결하고, Stage356(356단계)에는 작은 queue ref(대기열 참조)를 추적한다.

Effect(효과): 대형 feature_label_table(피처 라벨 표)을 커밋하지 않아도 다음 학습 실행이 어떤 입력을 써야 하는지 재현할 수 있다.
