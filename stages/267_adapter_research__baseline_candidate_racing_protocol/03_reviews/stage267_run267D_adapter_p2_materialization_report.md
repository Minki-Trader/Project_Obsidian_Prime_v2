# Stage267 Run267D Adapter/P2 Materialization(267단계 267D 어댑터/2차 대체 물질화)

- action(행동): late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체)를 `15`개 design row(설계 행)와 `30`개 MT5 attempt(메타트레이더5 시도)로 물질화했다.
- effect(효과): run267C(267C 실행)의 축 선택을 다음 Strategy Tester(전략 테스터) 실행 가능한 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 바꿨다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로 구조화해도 P1 수리 효과를 유지할 수 있고, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 similar replacement(유사 대체) 축으로 약점 설명력을 넓힐 수 있다.
- decision_use(결정 사용처): 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)가 Adapter(어댑터) 개발을 계속할지, P2 replacement(2차 대체)를 살릴지, 또는 실패 기억으로 닫을지 결정한다.
- comparison_baseline(비교 기준): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_axis_selection_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_adapter_p2_candidate_shortlist.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_soft_axis_kpi_summary.csv`.
- control_variables(고정 변수): Stage267(267단계) 5개 후보군, 2024 historical stress(2024 과거 압박), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), threshold(임계값), trade management(거래 관리)를 유지한다.
- changed_variables(변경 변수): run267D(267D 실행) 전용 artifact lineage(산출물 계보), runtime contract(런타임 계약), attempt namespace(시도 이름공간)만 바꾼다.
- sample_scope(표본 범위): Tier A(티어 A)와 Tier A+B(티어 A+B) routed historical 2024(라우팅 과거 2024) 재검증 준비.
- success_criteria(성공 기준): 실행 후 balance/equity curve(잔액/평가금 곡선), PF(수익 팩터), DD(drawdown, 손실폭), recovery(회복), expectancy(기대값), trade count(거래 수)가 후보별 역할에 맞게 덜 깨져야 한다.
- failure_criteria(실패 기준): 거래 수 붕괴, 특정 축 과의존, DD 악화, 또는 곡선 구멍이 확대되면 Adapter/P2(어댑터/2차 대체) 이월을 중단한다.
- invalid_conditions(무효 조건): feature order hash(피처 순서 해시), common file copy(공통 파일 복사), set/ini(설정/초기화), MT5 output(MT5 출력) 중 하나라도 불일치하면 실행 해석은 무효다.
- stop_conditions(중단 조건): 한 축/한 월/한 threshold(임계값) 미세조정만 반복되면 repair loop(수리 반복)를 닫고 다른 구조 질문으로 전환한다.
- evidence_plan(근거 계획): run267D attempt(시도), backtest forensics(백테스트 포렌식), KPI(KPI, 핵심 성과 지표), balance/time-slice review(잔액/시간 구간 검토)를 같은 장부에 연결한다.

## Adapter Prototype(어댑터 원형)

| candidate(후보) | pair role(쌍 역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | `primary_adapter_probe_pair(주 어댑터 탐침 쌍)` | 198.2 | 1.12 | 312 | 22.86 | adapter_probe_ready_not_selection(어댑터 탐침 준비, 선택은 아님) |
| `s264_lc` | `adapter_control_pair(어댑터 대조 쌍)` | 173.26 | 1.11 | 309 | 22.86 | adapter_probe_ready_not_selection(어댑터 탐침 준비, 선택은 아님) |
| `s262_lih` | `adapter_control_pair(어댑터 대조 쌍)` | 142.76 | 1.09 | 311 | 25.89 | exploratory_pair_requires_runtime_review(탐색 쌍, 런타임 검토 필요) |
| `s258_stc` | `adapter_stress_or_anchor_pair(어댑터 압박/앵커 쌍)` | 190.46 | 1.11 | 332 | 26.42 | adapter_probe_ready_not_selection(어댑터 탐침 준비, 선택은 아님) |
| `s264_aia` | `adapter_stress_or_anchor_pair(어댑터 압박/앵커 쌍)` | 189.67 | 1.12 | 313 | 22.88 | adapter_probe_ready_not_selection(어댑터 탐침 준비, 선택은 아님) |

## P2 Replacement(2차 대체)

| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | retention(유지율) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | `atrcomp` | 269.2 | 1.16 | 314 | 28.73 | 0.825925925926 | p2_net_strong_signal_cost_watch(2차 순수익 강함, 신호 비용 관찰) |
| `s264_aia` | `atrcomp` | 261.08 | 1.16 | 315 | 28.89 | 0.825925925926 | p2_net_strong_signal_cost_watch(2차 순수익 강함, 신호 비용 관찰) |
| `s258_stc` | `atrcomp` | 260.91 | 1.14 | 334 | 29.99 | 0.825925925926 | p2_net_strong_signal_cost_watch(2차 순수익 강함, 신호 비용 관찰) |
| `s264_lc` | `atrcomp` | 240.12 | 1.15 | 311 | 28.78 | 0.825925925926 | p2_net_strong_signal_cost_watch(2차 순수익 강함, 신호 비용 관찰) |
| `s258_stc` | `vlowadx` | 203.28 | 1.1 | 357 | 39.62 | 0.942592592593 | p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰) |
| `s262_lih` | `atrcomp` | 201.92 | 1.12 | 313 | 30.48 | 0.825925925926 | exploratory_pair_requires_runtime_review(탐색 쌍, 런타임 검토 필요) |
| `s264_aih` | `vlowadx` | 196.82 | 1.11 | 334 | 34.07 | 0.942592592593 | p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰) |
| `s264_aia` | `vlowadx` | 196.82 | 1.11 | 334 | 34.07 | 0.942592592593 | p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰) |
| `s264_lc` | `vlowadx` | 175.16 | 1.1 | 331 | 34.39 | 0.942592592593 | p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰) |
| `s262_lih` | `vlowadx` | 142.27 | 1.08 | 333 | 36.43 | 0.942592592593 | p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰) |

## Runtime Parity Boundary(런타임 동등성 경계)

- research_path(연구 경로): `stage_pipelines/stage267/run267D_adapter_p2_materialization.py`.
- runtime_path(런타임 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/attempts.csv`.
- shared_contract(공유 계약): feature order hash(피처 순서 해시), model CSV(모델 표), threshold(임계값), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 date window(2024 날짜 구간).
- known_differences(알려진 차이): run267D(267D 실행)는 run267C(267C 실행) P1 selected artifact(선택 산출물)를 새 lineage(계보) 아래 복사한다. 의사결정 로직은 아직 바꾸지 않는다.
- parity_check(동등성 검사): materialization hash/copy check(물질화 해시/복사 검사) 완료, Strategy Tester output(전략 테스터 출력)은 다음 실행 조건이다.
- runtime_claim_boundary(런타임 주장 경계): `research_only_runtime_execution_pending`.

## Judgment Boundary(판정 경계)

- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준선): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- result_subject(결과 대상): `run267D_adapter_p2_materialization`.
- evidence_available(사용 가능 근거): P1 axis selection(P1 축 선택), P1 KPI(P1 핵심 성과 지표), feature/model hashes(피처/모델 해시), set/ini manifest(설정/초기화 목록).
- evidence_missing(빠진 근거): run267D MT5 execution(267D MT5 실행), zoomed equity curve(확대 평가금 곡선), full time-slice breakdown(전체 시간 구간 분해), Adapter stability review(어댑터 안정성 검토), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 후보 선택 없음)`.
- next_condition(다음 조건): `run267D_execute_adapter_prototype_and_p2_replacement_mt5_batch`.
