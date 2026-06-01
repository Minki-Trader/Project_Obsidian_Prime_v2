# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- canonical_stage_id(정식 단계 ID): `358_runtime_probe_handoff__high_density_label_pivot_mt5_check`
- current_run_id(현재 실행 ID): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run358A_branch_stage357_to_runtime_probe_handoff_without_db_v1`
- source_stage_id(원천 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- source_run_id(원천 실행 ID): `run357B_design_high_density_label_pivot_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run357C_package_high_density_label_pivot_mt5_probe_without_db_v1`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_runtime_probe_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Stage357B(357B 실행)의 high-density H12 classifier proxy queue(고밀도 H12 분류기 프록시 대기열)를 MT5 package/runtime probe(MT5 패키지/런타임 탐침)로 옮기고, proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 의미 있게 비교할 수 있는가?

## Source Truth(원천 진실)

- trained_models(학습 모델): `12`
- onnx_parity_rows(온엑스 동등성 행): `12/12`
- threshold_sweep_rows(임계값 스윕 행): `6912`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `8`
- best_model_id(최선 모델 ID): `run357B_d04_h12_q45_55_high_density_band__extratrees_cls_depth5_leaf100_seed11`
- best_validation_trade_per_day(최선 검증 일별 거래수): `3.191256830601093`
- best_validation_stress_pf(최선 검증 압박 수익 팩터): `1.0468369083281632`
- best_oos_trade_per_day(최선 표본외 일별 거래수): `3.4427480916030535`
- best_oos_stress_pf(최선 표본외 압박 수익 팩터): `1.0837603236717956`
- candidate_gate(후보 게이트): `passed_proxy_mt5_probe_queue(프록시 MT5 탐침 대기열 통과)`

## Scope(범위)

Stage358(358단계)는 package/handoff/runtime probe(패키지/인계/런타임 탐침), proxy-to-MT5 attribution(프록시 대 MT5 귀속), runtime parity gap(런타임 동등성 차이) 기록을 다룬다. 새 model training(모델 학습)이나 새 proxy scout(프록시 탐색)는 이 단계의 기본 작업이 아니다.

## Next Work(다음 작업)

- next_run_id(다음 실행 ID): `run358B_package_high_density_label_pivot_mt5_probe_without_db_v1`
- primary_family(주 작업군): `runtime_backtest(런타임 백테스트)`
- required_boundary(필수 경계): MT5 execution evidence(MT5 실행 근거)가 없으면 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)를 주장하지 않는다.

Action(행동): MT5 probe(MT5 탐침) 작업을 새 단계로 분리한다.

Effect(효과): proxy scout(프록시 탐색) 기록과 runtime verification(런타임 검증) 기록이 섞이지 않고, 다음 회차가 패키지와 실행 근거만 좁게 다룰 수 있다.
