# Stage267 Run267C P1 Soft-Axis Follow-up Review(267단계 267C 실행 1차 부드러운 축 후속 검토)

- action(행동): P1 soft-axis MT5 batch(1차 부드러운 축 메타트레이더5 묶음 실행)를 run267B base(267B 기준값)와 P0 hard block(0차 강제 차단) 결과에 같이 맞춰 비교했다.
- effect(효과): 좋아 보이는 숫자만 고르지 않고, 거래 수 비용, DD drawdown(손실폭), P0 repair retention(0차 수리 효과 유지), signal retention(신호 유지율)을 같이 보게 했다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Axis Read(축 판독)

| axis(축) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | avg signal retention(평균 신호 유지율) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| late-session plus ADX 20-25 soft filter(후반 세션과 ADX 20-25 부드러운 필터) | 28.794 | 0.014 | -5.2 | -1.188 | 0.97037037037 | best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열) |
| late-session hour 21 soft filter(후반 세션 21시 부드러운 필터) | 98.6 | 0.068 | -42 | -14.15 | 0.898148148148 | best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열) |
| low-volatility plus ADX 20-25 soft filter(낮은 변동성과 ADX 20-25 부드러운 필터) | 102.6 | 0.058 | -19.6 | -2.616 | 0.942592592593 | best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열) |
| ATR compression replacement filter(ATR 압축 대체 필터) | 166.376 | 0.104 | -40 | -8.958 | 0.825925925926 | best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열) |
| late-session low-volatility intersection filter(후반 세션 낮은 변동성 교차 필터) | 67.334 | 0.03 | -5.2 | -5.416 | 0.97037037037 | best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열) |

## Top Routed Reads(상위 라우팅 판독)

| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | net delta(순수익 차이) | DD delta(손실폭 차이) | P1 vs P0 net(1차 대 0차 순수익) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | ATR compression replacement filter(ATR 압축 대체 필터) | 269.2 | 1.16 | 314 | 28.73 | 173.64 | -7.95 | -167.06 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s264_aia` | ATR compression replacement filter(ATR 압축 대체 필터) | 261.08 | 1.16 | 315 | 28.89 | 174.01 | -8.01 | -175.18 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s258_stc` | ATR compression replacement filter(ATR 압축 대체 필터) | 260.91 | 1.14 | 334 | 29.99 | 158.02 | -10.44 | -198.13 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s264_lc` | ATR compression replacement filter(ATR 압축 대체 필터) | 240.12 | 1.15 | 311 | 28.78 | 168.78 | -8.74 | -176.47 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s258_stc` | low-volatility plus ADX 20-25 soft filter(낮은 변동성과 ADX 20-25 부드러운 필터) | 203.28 | 1.1 | 357 | 39.62 | 100.39 | -0.81 | -255.76 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s262_lih` | ATR compression replacement filter(ATR 압축 대체 필터) | 201.92 | 1.12 | 313 | 30.48 | 157.43 | -9.65 | -214.67 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s264_aih` | late-session hour 21 soft filter(후반 세션 21시 부드러운 필터) | 198.2 | 1.12 | 312 | 22.86 | 102.64 | -13.82 | -33.22 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s264_aih` | low-volatility plus ADX 20-25 soft filter(낮은 변동성과 ADX 20-25 부드러운 필터) | 196.82 | 1.11 | 334 | 34.07 | 101.26 | -2.61 | -239.44 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s264_aia` | low-volatility plus ADX 20-25 soft filter(낮은 변동성과 ADX 20-25 부드러운 필터) | 196.82 | 1.11 | 334 | 34.07 | 109.75 | -2.83 | -239.44 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |
| `s258_stc` | late-session hour 21 soft filter(후반 세션 21시 부드러운 필터) | 190.46 | 1.11 | 332 | 26.42 | 87.57 | -14.01 | -39.78 | constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님) |

## Judgment Boundary(판정 경계)

- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- result_subject(결과 대상): `run267C_p1_soft_axis_followup_review`.
- evidence_available(사용 가능 근거): P1 KPI(KPI, 핵심 성과 지표), P1 backtest forensics(백테스트 포렌식), feature manifest(피처 목록), P0 comparison(0차 비교), run267B base(267B 기준값).
- evidence_missing(빠진 근거): equity curve(평가금 곡선) 확대 검토, 월별/세션별/요일별 breakdown(분해), adapter prototype(어댑터 원형), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `exploratory(탐색)`.
- next_condition(다음 조건): `run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement`. Effect(효과): P1에서 덜 깨진 축만 adapter prototype(어댑터 원형)이나 P2 replacement(2차 대체)로 넘기고, 약한 축은 실패 기억으로 닫는다.
