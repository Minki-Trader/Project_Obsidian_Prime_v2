# Stage269 Run269A Fresh Candidate Package Queue Design(269단계 269A 새 후보 패키지 대기열 설계)

- status(상태): `completed_design_no_candidate_selection`
- stage(단계): `269_onnx_candidate_campaign__fresh_thesis_candidate_construction`
- run(실행): `run269A_fresh_candidate_package_queue_design_v1`
- source_stage(원천 단계): `268_onnx_candidate_campaign__stage267_lineage_triage`
- queue_rows(대기열 행): `4`
- selectable_seed(선택 가능 씨앗): `3`
- support_control(보조 대조): `1`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run269B_materialize_candidate_package_blueprints`

## Plain Result(쉬운 결과)

run269A(269A 실행)는 Stage269(269단계)의 첫 후보 패키지 대기열(candidate package queue, 후보 패키지 대기열)을 만들었다.
효과(effect, 효과): Stage267(267단계)의 alias/profile(별칭/프로필)을 후보로 보존하지 않고, feature surface(피처 표면), scoring surface(점수 표면), decision surface(판단 표면), risk logic(위험 로직), Adapter path(어댑터 경로), runtime handoff(런타임 인계)를 함께 가진 설계 단위만 다음 실행으로 넘긴다.

## Queue Summary(대기열 요약)

| package_id | role(역할) | thesis(논제) | status(상태) |
|---|---|---|---|
| `cp269A_asymmetric_nonfilter_reentry_surface` | selectable_seed(선택 가능 씨앗) | asymmetric non-filter upside(비대칭 비필터 상방) | designed_no_selection(설계됨, 선택 아님) |
| `cp269B_identity_collapse_disambiguator` | selectable_seed(선택 가능 씨앗) | identity-collapse reconstruction(정체성 붕괴 재구성) | designed_no_selection(설계됨, 선택 아님) |
| `cp269C_session_skew_reward_surface` | selectable_seed(선택 가능 씨앗) | new risk/reward asymmetry(새 위험/보상 비대칭) | designed_no_selection(설계됨, 선택 아님) |
| `cp269D_runtime_handoff_isolation_control` | support_control(보조 대조) | runtime handoff isolation(런타임 인계 분리) | support_designed_no_selection(보조 설계됨, 선택 아님) |

## Design Rules(설계 규칙)

- candidate(후보)는 name(이름), alias(별칭), profile(프로필), run id(실행 ID)가 아니다.
- candidate package(후보 패키지)는 feature surface(피처 표면), scoring surface(점수 표면), decision surface(판단 표면), risk logic(위험 로직), Adapter path(어댑터 경로), runtime handoff(런타임 인계), verification plan(검증 계획), failure memory(실패 기억)를 함께 가져야 한다.
- Tier A separate(티어 A 분리), Tier B separate(티어 B 분리), Tier A+B combined(티어 A+B 합산)을 설계 시점부터 요구한다.
- routed run(라우팅 실행)에서는 Tier A used(티어 A 사용), Tier B fallback used(티어 B 대체 사용), actual routed total(실제 라우팅 전체)을 따로 기록한다.
- ONNX(온엑스)는 candidate package gate(후보 패키지 게이트)가 닫힌 뒤에만 시작한다.

## Package Seeds(패키지 씨앗)

### cp269A_asymmetric_nonfilter_reentry_surface

- source clue(원천 단서): `s258_stc_aggressive_nonfilter_reentry`는 upside clue(상방 단서)일 뿐 후보가 아니다.
- fresh thesis(새 논제): 비필터 재진입(non-filter reentry, 비필터 재진입)을 그대로 살리지 않고 reward skew score(보상 비대칭 점수)로 다시 만든다.
- Adapter path(어댑터 경로): `foundation/adapters/baseline_adapter.py`의 output contract(출력 계약)를 파생해 `entry_signal`, `route_code`, `model_risk_pct`, `atr_stop_multiplier`, `atr_take_profit_multiplier`, `max_hold_bars`, `reentry_cooldown_bars`를 유지한다.
- discard condition(폐기 조건): 2026.04 shared-state loss(2026년 4월 공유 상태 손실)를 반복하거나, trade count(거래 수)만 늘고 balance/equity curve(잔액/평가금 곡선)가 확대 구간에서 깨지면 폐기한다.

### cp269B_identity_collapse_disambiguator

- source clue(원천 단서): `s262_lih`와 `s264_aia` identity receipt(정체성 영수증)는 duplicate signature clue(중복 서명 단서)다.
- fresh thesis(새 논제): 같은 KPI signature(핵심 성과 지표 서명)로 접힌 원인을 feature order(피처 순서), decision hash(판단 해시), model handoff(모델 인계)로 분리한다.
- Adapter path(어댑터 경로): `foundation/adapters/baseline_adapter.py`의 telemetry fields(텔레메트리 필드)에 `feature_order_hash`, `model_hash`, `decision_hash` 영수증을 붙이는 방향으로 설계한다.
- discard condition(폐기 조건): decision surface(판단 표면)가 계속 동일하거나, 성과 차이가 telemetry(텔레메트리) 차이로 설명되지 않으면 폐기한다.

### cp269C_session_skew_reward_surface

- source clue(원천 단서): Stage267(267단계)의 weak month/session(약한 월/세션) 실패 기억을 단순 방어 필터로 반복하지 않는다.
- fresh thesis(새 논제): 약한 세션을 막는 대신 session-conditioned reward score(세션 조건 보상 점수)로 reward/risk asymmetry(보상/위험 비대칭)가 있는 구간만 남긴다.
- Adapter path(어댑터 경로): BaselineAdapter(기준선 어댑터) 출력 계약을 유지하되 `session_code`와 session risk cap(세션 위험 상한) 텔레메트리를 추가하는 후보로 둔다.
- discard condition(폐기 조건): trade count collapse(거래 수 붕괴), session overfit(세션 과적합), 또는 약한 월 확대 구간의 치명적 손상이 나오면 폐기한다.

### cp269D_runtime_handoff_isolation_control

- role(역할): selectable candidate(선택 가능 후보)가 아니라 support control(보조 대조)이다.
- source clue(원천 단서): blocked handoff precheck(차단된 인계 사전검사)는 성과 실패가 아니라 runtime handoff gap(런타임 인계 공백)이다.
- fresh thesis(새 논제): 후보 성과와 runtime/init failure(런타임/초기화 실패)를 분리해 잘못된 후보 폐기를 막는다.
- Adapter path(어댑터 경로): `foundation/adapters/baseline_adapter.py`와 `foundation/models/onnx_bridge.py`의 feature order hash(피처 순서 해시), model hash(모델 해시), handoff hash(인계 해시)를 연결하는 control receipt(대조 영수증)로 둔다.
- discard condition(폐기 조건): identity receipt(정체성 영수증)를 만들 수 없으면 성과 후보로 올리지 않고 blocked(차단) 근거로만 남긴다.

## Next Gate(다음 게이트)

run269B(269B 실행)는 위 네 행을 materialized blueprint(물질화된 청사진)로 바꿔야 한다.
효과(effect, 효과): 각 package(패키지)에 feature order source(피처 순서 원천), scoring owner(점수 소유자), decision rule(판단 규칙), risk rule(위험 규칙), Adapter output schema(어댑터 출력 스키마), runtime handoff file plan(런타임 인계 파일 계획)을 붙인다.

## Boundary(경계)

This design(이 설계)은 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), ONNX readiness(온엑스 준비), selected candidate(선택 후보), Goal Achieve(목표 달성)를 주장하지 않는다.
