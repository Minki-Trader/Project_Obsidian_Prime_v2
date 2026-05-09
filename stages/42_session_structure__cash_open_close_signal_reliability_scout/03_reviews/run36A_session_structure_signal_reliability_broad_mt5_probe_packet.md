# Stage42 run36A Session Structure Signal Reliability Packet(42단계 run36A 세션 구조 신호 신뢰도 묶음)

- stage_id(단계 ID): `42_session_structure__cash_open_close_signal_reliability_scout`
- idea_id(아이디어 ID): `IDEA-ST42-SESSION-STRUCTURE-SIGNAL-RELIABILITY`
- run_id(실행 ID): `run36A_session_structure_signal_reliability_broad_mt5_probe_v1`
- packet_id(묶음 ID): `stage42_run36A_session_structure_signal_reliability_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- claim boundary(주장 경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

## Session Designs(세션 설계)

- buckets(버킷): cash open 0-30(정규장 개장 0-30), early 30-60(초반 30-60), morning 60-120(오전 60-120), midday 120-240(중반 120-240), late 240-330(후반 240-330), close 330-390(마감 330-390), overnight/unmapped(야간/미매핑)
- timezone rule(시간대 규칙): broker-clock key(브로커 시계 키)를 Europe/Athens(유럽/아테네)로 보고 UTC event time(UTC 사건 시각)으로 변환해 진단한다.

## Broad Sweep(넓은 탐색)

- candidate_count(후보 수): `17`
- best_validation(검증 최상): `c06_cash_close_reliability` net `206.57` PF `2.53`
- worst_validation(검증 최하): `c02_session_feature_low_complexity`
- best_oos(OOS 표본외 최상): `c08_exclude_weak_session_bucket` net `239.33` PF `1.13`
- worst_oos(OOS 표본외 최하): `c02_session_feature_low_complexity`

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `failed`
- best_candidate(최상 후보): `None`
- rule(규칙): `micro-search requires positive validation and OOS, PF>=1.05, non-thin counts, non-pathological session distribution, per-session attribution, no Tier B carry, no cluster concentration, and session/time mechanism`

## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)

- command used(사용 명령): `C:\Program Files\MetaTrader 5\terminal64.exe /config:C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\opv2_run36A_session_structure_signal_reliability_broa_routed_c01_validation_is.ini`
- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
- .ini path(.ini 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/42_session_structure__cash_open_close_signal_reliability_scout/02_runs/run36A_session_structure_signal_reliability_broad_mt5_probe_v1/mt5/routed_c01_validation_is.ini`
- .set path(.set 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/42_session_structure__cash_open_close_signal_reliability_scout/02_runs/run36A_session_structure_signal_reliability_broad_mt5_probe_v1/mt5/routed_c01_validation_is.set`
- manifest path(목록 경로): `stages/42_session_structure__cash_open_close_signal_reliability_scout/02_runs/run36A_session_structure_signal_reliability_broad_mt5_probe_v1/run_manifest.json`
- terminal path(터미널 경로): `C:\Program Files\MetaTrader 5\terminal64.exe`
- Common Files path(Common Files 공용 파일 경로): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
- tester output path(테스터 출력 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/42_session_structure__cash_open_close_signal_reliability_scout/02_runs/run36A_session_structure_signal_reliability_broad_mt5_probe_v1/mt5/reports/Project_Obsidian_Prime_v2_run36A_session_structure_signal_reliability_broad_mt5_probe_v1_routed_c01_validation_is.htm`
- imported result path(가져온 결과 경로): `stages/42_session_structure__cash_open_close_signal_reliability_scout/02_runs/run36A_session_structure_signal_reliability_broad_mt5_probe_v1/mt5/mt5_result_import_summary.json`
- candidates tested in MT5(MT5 후보 수): `17`

## Promotion Candidate Gate(승격 후보 게이트)

- status(상태): `failed`
- candidate_id(후보 ID): `None`
- promotion packet path(승격 묶음 경로): `None`

## Result Judgment(결과 판정)

`reviewed_completed_negative_memory_runtime_probe_only`

Stage42 run36A remains runtime_probe_only(런타임 탐침 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).
