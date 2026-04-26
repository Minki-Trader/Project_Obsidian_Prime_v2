# Negative Result Register

| result_id | idea_id | hypothesis | why_failed | salvage_value | reopen_condition |
|---|---|---|---|---|---|
| `NR-001` | `time_semantics_direct_utc` | 원천 `time_open_unix`를 직접 UTC(direct UTC, 직접 협정세계시)로 보고 미국 정규장 피처(US cash-session features, 미국 정규장 피처)를 계산할 수 있다 | `20260424_time_semantics_probe`에서 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율)이 `0.0`이었다 | 원천 timestamp(타임스탬프)는 브로커 시계 정렬 키(broker-clock alignment key, 브로커 시계 정렬 키)로는 쓸 수 있다 | 새 export(내보내기) 또는 브로커 문서(broker documentation, 브로커 문서)가 UTC 의미를 명확히 증명할 때 |
| `NR-002` | `IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY` | LGBM(`LightGBM`, 라이트GBM) short-only(숏만) 방향 분리가 RUN02A/RUN02B(실행 02A/02B)의 약함을 회복할 수 있다 | RUN02D(실행 02D) OOS(표본외) net/PF(순수익/수익 팩터)가 `-211.48 / 0.31`로 크게 약했다 | validation(검증)은 `-18.33 / 0.89`라서 short-specific label(숏 전용 라벨)의 필요성을 알려준다 | 새 short-specific label(숏 전용 라벨) 또는 short-side model(숏 전용 모델)이 생길 때 |
| `NR-003` | `IDEA-ST11-LGBM-CALM-TREND-GATE` | `adx_14 >= 25`와 `historical_vol_5_over_20 <= 1.25` calm trend gate(차분한 추세 문맥 제한)가 LGBM(라이트GBM) 신호를 정화할 수 있다 | RUN02F(실행 02F) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-234.03 / 0.46`, `-163.22 / 0.41`로 둘 다 약했다 | context gating(문맥 제한)은 필요할 수 있지만 이 조건 조합은 약하다 | 다른 context feature(문맥 피처) 조합이나 regime label(국면 라벨)이 생길 때 |

Negative results are preserved because they prevent repeated dead ends.
