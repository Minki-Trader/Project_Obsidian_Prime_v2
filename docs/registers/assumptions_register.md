# Assumptions Register

| assumption_id | assumption | effect | status |
|---|---|---|---|
| `A-001` | existing shared window may remain `2022-08-01` through `2026-04-13` until the clean inventory confirms it | stage 01 must verify it before model work relies on it | closed_by_20260424_raw_m5_inventory |
| `A-002` | raw `time_open_unix` can be treated as direct UTC(직접 협정세계시) for US cash-session features(미국 정규장 피처) | session features(세션 피처) would use timestamp(타임스탬프) without conversion | rejected_by_20260424_time_semantics_probe |
| `A-003` | raw `time_close_unix` can remain the broker-clock alignment key(브로커 시계 정렬 키) for exact external-symbol matching(정확 외부 심볼 매칭) | feature rows can preserve exact FPMarkets cross-symbol alignment(교차 심볼 정렬) while session time is handled separately | accepted_by_2026-04-24_stage01_timestamp_policy |
| `A-004` | the first clean feature-frame target should keep the practical modeling start(실용 모델링 시작), use cash-open valid rows(정규장 유효행), and exclude partial cash-session days(부분 정규장 일자) | the first shared freeze can stay simple while broader valid-row scopes remain later candidates | accepted_by_2026-04-24_stage01_first_feature_frame_target |
