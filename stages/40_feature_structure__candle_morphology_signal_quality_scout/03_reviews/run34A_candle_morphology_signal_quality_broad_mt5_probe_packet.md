# Stage40 run34A Candle Morphology Signal Quality Packet(40단계 run34A 캔들 형태 신호 품질 묶음)

- stage_id(단계 ID): `40_feature_structure__candle_morphology_signal_quality_scout`
- idea_id(아이디어 ID): `IDEA-ST40-CANDLE-MORPHOLOGY-SIGNAL-QUALITY`
- run_id(실행 ID): `run34A_candle_morphology_signal_quality_broad_mt5_probe_v1`
- packet_id(묶음 ID): `stage40_run34A_candle_morphology_signal_quality_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- claim boundary(주장 경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

## Broad Sweep(넓은 탐색)

- candidate_count(후보 수): `17`
- best_validation(검증 최상): `c07_rejection_tail_directional` net `29.36` PF `1.07`
- worst_validation(검증 최하): `c01_reference_no_candle_morphology`
- best_oos(OOS 최상): `c15_morphology_score_low_complexity` net `195.55` PF `1.1`
- worst_oos(OOS 최하): `c16_directional_morphology_score`

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `failed`
- best_candidate(최상 후보): `None`
- rule(규칙): `micro-search is allowed only when broad MT5 validation and OOS are both positive, PF>=1.05, not thin, not Tier-B-carried, and split gap is bounded`

## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)

- command used(사용 명령): `C:\Program Files\MetaTrader 5\terminal64.exe /config:C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\opv2_run34A_candle_morphology_signal_quality_broad_mt_routed_c01_reference_no_candle_morphology_validation_is.ini`
- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
- .ini path(.ini 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_structure__candle_morphology_signal_quality_scout/02_runs/run34A_candle_morphology_signal_quality_broad_mt5_probe_v1/mt5/routed_c01_reference_no_candle_morphology_validation_is.ini`
- .set path(.set 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_structure__candle_morphology_signal_quality_scout/02_runs/run34A_candle_morphology_signal_quality_broad_mt5_probe_v1/mt5/routed_c01_reference_no_candle_morphology_validation_is.set`
- manifest path(목록 경로): `stages/40_feature_structure__candle_morphology_signal_quality_scout/02_runs/run34A_candle_morphology_signal_quality_broad_mt5_probe_v1/run_manifest.json`
- terminal path(터미널 경로): `C:\Program Files\MetaTrader 5\terminal64.exe`
- Common Files path(Common Files 공용 파일 경로): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
- tester output path(테스터 출력 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/40_feature_structure__candle_morphology_signal_quality_scout/02_runs/run34A_candle_morphology_signal_quality_broad_mt5_probe_v1/mt5/reports/Project_Obsidian_Prime_v2_run34A_candle_morphology_signal_quality_broad_mt5_probe_v1_routed_c01_reference_no_candle_morphology_validation_is.htm`
- imported result path(가져온 결과 경로): `stages/40_feature_structure__candle_morphology_signal_quality_scout/02_runs/run34A_candle_morphology_signal_quality_broad_mt5_probe_v1/mt5/mt5_result_import_summary.json`
- candidates tested in MT5(MT5 후보 수): `17`

## Promotion Candidate Gate(승격 후보 게이트)

- status(상태): `failed`
- candidate_id(후보 ID): `None`
- promotion packet path(승격 묶음 경로): `None`

## Result Judgment(결과 판정)

`reviewed_completed_negative_memory_runtime_probe_only`

Stage40 run34A remains runtime_probe_only(런타임 탐침 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).
