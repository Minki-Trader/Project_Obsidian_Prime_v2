# Stage243 Stage242 Follow-up Review(243단계 242단계 후속 검토)

- stage(단계): `243_adapter_research__stage242_selective_midsegment_followup_review`
- run(실행): `run243A_stage243_stage242_selective_midsegment_followup_review_v1`
- source_stage(원천 단계): `242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff`
- source_run(원천 실행): `run242A_stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff_v1`
- source_stage242_evidence_commit(원천 242단계 근거 커밋): `a62f41abb82b2879008fdad85578eda1c78b1c21`
- source_stage242_hash_record_commit(원천 242단계 해시 기록 커밋): `00b3182ba007d87ff20d3f5dbbeeb7370a4a853b`
- external_verification_status(외부 검증 상태): `review_only_source_stage242_mt5_reports_completed`
- decision(판정): `open_stage244_bounded_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

- Stage242(242단계)는 34D(34D 기준)에 더 가까운 near-miss(근접 실패)를 찾았다. `s242_midlowmid_guard_cap0305`는 validation net(검증 순손익) `976.67`, DD(낙폭) `12.9428`, OOS net(표본외 순손익) `775.76`이다.
- 하지만 `mid_window_rows`(중간 창 행 수)와 `selective_blocked_signal_rows`(선택 차단 신호 행 수)가 전부 `0`이다. Effect(효과): Stage242(242단계)의 middle-window guard(중간 기간 보호문)는 실제로 작동하지 않았다.
- 그래서 `s242_midlowmid_guard_cap0305`의 개선은 active guard(작동 보호문)가 아니라 mild model-risk cap(완만한 모델 위험 상한) `0.0305`의 효과로 본다.
- KPI(핵심 성과 지표) 기준으로는 아직 최종 후보가 아니다. validation net(검증 순손익)은 34D보다 `10.93` 낮고, DD(낙폭)는 `0.033664` percentage point(퍼센트포인트) 높고, mid PF(중간 수익요인)는 `1.522877`로 부족하다.

## Tradeoff Matrix(상충 행렬)

| adapter(어댑터) | class(분류) | val net(검증 순손익) | DD%(낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | guard rows(보호문 행) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---|
| s242_samecap_control | control_still_below_34d | 967.85 | 13.3771 | 1.498473078 | 812.8 | 0 | 순손익/OOS(표본외)는 강하지만 DD/PF(낙폭/수익요인)가 아직 34D에 못 닿는다. |
| s242_midlow_guard | guard_variant_identical_to_control_due_to_inactive_window | 967.85 | 13.3771 | 1.498473078 | 812.8 | 0 | 의도한 middle-window guard(중간 기간 보호문)가 0건이라 samecap control(동일 상한 대조군)과 같다. |
| s242_midlowmid_guard | guard_variant_identical_to_control_due_to_inactive_window | 967.85 | 13.3771 | 1.498473078 | 812.8 | 0 | 의도한 middle-window guard(중간 기간 보호문)가 0건이라 samecap control(동일 상한 대조군)과 같다. |
| s242_midlowmid_guard_cap0305 | near_miss_mild_cap_oos_damage_guard_inactive | 976.67 | 12.9428 | 1.522877251 | 775.76 | 0 | 34D(34D 기준)에 아주 가까워졌지만 OOS(표본외) 순손익을 깎고 중간 보호문은 작동하지 않았다. |

## Attribution(성과 기여 분석)

- guard_inactive(보호문 비활성): Stage242(242단계) parser(파서)가 `YYYY.MM.DD HH:MM:SS` feature time(피처 시간)을 ISO date(ISO 날짜)처럼 해석하지 못했다. Effect(효과): 선택적 차단은 0건이었다.
- cap0305_near_miss(0.0305 상한 근접 실패): validation net(검증 순손익)은 samecap control(동일 상한 대조군)보다 `8.82` 좋아졌고 DD(낙폭)는 `-0.4343` 낮아졌지만 OOS net(표본외 순손익)은 `-37.04` 나빠졌다.
- route(경로): Stage244(244단계)는 timestamp-aware midwindow guard(시간 형식 인식 중간 창 보호문)를 실제로 작동시키고, cap0305(0.0305 상한)는 control arm(대조군)으로 남긴다.

## Judgment(판정)

- result_subject(판정 대상): `run243A_stage243_stage242_selective_midsegment_followup_review_v1`
- evidence_available(사용 근거): Stage242(242단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), quality matrix(품질 행렬), gate feature summary(보호문 피처 요약), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(부족 근거): active middle-window guard(작동 중간 기간 보호문) 측정, 34D(34D 기준) 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `stage242_inactive_guard_near_miss_not_final(242단계 비활성 보호문 근접 실패, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). no deployment(배포 없음), no live_readiness(실거래 준비 없음), no runtime_authority(런타임 권위 없음).
- next_condition(다음 조건): `244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard`에서 날짜 파서와 middle-window guard(중간 기간 보호문)를 고친 뒤 같은 KPI(핵심 성과 지표)를 다시 측정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
