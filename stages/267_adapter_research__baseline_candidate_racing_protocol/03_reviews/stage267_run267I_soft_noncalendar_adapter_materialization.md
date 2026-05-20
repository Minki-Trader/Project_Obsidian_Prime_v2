# Stage267 Run267I Soft Non-Calendar Adapter Materialization(267단계 267I 부드러운 비달력 어댑터 물질화)

- action(행동): run267H(267H 실행)의 P0 queue(P0 대기열)를 받아 `s264_aih`, `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음을 만들었다.
- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 hard guard(강한 방어)가 아니라 soft score(부드러운 점수) 모델 입력이 약한 월/구간을 덜 깨뜨리는지 검증할 수 있다.
- candidate_count(후보 수): `2`
- attempt_count(시도 수): `4`
- feature_count(피처 수): `4`
- model_materialization_type(모델 물질화 유형): `research_score_table_extension_not_retrained`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 판독)

이번 작업은 숫자가 좋아졌다는 판정이 아니다. 실제 실행 가능한 입력 묶음을 만든 것이다.
`s264_aih`는 core challenger(핵심 도전자), `s264_lc`는 defensive control(방어 기준)로 함께 물질화했다.
모델은 true retrain(진짜 재학습)이 아니라 작은 additive score-table extension(가산 점수표 확장)이다. 효과는 MT5(MetaTrader 5, 메타트레이더5) 실행 전 단계에서 feature order(피처 순서), model hash(모델 해시), set/ini(설정/초기화)를 먼저 고정하는 것이다.

## Materialized Candidates(물질화 후보)

| lane(레인) | candidate(후보) | feature hash(피처 해시) | model hash(모델 해시) | high score signal ratio(높은 점수 신호 비율) |
| --- | --- | --- | --- | --- |
| `P0` | `s264_aih` | `a5a1a50b36d2` | `95c6242f2d1c` | `0.0296296296296` |
| `P0_control` | `s264_lc` | `065de1995918` | `95c6242f2d1c` | `0.0296296296296` |

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): ADX/ATR(추세 강도/ATR) 약점 문맥은 hard block(강한 차단)보다 soft model feature(부드러운 모델 피처)로 넣을 때 거래 수 붕괴를 줄일 수 있다.
- decision_use(결정 용도): 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음) 실행에서 P0 후보를 계속 밀지, branch(분기)를 닫을지 판단한다.
- comparison_baseline(비교 기준): run267D atrcomp(ATR 압축), run267E Monday guard(월요일 방어), run267F adx2025/dilowq33(ADX/DI 방어), run267H design(설계).
- control_variables(고정 변수): 후보 2개, 2024 historical window(2024 과거 구간), thresholds(임계값), trade management(거래 관리), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문).
- changed_variables(변경 변수): `stage267_adx_atr_soft_score` feature(피처), feature order hash(피처 순서 해시), additive score-table term(가산 점수표 항).
- success_criteria(성공 기준): net/PF(순수익/수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), Monday/July/chron_mid(월요일/7월/중간 구간)가 함께 덜 깨져야 한다.
- failure_criteria(실패 기준): 거래 수 붕괴, DD(drawdown, 손실폭) 악화, 약한 월 미개선, 또는 P0 control(우선순위 0 기준)까지 함께 망가지면 실패다.
- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), model hash missing(모델 해시 누락), set/ini path missing(설정/초기화 경로 누락), MT5 report missing(MT5 보고서 누락).
- stop_conditions(중단 조건): 실행 후 hard guard(강한 방어)보다 낫지 않거나 약한 구간이 그대로면 ADX/ATR soft branch(부드러운 분기)를 닫거나 true retrain(진짜 재학습) 설계로 전환한다.
- evidence_plan(근거 계획): attempt manifest(시도 목록), MT5 reports(MT5 보고서), trade/time-slice/curve review(거래/시간 구간/곡선 검토), artifact hashes(산출물 해시).

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/soft_feature_engineering_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv`
- producer(생산자): `stage_pipelines/stage267/run267I_soft_noncalendar_adapter_materialization.py`
- consumer(소비자): `run267I_execute_p0_soft_noncalendar_adapter_mt5_batch`
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/feature_model_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/runtime_contract.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/soft_score_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/lineage.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/result.json`
- availability(가용성): tracked(추적됨) after commit; reproducible_from_command(명령으로 재생성 가능).
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267I_p0_soft_noncalendar_adapter_materialization`.
- evidence_available(사용 가능 근거): feature/model/set/ini(피처/모델/설정/초기화) 산출물, runtime contract(런타임 계약), hash(해시), manifest(목록).
- evidence_missing(빠진 근거): MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선), trade/time-slice KPI(거래/시간 구간 핵심 성과 지표).
- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267I_execute_p0_soft_noncalendar_adapter_mt5_batch`.
