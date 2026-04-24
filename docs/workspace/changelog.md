# Workspace Changelog

## 2026-04-24

- 깨끗한 단계 재시작(clean stage restart, 깨끗한 단계 재시작)을 만들었다.
- `.agents/skills`, `docs/contracts`, 개념 노트(concept notes, 개념 노트), 데이터(data, 데이터), 재사용 foundation 도구(reusable foundation tools, 재사용 기반 도구)를 보존했다.
- 오래된 Stage 00부터 Stage 07까지의 이력(history, 이력)을 현재 단계 진실(current stage truth, 현재 단계 진실)에서 제거했다.
- `Tier A(티어 A)`와 `Tier B(티어 B)`를 둘 다 완전히 탐색 가능한 표본 라벨(sample label, 표본 라벨)로 다시 정의했다.
- 첫 단계(first stage, 첫 단계)로 `01_data_foundation__raw_m5_inventory`를 열었다.
- `20260424_raw_m5_inventory` 실행(run, 실행)으로 원천 `M5` 재고(raw M5 inventory, 원천 M5 재고)를 확인했다. 예상 심볼(expected symbols, 예상 심볼) 12개가 모두 사용 가능했고, 공통 사용 창(common usable window, 공통 사용 기간)은 `2022-08-01T16:35:00Z`부터 `2026-04-13T22:55:00Z`까지다.
- `20260424_time_semantics_probe` 실행(run, 실행)으로 원천 timestamp(타임스탬프)가 직접 UTC(direct UTC, 직접 협정세계시)로는 미국 주식 정규장과 맞지 않고, 브로커/서버 시계 후보(broker/server clock candidate, 브로커/서버 시계 후보)에 가깝다는 근거를 남겼다.
- `2026-04-24_stage01_timestamp_policy` 결정(decision, 결정)으로 이중 시간축 정책(dual time axis policy, 이중 시간축 정책)을 채택했다. 원천 정렬(alignment, 정렬)은 브로커 시계 키(broker-clock key, 브로커 시계 키)를 쓰고, 세션 피처(session features, 세션 피처)는 검증된 이벤트 UTC(event UTC, 이벤트 UTC) 또는 브로커 세션 달력(broker session calendar, 브로커 세션 달력)이 필요하다.
- `20260424_broker_session_calendar_mapper` 실행(run, 실행)으로 `Europe/Athens` 브로커 시계(broker clock, 브로커 시계)에서 `America/New_York` 세션 시간(session time, 세션 시간)으로 가는 매퍼(mapper, 매퍼)를 만들고 검토했다.
- 외부 검증 지연 방지(External Verification Anti-Deferral, 외부 검증 지연 방지) 규칙을 추가했다. 효과(effect, 효과)는 MT5(`MetaTrader 5`, 메타트레이더5), 전략 테스터(strategy tester, 전략 테스터), 런타임 동등성(runtime parity, 런타임 동등성)이 필요한 주장을 다음 작업(next work, 다음 작업)으로 반복해서 미루지 못하게 하는 것이다.
- `20260424_feature_frame_target_probe` 실행(run, 실행)으로 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)을 `practical_start_full_cash_day_valid_rows_only`로 선택했다.
- Stage 01(1단계)을 닫고 `02_feature_frame__practical_full_cash_freeze`를 열었다. 효과(effect, 효과)는 첫 shared freeze(공유 동결 산출물)를 실제로 물질화할 단계가 분명해졌다는 것이다.
- `20260424_practical_full_cash_freeze_materialization` 실행(run, 실행)으로 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 실제로 만들었다. 데이터셋 ID(dataset ID, 데이터셋 ID)는 `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`이고, 선택 행(selected rows, 선택 행)은 `54439`다.
- Stage 02(2단계)를 닫고 `03_training_dataset__label_split_contract`를 열었다. 효과(effect, 효과)는 이제 라벨(label, 라벨)과 분할(split, 분할)을 실제 공유 동결 산출물 위에서 정할 수 있다는 것이다.
- agent guard(에이전트 가드)와 policy routing(정책 라우팅)을 단순화했다. 효과(effect, 효과)는 낡은 stage ownership(단계 소유권) 문구를 제거하고, claim discipline(주장 규율)을 공식 라우팅에 남기며, agent settings validator(에이전트 설정 검사기)가 `openai.yaml`의 필수 설명을 확인하게 된 것이다.
- 답변 명확성(answer clarity, 답변 명확성), 코드 품질(code quality, 코드 품질), workflow drift guard(작업 드리프트 가드), reference scout(참고자료 탐색) 스킬을 추가했다. 효과(effect, 효과)는 Codex 답변, 구현 품질, 막힘 상황 분류, 외부 사용법 확인을 더 직접적으로 다루는 것이다.
- workflow drift guard(작업 드리프트 가드)에 material recovery order(재료 복구 순서)를 추가했다. 효과(effect, 효과)는 필요한 재료가 없을 때 외부/레거시를 기본 대체 경로로 쓰지 않고, 현재 프로젝트 안에서 복구 또는 재생성할 수 있는지 먼저 확인하게 하는 것이다.
- workflow drift guard(작업 드리프트 가드)에 recovery action rule(복구 행동 규칙)을 추가했다. 효과(effect, 효과)는 Codex가 직접 풀 수 있는 blocker(차단 지점)는 직접 풀고, 사용자 협조가 필요한 경우에는 정확한 요청과 복귀 지점을 남기게 하는 것이다.
