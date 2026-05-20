# Stage267 Run267E Adapter/P2 Follow-up Materialization(267단계 267E 어댑터/2차 대체 후속 물질화)

- action(행동): run267D(267D 실행) review(검토)에서 나온 atrcomp(ATR 압축 대체) Monday(월요일) 약점을 entry weekday guard(진입 요일 방어) feature variant(피처 변형)로 물질화했다.
- effect(효과): Stage58(58단계) 이후 연구가 압축 피처(compressed feature, 압축 피처)로만 남지 않고, 실제 MT5(MetaTrader 5, 메타트레이더5) 재실행 가능한 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 이어진다.
- followup_rows(후속 행): `15`
- materialized_feature_variants(물질화 피처 변형): `5`
- attempts_planned(계획 시도): `10`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Stage58 Answer(58단계 질문 답)

충분히 활용했다고 보기는 어렵다.

- used(활용): Stage58(58단계) 이후 risk/ATR(위험/ATR), state/context(상태/문맥), rank/gate bucket(순위/게이트 구간)은 후속 후보의 재료로 남았다.
- not enough(부족): 후보군 기준의 full ablation(전체 제거), similar replacement(유사 대체), 2024 stress(2024 압박), zoom equity review(확대 평가금 검토)는 뒤늦게 Stage267(267단계)에서 다시 열렸다.
- practical read(실전 판독): 이전 연구는 버려진 것이 아니라 압축되어 있었고, 지금 goal(목표)에는 그 압축을 다시 풀어 공통 검증판으로 올리는 일이 필요하다.

## Materialized Branch(물질화 분기)

| candidate(후보) | source axis(원천 축) | run267D net(267D 순수익) | run267D PF(267D 수익 팩터) | DD%(손실폭) | blocked signals(차단 신호) | retention(유지율) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `s264_aih` | `atrcomp` | 269.2 | 1.16028 | 28.73 | 83 | 0.813901345291 |
| `s264_aia` | `atrcomp` | 261.08 | 1.156383 | 28.89 | 83 | 0.813901345291 |
| `s258_stc` | `atrcomp` | 260.91 | 1.138808 | 29.99 | 83 | 0.813901345291 |
| `s264_lc` | `atrcomp` | 240.12 | 1.147474 | 28.78 | 83 | 0.813901345291 |
| `s262_lih` | `atrcomp` | 201.92 | 1.124029 | 30.48 | 83 | 0.813901345291 |

## Held Branches(보류 분기)

| candidate(후보) | source axis(원천 축) | decision(판정) | effect(효과) |
| --- | --- | --- | --- |
| `s264_aih` | `late21` | `carry_late21_as_adapter_control_reference` | late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다. |
| `s264_lc` | `late21` | `carry_late21_as_adapter_control_reference` | late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다. |
| `s262_lih` | `late21` | `carry_late21_as_adapter_control_reference` | late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다. |
| `s258_stc` | `late21` | `carry_late21_as_adapter_control_reference` | late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다. |
| `s264_aia` | `late21` | `carry_late21_as_adapter_control_reference` | late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다. |
| `s258_stc` | `vlowadx` | `hold_vlowadx_for_redesign_or_reject` | vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다. |
| `s264_aih` | `vlowadx` | `hold_vlowadx_for_redesign_or_reject` | vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다. |
| `s264_aia` | `vlowadx` | `hold_vlowadx_for_redesign_or_reject` | vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다. |
| `s264_lc` | `vlowadx` | `hold_vlowadx_for_redesign_or_reject` | vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다. |
| `s262_lih` | `vlowadx` | `hold_vlowadx_for_redesign_or_reject` | vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다. |

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): atrcomp(ATR 압축 대체)의 headline KPI(대표 핵심 성과 지표)는 건설적이지만 Monday(월요일) 약점이 공통으로 반복되므로, source-bar Monday(원천 봉 월요일) 진입을 막으면 DD(drawdown, 손실폭)가 줄어드는지 확인한다.
- comparison(비교): run267D(267D 실행) atrcomp(ATR 압축 대체) 결과와 run267E(267E 실행) atrcomp Monday guard(ATR 압축 월요일 방어)를 candidate(후보)별로 비교한다.
- control(통제): model CSV(모델 표), threshold(임계값), max hold(최대 보유), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 date window(2024 날짜 구간)는 유지한다.
- changed variable(변경 변수): entry signal(진입 신호)만 Monday(월요일) source bar(원천 봉)에서 flat(무거래)으로 바꾼다.
- invalid condition(무효 조건): 단순 거래 절단으로 순수익만 좋아지고 trade count(거래 수), curve shape(곡선 형태), DD(drawdown, 손실폭)가 불편하면 후보 개선으로 보지 않는다.
- stop condition(중단 조건): 이 분기가 월요일 하나에 과적합하거나 손실을 다른 구간으로 밀면 repair loop(수리 반복)를 닫고 feature engineering(피처 엔지니어링) 또는 후보 탈락으로 넘긴다.

## Judgment Boundary(판정 경계)

- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준선): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- result_subject(결과 대상): `run267E_adapter_p2_followup_materialization`.
- evidence_available(사용 가능 근거): run267D(267D 실행) review(검토), feature/model lineage(피처/모델 계보), set/ini manifest(설정/초기화 목록).
- evidence_missing(빠진 근거): run267E(267E 실행) MT5(MetaTrader 5, 메타트레이더5) execution(실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice review(시간 구간 검토).
- next_action(다음 행동): `run267E_execute_atrcomp_monday_guard_mt5_batch`.
