# Stage267 Run267P Internal Feature Order Confirmation and Adapter Design(267P 내부 피처 순서 확인 및 어댑터 설계)

## Summary(요약)

- status(상태): `run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design_completed`
- run_id(실행 ID): `run267P_stage267_pool_wide_internal_feature_order_confirmation_and_adapter_design_v1`
- source_run(원천 실행): `run267O_stage267_pool_wide_balance_timeslice_trade_quality_review_v1`
- action(행동): run267O(267O 실행)의 강한 KPI(핵심 성과 지표) 단서를 run267N(267N 실행)의 feature order(피처 순서), runtime contract(런타임 계약), materialization boundary(물질화 경계)와 다시 대조했다.
- effect(효과): proxy clue(대체 단서), direct gate clue(직접 게이트 단서), failure memory(실패 기억)를 분리해 다음 Adapter(어댑터) 물질화가 숫자만 따라가지 않게 했다.
- audit_rows(감사 행): `24`
- adapter_queue_rows(어댑터 큐 행): `8`
- p0_adapter_rows(P0 어댑터 행): `4`
- failure_memory_rows(실패 기억 행): `19`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267Q_materialize_internal_feature_order_confirmed_adapter_candidates`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

이전 stage(단계) 연구는 버려지지 않았지만, 충분히 펼쳐졌다고 보기는 어렵다. run267P(267P 실행)는 그 빈칸을 줄이는 작업이다.
특히 run267O(267O 실행)에서 좋아 보인 volatility/ATR(변동성/ATR) 축은 아직 true internal feature ablation(진짜 내부 피처 제거)이 아니라 proxy adapter variant(대체 어댑터 변형)이다.
그래서 이번 결론은 후보 선택이 아니라, 어떤 단서를 Adapter(어댑터) 설계로 넘길 수 있고 어떤 단서는 실패 기억으로 묶어야 하는지 정리한 것이다.

## Adapter Design Queue(어댑터 설계 큐)

| priority(우선순위) | candidate(후보) | test(시험) | class(분류) | action(행동) |
| --- | --- | --- | --- | --- |
| `P0` | `s264_aih` | `abl_volatility_bandwidth` | `adapter_design_p0_internal_feature_order_confirmed` | rebuild proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 물질화하고 feature order(피처 순서)를 고정한다 |
| `P0` | `s264_aih` | `rep_volatility_atr` | `adapter_design_p0_internal_feature_order_confirmed` | rebuild proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 물질화하고 feature order(피처 순서)를 고정한다 |
| `P0` | `s264_aia` | `abl_volatility_bandwidth` | `adapter_design_p0_internal_feature_order_confirmed` | rebuild proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 물질화하고 feature order(피처 순서)를 고정한다 |
| `P0` | `s264_aia` | `rep_volatility_atr` | `adapter_design_p0_internal_feature_order_confirmed` | rebuild proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 물질화하고 feature order(피처 순서)를 고정한다 |
| `AUDIT` | `s264_lc` | `abl_gate_variant_rule` | `direct_gate_audit_control_not_adapter` | direct gate/rank contrast(직접 게이트/순위 대조)를 먼저 수행하고 Adapter(어댑터) 후보로 승격하지 않는다 |
| `P1` | `s258_stc` | `abl_volatility_bandwidth` | `adapter_design_p1_stress_watch` | P0 결과와 같은 산출물 형식으로만 보조 비교하고 단독 후보로 올리지 않는다 |
| `P1` | `s264_lc` | `rep_volatility_atr` | `adapter_design_p1_control_or_salvage_watch` | P0 결과와 같은 산출물 형식으로만 보조 비교하고 단독 후보로 올리지 않는다 |
| `P1` | `s262_lih` | `rep_volatility_atr` | `adapter_design_p1_control_or_salvage_watch` | P0 결과와 같은 산출물 형식으로만 보조 비교하고 단독 후보로 올리지 않는다 |

## Candidate Decisions(후보별 판정)

| candidate(후보) | P0 | P1 | audit(감사) | failures(실패) | decision(판정) |
| --- | ---: | ---: | ---: | ---: | --- |
| `s258_stc` | 0 | 1 | 0 | 0 | `retain_as_watch_or_stress_control_no_selection` |
| `s262_lih` | 0 | 1 | 0 | 1 | `retain_as_watch_or_stress_control_no_selection` |
| `s264_aia` | 2 | 0 | 0 | 0 | `advance_volatility_proxy_to_adapter_design_p0_no_selection` |
| `s264_aih` | 2 | 0 | 0 | 0 | `advance_volatility_proxy_to_adapter_design_p0_no_selection` |
| `s264_lc` | 0 | 1 | 1 | 1 | `retain_direct_gate_audit_control_no_adapter_selection` |

## Failure Memory(실패 기억)

| candidate(후보) | test(시험) | flags(표식) | worst month(최악 월) | slice(구간) |
| --- | --- | --- | --- | --- |
| `s264_lc` | `abl_gate_variant_rule` | `['severe_session_le_-150', 'severe_hour_le_-140', 'chron_segment_negative']` | `2024-07` -86.87 | `session_report` `session_07_12_report_time` -219.59 |
| `s258_stc` | `abl_volatility_bandwidth` | `['chron_segment_negative']` | `2024-06` -46.68 | `session_report` `session_07_12_report_time` -93.19 |
| `s262_lih` | `rep_volatility_atr` | `['chron_segment_negative']` | `2024-06` -32.37 | `weekday` `Monday` -96.28 |
| `s264_aia` | `abl_session_timing` | `['chron_segment_negative']` | `2024-07` -72.07 | `weekday` `Monday` -109.7 |
| `s258_stc` | `abl_session_timing` | `['severe_month_le_-100', 'severe_weekday_le_-120', 'chron_segment_negative']` | `2024-07` -117.58 | `weekday` `Monday` -130.54 |
| `s258_stc` | `abl_price_return_range` | `['severe_weekday_le_-120', 'chron_segment_negative']` | `2024-04` -78.2 | `weekday` `Monday` -121.57 |
| `s258_stc` | `abl_trend_strength_direction` | `['severe_month_le_-100', 'chron_segment_negative']` | `2024-07` -122.87 | `chron_segment` `chron_mid` -130.18 |
| `s258_stc` | `rep_trend_strength_adx` | `['severe_month_le_-100', 'chron_segment_negative']` | `2024-07` -122.87 | `chron_segment` `chron_mid` -130.18 |
| `s264_aih` | `abl_trend_strength_direction` | `['negative_month_count_ge_6', 'chron_segment_negative']` | `2024-07` -74.27 | `weekday` `Monday` -114.07 |
| `s264_aih` | `rep_trend_strength_adx` | `['negative_month_count_ge_6', 'chron_segment_negative']` | `2024-07` -74.27 | `weekday` `Monday` -114.07 |
| `s264_aia` | `abl_trend_strength_direction` | `['negative_month_count_ge_6', 'chron_segment_negative']` | `2024-07` -74.27 | `weekday` `Monday` -114.07 |
| `s264_aia` | `rep_trend_strength_adx` | `['negative_month_count_ge_6', 'chron_segment_negative']` | `2024-07` -74.27 | `weekday` `Monday` -114.07 |

## Performance Attribution(성과 귀속)

- observed_change(관측 변화): volatility/ATR(변동성/ATR) proxy(대체) 축은 `s264_aih`와 `s264_aia`에서 반복 단서가 되었고, `s264_lc`의 gate variant(게이트 변형)는 숫자는 강하지만 직접 런타임 표면 변경이다.
- likely_driver(가능 원인): 변동성 압축/확장 문맥이 2024년 약한 구간의 손실폭을 줄였을 수 있다.
- weakness(약점): `s264_lc` gate variant(게이트 변형)는 session_07_12(07~12시 세션)와 hour 22(22시) 약점이 크고, gate rank bucket(게이트 순위 구간)은 실패 기억이다.
- attribution_boundary(귀속 경계): 이번 실행은 설계 감사이며, Adapter(어댑터) 물질화나 MT5(MetaTrader 5, 메타트레이더5) 재실행 결과가 아니다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.py`
- source_candidate_test_review(원천 후보-시험 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/candidate_test_review.csv`
- source_variant_manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/p0_materialized_variant_manifest.csv`
- internal_feature_order_audit(내부 피처 순서 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/internal_feature_order_audit.csv`
- adapter_design_queue(어댑터 설계 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/adapter_design_queue.csv`
- candidate_axis_decision(후보 축 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/candidate_axis_decision.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/failure_memory.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/lineage.json`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design`.
- judgment_label(판정 라벨): `design_audit_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
