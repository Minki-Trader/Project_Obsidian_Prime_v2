# F66A Runtime Probe Coverage Inventory(런타임 탐침 커버리지 인벤토리)

Superseded note(대체 갱신 메모): F66C `frontier66C_proxy_signal_mt5_backfill_v1` later materialized(이후 물질화) F11,F15,F18-F49 proxy signal(프록시 신호) into MT5 runtime probe(런타임 탐침) handoff(인계) and executed(실행) 64/64 split runs(분할 실행). This F66A report(보고서)는 초기 inventory(인벤토리) 관찰로 보존하며 current truth(현재 진실)는 F66C 산출물을 우선한다.


- created_at_utc(생성 시각): `2026-06-16T02:49:06Z`
- audited stages(감사 단계): `F02-F64`
- actual runtime KPI stage count(실제 런타임 KPI 단계 수): `29`
- missing runtime KPI stage count(런타임 KPI 누락 단계 수): `34`
- status materialized or reused(상태 물질화 또는 재사용): `34`
- claim boundary(주장 경계): `runtime_probe_backfill_gap_audit_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Stage Sets(단계 묶음)

- actual runtime KPI present(실제 런타임 KPI 있음): `F02-F10, F12-F14, F16-F17, F50-F64`
- actual runtime KPI missing(실제 런타임 KPI 누락): `F11, F15, F18-F49`
- missing KPI with raw runtime material(런타임 재료는 있으나 KPI 누락): `F15, F18-F19`
- missing KPI without raw runtime material(런타임 재료도 없는 KPI 누락): `F11, F20-F49`
- actual KPI present but gap report missing(실제 KPI는 있으나 간극 보고 누락): `F02-F10, F12-F14, F16-F17`

## Missing Runtime KPI Detail(런타임 KPI 누락 상세)

| stage(단계) | materialization(물질화) | ONNX(온엑스) | joblib(잡리브) | closeout tokens(마감 토큰) |
|---:|---|---:|---:|---|
| F11 | invalid_setup_no_runtime_material | 0 | 0 | invalid_setup, no ONNX, negative_memory |
| F15 | missing_artifact_blocked | 9 | 9 | missing_artifact, blocked, negative_memory |
| F18 | invalid_setup_no_runtime_material | 3 | 3 | no_runtime_handoff_candidate, invalid_setup, negative_memory |
| F19 | invalid_setup_no_runtime_material | 6 | 0 | no_runtime_handoff_candidate, invalid_setup, negative_memory |
| F20 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F21 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F22 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F23 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F24 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F25 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, blocked, negative_memory |
| F26 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup |
| F27 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F28 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, blocked, negative_memory |
| F29 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, blocked, negative_memory |
| F30 | invalid_setup_no_runtime_material | 0 | 0 | invalid_setup, no ONNX, blocked, negative_memory |
| F31 | invalid_setup_no_runtime_material | 0 | 0 | invalid_setup, no ONNX, negative_memory |
| F32 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F33 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F34 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F35 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F36 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F37 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F38 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F39 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F40 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F41 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F42 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F43 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F44 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F45 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F46 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F47 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F48 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |
| F49 | invalid_setup_no_runtime_material | 0 | 0 | runtime_probe_ineligible, invalid_setup, negative_memory |

## Effect(효과)

이 인벤토리는 runtime probe(런타임 탐침)가 없던 단계를 무조건 백테스트 성공/실패로 섞지 않고, 먼저 실행 가능한 material(재료)과 EA-compatible candidate contract(EA 호환 후보 계약)가 있는지로 분리한다. F15/F18/F19는 raw material(원 재료)은 있으나 실행 계약 또는 handoff candidate(인계 후보)가 불명확/부적격이고, 나머지 누락 stage(단계)는 raw runtime material(원 런타임 재료)도 없다. 그래서 이번 감사에서 새 MT5 KPI(MT5 핵심 성과 지표)를 추가로 뽑을 수 있는 executable candidate(실행 가능 후보)는 발견되지 않았다.
