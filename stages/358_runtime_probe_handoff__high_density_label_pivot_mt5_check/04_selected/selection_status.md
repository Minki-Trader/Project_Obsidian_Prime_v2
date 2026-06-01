# Stage358 Selection Status(358단계 선택 상태)

- selection_status(선택 상태): `runtime_probe_package_ready_no_selection(런타임 탐침 패키지 준비, 선택 없음)`
- active_stage_id(활성 단계 ID): `358_runtime_probe_handoff__high_density_label_pivot_mt5_check`
- latest_run_id(최근 실행 ID): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- current_run_id(현재 실행 ID): `run358C_execute_high_density_label_pivot_mt5_probe_without_db_v1`
- source_stage_id(원천 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- source_run_id(원천 실행 ID): `run357B_design_high_density_label_pivot_without_db_v1`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `8`
- executable_attempt_rows(실행 가능 시도 행): `4`
- executable_queue_rows(실행 가능 대기열 행): `2`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `6`
- expected_tape_rows(예상 테이프 행): `139424`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): `pside/all(방향확률/전체 세션)` 후보만 MT5 execution attempt(MT5 실행 시도)로 열고, 나머지는 mapping gap(매핑 차이)으로 보존했다.

Effect(효과): Stage358C(358C 실행)는 바로 실행 가능한 4개 attempt(시도)를 돌리며, 지원되지 않는 score policy(점수 정책)는 별도 수리 주제로 밀어낼 수 있다.
