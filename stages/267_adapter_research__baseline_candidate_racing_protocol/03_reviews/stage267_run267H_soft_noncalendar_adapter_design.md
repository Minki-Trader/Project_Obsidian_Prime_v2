# Stage267 Run267H Soft Non-Calendar Adapter Design(267단계 267H 부드러운 비달력 어댑터 설계)

- action(행동): run267G(267G 실행)의 failure memory(실패 기억)를 받아 soft feature engineering matrix(부드러운 피처 엔지니어링 행렬), Adapter surface matrix(어댑터 표면 행렬), experiment queue(실험 대기열)를 만들었다.
- effect(효과): hard guard(강한 방어) 반복을 막고, ADX/ATR/DI(추세 강도/ATR/방향성 차이)를 model feature(모델 피처), exit overlay(청산 오버레이), risk sizing probe(위험 크기 조절 탐침)로 나눠 다음 물질화 후보를 좁힌다.
- feature_rows(피처 행): `20`
- adapter_surface_rows(어댑터 표면 행): `3`
- experiment_queue_rows(실험 대기열 행): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 판독)

이번 단계는 숫자를 더 좋게 보이게 만드는 실행이 아니다. 어떤 구조를 다음에 실제로 물질화할지 정하는 설계다.
`s264_aih`는 핵심 challenger(도전자)라 P0(우선순위 0)이고, `s264_lc`는 defensive control(방어 기준)로 같이 둔다.
`dilowq33` 같은 hard filter(강한 필터)는 반복하지 않고, DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 continuous feature(연속 피처)로만 다시 본다.

## P0 Queue(P0 대기열)

| lane(레인) | candidate(후보) | feature design(피처 설계) | adapter mode(어댑터 모드) | decision(결정) |
| --- | --- | --- | --- | --- |
| `P0` | `s264_aih` | `adx_atr_soft_score` | `feature_only_model_retrain` | `materialize_next` |
| `P0_control` | `s264_lc` | `adx_atr_soft_score` | `feature_only_model_retrain` | `materialize_next` |

## Adapter Surfaces(어댑터 표면)

| adapter mode(어댑터 모드) | support(지원 상태) | implementation(구현 범위) | verification(검증 필요) |
| --- | --- | --- | --- |
| `exit_overlay_existing_runtime_possible` | `partially_supported_by_exit_risk_overlay` | materialize overlay flags and set InpExitRisk* feature indexes; no EA logic change if existing inputs suffice | set/ini hash(설정/초기화 해시), telemetry close reason(원격 측정 청산 사유), time-slice review(시간 구간 검토) |
| `feature_only_model_retrain` | `supported_after_feature_materialization` | create engineered feature columns; retrain or rematerialize model CSV; preserve feature order hash | feature order audit(피처 순서 감사), model hash(모델 해시), MT5 parity smoke(MT5 동등성 스모크) |
| `set_level_runtime_probe_no_model_change` | `supported_as_runtime_probe_only` | vary model risk sizing settings; compare against fixed lot without calling it model improvement | risk telemetry(위험 원격 측정), min lot floor count(최소 랏 바닥 횟수), DD/trade count attribution(손실폭/거래 수 귀속) |

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): ADX/ATR/DI(추세 강도/ATR/방향성 차이)는 hard prune(강한 절단)이 아니라 soft feature/risk-scale(부드러운 피처/위험 배율) 구조에서만 후보군 안정성을 높일 수 있다.
- decision_use(결정 용도): run267I(267I 실행)에서 P0 candidate/control(후보/기준)을 물질화할지 결정한다.
- comparison_baseline(비교 기준): run267D(267D 실행) atrcomp(ATR 압축), run267E(267E 실행) Monday guard(월요일 방어), run267F(267F 실행) adx2025/dilowq33, run267G(267G 실행) failure memory(실패 기억).
- control_variables(고정 변수): baseline candidate pool(기준 후보군), 2024 historical window(2024 과거 구간), MT5(MetaTrader 5, 메타트레이더5) settings(설정), model identity(모델 정체성) 또는 명시된 model rematerialization(모델 재물질화).
- changed_variables(변경 변수): engineered feature(설계 피처), feature order(피처 순서), optional exit overlay/risk sizing set surface(선택 청산 오버레이/위험 크기 설정 표면).
- sample_scope(표본 범위): FPMarkets US100 M5, 2024 historical stress(2024 과거 압박), Tier A(티어 A)와 routed total(라우팅 전체) 비교.
- success_criteria(성공 기준): net/PF(순수익/수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), Monday/July/chron_mid(월요일/7월/중간 구간)가 함께 덜 깨져야 한다.
- failure_criteria(실패 기준): 특정 feature(피처) 하나에만 붙거나, 거래 수만 줄거나, DI q33 hard repeat(강한 반복)로 돌아가면 실패다.
- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), model hash missing(모델 해시 누락), set/ini path missing(설정/초기화 경로 누락), parser error(파서 오류), MT5 report missing(MT5 보고서 누락).
- stop_conditions(중단 조건): P0 물질화와 MT5 review(MT5 검토) 후에도 약한 구간이 그대로면 ADX/DI branch(분기)를 닫거나 다른 구조 가설로 전환한다.
- evidence_plan(근거 계획): feature matrix(피처 행렬), Adapter surface(어댑터 표면), experiment queue(실험 대기열), materialization manifest(물질화 목록), MT5 reports(MT5 보고서), trade/time-slice/curve review(거래/시간 구간/곡선 검토).

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267G/adx_followup_failure_memory/followup_design.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267G/adx_followup_failure_memory/failure_memory.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267G/adx_followup_failure_memory/stop_rules.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/guard_comparison.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/negative_slice_summary.csv`
- producer(생산자): `stage_pipelines/stage267/run267H_soft_noncalendar_adapter_design.py`
- consumer(소비자): `run267I_materialize_top_soft_noncalendar_adapter_candidates`
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/soft_feature_engineering_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/adapter_surface_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/lineage.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267H/soft_noncalendar_adapter_design/result.json`
- availability(가용성): tracked(추적됨) after commit; reproducible_from_command(명령으로 재생성 가능).
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267H_soft_noncalendar_adapter_design`.
- evidence_available(사용 가능 근거): run267G design/failure memory(설계/실패 기억), run267F MT5 KPI(MT5 핵심 성과 지표), feature/adapter/queue matrices(피처/어댑터/대기열 행렬).
- evidence_missing(빠진 근거): actual materialized features(실제 물질화 피처), model retraining(모델 재학습), MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선).
- judgment_label(판정 라벨): `design_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267I_materialize_top_soft_noncalendar_adapter_candidates`.
