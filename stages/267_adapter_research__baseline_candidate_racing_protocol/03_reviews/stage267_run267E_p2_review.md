# Stage267 Run267E Atrcomp Monday Guard MT5 Review(267단계 267E ATR 압축 월요일 방어 MT5 검토)

- action(행동): run267E(267E 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), run267D 대비 comparison(비교)을 만들었다.
- effect(효과): 순수익만 보지 않고 거래 수 감소, DD(drawdown, 손실폭), 약한 월/요일/시간/시간순 구간을 함께 본다.
- trade_records(거래 기록): `2610`
- time_slice_rows(시간 구간 행): `350`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Guard Comparison(방어 비교)

| candidate(후보) | net delta(순수익 차이) | PF delta(수익 팩터 차이) | trade delta(거래 수 차이) | DD delta(손실폭 차이) | weakest month(약한 월) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | 164.66 | 0.141462 | -60.0 | -5.4 | `2024-08` -49.21 | constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의) |
| `s264_aih` | 151.91 | 0.144072 | -56.0 | -6.91 | `2024-08` -55.9 | constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의) |
| `s264_aia` | 146.41 | 0.140515 | -56.0 | -6.95 | `2024-08` -55.69 | constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의) |
| `s264_lc` | 166.07 | 0.149334 | -55.0 | -6.88 | `2024-08` -55.32 | constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의) |
| `s262_lih` | 160.41 | 0.138326 | -55.0 | -6.91 | `2024-08` -53.29 | constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의) |

## Weak Slices(약한 구간)

| record_view(기록 보기) | axis(축) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |
| --- | --- | --- | ---: | ---: | ---: |
| `mt5_rt_s262_lih_atrmon_historical_2024_tier_a_train_era_stress` | `chron_segment` | `chron_mid` | 86 | -83.22 | 0.850678 |
| `mt5_rt_s264_lc_atrmon_historical_2024_tier_a_train_era_stress` | `chron_segment` | `chron_mid` | 86 | -68.03 | 0.875706 |
| `mt5_rt_s258_stc_atrmon_historical_2024_tier_a_train_era_stress` | `chron_segment` | `chron_mid` | 92 | -65.57 | 0.899076 |
| `mt5_rt_s264_aih_atrmon_historical_2024_tier_a_train_era_stress` | `chron_segment` | `chron_mid` | 86 | -65.12 | 0.882686 |
| `mt5_rt_s264_aia_atrmon_historical_2024_tier_a_train_era_stress` | `chron_segment` | `chron_mid` | 87 | -64.41 | 0.882459 |
| `mt5_rt_s264_aih_atrmon_historical_2024_tier_a_train_era_stress` | `month` | `2024-08` | 30 | -55.9 | 0.702881 |
| `mt5_rt_s264_aia_atrmon_historical_2024_tier_a_train_era_stress` | `month` | `2024-08` | 30 | -55.69 | 0.700237 |
| `mt5_rt_s264_lc_atrmon_historical_2024_tier_a_train_era_stress` | `month` | `2024-08` | 30 | -55.32 | 0.701634 |
| `mt5_rt_s262_lih_atrmon_historical_2024_tier_a_train_era_stress` | `month` | `2024-08` | 30 | -53.29 | 0.704322 |
| `mt5_rt_s258_stc_atrmon_historical_2024_tier_a_train_era_stress` | `month` | `2024-08` | 31 | -49.21 | 0.74558 |

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267E_atrcomp_monday_guard_mt5_review`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 10개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단), guard_comparison(방어 비교).
- evidence_missing(빠진 근거): source-bar Monday(원천 봉 월요일) guard가 market-structure feature(시장 구조 피처)인지 calendar prune(달력 절단)인지 판별하는 추가 비달력 검증, visual zoom chart(확대 시각 차트), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`.
