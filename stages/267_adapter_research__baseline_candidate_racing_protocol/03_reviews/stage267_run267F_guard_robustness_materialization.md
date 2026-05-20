# Stage267 Run267F Atrcomp Guard Robustness Materialization(267단계 267F ATR 압축 방어 견고성 물질화)

- action(행동): run267D(267D 실행) atrcomp(ATR 압축 대체) feature(피처)를 출발점으로 ADX 20-25(추세 강도 20-25) guard(방어)와 DI-low q33(DI 낮은 33%) guard(방어)를 물질화했다.
- effect(효과): run267E(267E 실행)의 Monday guard(월요일 방어)가 calendar prune(달력 절단)인지, 비달력 market-structure feature(시장 구조 피처)에서도 비슷한 개선을 만들 수 있는지 MT5(MetaTrader 5, 메타트레이더5)로 확인할 수 있다.
- feature_variants(피처 변형): `10`
- attempts_planned(계획 시도): `20`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 판독)

Stage58(58단계) 이후 연구를 충분히 활용했는가에 대한 답은 아직 `아니다`에 가깝다.
이전 연구는 후보를 만든 재료로는 쓰였지만, 지금 goal(목표)이 요구하는 공통 검증판까지 충분히 펼쳐지진 않았다.
이번 run267F(267F 실행)는 그 부족분 중 하나인 similar replacement(유사 대체)와 calendar-prune check(달력 절단 확인)를 실제 실행 가능한 묶음으로 바꾼 것이다.

## Materialized Variants(물질화 변형)

| candidate(후보) | guard(방어) | family(계열) | blocked signals(차단 신호) | retention(유지율) | run267E anchor(267E 기준) |
| --- | --- | --- | ---: | ---: | --- |
| `s264_aih` | `adx2025` | `trend_strength_non_calendar` | 86 | 0.807174887892 | net_delta=151.91; PF_delta=0.144072 |
| `s264_aia` | `adx2025` | `trend_strength_non_calendar` | 86 | 0.807174887892 | net_delta=146.41; PF_delta=0.140515 |
| `s258_stc` | `adx2025` | `trend_strength_non_calendar` | 86 | 0.807174887892 | net_delta=164.66; PF_delta=0.141462 |
| `s264_lc` | `adx2025` | `trend_strength_non_calendar` | 86 | 0.807174887892 | net_delta=166.07; PF_delta=0.149334 |
| `s262_lih` | `adx2025` | `trend_strength_non_calendar` | 86 | 0.807174887892 | net_delta=160.41; PF_delta=0.138326 |
| `s264_aih` | `dilowq33` | `directional_imbalance_replacement` | 123 | 0.724215246637 | net_delta=151.91; PF_delta=0.144072 |
| `s264_aia` | `dilowq33` | `directional_imbalance_replacement` | 123 | 0.724215246637 | net_delta=146.41; PF_delta=0.140515 |
| `s258_stc` | `dilowq33` | `directional_imbalance_replacement` | 123 | 0.724215246637 | net_delta=164.66; PF_delta=0.141462 |
| `s264_lc` | `dilowq33` | `directional_imbalance_replacement` | 123 | 0.724215246637 | net_delta=166.07; PF_delta=0.149334 |
| `s262_lih` | `dilowq33` | `directional_imbalance_replacement` | 123 | 0.724215246637 | net_delta=160.41; PF_delta=0.138326 |

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): run267E(267E 실행)의 개선이 월요일이라는 calendar(달력) 자체 때문이 아니라 약한 trend-strength(추세 강도) 또는 directional imbalance(방향성 불균형) 구간을 줄인 효과라면, 비달력 guard(방어)에서도 일부 유지되어야 한다.
- decision_use(결정 용도): run267E(267E 실행)를 계속 밀지, calendar prune(달력 절단) 의존으로 낮출지, Adapter(어댑터) 후보 축을 비달력 feature(피처) 쪽으로 다시 설계할지 판단한다.
- comparison_baseline(비교 기준): run267D(267D 실행) atrcomp(ATR 압축 대체)와 run267E(267E 실행) atrcomp Monday guard(ATR 압축 월요일 방어).
- control_variables(고정 변수): model CSV(모델 CSV), threshold(임계값), max_hold_bars(최대 보유 봉), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 historical window(2024 과거 구간).
- changed_variables(변경 변수): source-bar entry signal(원천 봉 진입 신호)을 ADX 20-25(추세 강도 20-25) 또는 DI-low q33(DI 낮은 33%) 문맥에서만 0으로 바꾼다.
- sample_scope(표본 범위): FPMarkets US100 M5, Tier A(티어 A)와 Tier A+B routed(티어 A+B 라우팅), 2024-01-02부터 2025-01-01 전까지.
- success_criteria(성공 기준): 순수익/PF(수익 팩터)/DD(drawdown, 손실폭)가 run267E(267E 실행)와 비슷하게 방어되면서 trade count(거래 수)가 과하게 무너지지 않고 약한 월/chron_mid(시간순 중간 구간)가 덜 깨진다.
- failure_criteria(실패 기준): 수익이 좋아 보여도 거래 수가 과하게 줄거나, DD(drawdown, 손실폭)와 약한 월이 그대로이거나, DI/ADX(방향성/추세 강도) 한 축에만 과적합된 모양이면 실패 또는 보류로 본다.
- invalid_conditions(무효 조건): MT5(MetaTrader 5, 메타트레이더5) report(보고서) 누락, feature order(피처 순서) 불일치, parser error(파서 오류), set/ini(설정/초기화) 경로 누락.
- stop_conditions(중단 조건): 같은 guard(방어)를 3 stage(단계) 이상 끌지 않는다. 2 stage(단계) 안에 살릴지, 버릴지, 구조 전환할지 닫는다.
- evidence_plan(근거 계획): attempts.csv(시도 목록), MT5 report(보고서), trade_records(거래 기록), time_slice KPI(시간 구간 핵심 성과 지표), curve diagnostics(곡선 진단), guard comparison(방어 비교), ledger/register(장부/등록부).

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/design.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/candidate_axis_review.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267E/adapter_p2_followup_design/guard_comparison.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267E/adapter_p2_followup_design/negative_slice_summary.csv`
- producer(생산자): `stage_pipelines/stage267/run267F_atrcomp_guard_robustness_materialization.py`
- consumer(소비자): `run267F_execute_non_calendar_guard_mt5_batch`
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/design.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/feature_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/contract.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/lineage.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/result.json`
- availability(가용성): repo tracked manifest(저장소 추적 목록) + Common Files(MT5 공용 파일) handoff(인계).
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Context Edges(문맥 경계값)

- atr_14_over_atr_50_q33(ATR 14/50 하위 33%): `1.15670530001`
- historical_vol_20_edges(20봉 과거 변동성 경계): `0.19134930272897085;0.2737485865751902`
- di_spread_14_abs_q33(DI 차이 절대값 하위 33%): `6.31721814473`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267F_atrcomp_guard_robustness_materialization`.
- evidence_available(사용 가능 근거): feature/model lineage(피처/모델 계보), runtime contract(런타임 계약), set/ini attempt manifest(설정/초기화 시도 목록).
- evidence_missing(빠진 근거): MT5(MetaTrader 5, 메타트레이더5) execution(실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice review(시간 구간 검토).
- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267F_execute_non_calendar_guard_mt5_batch`.
