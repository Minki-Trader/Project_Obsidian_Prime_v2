# Stage41 run35A Directional Asymmetric Label/Horizon Packet(41단계 run35A 방향 비대칭 라벨/수평선 묶음)

- stage_id(단계 ID): `41_label_horizon__directional_asymmetric_return_target_rebuild`
- idea_id(아이디어 ID): `IDEA-ST41-DIRECTIONAL-ASYMMETRIC-LABEL-HORIZON`
- run_id(실행 ID): `run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1`
- packet_id(묶음 ID): `stage41_run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- claim boundary(주장 경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

## Label Designs(라벨 설계)

- families(계열): current reference(현재 참조), asymmetric horizon(비대칭 수평선), flat band(무거래 구간), volatility normalized(변동성 정규화), session adjusted(세션 조정), direction pressure(방향 압박), simple rebuilt-label models(단순 재구축 라벨 모델)
- leakage audit(누수 감사): label-only future returns(라벨 전용 미래 수익률)만 만들고 model features(모델 피처)에는 미래 열을 넣지 않음

## Broad Sweep(광범위 탐색)

- candidate_count(후보 수): `17`
- best_validation(검증 최상): `c12_long_only_label_pressure_test` net `211.3` PF `1.09`
- worst_validation(검증 최하): `c11_direction_specific_threshold_label`
- best_oos(OOS 최상): `c10_session_adjusted_label` net `199.07` PF `1.22`
- worst_oos(OOS 최하): `c13_short_only_label_pressure_test`

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `failed`
- best_candidate(최상 후보): `None`
- rule(규칙): `micro-search requires positive validation and OOS, PF>=1.05, non-thin counts, usable label distribution, bounded gap, no Tier B carry, and label/horizon mechanism`

## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)

- command used(사용 명령): `C:\Program Files\MetaTrader 5\terminal64.exe /config:C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\opv2_run35A_directional_asymmetric_label_horizon_broa_routed_c01_current_label_reference_validation_is.ini`
- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
- .ini path(.ini 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/41_label_horizon__directional_asymmetric_return_target_rebuild/02_runs/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1/mt5/routed_c01_current_label_reference_validation_is.ini`
- .set path(.set 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/41_label_horizon__directional_asymmetric_return_target_rebuild/02_runs/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1/mt5/routed_c01_current_label_reference_validation_is.set`
- manifest path(목록 경로): `stages/41_label_horizon__directional_asymmetric_return_target_rebuild/02_runs/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1/run_manifest.json`
- terminal path(터미널 경로): `C:\Program Files\MetaTrader 5\terminal64.exe`
- Common Files path(Common Files 공용 파일 경로): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
- tester output path(테스터 출력 경로): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/41_label_horizon__directional_asymmetric_return_target_rebuild/02_runs/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1/mt5/reports/Project_Obsidian_Prime_v2_run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1_routed_c01_current_label_reference_validation_is.htm`
- imported result path(가져온 결과 경로): `stages/41_label_horizon__directional_asymmetric_return_target_rebuild/02_runs/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1/mt5/mt5_result_import_summary.json`
- candidates tested in MT5(MT5 후보 수): `17`

## Promotion Candidate Gate(승격 후보 게이트)

- status(상태): `failed`
- candidate_id(후보 ID): `None`
- promotion packet path(승격 묶음 경로): `None`

## Result Judgment(결과 판정)

`reviewed_completed_negative_memory_runtime_probe_only`

Stage41 run35A remains runtime_probe_only(런타임 탐침 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).
