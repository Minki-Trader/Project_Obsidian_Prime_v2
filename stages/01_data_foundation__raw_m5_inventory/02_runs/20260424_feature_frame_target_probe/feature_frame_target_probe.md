# Feature Frame Target Probe Review(피처 프레임 목표 탐침 검토)

## 판정(Judgment, 판정)

`20260424_feature_frame_target_probe` 실행(run, 실행)은 `positive(긍정)`로 본다.

쉽게 말하면 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)은 practical modeling start(실용 모델링 시작) 이후 `valid_row(유효행)`만 쓰고, partial cash session(부분 정규장) 일자를 빼는 범위가 가장 깔끔하다.

## 선택된 목표(Selected Target, 선택된 목표)

- target_id(목표 ID): `practical_start_full_cash_day_valid_rows_only`
- start_utc(시작 UTC): `2022-09-01T00:00:00+00:00`
- row_scope(행 범위): `valid_row_only`
- session_scope(세션 범위): `cash_open_rows_only`
- day_scope(일 범위): `full_cash_session_days_only`
- valid rows(유효행 수): `54439`
- NY days(뉴욕 일수): `887`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- excluded partial-day valid rows(제외된 부분 정규장 유효행 수): `252`
- first valid timestamp(첫 유효 타임스탬프): `2022-09-01T16:40:00+00:00`
- last valid timestamp(마지막 유효 타임스탬프): `2026-04-13T23:00:00+00:00`

## 후보 비교(Candidate Comparison, 후보 비교)

| target_id | rows | ny_day_count | session_scope | day_scope |
|---|---:|---:|---|---|
| `full_window_valid_rows_only` | `56939` | `914` | `all_rows` | `all_days` |
| `practical_start_valid_rows_only` | `55408` | `892` | `all_rows` | `all_days` |
| `practical_start_cash_open_valid_rows_only` | `54691` | `892` | `cash_open_rows_only` | `cash_open_rows` |
| `practical_start_full_cash_day_valid_rows_only` | `54439` | `887` | `cash_open_rows_only` | `full_cash_session_days_only` |

## 이유(Why, 이유)

- cash-open valid ratio(정규장 유효 비율): `0.769595`
- full cash days(완전 정규장 일수): `913`
- partial cash days(부분 정규장 일수): `40`
- partial cash session(부분 정규장) 일자는 holiday(휴일) 전후나 early close(조기 종료)처럼 행 형태(row shape, 행 형태)가 흔들리는 경우가 많다.
- 첫 freeze(첫 동결)를 가능한 한 균일한 NY core session day boundary(뉴욕 핵심 정규장 일 경계)로 묶는 편이 다음 단계의 artifact identity(산출물 정체성)를 더 단순하게 만든다.

## 부분 정규장 예시(Worst Partial-Day Examples, 부분 정규장 예시)

| date_ny | cash_rows | valid_rows | valid_ratio |
|---|---:|---:|---:|
| `2025-01-09` | `1` | `0` | `0.000000` |
| `2025-09-01` | `30` | `0` | `0.000000` |
| `2022-11-24` | `42` | `0` | `0.000000` |
| `2023-02-20` | `42` | `0` | `0.000000` |
| `2023-05-29` | `42` | `0` | `0.000000` |
| `2023-06-19` | `42` | `0` | `0.000000` |
| `2023-07-04` | `42` | `0` | `0.000000` |
| `2024-01-15` | `42` | `0` | `0.000000` |
| `2024-02-19` | `42` | `0` | `0.000000` |
| `2025-05-26` | `42` | `0` | `0.000000` |

## 효과(Effect, 효과)

Stage 01(1단계)은 이제 첫 feature frame target(피처 프레임 목표)을 분명하게 갖고 있다.
다음 단계(next stage, 다음 단계)는 이 목표를 실제 shared freeze(공유 동결 산출물)로 물질화하는 일이다.

## 경계(Boundary, 경계)

이 검토(review, 검토)는 첫 clean target(깨끗한 목표)을 고르는 근거다.
더 넓은 valid-row scope(유효행 범위)가 무효라는 뜻은 아니다. model readiness(모델 준비), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지도 않는다.
