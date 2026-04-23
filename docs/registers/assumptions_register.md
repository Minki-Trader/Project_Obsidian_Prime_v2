# Assumptions Register

| assumption_id | assumption | effect | status |
|---|---|---|---|
| `A-001` | existing shared window may remain `2022-08-01` through `2026-04-13` until the clean inventory confirms it | stage 01 must verify it before model work relies on it | closed_by_20260424_raw_m5_inventory |
| `A-002` | raw `time_open_unix` can be treated as direct UTC(직접 협정세계시) for US cash-session features(미국 정규장 피처) | session features(세션 피처) would use timestamp(타임스탬프) without conversion | rejected_by_20260424_time_semantics_probe |
