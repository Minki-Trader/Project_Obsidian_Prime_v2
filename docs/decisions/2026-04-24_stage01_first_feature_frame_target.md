# Decision Memo

## 결정(Decision, 결정)

Stage 01(1단계)의 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)은 `practical_start_full_cash_day_valid_rows_only`로 둔다.

- start_utc(시작 UTC): `2022-09-01T00:00:00Z`
- row_scope(행 범위): `valid_row_only`
- day_scope(일 범위): `full_cash_session_days_only`

## 이유(Why, 이유)

`20260424_feature_frame_target_probe` 실행(run, 실행)은 다음을 보여줬다.

- practical-start valid rows only(실용 시작 유효행 전체): `55408`
- practical-start cash-open valid rows only(실용 시작 정규장 유효행): `54691`
- practical-start full-cash-day valid rows only(실용 시작 완전 정규장 유효행): `54439`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- excluded partial-day valid rows(제외된 부분 정규장 유효행 수): `252`

쉽게 말하면, 부분 정규장(partial cash session, 부분 정규장) 일자를 빼도 잃는 유효행(valid rows, 유효행)은 작고, 첫 shared freeze(공유 동결 산출물)의 경계(boundary, 경계)는 더 단순해진다.

## 효과(Effect, 효과)

- Stage 01(1단계)은 닫힌다.
- 다음 활성 단계(next active stage, 다음 활성 단계)는 `02_feature_frame__practical_full_cash_freeze`다.
- 더 넓은 valid-row scope(유효행 범위)는 죽은 후보가 아니라 나중 후보(later candidate, 나중 후보)로 남긴다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 첫 feature-frame freeze target(첫 피처 프레임 동결 목표)을 고르는 것이다.

모델 준비(model readiness, 모델 준비), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)을 주장하지 않는다.
