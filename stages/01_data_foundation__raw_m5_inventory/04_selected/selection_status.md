# Selection Status

## 현재 판독(Current Read, 현재 판독)

- active_stage(활성 단계): `01_data_foundation__raw_m5_inventory`
- status(상태): `timestamp_policy_decided_next_calendar_mapper_open`
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
- decision(결정): `2026-04-24_stage01_timestamp_policy`
- contract(계약): `docs/contracts/time_axis_policy_fpmarkets_v2.md`
- policy(정책): 이중 시간축 정책(dual time axis policy, 이중 시간축 정책)

## 다음 근거(Next Evidence, 다음 근거)

브로커 세션 달력 매퍼(broker session calendar mapper, 브로커 세션 달력 매퍼)를 만든다. 효과(effect, 효과)는 미국 정규장 피처(US cash-session features, 미국 정규장 피처)를 직접 UTC 가정(direct UTC assumption, 직접 UTC 가정) 없이 계산할 수 있게 하는 것이다.

## 경계(Boundary, 경계)

이 단계(stage, 단계)는 알파 품질(alpha quality, 알파 품질), 런타임 준비(runtime readiness, 런타임 준비), 운영 승격(operating promotion, 운영 승격)을 결정하지 않는다.
