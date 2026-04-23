# Selection Status

## 현재 판독(Current Read, 현재 판독)

- active_stage(활성 단계): `01_data_foundation__raw_m5_inventory`
- status(상태): `time_semantics_evidence_complete_next_policy_open`
- current operating reference(현재 운영 기준): `none`
- exploration rule(탐색 규칙): `Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색 가능

## 확인된 근거(Confirmed Evidence, 확인된 근거)

- run_id(실행 ID): `20260424_raw_m5_inventory`
- judgment(판정): `positive(긍정)` for raw inventory only
- usable symbols(사용 가능 심볼): `12 / 12`
- common usable window(공통 사용 기간): `2022-08-01T16:35:00Z` through `2026-04-13T22:55:00Z`
- report(보고서): `stages/01_data_foundation__raw_m5_inventory/02_runs/20260424_raw_m5_inventory/raw_m5_inventory.md`
- run_id(실행 ID): `20260424_time_semantics_probe`
- judgment(판정): `negative(부정)` for direct UTC assumption, `positive(긍정)` for broker/server clock candidate
- direct UTC match ratio(직접 UTC 일치율): `0.0`
- broker wall-clock-like ratio(브로커 시계 유사율): `0.929082`
- report(보고서): `stages/01_data_foundation__raw_m5_inventory/02_runs/20260424_time_semantics_probe/time_semantics_probe.md`

## 다음 근거(Next Evidence, 다음 근거)

피처 프레임(feature frame, 피처 프레임)의 timestamp policy(타임스탬프 정책)를 정한다. 선택지는 원천 브로커 시계 키(raw broker-clock key, 원천 브로커 시계 키)를 유지하는 방식과 명시적 UTC 이벤트 시간(explicit UTC event time, 명시적 UTC 이벤트 시간)으로 변환하는 방식이다.

## 경계(Boundary, 경계)

이 단계(stage, 단계)는 알파 품질(alpha quality, 알파 품질), 런타임 준비(runtime readiness, 런타임 준비), 운영 승격(operating promotion, 운영 승격)을 결정하지 않는다.
