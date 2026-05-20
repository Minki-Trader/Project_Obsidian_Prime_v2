# Stage267 Run267D Adapter/P2 MT5 Review(267단계 267D 어댑터/2차 대체 MT5 검토)

- action(행동): run267D(267D 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단)와 time-slice KPI(시간 구간 핵심 성과 지표)를 만들었다.
- effect(효과): 순수익/net profit(순수익)만 보지 않고 월, 시간, chron segment(시간 순서 구간), DD(drawdown, 손실폭)를 함께 본다.
- trade_records(거래 기록): `9706`
- time_slice_rows(시간 구간 행): `1000`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Routed Axis Review(라우팅 축 검토)

| candidate(후보) | axis(축) | role(역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | equity DD%(평가금 손실폭) | weakest month(약한 월) | read(판독) |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_aih` | `atrcomp` | `p2_replacement` | 269.2 | 1.16028 | 314 | 28.73 | `2024-07` -82.56 | p2_constructive_dd_watch(2차 대체 건설적, 손실폭 감시) |
| `s264_aia` | `atrcomp` | `p2_replacement` | 261.08 | 1.156383 | 315 | 28.89 | `2024-07` -84.18 | p2_constructive_dd_watch(2차 대체 건설적, 손실폭 감시) |
| `s258_stc` | `atrcomp` | `p2_replacement` | 260.91 | 1.138808 | 334 | 29.99 | `2024-07` -102.49 | mixed_review_needed(혼합 결과, 추가 검토 필요) |
| `s264_lc` | `atrcomp` | `p2_replacement` | 240.12 | 1.147474 | 311 | 28.78 | `2024-07` -80.24 | p2_constructive_dd_watch(2차 대체 건설적, 손실폭 감시) |
| `s262_lih` | `atrcomp` | `p2_replacement` | 201.92 | 1.124029 | 313 | 30.48 | `2024-07` -96.78 | mixed_review_needed(혼합 결과, 추가 검토 필요) |
| `s264_aih` | `late21` | `adapter_prototype` | 198.2 | 1.122222 | 312 | 22.86 | `2024-12` -88.07 | adapter_prototype_watch_not_selection(어댑터 원형 관찰, 선택 아님) |
| `s258_stc` | `late21` | `adapter_prototype` | 190.46 | 1.105067 | 332 | 26.42 | `2024-07` -101.06 | adapter_prototype_watch_not_selection(어댑터 원형 관찰, 선택 아님) |
| `s264_aia` | `late21` | `adapter_prototype` | 189.67 | 1.117835 | 313 | 22.88 | `2024-12` -87.91 | adapter_prototype_watch_not_selection(어댑터 원형 관찰, 선택 아님) |
| `s264_lc` | `late21` | `adapter_prototype` | 173.26 | 1.110259 | 309 | 22.86 | `2024-12` -84.54 | adapter_prototype_watch_not_selection(어댑터 원형 관찰, 선택 아님) |
| `s262_lih` | `late21` | `adapter_prototype` | 142.76 | 1.090721 | 311 | 25.89 | `2024-07` -95.91 | mixed_review_needed(혼합 결과, 추가 검토 필요) |
| `s258_stc` | `vlowadx` | `p2_replacement` | 203.28 | 1.095019 | 357 | 39.62 | `2024-07` -170.21 | p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계) |
| `s264_aih` | `vlowadx` | `p2_replacement` | 196.82 | 1.108254 | 334 | 34.07 | `2024-07` -105.58 | p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계) |
| `s264_aia` | `vlowadx` | `p2_replacement` | 196.82 | 1.108254 | 334 | 34.07 | `2024-07` -105.58 | p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계) |
| `s264_lc` | `vlowadx` | `p2_replacement` | 175.16 | 1.099137 | 331 | 34.39 | `2024-07` -100.37 | p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계) |
| `s262_lih` | `vlowadx` | `p2_replacement` | 142.27 | 1.080619 | 333 | 36.43 | `2024-07` -116.16 | p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계) |

## Weak Slices(약한 구간)

| record_view(기록 보기) | axis(축) | slice(구간) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `mt5_rt_s258_stc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `chron_segment` | `chron_mid` | 119 | -205.89 | 0.760298 |
| `mt5_rt_s258_stc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `weekday` | `Monday` | 61 | -195.43 | 0.567 |
| `mt5_rt_s264_lc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `weekday` | `Monday` | 56 | -180.25 | 0.533297 |
| `mt5_rt_s262_lih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `weekday` | `Monday` | 56 | -178.09 | 0.528788 |
| `mt5_rt_s264_aih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `weekday` | `Monday` | 57 | -173.09 | 0.566495 |
| `mt5_rt_s264_aia_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `weekday` | `Monday` | 57 | -172.22 | 0.564892 |
| `mt5_rt_s258_stc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `month` | `2024-07` | 40 | -170.21 | 0.479687 |
| `mt5_rt_s264_lc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `weekday` | `Monday` | 59 | -151.1 | 0.612306 |

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267D_adapter_p2_mt5_review`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 30개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단).
- evidence_missing(빠진 근거): visual zoom chart(확대 시각 차트), post-review redesigned adapter(검토 후 재설계 어댑터), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비도): `not_claimed`.
- next_action(다음 행동): `run267E_design_adapter_p2_followup_from_run267D_review`.
