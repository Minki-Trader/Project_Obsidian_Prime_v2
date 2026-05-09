# Stage40 run34A Volatility Squeeze Expansion Packet(40단계 run34A 변동성 수축/확장 묶음)

- stage_id(단계 ID): `40_feature_interaction__volatility_squeeze_expansion_scout`
- idea_id(아이디어 ID): `IDEA-ST40-VOLATILITY-SQUEEZE-EXPANSION`
- run_id(실행 ID): `run34A_volatility_squeeze_expansion_broad_mt5_probe_v1`
- packet_id(묶음 ID): `stage40_run34A_volatility_squeeze_expansion_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- claim boundary(주장 경계): `exploration_only_until_explicit_promotion_packet_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

## Broad Sweep(넓은 탐색)

- candidate_count(후보 수): `12`
- best_validation(검증 최상): `c07_high_vol_breakout_return_z` net `199.44` PF `1.07`
- worst_validation(검증 최하): `c01_reference_return_z_momentum`
- best_oos(OOS 최상): `c11_expansion_without_squeeze_reference` net `204.58` PF `1.09`
- worst_oos(OOS 최하): `c02_squeeze_breakout_bb_position`

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `passed`
- best_candidate(최상 후보): `c07_high_vol_breakout_return_z`
- rule(규칙): `micro-search is allowed only when broad MT5 validation and OOS are both positive, PF>=1.05, not thin, not Tier-B-carried, and split gap is bounded`
- result(결과): micro candidates(미세 후보) 6개 중 5개는 validation/OOS(검증/표본밖) MT5 KPI(KPI, 핵심성과지표) 행을 만들었다. `m01_relaxed_return_c07_high_vol_breakout_return_z` validation(검증)은 feature_csv_open_failed_5003(피처 CSV 열기 실패 5003)로 KPI 행 없이 차단됐다.

## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)

- command used(사용 명령): `C:\Program Files\MetaTrader 5\terminal64.exe /config:C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\opv2_run34A_volatility_squeeze_expansion_broad_mt5_pr_routed_c01_reference_return_z_momentum_validation_is.ini`
- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
- .ini path(.ini 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_interaction__volatility_squeeze_expansion_scout/02_runs/run34A_volatility_squeeze_expansion_broad_mt5_probe_v1/mt5/routed_c01_reference_return_z_momentum_validation_is.ini`
- .set path(.set 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_interaction__volatility_squeeze_expansion_scout/02_runs/run34A_volatility_squeeze_expansion_broad_mt5_probe_v1/mt5/routed_c01_reference_return_z_momentum_validation_is.set`
- manifest path(목록 경로): `stages/40_feature_interaction__volatility_squeeze_expansion_scout/02_runs/run34A_volatility_squeeze_expansion_broad_mt5_probe_v1/run_manifest.json`
- terminal path(터미널 경로): `C:\Program Files\MetaTrader 5\terminal64.exe`
- Common Files path(Common Files 공용 파일 경로): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
- tester output path(테스터 출력 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_interaction__volatility_squeeze_expansion_scout/02_runs/run34A_volatility_squeeze_expansion_broad_mt5_probe_v1/mt5/reports/Project_Obsidian_Prime_v2_run34A_volatility_squeeze_expansion_broad_mt5_probe_v1_routed_c01_reference_return_z_momentum_validation_is.htm`
- imported result path(가져온 결과 경로): `stages/40_feature_interaction__volatility_squeeze_expansion_scout/02_runs/run34A_volatility_squeeze_expansion_broad_mt5_probe_v1/mt5/mt5_result_import_summary.json`
- candidates tested in MT5(MT5 후보 수): `18`
- MT5 attempts/reports(MT5 시도/보고서): `36` attempts(시도), `36` Strategy Tester reports(전략 테스터 보고서), `105` KPI rows(KPI 행)
- partial blocker(부분 차단): `m01` validation(검증) micro attempt(미세 시도) 1개는 runtime_outputs.wait_status_timeout(런타임 출력 대기 시간 초과)과 feature_csv_open_failed_5003(피처 CSV 열기 실패 5003)을 기록했다.

## Promotion Candidate Gate(승격 후보 게이트)

- status(상태): `failed`
- candidate_id(후보 ID): `None`
- promotion packet path(승격 묶음 경로): `None`

## Result Judgment(결과 판정)

`reviewed_completed_negative_memory_runtime_probe_only`

Stage40 remains exploration_only_until_explicit_promotion_packet(명시 승격 묶음 전 탐색 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).
