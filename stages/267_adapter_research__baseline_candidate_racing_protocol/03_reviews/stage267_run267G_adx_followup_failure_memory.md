# Stage267 Run267G ADX Follow-up and DI Failure Memory(267단계 267G ADX 후속과 DI 실패 기억)

- action(행동): run267F(267F 실행)의 guard comparison(방어 비교)과 weak slices(약한 구간)를 failure memory(실패 기억), follow-up design(후속 설계), stop rules(중단 규칙)로 정리했다.
- effect(효과): `adx2025`는 soft context seed(부드러운 문맥 씨앗)로만 남기고, `dilowq33` exact repeat(정확 반복)는 막아 다음 Adapter(어댑터) 연구가 좁은 미세조정에 갇히지 않게 한다.
- source_evidence(원천 근거): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/guard_comparison.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/negative_slice_summary.csv`
- failure_rows(실패 기억 행): `10`
- followup_design_rows(후속 설계 행): `5`
- stop_rule_rows(중단 규칙 행): `3`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 판독)

이전 단계 연구는 버려진 것이 아니라, 이제 실제 R&D racing(연구개발 경주) 문법으로 재사용되기 시작했다.
run267F(267F 실행)는 ADX(추세 강도)가 약간의 구조 신호일 수 있음을 보여줬지만, 월요일과 7월 약점까지 해결하지는 못했다.
DI spread(방향성 차이) q33 대체는 강하게 나빠졌으므로 같은 형태는 실패 기억으로 묶는다.

## Key Reads(핵심 판독)

- best_adx_partial(가장 나은 ADX 부분 지지): `s258_stc` net_delta_vs_run267D(267D 대비 순수익 변화) `61.3`, weakest_weekday(약한 요일) `Monday` `-181.07`.
- worst_di_failure(가장 나쁜 DI 실패): `s258_stc` net_delta_vs_run267D(267D 대비 순수익 변화) `-233.47`, dd_delta_vs_run267D(267D 대비 손실폭 변화) `6.23`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.

## Failure Memory(실패 기억)

| candidate(후보) | guard(방어) | classification(분류) | net vs D(267D 대비) | net vs E(267E 대비) | weakest(약점) | reuse rule(재사용 규칙) |
| --- | --- | --- | ---: | ---: | --- | --- |
| `s258_stc` | `adx2025` | `partial_support_keep_as_soft_context_seed` | 61.3 | -103.36 | `Monday` -181.07; `2024-07` -98.91 | 정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다. |
| `s264_aih` | `adx2025` | `partial_support_keep_as_soft_context_seed` | 35.73 | -116.18 | `Monday` -156.64; `2024-07` -96.82 | 정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다. |
| `s264_aia` | `adx2025` | `partial_support_keep_as_soft_context_seed` | 43.85 | -102.56 | `Monday` -156.64; `2024-07` -96.82 | 정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다. |
| `s264_lc` | `adx2025` | `partial_support_keep_as_soft_context_seed` | 45.62 | -120.45 | `Monday` -161.21; `2024-07` -93.54 | 정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다. |
| `s262_lih` | `adx2025` | `partial_support_keep_as_soft_context_seed` | 41.09 | -119.32 | `Monday` -158.19; `2024-07` -107.49 | 정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다. |
| `s264_aih` | `dilowq33` | `negative_failure_memory_block_exact_repeat` | -218.49 | -370.4 | `Monday` -97.09; `2024-06` -65.44 | standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다. |
| `s264_aia` | `dilowq33` | `negative_failure_memory_block_exact_repeat` | -210.37 | -356.78 | `Monday` -97.09; `2024-06` -65.44 | standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다. |
| `s264_lc` | `dilowq33` | `negative_failure_memory_block_exact_repeat` | -197.9 | -363.97 | `Monday` -97.29; `2024-06` -64.95 | standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다. |
| `s258_stc` | `dilowq33` | `negative_failure_memory_block_exact_repeat` | -233.47 | -398.13 | `Monday` -125.18; `2024-06` -81.14 | standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다. |
| `s262_lih` | `dilowq33` | `negative_failure_memory_block_exact_repeat` | -189.09 | -349.5 | `Monday` -96.02; `2024-06` -64.95 | standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다. |

## Follow-up Design(후속 설계)

- hypothesis(가설): ADX/ATR compression(추세 강도/ATR 압축)은 hard prune(강한 절단)보다 soft score/risk scale(부드러운 점수/위험 배율)로 구조화해야 덜 깨질 수 있다.
- comparison_baseline(비교 기준): run267D(267D 실행), run267E(267E 실행), run267F(267F 실행).
- success_criteria(성공 기준): net/PF(순수익/수익 팩터) 개선만이 아니라 Monday/July/chron_mid(월요일/7월/중간 구간)가 덜 깨져야 한다.
- failure_criteria(실패 기준): 거래 수만 줄이거나 특정 약한 구간이 그대로면 실패다.
- stop_condition(중단 조건): 같은 hard guard(강한 방어)는 반복하지 않고, run267H(267H 실행)에서 soft feature/risk-scale(부드러운 피처/위험 배율) 물질화 여부를 결정한다.

## Stop Rules(중단 규칙)

- `run267G_stop_exact_dilowq33`: dilowq33 standalone hard filter(DI 낮은 33% 단독 강한 필터)는 반복 금지한다. Effect(효과): run267F에서 모든 후보가 악화된 조건을 다시 실행해 시간을 쓰지 않는다.
- `run267G_stop_adx_hard_equivalence_claim`: adx2025를 run267E Monday guard(월요일 방어)와 동급이라고 말하지 않는다. Effect(효과): 부분 지지 evidence(근거)를 후보 선택이나 ONNX(ONNX) 준비로 과장하지 않는다.
- `run267G_stop_monday_only_bottleneck`: Monday(월요일) 손실만 줄이는 미세 조정으로 3 stage(단계) 이상 끌지 않는다. Effect(효과): 월요일 한 구간에 갇히지 않고 feature engineering(피처 엔지니어링)과 Adapter(어댑터) 구조로 넓힌다.

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267G_adx_followup_failure_memory`.
- evidence_available(사용 가능 근거): run267F MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표), guard comparison(방어 비교), weak slices(약한 구간), generated failure/design/stop files(생성 실패/설계/중단 파일).
- evidence_missing(빠진 근거): run267H materialization/execution(물질화/실행), new balance/equity curve(잔액/평가금 곡선), expanded period(확장 기간) 재검증.
- judgment_label(판정 라벨): `design_review_completed_no_candidate_selection`.
- claim_boundary(주장 경계): design/failure-memory only(설계/실패 기억 전용). 후보 선택, ONNX(ONNX), 운영 의미를 주장하지 않는다.
- next_action(다음 행동): `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`.
