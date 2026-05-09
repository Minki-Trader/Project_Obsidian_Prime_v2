# Stage39 run33A Exit Risk Non-Entry Overlay Packet(39단계 33A 청산 위험 비진입 덧씌움 묶음)

- stage_id(단계 ID): `39_exit_risk__non_entry_lifecycle_tail_overlay`
- idea_id(아이디어 ID): `IDEA-ST39-EXIT-RISK-NON-ENTRY-OVERLAY`
- run_id(실행 ID): `run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1`
- packet_id(묶음 ID): `stage39_run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- claim boundary(주장 경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

## Design(설계)

Entry permission(진입 허용)은 Stage38 c01 reference(38단계 c01 참고) 신호로 고정했다. Stage39 후보는 position exists(포지션 존재) 이후에만 close/reduce-hold(청산/보유 축소)를 수행한다.

## Broad Sweep(넓은 훑기)

- candidate_count(후보 수): `17`
- best_validation(검증 최상): `c11_tail_only_after_adverse_excursion_proxy`
- worst_validation(검증 최하): `c02_survival_clock_exit`
- best_oos(표본외 최상): `c06_survival_tail_exit`
- worst_oos(표본외 최하): `c12_hazard_only_after_adverse_excursion_proxy`

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `failed`
- best_candidate(최상 후보): `None`
- decision(결정): broad sweep(넓은 훑기) 뒤 조건을 통과한 후보만 micro-search(미세 탐색)를 허용한다.

## MT5 Strategy Tester Execution

- command used(사용 명령): `C:\Program Files\MetaTrader 5\terminal64.exe /config:C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\opv2_run33A_exit_risk_non_entry_overlay_broad_mt5_pro_routed_c01_no_overlay_reference_validation_is.ini`
- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
- .ini path(.ini 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/39_exit_risk__non_entry_lifecycle_tail_overlay/02_runs/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1/mt5/routed_c01_no_overlay_reference_validation_is.ini`
- .set path(.set 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/39_exit_risk__non_entry_lifecycle_tail_overlay/02_runs/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1/mt5/routed_c01_no_overlay_reference_validation_is.set`
- manifest path(목록 경로): `stages/39_exit_risk__non_entry_lifecycle_tail_overlay/02_runs/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1/run_manifest.json`
- terminal path(터미널 경로): `C:\Program Files\MetaTrader 5\terminal64.exe`
- Common Files path(공용 파일 경로): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
- tester output path(테스터 출력 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/39_exit_risk__non_entry_lifecycle_tail_overlay/02_runs/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1/mt5/reports/Project_Obsidian_Prime_v2_run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1_routed_c01_no_overlay_reference_validation_is.htm`
- imported result path(가져온 결과 경로): `stages/39_exit_risk__non_entry_lifecycle_tail_overlay/02_runs/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1/mt5/mt5_result_import_summary.json`
- candidates tested in MT5(MT5 후보 수): `17`
- validation MT5 KPI summary(검증 KPI 요약): best `c11_tail_only_after_adverse_excursion_proxy` net `698.74` PF `1.15`
- OOS MT5 KPI summary(표본외 KPI 요약): best `c06_survival_tail_exit` net `-266.79` PF `0.93`

## Result Judgment(결과 판정)

`reviewed_completed_negative_memory_runtime_probe_only`

Stage39 run33A remains runtime_probe_only: no baseline, no promotion, no runtime authority, no live readiness, and no operating reference.
