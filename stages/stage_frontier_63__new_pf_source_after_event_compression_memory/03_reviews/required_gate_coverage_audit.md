# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `True`
- stage_open_local_checks(단계 개방 로컬 검증): `completed(완료)`
- pre_mt5_grok_review(MT5 전 그록 검토): `True`
- mt5_runtime_probe(MT5 런타임 탐침): `runtime_probe_observation_no_authority`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `True`
- Tier A separate(Tier A 분리): `validation_is/oos MT5 rows recorded(검증/OOS MT5 행 기록됨)`
- Tier B separate(Tier B 분리): `missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖)` because no Tier B payload was materialized(티어 B 페이로드 없음)
- Tier A+B combined(Tier A+B 합산): `missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖)` because no routed combined payload was materialized(합산 라우팅 페이로드 없음)
- event_gated_vs_raw_signal_summary(이벤트 게이트/원신호 요약): `recorded in runtime_probe_report(런타임 탐침 보고에 기록됨)`
- f62_signal_polarity_delta(F62 신호 극성 비교): `reference_only(참조 전용)`; F63 tests inverse polarity(역전 극성) only, not F62 inheritance(상속) or authority(권위)
- forbidden_claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve not_claimed(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음)
