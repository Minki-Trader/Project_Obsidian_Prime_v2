# Stage359 Input Refs(359단계 입력 참조)

- parent_stage(부모 단계): `358_runtime_probe_handoff__high_density_label_pivot_mt5_check`
- parent_run(부모 실행): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- source_model_run(원천 모델 실행): `run357B_design_high_density_label_pivot_without_db_v1`
- next_run(다음 실행): `run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1`

## Durable Inputs(지속 입력)

- final_decision(최종 결정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/final_decision.json`
- attempt_package(시도 패키지): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/runtime_probe_attempt_package.csv`
- expected_tape(예상 테이프): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/expected/proxy_expected_tape.csv`
- expected_tape_index(예상 테이프 색인): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/expected/proxy_expected_tape_index.csv`
- tester_sets(테스터 설정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/tester_set_manifest.csv`
- tester_inis(테스터 ini 설정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/tester_ini_manifest.csv`
- mapping_audit(매핑 감사): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/runtime_mapping_audit.csv`

Action(행동): Stage359A(359A 실행)는 Stage358B(358B 실행) 입력의 hash(해시)와 consumer(소비자)를 `handoff_manifest.csv`에 기록한다.

Effect(효과): Stage359B(359B 실행)가 같은 source package(원천 패키지)를 쓴다는 lineage(계보)를 확인할 수 있다.
