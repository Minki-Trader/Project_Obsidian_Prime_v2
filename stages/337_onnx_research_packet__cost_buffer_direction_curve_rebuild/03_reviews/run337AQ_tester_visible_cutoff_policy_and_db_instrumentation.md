# Stage337AQ Tester Visible Cutoff Policy And D/B Instrumentation(337AQ 테스터 가시 컷오프 정책 및 D/B 계측)

- run_id(실행 ID): `run337AQ_tester_visible_cutoff_policy_and_db_instrumentation_v1`
- status(상태): `completed_stage337AQ_tester_visible_cutoff_policy_db_instrumentation_no_forward_decision`
- judgment(판정): `tester_current_day_intraday_cutoff_policy_confirmed_db_source_still_missing`
- decision(결정): `stage337AQ_open_run337AR_db_source_sidecar_or_out_of_scope_lock_no_selection`
- next_action(다음 행동): `run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock_v1`
- cutoff evidence rows(컷오프 근거 행): `18`
- broker current-day gap rows(브로커 현재일 공백 행): `16`
- completed visible rows(완성일 가시 행): `1`
- shifted custom rows(이동 커스텀 행): `1`
- latest API close(API 최신 종가): `2026-05-27T09:30:00Z`
- D/B missing columns(D/B 누락 컬럼): `7`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Cutoff Policy(컷오프 정책)

| policy(정책) | status(상태) | evidence(근거) | allowed(허용) | forbidden(금지) |
|---|---:|---:|---|---|
| `broker_current_day_intraday_cutoff` | `confirmed` | `16` | Use completed-day or tester-visible windows only(완성일 또는 테스터 가시 구간만 사용). | Do not use current-day intraday feature rows for Forward Passed/Failed(현재일 장중 피처 행으로 전진 통과/실패 판정 금지). |
| `completed_day_window_allowed` | `allowed_with_boundary` | `1` | Runtime signal parity, attribution, cost stress, curve pocket diagnostics(런타임 신호 동등성, 귀속, 비용 압박, 곡선 포켓 진단). | Do not promote to operating readiness or broad forward pass(운영 준비나 넓은 전진 통과로 승격 금지). |
| `synthetic_shifted_custom_proxy_scope` | `parity_only` | `1` | Proxy-MT5 timestamp and signal sanity check(프록시-MT5 시점 및 신호 점검). | Do not use shifted custom result as broker forward profitability evidence(이동 커스텀 결과를 브로커 전진 수익성 근거로 사용 금지). |
| `api_history_warmup_not_sufficient` | `confirmed` | `18` | Use API freshness as data availability evidence only(API 최신성은 데이터 확보 근거로만 사용). | Do not infer tester forward availability from API latest close alone(API 최신 종가만으로 테스터 전진 가시성 추론 금지). |

## D/B Instrumentation(D/B 계측)

D/B source(D/B 원천)는 run337AP runtime telemetry(런타임 기록)와 feature matrix(피처 행렬)에 없다. decision(결정) 컬럼은 방향 proxy(대리값)일 뿐이며 D/B attribution(D/B 귀속)을 대신하지 않는다.

| action(행동) | priority(우선순위) | allowed change(허용 변경) | forbidden change(금지 변경) |
|---|---:|---|---|
| `db_source_sidecar_search` | `P0` | read-only lineage and sidecar materialization(읽기 전용 계보 확인 및 보조표 물질화) | threshold retune; D/B rule rewrite; inferring source from direction(임계값 재조정, D/B 규칙 재작성, 방향에서 원천 추론 금지) |
| `tester_window_policy_lock` | `P0` | window labeling and evidence boundary only(구간 라벨과 근거 경계만 변경) | using proxy or shifted custom result as broker forward KPI(프록시나 이동 커스텀 결과를 브로커 전진 KPI로 사용 금지) |
| `runtime_telemetry_schema_extension_gate` | `P1` | instrumentation-only telemetry schema(계측 전용 텔레메트리 스키마) | model, ONNX, feature order, score threshold, lot, risk, ATR exit, runtime handoff semantics(모델, 온엑스, 피처 순서, 점수 임계값, 랏, 위험, ATR 청산, 런타임 인계 의미 변경 금지) |

## Boundary(경계)

run337AQ(337AQ 실행)는 새 training(학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화)을 하지 않았다. 효과(effect, 효과)는 tester-visible(테스터 가시) 데이터만 forward decision(전진 판정)에 쓸 수 있게 경계를 고정하고, D/B source(D/B 원천)는 실제 source sidecar(원천 보조표)나 out_of_scope(범위 밖) 중 하나로 닫게 하는 것이다.
