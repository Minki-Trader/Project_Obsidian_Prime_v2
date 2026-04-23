# Negative Result Register

| result_id | idea_id | hypothesis | why_failed | salvage_value | reopen_condition |
|---|---|---|---|---|---|
| `NR-001` | `time_semantics_direct_utc` | 원천 `time_open_unix`를 직접 UTC(direct UTC, 직접 협정세계시)로 보고 미국 정규장 피처(US cash-session features, 미국 정규장 피처)를 계산할 수 있다 | `20260424_time_semantics_probe`에서 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율)이 `0.0`이었다 | 원천 timestamp(타임스탬프)는 브로커 시계 정렬 키(broker-clock alignment key, 브로커 시계 정렬 키)로는 쓸 수 있다 | 새 export(내보내기) 또는 브로커 문서(broker documentation, 브로커 문서)가 UTC 의미를 명확히 증명할 때 |

Negative results are preserved because they prevent repeated dead ends.
