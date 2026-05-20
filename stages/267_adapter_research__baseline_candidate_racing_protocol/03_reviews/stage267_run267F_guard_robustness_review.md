# Stage267 Run267F Non-Calendar Guard MT5 Review(267단계 267F 비달력 방어 MT5 검토)

- action(행동): run267F(267F 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), run267D/run267E 대비 comparison(비교)을 만들었다.
- effect(효과): ADX 20-25(추세 강도 20-25)는 비달력 축으로 일부 지지를 주는지, DI-low q33(DI 낮은 33%)은 유사 대체로 버티는지 따로 판정한다.
- trade_records(거래 기록): `4816`
- time_slice_rows(시간 구간 행): `680`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 판독)

`adx2025`는 run267E(267E 실행)의 Monday guard(월요일 방어)만큼 강하지는 않지만, run267D(267D 실행) atrcomp(ATR 압축 대체)보다 일부 개선을 보였다.
`dilowq33`는 유사 피처 대체(similar feature replacement, 유사 피처 대체)에서 크게 약해져 실패 기억(failure memory, 실패 기억)으로 남겨야 한다.
즉, 이전 연구를 이후 stage(단계)에서 충분히 활용했다고 말하기보다는, 이제야 비달력 검증판으로 펼치기 시작한 상태다.

## Guard Comparison(방어 비교)

| candidate(후보) | guard(방어) | net vs D(267D 대비 순수익) | net vs E(267E 대비 순수익) | PF vs D(267D 대비 PF) | trade vs D(267D 대비 거래) | DD vs D(267D 대비 손실폭) | weakest month(약한 월) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | `adx2025` | 61.3 | -103.36 | 0.07222 | -64.0 | -2.02 | `2024-07` -98.91 | partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님) |
| `s264_aih` | `adx2025` | 35.73 | -116.18 | 0.069103 | -61.0 | -0.84 | `2024-07` -96.82 | partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님) |
| `s264_aia` | `adx2025` | 43.85 | -102.56 | 0.073 | -62.0 | -1.0 | `2024-07` -96.82 | partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님) |
| `s264_lc` | `adx2025` | 45.62 | -120.45 | 0.074269 | -61.0 | -0.82 | `2024-07` -93.54 | partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님) |
| `s262_lih` | `adx2025` | 41.09 | -119.32 | 0.06281 | -61.0 | -0.81 | `2024-07` -107.49 | partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님) |
| `s264_aih` | `dilowq33` | -218.49 | -370.4 | -0.11056 | -91.0 | 2.87 | `2024-06` -65.44 | similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단) |
| `s264_aia` | `dilowq33` | -210.37 | -356.78 | -0.106663 | -92.0 | 2.71 | `2024-06` -65.44 | similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단) |
| `s264_lc` | `dilowq33` | -197.9 | -363.97 | -0.105534 | -90.0 | 3.87 | `2024-06` -64.95 | similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단) |
| `s258_stc` | `dilowq33` | -233.47 | -398.13 | -0.114579 | -94.0 | 6.23 | `2024-06` -81.14 | similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단) |
| `s262_lih` | `dilowq33` | -189.09 | -349.5 | -0.111377 | -90.0 | 5.61 | `2024-06` -64.95 | similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단) |

## Weak Slices(약한 구간)

| record_view(기록 보기) | guard(방어) | axis(축) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `mt5_rt_s258_stc_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `weekday` | `Monday` | 52 | -181.07 | 0.55695 |
| `mt5_rt_s262_lih_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `chron_segment` | `chron_mid` | 75 | -176.01 | 0.569289 |
| `mt5_rt_s264_lc_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `weekday` | `Monday` | 47 | -161.21 | 0.523794 |
| `mt5_rt_s262_lih_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `weekday` | `Monday` | 47 | -158.19 | 0.519749 |
| `mt5_rt_s264_aia_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `weekday` | `Monday` | 48 | -156.64 | 0.551149 |
| `mt5_rt_s264_aih_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `weekday` | `Monday` | 48 | -156.64 | 0.551149 |
| `mt5_rt_s264_lc_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `chron_segment` | `chron_mid` | 74 | -129.9 | 0.675169 |
| `mt5_rt_s258_stc_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `weekday` | `Monday` | 49 | -125.18 | 0.543522 |
| `mt5_rt_s262_lih_adx2025_historical_2024_tier_a_train_era_stress` | `adx2025` | `chron_segment` | `chron_mid` | 84 | -122.85 | 0.770447 |
| `mt5_rt_s264_aia_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `chron_segment` | `chron_mid` | 75 | -122.2 | 0.700071 |
| `mt5_rt_s264_aih_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `chron_segment` | `chron_mid` | 75 | -122.2 | 0.700071 |
| `mt5_rt_s258_stc_dilowq33_historical_2024_tier_a_train_era_stress` | `dilowq33` | `chron_segment` | `chron_mid` | 80 | -121.23 | 0.738023 |

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267F_non_calendar_guard_mt5_review`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 20개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단), guard_comparison(방어 비교).
- evidence_missing(빠진 근거): 후속 feature engineering(피처 엔지니어링), Adapter(어댑터) 구조화, expanded period(확장 기간) 재검증, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`.
