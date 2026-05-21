# Stage267 run267BF MT5 Tester Unique Report Repair(267BF MT5 테스터 고유 보고서 수리)

## Summary(요약)

- run_id(실행 ID): `run267BF_stage267_mt5_tester_unique_report_repair_v1`
- parent_run(상위 실행): `run267BE_stage267_mt5_tester_start_diagnostic_v1`
- status(상태): `run267BF_mt5_tester_unique_report_repair_q02_runtime_report_completed`
- judgment(판정): `unique_report_profile_repaired_tester_start_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BD(267BD 실행)의 q02 adjacent-period replacement(q02 인접 기간 대체)를 fresh unique Report(새 고유 보고서) profile(프로필)로 다시 실행했다.
Effect(효과): 이전 blocker(차단)가 candidate weakness(후보 약점)가 아니라 stale report/profile handoff(낡은 보고서/프로필 인계) 문제였는지 분리했다.

## Result Read(결과 판독)

- report_name(보고서명): `Project_Obsidian_Prime_v2_run267BF_q02_unique_202202`
- tester_returncode(테스터 반환 코드): `0`
- tester_start_found(테스터 시작 확인): `True`
- runtime_status(런타임 상태): `completed`
- runtime_wait(런타임 대기): `completed`
- report_status(보고서 상태): `completed`
- net_profit(순수익): `104.75`
- profit_factor(수익 팩터): `1.16`
- trade_count(거래 수): `212`
- max_drawdown(최대 손실폭): `None`

## Interpretation(해석)

Unique Report(고유 보고서) profile(프로필)에서는 q02(큐 02)가 tester start(테스터 시작), runtime output(런타임 출력), strategy report(전략 보고서)까지 이어졌다.
Effect(효과): run267BD(267BD 실행)의 `kpi_records=0`은 q02 feature/model(피처/모델) 자체 실패로 판정하지 않고, fresh report/profile(새 보고서/프로필) 정책을 적용한 다음 batch(묶음)를 다시 실행해야 한다.

이 run(실행)은 수리 검증(repair verification, 수리 검증)이다.
Effect(효과): q02(큐 02) 숫자는 다음 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)의 입력 후보일 수 있지만, selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)를 만들지는 않는다.

## Forensics(포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간봉) `M5`, model(모델링) `4`, date range(날짜 범위) `2025.01.02` to `2025.07.01`.
- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hashes(모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/repair_result.json`에 기록했다.
- report_identity(보고서 정체성): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/reports_manifest.csv`.
- trade_evidence(거래 근거): strategy report(전략 보고서) metrics(지표)와 runtime summary(런타임 요약)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/repair_result.json`에 기록했다.
- cost_assumptions(비용 가정): source ini/set(원천 초기화/설정) 그대로 사용했고, 이 run(실행)은 비교 판정이 아니라 tester start(테스터 시작) 수리 검증이다.
- forensic_checks(포렌식 확인): unique Report(고유 보고서), tester start log(테스터 시작 로그), telemetry/summary(텔레메트리/요약), report artifact(보고서 산출물).
- backtest_judgment(백테스트 판정): `unique_report_profile_repaired_tester_start_no_candidate_selection`.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/execution_result.json`.
- runtime_path(런타임 경로): set(설정) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/mt5/prepared_sets/q02_rep_trend_strength_adjacent_2025_h1_validat.set`, profile(프로필) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/mt5/profiles/Project_Obsidian_Prime_v2_run267BF_q02_unique_202202.ini`.
- shared_contract(공유 계약): q02 feature/model path(q02 피처/모델 경로), feature order hash(피처 순서 해시), MT5 US100 M5 tester settings(MT5 US100 M5 테스터 설정).
- known_differences(알려진 차이): Report(보고서) 이름만 fresh unique(새 고유) 값으로 바꿨다.
- parity_check(동등성 확인): tester start log(테스터 시작 로그), runtime CSV handoff(런타임 CSV 인계), strategy report(전략 보고서).
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only(전용), no authority(권위 없음).

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BE_mt5_tester_start_diagnostic.md`.
- producer(생산자): `stage_pipelines/stage267/run267BF_mt5_tester_unique_report_repair.py`.
- consumer(소비자): `run267BG_execute_remaining_adjacent_period_replacement_with_fresh_report_profiles`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/repair_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/diagnostic_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/runtime_output_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BF/mt5_tester_unique_report_repair/reports_manifest.csv`.
- registry_links(등록부 연결): `docs/registers/run_registry.csv`, `docs/registers/alpha_run_ledger.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage_run_ledger.csv`, `docs/registers/artifact_registry.csv`.
- availability(가용성): `tracked_for_repo_artifacts_external_profile_context_recorded`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Next Action(다음 행동)

`run267BG_execute_remaining_adjacent_period_replacement_with_fresh_report_profiles`

Effect(효과): remaining adjacent-period replacement(남은 인접 기간 대체) batch(묶음)를 fresh report/profile(새 보고서/프로필) 정책으로 다시 실행해 KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice(시간구간), trade quality(거래 품질)를 검토할 수 있게 한다.

## Boundary(경계)

이 run(실행)은 selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
