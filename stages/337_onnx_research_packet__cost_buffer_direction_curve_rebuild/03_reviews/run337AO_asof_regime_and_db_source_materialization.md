# Stage337AO As-Of Regime And D/B Source Materialization(337AO 시점 기준 국면 및 D/B 원천 물질화)

- run_id(실행 ID): `run337AO_asof_regime_and_db_source_materialization_v1`
- status(상태): `completed_stage337AO_asof_regime_db_source_inputs_materialized_no_training_no_selection`
- judgment(판정): `asof_regime_sources_hash_lag_and_db_schema_materialized_broker_gap_still_blocks_forward`
- decision(결정): `stage337AO_open_run337AP_broker_tester_history_repair_no_selection`
- next_action(다음 행동): `run337AP_broker_tester_history_repair_or_next_rollover_v1`
- source_identity_rows(원천 정체성 행): `12`
- release_lag_rows(공표 지연 행): `12`
- asof_join_trade_rows(시점 기준 거래 조인 행): `344`
- regime_slice_rows(국면 구간 행): `34`
- macro_sources_usable_with_age_bucket(나이 버킷 포함 사용 가능 거시 원천): `3`
- no_future_source_violations(미래 원천 위반): `0`
- db_missing_required_columns(D/B 필수 누락 컬럼): `7`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AO(337AO 실행)는 VIX/US10YR/USDX(변동성/금리/달러) 원천을 trade feature timestamp(거래 피처 시각) 이전 값으로만 붙였다. 효과(effect, 효과)는 macro regime attribution(거시 국면 귀속)을 미래참조 없이 다시 볼 수 있게 하는 것이다.

## Boundary(경계)

D/B source(D/B 원천) 필드는 run337AN telemetry(런타임 기록)와 u42 feature(피처)에 없다. 효과(effect, 효과)는 direction attribution(방향 귀속)을 D/B attribution(D/B 귀속)처럼 말하지 못하게 막는 것이다.

Broker forward boundary(브로커 전진 경계)는 부모 run337AN(337AN 실행)에서 `failed`다. 따라서 이 실행은 data instrumentation(데이터 계측)일 뿐 Forward Passed/Failed(전진 통과/실패)가 아니다.
