# Stage267 Run267C P1 Soft-Axis Follow-up Materialization(267단계 267C P1 부드러운 축 후속 물질화)

- action(행동): `25`개 feature variant(피처 변형)와 `50`개 MT5 attempt(메타트레이더5 시도)를 만들었다.
- effect(효과): P0 hard block(강제 차단)을 그대로 채택하지 않고, late session(후반 세션), vol-low(낮은 변동성), ADX(추세 강도), ATR compression(ATR 압축) 상호작용으로 좁혀 다음 MT5 실행 준비를 끝냈다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Experiment Design(실험 설계)

- hypothesis(가설): P0 broad hard block(넓은 강제 차단)의 개선은 일부 약점 regime(국면)에 집중되어 있으며, 좁은 soft-axis feature(부드러운 축 피처)로 바꾸면 거래 수 붕괴를 줄이면서 DD(drawdown, 손실폭)를 낮출 수 있다.
- decision_use(결정 사용처): 어떤 축을 실제 Adapter(어댑터) 후보로 확장할지 고른다.
- comparison_baseline(비교 기준): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5_kpi_summary.csv` and `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p0_mt5_variants/p0_mt5_full_batch_candidate_variant_summary.csv`.
- control_variables(고정 변수): 후보군, model CSV(모델 표), MT5 EA(메타트레이더5 전문가 자문), 기간, threshold(임계값), trade management(거래 관리)를 유지한다.
- changed_variables(변경 변수): entry signal(진입 신호)을 좁은 P1 약점 조건에서만 flat(무거래)으로 바꾼다.
- sample_scope(표본 범위): US100 M5 Tier A historical 2024 train-era stress(학습 기간 과거 압박)와 Tier A+B routed total(라우팅 합산) 실행 계획.
- success_criteria(성공 기준): P1 MT5 실행에서 P0보다 거래 수 비용이 작고, run267B보다 DD(손실폭), PF(수익 팩터), recovery(회복)가 개선되는 축을 찾는다.
- failure_criteria(실패 기준): P1 축이 trade count collapse(거래 수 붕괴)를 만들거나, DD(손실폭)를 줄이지 못하거나, 특정 달력 규칙으로만 설명된다.
- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), timestamp mismatch(시각 불일치), common file copy missing(공용 파일 복사 누락), MT5 output missing(MT5 출력 누락).
- stop_conditions(중단 조건): 한 축이 두 번 연속 hard block(강제 차단)과 같은 과차단으로 보이면 repair loop(수리 반복)를 열지 않고 failure memory(실패 기억)로 닫는다.
- evidence_plan(근거 계획): attempts.csv(시도 목록), feature_variant_manifest.csv(피처 변형 목록), p1 MT5 KPI summary(P1 핵심 성과 지표 요약), backtest forensics(백테스트 포렌식), full batch review(전체 묶음 검토)를 요구한다.

## P1 Axes(P1 축)

| followup variant(후속 변형) | source P0 axis(원천 P0 축) | materialization rule(물질화 규칙) | intent(의도) |
| --- | --- | --- | --- |
| `p1_late_adx20_25_soft_filter` | `lateblk` | entry signal(진입 신호)을 late session(후반 세션)이면서 ADX 20-25(추세 강도 20-25)인 행에서만 flat(무거래)으로 바꾼다. | late-session hard block(후반 세션 강제 차단)을 더 좁은 trend-strength feature(추세 강도 피처) 조건으로 바꾼다. |
| `p1_late_hour21_soft_filter` | `lateblk` | entry signal(진입 신호)을 late session(후반 세션)이면서 UTC hour 21(협정세계시 21시)인 행에서만 flat(무거래)으로 바꾼다. | late-session block(후반 세션 차단)을 전체 세션 규칙이 아니라 실제 진입 신호가 있는 후반 시간대 단서로 줄인다. |
| `p1_vol_low_adx20_25_soft_filter` | `vollowblk` | entry signal(진입 신호)을 vol_low(낮은 변동성)이면서 ADX 20-25(추세 강도 20-25)인 행에서만 flat(무거래)으로 바꾼다. | vol-low hard block(낮은 변동성 강제 차단)을 trend-strength interaction(추세 강도 상호작용)으로 좁힌다. |
| `p1_atr_compression_replacement_filter` | `vollowblk` | entry signal(진입 신호)을 ATR 14/50 compression(ATR 14/50 압축) 하위 33% 행에서만 flat(무거래)으로 바꾼다. | historical_vol_20(20봉 역사 변동성)에 우연히 붙은 것인지 ATR ratio(ATR 비율) 대체축으로 확인한다. |
| `p1_late_vol_low_intersection_filter` | `lateblk+vollowblk` | entry signal(진입 신호)을 late session(후반 세션)이면서 vol_low(낮은 변동성)인 교집합 행에서만 flat(무거래)으로 바꾼다. | 세션 약점과 낮은 변동성 약점이 같은 시장 구조인지 교집합으로 확인한다. |

## Candidate Signal Cost(후보별 신호 비용)

| candidate(후보) | variant(변형) | matched rows(조건 행) | blocked signals(차단 신호) | kept signals(유지 신호) | retention(유지율) |
| --- | --- | ---: | ---: | ---: | ---: |
| `s258_stc` | `p1_atr_compression_replacement_filter` | 3845 | 94 | None | 0.825925925926 |
| `s258_stc` | `p1_late_adx20_25_soft_filter` | 778 | 16 | None | 0.97037037037 |
| `s258_stc` | `p1_late_hour21_soft_filter` | 1825 | 55 | None | 0.898148148148 |
| `s258_stc` | `p1_late_vol_low_intersection_filter` | 1852 | 16 | None | 0.97037037037 |
| `s258_stc` | `p1_vol_low_adx20_25_soft_filter` | 926 | 31 | None | 0.942592592593 |
| `s262_lih` | `p1_atr_compression_replacement_filter` | 3845 | 94 | None | 0.825925925926 |
| `s262_lih` | `p1_late_adx20_25_soft_filter` | 778 | 16 | None | 0.97037037037 |
| `s262_lih` | `p1_late_hour21_soft_filter` | 1825 | 55 | None | 0.898148148148 |
| `s262_lih` | `p1_late_vol_low_intersection_filter` | 1852 | 16 | None | 0.97037037037 |
| `s262_lih` | `p1_vol_low_adx20_25_soft_filter` | 926 | 31 | None | 0.942592592593 |
| `s264_aia` | `p1_atr_compression_replacement_filter` | 3845 | 94 | None | 0.825925925926 |
| `s264_aia` | `p1_late_adx20_25_soft_filter` | 778 | 16 | None | 0.97037037037 |
| `s264_aia` | `p1_late_hour21_soft_filter` | 1825 | 55 | None | 0.898148148148 |
| `s264_aia` | `p1_late_vol_low_intersection_filter` | 1852 | 16 | None | 0.97037037037 |
| `s264_aia` | `p1_vol_low_adx20_25_soft_filter` | 926 | 31 | None | 0.942592592593 |
| `s264_aih` | `p1_atr_compression_replacement_filter` | 3845 | 94 | None | 0.825925925926 |
| `s264_aih` | `p1_late_adx20_25_soft_filter` | 778 | 16 | None | 0.97037037037 |
| `s264_aih` | `p1_late_hour21_soft_filter` | 1825 | 55 | None | 0.898148148148 |
| `s264_aih` | `p1_late_vol_low_intersection_filter` | 1852 | 16 | None | 0.97037037037 |
| `s264_aih` | `p1_vol_low_adx20_25_soft_filter` | 926 | 31 | None | 0.942592592593 |
| `s264_lc` | `p1_atr_compression_replacement_filter` | 3845 | 94 | None | 0.825925925926 |
| `s264_lc` | `p1_late_adx20_25_soft_filter` | 778 | 16 | None | 0.97037037037 |
| `s264_lc` | `p1_late_hour21_soft_filter` | 1825 | 55 | None | 0.898148148148 |
| `s264_lc` | `p1_late_vol_low_intersection_filter` | 1852 | 16 | None | 0.97037037037 |
| `s264_lc` | `p1_vol_low_adx20_25_soft_filter` | 926 | 31 | None | 0.942592592593 |

## Boundary(경계)

- 이 결과는 materialization(물질화)이다. Effect(효과): MT5 KPI(핵심 성과 지표)가 아직 없으므로 후보 선택이나 ONNX readiness(ONNX 준비)를 주장하지 않는다.
- direct July rule(직접 7월 규칙)은 만들지 않았다. Effect(효과): 달력 overfit(과적합)을 피하고, vol/session/trend proxy(변동성/세션/추세 대리 피처)로 검증한다.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267C_execute_p1_soft_axis_followup_mt5_batch`.
