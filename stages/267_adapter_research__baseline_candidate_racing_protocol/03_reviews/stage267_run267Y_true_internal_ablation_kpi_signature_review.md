# Stage267 Run267Y True Internal Ablation KPI Signature Review(267단계 267Y 진짜 내부 제거 KPI 서명 검토)

- action(행동): run267X(267X 실행)의 `48`개 KPI(핵심 성과 지표)를 signature(서명), candidate(후보), Tier pair(티어 쌍)로 나눠 봤다.
- effect(효과): 숫자만 좋아 보이는지, 실제로 변형 차이가 살아났는지, 그리고 Tier A+B(Tier A+B 합산)가 진짜 fallback(대체) 근거인지 분리한다.
- status(상태): `run267Y_true_internal_ablation_kpi_signature_review_completed`
- judgment(판정): `diagnostic_kpi_review_completed_routed_total_gap_named_no_candidate_selection`
- unique_metric_signatures(고유 지표 서명): `24`
- tier_duplicate_pairs(티어 중복 쌍): `24`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267T(267T 실행)에서는 34개 MT5(MetaTrader 5, 메타트레이더5) 결과가 2개 KPI signature(KPI 서명)로 접혔다.
이번 run267X(267X 실행)는 24개 true internal variant(진짜 내부 변형)가 각각 다른 Tier A(Tier A) signature(서명)를 만들었다.
Effect(효과): 이전보다 후보와 제거/대체 축을 구분할 수 있게 됐다.

하지만 Tier A+B(Tier A+B 합산)는 전부 Tier A(Tier A)와 같은 값이다.
Effect(효과): fallback(대체)이 실제로 빈 구간을 메운 근거가 아니므로, 이 행은 routed robustness(라우팅 견고성) 근거로 쓰면 안 된다.

숫자상 상위 후보는 보이지만, curve(곡선), weak month(약한 월), session/hour(세션/시간), trade quality(거래 품질)를 아직 보지 않았다.
Effect(효과): selected candidate(선택 후보)나 ONNX(ONNX) 검토는 여전히 금지다.

## Top Tier A Rows(상위 Tier A 행)

| rank(순위) | candidate(후보) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | boundary(경계) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `s264_lc` | `abl_gate_variant_rule` | 1700.94 | 1.47 | 400 | 19.42 | `not_candidate_selection_requires_curve_timeslice_review` |
| 2 | `s258_stc` | `rep_trend_strength_adx` | 1413.66 | 1.49 | 340 | 19.15 | `not_candidate_selection_requires_curve_timeslice_review` |
| 3 | `s258_stc` | `abl_volatility_bandwidth` | 1393.91 | 1.5 | 336 | 18.57 | `not_candidate_selection_requires_curve_timeslice_review` |
| 4 | `s264_aia` | `rep_trend_strength_adx` | 1390.83 | 1.56 | 332 | 15.44 | `not_candidate_selection_requires_curve_timeslice_review` |
| 5 | `s264_aia` | `abl_session_timing` | 1275.28 | 1.53 | 330 | 19.17 | `not_candidate_selection_requires_curve_timeslice_review` |
| 6 | `s264_aih` | `abl_volatility_bandwidth` | 1269.97 | 1.53 | 323 | 17.52 | `not_candidate_selection_requires_curve_timeslice_review` |
| 7 | `s262_lih` | `rep_volatility_atr` | 1259.93 | 1.53 | 325 | 16.85 | `not_candidate_selection_requires_curve_timeslice_review` |
| 8 | `s264_aia` | `abl_trend_strength_direction` | 1237.02 | 1.5 | 329 | 20.98 | `not_candidate_selection_requires_curve_timeslice_review` |

## Candidate Summary(후보 요약)

| candidate(후보) | rows(행) | net min(순수익 최소) | net max(순수익 최대) | net mean(순수익 평균) | worst DD%(최악 손실폭) | PF min(PF 최소) | trades total(거래 총수) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `s258_stc` | 5 | 906.92 | 1413.66 | 1170.61 | 21.43 | 1.38 | 1664 |
| `s262_lih` | 5 | 34.85 | 1259.93 | 871.47 | 22.36 | 1.06 | 1475 |
| `s264_aia` | 5 | 1093.77 | 1390.83 | 1237.64 | 20.98 | 1.50 | 1620 |
| `s264_aih` | 4 | 1097.96 | 1269.97 | 1168.95 | 19.46 | 1.44 | 1322 |
| `s264_lc` | 5 | 52.75 | 1700.94 | 1046.69 | 20.42 | 1.09 | 1568 |

## Boundary(경계)

- result_subject(결과 대상): `run267Y_true_internal_ablation_kpi_signature_review`.
- positive_claim(긍정 주장): `none`.
- useful_evidence(유용 근거): proxy collapse(대체 접힘)는 풀렸고, 24개 Tier A(Tier A) 변형이 서로 다른 KPI signature(KPI 서명)를 만들었다.
- gap_named(이름 붙인 공백): Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성)라 Tier A(Tier A) 중복이다.
- missing_required(필수 누락): balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 KPI), trade quality(거래 품질), failure memory(실패 기억) 검토.
- next_action(다음 행동): `run267Z_balance_timeslice_trade_quality_review_true_internal_ablation_results`.
