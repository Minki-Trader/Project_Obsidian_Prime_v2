# Stage267 Run267BU Pool-Wide Directional/Impulse Follow-Up Balance/Time-slice/Trade-quality Review(267단계 267BU 후보군 전체 방향/임펄스 후속 잔액/시간구간/거래품질 검토)

## Summary(요약)

- run_id(실행 ID): `run267BU_stage267_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_v1`
- source_run(원천 실행): `run267BT_stage267_pool_wide_directional_impulse_followup_mt5_execution_v1`
- status(상태): `run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_completed`
- trade_records(거래 기록): `3574`
- time_slice_rows(시간 구간 행): `410`
- negative_slices(음수 구간): `80`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BT(267BT 실행)의 10개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고, 월/요일/시간/세션/방향/초중후반 구간으로 분해했다.
Effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아 보이는 aggressive_impulse_replacement(공격형 임펄스 대체)도 DD(손실폭), 약한 월, 후반 구간을 숨기지 못하게 했다.

## Profile Summary(프로필 요약)

| profile(프로필) | positive(양수) | negative/PF broken(음수/PF 붕괴) | high DD(높은 손실폭) | net mean(순수익 평균) | DD worst(최악 손실폭) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `aggressive_impulse_replacement` | 5 | 0 | 5 | 82.886 | 40.04 | `salvage_as_aggressive_clue_not_selection(공격형 단서로 회수, 선택 아님)` |
| `directional_asymmetry` | 0 | 5 | 5 | -40.142 | 53.29 | `prune_as_standalone_profile(독립 프로필 가지치기)` |

## Candidate/Profile Review(후보/프로필 검토)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | report DD%(보고서 손실폭 %) | worst month(최악 월) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | `aggressive_impulse_replacement` | 105.26 | 1.048388 | 378 | 40.04 | `2024-07` -173.99 | `positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)` |
| `s264_aih` | `aggressive_impulse_replacement` | 93.46 | 1.04998 | 353 | 36.1 | `2024-07` -110.37 | `positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)` |
| `s264_aia` | `aggressive_impulse_replacement` | 92.91 | 1.049734 | 354 | 35.76 | `2024-07` -109.65 | `positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)` |
| `s264_lc` | `aggressive_impulse_replacement` | 71.38 | 1.03919 | 350 | 36.59 | `2024-07` -107.43 | `positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)` |
| `s262_lih` | `aggressive_impulse_replacement` | 51.42 | 1.028254 | 352 | 39.01 | `2024-07` -119.67 | `positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)` |
| `s258_stc` | `directional_asymmetry` | -22.07 | 0.990877 | 378 | 51.57 | `2024-07` -211.58 | `negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)` |
| `s264_aih` | `directional_asymmetry` | -26.15 | 0.987505 | 353 | 49.73 | `2024-07` -142.82 | `negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)` |
| `s264_aia` | `directional_asymmetry` | -34.51 | 0.983365 | 354 | 49.98 | `2024-07` -142.83 | `negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)` |
| `s264_lc` | `directional_asymmetry` | -48.21 | 0.976112 | 350 | 50.89 | `2024-07` -138.48 | `negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)` |
| `s262_lih` | `directional_asymmetry` | -69.77 | 0.965321 | 352 | 53.29 | `2024-07` -150.45 | `negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)` |

## Worst Negative Slices(최악 음수 구간)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `s258_stc` | `directional_asymmetry` | `chron_segment` | `chron_mid` | 126 | -229.56 | 60.767082 |
| `s258_stc` | `directional_asymmetry` | `month` | `2024-07` | 41 | -211.58 | 45.079688 |
| `s264_aih` | `directional_asymmetry` | `chron_segment` | `chron_mid` | 118 | -195.12 | 53.098 |
| `s262_lih` | `directional_asymmetry` | `chron_segment` | `chron_mid` | 118 | -177.04 | 49.664 |
| `s258_stc` | `aggressive_impulse_replacement` | `month` | `2024-07` | 41 | -173.99 | 37.407829 |
| `s258_stc` | `directional_asymmetry` | `weekday` | `Friday` | 88 | -173.47 | 47.407827 |
| `s258_stc` | `aggressive_impulse_replacement` | `chron_segment` | `chron_mid` | 126 | -170.42 | 51.873432 |
| `s264_lc` | `directional_asymmetry` | `weekday` | `Monday` | 60 | -167.29 | 36.541534 |
| `s262_lih` | `directional_asymmetry` | `direction` | `sell` | 207 | -166.32 | 60.119088 |
| `s262_lih` | `directional_asymmetry` | `weekday` | `Friday` | 84 | -165.83 | 43.332638 |
| `s262_lih` | `directional_asymmetry` | `weekday` | `Monday` | 60 | -164.12 | 35.908311 |
| `s264_aia` | `directional_asymmetry` | `chron_segment` | `chron_mid` | 118 | -163.44 | 48.111121 |

## Judgment(판정)

- directional_asymmetry(방향 비대칭)는 후보군 전체가 음수라 standalone branch(독립 분기)로는 가지치기한다.
- aggressive_impulse_replacement(공격형 임펄스 대체)는 전 후보 양수지만 report DD(보고서 손실폭)가 35% 이상이라 선택 후보가 아니다.
- 다음은 run267BV(267BV 실행)에서 aggressive impulse(공격형 임펄스)를 DD-shape pressure(손실폭 형태 압박)와 cross-period(확장 기간)로 설계할지, 또는 가지치기할지 결정한다.
- ONNX parity(ONNX 동등성)와 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간 구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- followup_queue(후속 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/followup_queue.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BU/pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review/failure_memory.csv`
- next_action(다음 행동): `run267BV_design_directional_impulse_followup_or_prune_from_run267BU_review`
